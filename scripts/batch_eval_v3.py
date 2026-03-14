import boto3
import json
import time
import argparse
import csv
import os
from datetime import datetime
from pathlib import Path

# ------------------ Config / Constants ------------------
REGION = "us-east-1" # your Bedrock region
MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"  # your model ID, e.g. "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
GUARDRAIL_VERSION = "3"  # your current v3
GUARDRAIL_ID = "9g6hem28nedj" # your guardrail ID, e.g. "9g6hem28nedj" (find in Bedrock console under Guardrails)

bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION)

# Load your schema (copy from your existing script or external file)
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string", "description": "Extracted full name or null"},
        "age": {"type": "integer", "description": "Age as integer or null"},
        "city": {"type": "string", "description": "City or null"},
        "job_title": {"type": "string", "description": "Job title or null"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1, "description": "Model confidence in extraction"}
    },
    "required": ["confidence"],
    "additionalProperties": False
}

# ------------------ Helper Functions ------------------
def load_golden_tests(path="evaluation/golden_test.json"):
    with open(path, 'r') as f:
        data = json.load(f)
    # Assume format: list of dicts, e.g. [{"test_id": 1, "input_text": "...", "expected": {...}}, ...]
    return data

def run_converse_single(user_message, temperature=0.0, max_tokens=512):
    start_time = time.time()
    
    messages = [{"role": "user", "content": [{"text": user_message}]}]
    
    # Guardrail config (adapt from your existing script)
    guardrail_config = {
        "guardrailIdentifier": GUARDRAIL_ID,
        "guardrailVersion": GUARDRAIL_VERSION,
        "trace": "enabled"  # for parsing blocks
    } if GUARDRAIL_VERSION else None
    
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
        },
        guardrailConfig=guardrail_config if guardrail_config else None
    )
    
    latency = time.time() - start_time
    output_text = response['output']['message']['content'][0]['text']
    usage = response['usage']
    
    # Improved guardrail trace parsing
    guardrail_blocked = False
    trace_category = None
    if 'trace' in response:
        trace_data = response['trace']
        if isinstance(trace_data, dict) and 'guardrail' in trace_data:
            gr = trace_data['guardrail']
            guardrail_blocked = gr.get('blocked', False)
            trace_category = gr.get('category') or gr.get('violatedFilter') or None
    
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
        "raw_response": response  # optional: for deep debug
    }

def validate_result(result, expected_snippet=None):
    # Your existing validation logic here
    # e.g. confidence >= 0.8 and valid_json and semantic match check
    # For now, simple: return flake_reason if failed, else None
    if not result["valid_json"]:
        return "invalid_json"
    if result["confidence"] < 0.8:
        return "low_confidence"
    if result["guardrail_blocked"]:
        return "guardrail_block"
    # Add semantic check against expected if you have it
    return None

# ------------------ Main Batch Logic ------------------
def main():
    parser = argparse.ArgumentParser(description="Batch evaluation on Bedrock Converse V3")
    parser.add_argument("--runs", type=int, default=10, help="Runs per test case")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--model-id", default=MODEL_ID)
    parser.add_argument("--guardrail-version", default=GUARDRAIL_VERSION)
    parser.add_argument("--output-dir", default=f"evaluation/batch_{datetime.now().strftime('%Y%m%d')}")
    args = parser.parse_args()

    # Override globals if CLI provided
    global MODEL_ID, GUARDRAIL_VERSION
    MODEL_ID = args.model_id
    GUARDRAIL_VERSION = args.guardrail_version

    tests = load_golden_tests()
    print(f"Loaded {len(tests)} golden test cases")

    os.makedirs(args.output_dir, exist_ok=True)
    csv_path = Path(args.output_dir) / "batch_metrics.csv"

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            "test_id", "run_id", "input_text", "expected_json_snippet",
            "actual_json", "valid_json", "confidence", "tokens_input",
            "tokens_output", "latency_sec", "guardrail_blocked",
            "guardrail_trace_category", "flake_reason"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for test in tests:
            test_id = test.get("test_id", "unknown")
            input_text = test.get("input_text", "")
            expected_snippet = json.dumps(test.get("expected", {}))[:100]  # truncate for CSV

            for run_id in range(1, args.runs + 1):
                print(f"Running test {test_id} / run {run_id} ...")
                result = run_converse_single(input_text, temperature=args.temperature)
                
                flake_reason = validate_result(result, expected_snippet)
                
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
                    "latency_sec": round(result["latency_sec"], 3),
                    "guardrail_blocked": result["guardrail_blocked"],
                    "guardrail_trace_category": result["guardrail_trace_category"],
                    "flake_reason": flake_reason
                }
                writer.writerow(row)
                csvfile.flush()  # save progressively

    print(f"Batch complete. Results in: {csv_path}")

if __name__ == "__main__":
    main()
