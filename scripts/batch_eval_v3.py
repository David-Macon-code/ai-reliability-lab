import boto3
import json
import time
import argparse
import csv
import os
from datetime import datetime
from pathlib import Path

# ------------------ Config / Constants ------------------
REGION = "us-east-1"
MODEL_ID = 'global.anthropic.claude-sonnet-4-5-20250929-v1:0'

bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION)

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string", "description": "Extracted full name or null"},
        "age": {"type": "integer", "description": "Age as integer or null"},
        "city": {"type": "string", "description": "City or null"},
        "job_title": {"type": "string", "description": "Job title or null"},
        "confidence": {
            "type": "number",
            "description": "Model confidence in extraction (0.0 to 1.0)"
        }
    },
    "required": ["confidence"],
    "additionalProperties": False
}

# ------------------ Helper Functions ------------------
def load_golden_tests(path="evaluation/golden_test.json"):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def run_converse_single(user_message, temperature=0.0, max_tokens=512):
    start_time = time.time()
    
    # Instructions + user message combined (no "system" role)
    instructions = (
        "You are a precise information extractor. "
        "Respond ONLY with valid JSON matching the schema below. "
        "Use null for missing values. "
        "Always include a 'confidence' field from 0.0 to 1.0 based on how clearly the information is stated in the text. "
        "Do not include any explanations, markdown, or extra text outside the JSON object."
    )
    
    full_prompt = f"{instructions}\n\nExtract from this biography:\n{user_message}"
    
    messages = [
        {"role": "user", "content": [{"text": full_prompt}]}
    ]
    
    try:
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=messages,
            inferenceConfig={"maxTokens": max_tokens, "temperature": temperature},
            outputConfig={
                "textFormat": {
                    "type": "json_schema",
                    "structure": {
                        "jsonSchema": {
                            "schema": json.dumps(EXTRACTION_SCHEMA),
                            "name": "extraction_output",
                            "description": "Structured extraction result"
                        }
                    }
                }
            }
            # guardrailConfig intentionally omitted → disabled
        )
    except Exception as api_err:
        latency = time.time() - start_time
        print(f"API call failed: {str(api_err)}")
        return {
            "actual_json": None,
            "valid_json": False,
            "confidence": 0.0,
            "tokens_input": 0,
            "tokens_output": 0,
            "latency_sec": latency,
            "guardrail_blocked": False,
            "guardrail_trace_category": None,
            "flake_reason": f"API error: {str(api_err)}",
            "raw_response": None
        }

    latency = time.time() - start_time

    # Safe access to output_text
    try:
        output_text = response['output']['message']['content'][0]['text']
    except (KeyError, IndexError, TypeError) as e:
        print(f"Response structure error: {str(e)}")
        output_text = ""

    usage = response.get('usage', {})

    # No guardrail since disabled
    guardrail_blocked = False
    trace_category = None

    try:
        parsed = json.loads(output_text)
        valid_json = True
        confidence = parsed.get("confidence", 0.0)
        flake_reason = None
    except Exception as e:
        parsed = None
        valid_json = False
        confidence = 0.0
        flake_reason = str(e)

    return {
        "actual_json": parsed,
        "valid_json": valid_json,
        "confidence": confidence,
        "tokens_input": usage.get("inputTokens", 0),
        "tokens_output": usage.get("outputTokens", 0),
        "latency_sec": latency,
        "guardrail_blocked": guardrail_blocked,
        "guardrail_trace_category": trace_category,
        "flake_reason": flake_reason,
        "raw_response": response
    }

def validate_result(result, expected_snippet=None):
    if not result["valid_json"]:
        return "invalid_json"
    if result["confidence"] < 0.8:
        return "low_confidence"
    if result["guardrail_blocked"]:
        return "guardrail_block"
    return None

# ------------------ Main Batch Logic ------------------
def main():
    global MODEL_ID

    parser = argparse.ArgumentParser(description="Batch evaluation on Bedrock Converse V3")
    parser.add_argument("--runs", type=int, default=10, help="Runs per test case")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--model-id", default=MODEL_ID)
    parser.add_argument("--output-dir", default=f"evaluation/batch_{datetime.now().strftime('%Y%m%d')}")
    args = parser.parse_args()

    MODEL_ID = args.model_id

    tests = load_golden_tests()
    print(f"Loaded {len(tests)} golden test cases")

    total_runs = 0
    success_runs = 0

    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = Path(args.output_dir) / "batch_metrics.csv"

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            "test_id", "run_id", "input_text", "expected_json_snippet",
            "actual_json", "valid_json", "confidence", "tokens_input",
            "tokens_output", "total_tokens", "latency_sec", "guardrail_blocked",
            "guardrail_trace_category", "flake_reason"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        total_confidence = 0.0
        total_tokens_success = 0      # we'll sum total_tokens only on successes
        success_count = 0             # we'll count only clean passes here (can reuse or separate from success_runs)

        for test in tests:
            test_id = test.get("test_id", "unknown")
            input_text = test.get("bio", "")
            expected_snippet = json.dumps(test.get("expected", {}))[:100]

            for run_id in range(1, args.runs + 1):
                print(f"Running test {test_id} / run {run_id} ...")
                result = run_converse_single(input_text, temperature=args.temperature)
                
                flake_reason = validate_result(result, expected_snippet)

                total_runs += 1
                if flake_reason is None:
                    success_runs += 1
                
                row = {
                    "test_id": test_id,
                    "run_id": run_id,
                    "input_text": input_text,
                    "expected_json_snippet": expected_snippet,
                    "actual_json": json.dumps(result["actual_json"]) if result["actual_json"] else "",
                    "valid_json": result["valid_json"],
                    "confidence": result["confidence"],
                    "tokens_input": result["tokens_input"],
                    "tokens_output": result["tokens_output"],
                    "total_tokens": result["tokens_input"] + result["tokens_output"],
                    "latency_sec": round(result["latency_sec"], 3),
                    "guardrail_blocked": result["guardrail_blocked"],
                    "guardrail_trace_category": result["guardrail_trace_category"],
                    "flake_reason": flake_reason
                }
                writer.writerow(row)
                csvfile.flush()

                if flake_reason is None:  # only count clean successes (valid JSON + high conf + no guardrail block)
                      success_count += 1
                      total_confidence += result["confidence"]
                      total_tokens_success += row["total_tokens"]   # already calculated in row

    # Final summary
print(f"\nBatch complete. Results in: {csv_path}")
print("\nQuick summary:")
print(f"Total test cases: {len(tests)}")
print(f"Runs per case: {args.runs}")
print(f"Output directory: {args.output_dir}")
print(f"Processed {len(tests) * args.runs} total API calls")

print("\n" + "=" * 60)
print("Batch evaluation complete!")
print(f"Results saved to: {csv_path}")
print(f"Golden test cases: {len(tests)}")
print(f"Runs per case: {args.runs}")
print(f"Total API calls made: {len(tests) * args.runs}")

pass_rate = (success_runs / total_runs * 100) if total_runs > 0 else 0
print(f"Overall pass rate: {pass_rate:.1f}% ({success_runs}/{total_runs} runs)")

if success_count > 0:
    avg_confidence = total_confidence / success_count
    avg_tokens = total_tokens_success / success_count
    print(f"Average confidence (successful runs): {avg_confidence:.3f}")
    print(f"Average total tokens (successful runs): {avg_tokens:.1f}")
else:
    print("No successful runs → no average confidence/tokens available")

print("Tip: Open the CSV and check the 'total_tokens' column for usage stats.")
print("=" * 60 + "\n")

if __name__ == "__main__":
    main()