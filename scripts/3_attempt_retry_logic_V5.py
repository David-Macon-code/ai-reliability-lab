import argparse
import json
import csv
import time
import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

# -------------------------------
# Configuration constants
# -------------------------------
GUARDRAIL_ID = "9g6hem28nedj"
MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
DEFAULT_REGION = "us-east-1"

# -------------------------------
# Schema for structured output
# -------------------------------
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "city": {"type": "string"},
        "confidence": {"type": "number"}
    },
    "required": ["name", "confidence"],
    "additionalProperties": False
}

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--output-dir", type=str, default="evaluation/no_guardrail")
    parser.add_argument("--model-id", type=str, default=MODEL_ID)
    parser.add_argument("--guardrail-version", type=str, default=None)
    parser.add_argument("--adversarial", action="store_true")
    parser.add_argument("--test-ids", type=str, default=None)
    return parser.parse_args()

def get_bedrock_client(region=DEFAULT_REGION):
    return boto3.client("bedrock-runtime", region_name=region)

def run_converse_single(client, model_id, user_message, temperature=0.0, guardrail_version=None):
    messages = [{"role": "user", "content": [{"text": user_message}]}]

    inference_config = {"maxTokens": 512, "temperature": temperature}

    output_config = {
        "textFormat": {
            "type": "json_schema",
            "structure": {
                "jsonSchema": {
                    "schema": json.dumps(OUTPUT_SCHEMA),
                    "name": "extraction_output"
                }
            }
        }
    }

    guardrail_config = None
    if guardrail_version:
        guardrail_config = {
            "guardrailIdentifier": GUARDRAIL_ID,
            "guardrailVersion": guardrail_version,
            "trace": "enabled"
        }

    try:
        max_retries = 3
        retry_delay = 1
        retry_count = 0

        for attempt in range(max_retries):
            try:
                start_time = time.time()

                params = {
                    "modelId": model_id,
                    "messages": messages,
                    "inferenceConfig": inference_config,
                    "outputConfig": output_config,
                }
                if guardrail_config:
                    params["guardrailConfig"] = guardrail_config

                response = client.converse(**params)
                latency = time.time() - start_time
                break

            except ClientError as e:
                error_str = str(e)
                print(f"DEBUG: attempt {attempt+1} failed: {error_str}")

                retry_count += 1

                if attempt < max_retries - 1:
                    sleep_time = retry_delay * (2 ** attempt)
                    time.sleep(sleep_time)
                else:
                    return None, error_str

        content = response.get('output', {}).get('message', {}).get('content', [])
        if not content or not content[0].get('text'):
            return None, "Empty response"

        output_text = content[0]['text']
        parsed = json.loads(output_text)

        return {
            "success": True,
            "parsed": parsed,
            "latency": latency,
            "usage": response.get('usage', {}),
            "raw_response": response,
            "output_text": output_text,
            "retry_count": retry_count
        }, None

    except Exception as e:
        return None, str(e)

def main():
    args = parse_arguments()
    client = get_bedrock_client()

    test_path = Path("evaluation/adversarial_test.json" if args.adversarial else "evaluation/golden_test.json")

    with open(test_path, 'r') as f:
        tests = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = Path(args.output_dir) / "batch_metrics.csv"

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            "test_id","run_id","input_text","latency","total_tokens",
            "input_tokens","output_tokens","confidence","flake_reason",
            "guardrail_intervened","leak_detected","retry_count",
            "match_score","match_percentage","timestamp"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for test_idx, test in enumerate(tests):
            user_message = test.get("input", "")

            for run_id in range(args.runs):
                result, error = run_converse_single(
                    client, args.model_id, user_message,
                    temperature=args.temperature,
                    guardrail_version=args.guardrail_version
                )

                flake_reason = None
                confidence = 0.0
                intervened = False
                leak_detected = False
                match_score = 0
                match_percentage = 0.0

                if result and result["success"]:
                    parsed = result["parsed"]
                    confidence = parsed.get("confidence", 0.0)

                    expected = test.get("expected", {})
                    if expected:
                        matches = 0
                        total_fields = 0

                        if "name" in parsed and "full_name" in expected:
                            total_fields += 1
                            if parsed["name"].lower().strip() == expected["full_name"].lower().strip():
                                matches += 1

                        if "age" in parsed and "age" in expected:
                            total_fields += 1
                            if parsed["age"] == expected["age"]:
                                matches += 1

                        if "city" in parsed and "city" in expected:
                            total_fields += 1
                            if parsed["city"].lower().strip() == expected["city"].lower().strip():
                                matches += 1

                        if total_fields > 0:
                            match_score = matches
                            match_percentage = (matches / total_fields) * 100

                    if confidence < 0.7:
                        flake_reason = "low_confidence"

                    if result["raw_response"].get("guardrailIntervened", False):
                        intervened = True
                        flake_reason = flake_reason or "guardrail_block"

                    if flake_reason is None:
                        pass
                else:
                    flake_reason = error or "api_failed"

                row = {
                    "test_id": test_idx + 1,
                    "run_id": run_id + 1,
                    "input_text": user_message,
                    "latency": result["latency"] if result else None,
                    "total_tokens": result["usage"].get("totalTokens", 0) if result else 0,
                    "input_tokens": result["usage"].get("inputTokens", 0) if result else 0,
                    "output_tokens": result["usage"].get("outputTokens", 0) if result else 0,
                    "confidence": round(confidence, 3),
                    "flake_reason": flake_reason,
                    "guardrail_intervened": intervened,
                    "leak_detected": leak_detected,
                    "retry_count": result.get("retry_count", 0) if result else 0,
                    "match_score": match_score,
                    "match_percentage": round(match_percentage, 1),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

                writer.writerow(row)

    print(f"Done. Results: {csv_path}")

if __name__ == "__main__":
    main()

    