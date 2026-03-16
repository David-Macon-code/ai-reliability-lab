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
GUARDRAIL_ID = "9g6hem28nedj"  # Your guardrail ID
MODEL_ID = "anthropic.claude-sonnet-4-5-20250929-v1:0"  # Adjust if needed
DEFAULT_REGION = "us-east-1"

# -------------------------------
# Schema for structured output
# -------------------------------
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Full name extracted"},
        "age": {"type": "integer", "description": "Age as number or null if missing"},
        "city": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["name", "confidence"],
    "additionalProperties": False
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Batch evaluation for Bedrock Converse API with structured outputs")
    parser.add_argument("--runs", type=int, default=5, help="Number of runs per test case")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for inference")
    parser.add_argument("--output-dir", type=str, default="evaluation/no_guardrail", help="Output directory")
    parser.add_argument("--model-id", type=str, default=MODEL_ID, help="Bedrock model ID")
    parser.add_argument("--guardrail-version", type=str, default=None, 
                        help="Guardrail version to use (omit to disable)")
    return parser.parse_args()

def get_bedrock_client(region=DEFAULT_REGION):
    return boto3.client("bedrock-runtime", region_name=region)

def run_converse_single(client, model_id, user_message, temperature=0.0, guardrail_version=None):
    messages = [{"role": "user", "content": [{"text": user_message}]}]
    
    inference_config = {
        "maxTokens": 512,
        "temperature": temperature,
        "topP": 1.0
    }
    
    output_config = {
        "textFormat": {
            "type": "json_schema",
            "structure": {
                "jsonSchema": {
                    "schema": json.dumps(OUTPUT_SCHEMA),
                    "name": "extraction_output",
                    "description": "Structured extraction result"
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
        start_time = time.time()
        
        # Build params dynamically to avoid passing guardrailConfig=None
        params = {
            "modelId": model_id,
            "messages": messages,
            "inferenceConfig": inference_config,
            "outputConfig": output_config,
        }
        if guardrail_config is not None:
            params["guardrailConfig"] = guardrail_config
        
        response = client.converse(**params)
        
        latency = time.time() - start_time
        
        output_text = response['output']['message']['content'][0]['text']
        parsed = json.loads(output_text)
        
        usage = response.get('usage', {})
        
        return {
            "success": True,
            "parsed": parsed,
            "latency": latency,
            "usage": usage,
            "raw_response": response
        }, None
    
    except ClientError as e:
        return None, str(e)
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {str(e)}"
    except Exception as e:
        return None, str(e)

def main():
    args = parse_arguments()
    
    client = get_bedrock_client()
    
    golden_path = Path("evaluation/golden_test.json")
    if not golden_path.exists():
        print(f"Golden test set not found: {golden_path}")
        return
    
    with open(golden_path, 'r') as f:
        tests = json.load(f)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    csv_path = Path(args.output_dir) / "batch_metrics.csv"
    
    total_confidence = 0.0
    total_tokens_success = 0
    success_count = 0
    
    total_runs = len(tests) * args.runs
    success_runs = 0
    
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = [
            "test_id", "run_id", "input_text", "latency", "total_tokens",
            "input_tokens", "output_tokens", "confidence", "flake_reason",
            "guardrail_intervened", "timestamp"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for test_idx, test in enumerate(tests):
            user_message = test.get("input", "Extract details from sample text here.")
            
            for run_id in range(args.runs):
                print(f"Running test {test_idx+1}/{len(tests)} - run {run_id+1}/{args.runs}")
                
                result, error = run_converse_single(
                    client,
                    args.model_id,
                    user_message,
                    temperature=args.temperature,
                    guardrail_version=args.guardrail_version
                )
                
                flake_reason = None
                confidence = 0.0
                intervened = False
                
                if result and result["success"]:
                    parsed = result["parsed"]
                    confidence = parsed.get("confidence", 0.0)
                    
                    if confidence < 0.7:
                        flake_reason = "low_confidence"
                    
                    if result["raw_response"].get("guardrailIntervened", False):
                        intervened = True
                        flake_reason = flake_reason or "guardrail_block"
                    
                    if flake_reason is None:
                        success_runs += 1
                else:
                    flake_reason = error or "api_call_failed"
                
                # Safe row creation
                row = {
                    "test_id": test_idx + 1,
                    "run_id": run_id + 1,
                    "input_text": user_message[:100] + "..." if len(user_message) > 100 else user_message,
                    "latency": round(result["latency"], 3) if result and "latency" in result else None,
                    "total_tokens": result["usage"].get("totalTokens", 0) if result and "usage" in result else 0,
                    "input_tokens": result["usage"].get("inputTokens", 0) if result and "usage" in result else 0,
                    "output_tokens": result["usage"].get("outputTokens", 0) if result and "usage" in result else 0,
                    "confidence": round(confidence, 3),
                    "flake_reason": flake_reason,
                    "guardrail_intervened": intervened,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                writer.writerow(row)
                csvfile.flush()
                
                if flake_reason is None:
                    success_count += 1
                    total_confidence += result["parsed"].get("confidence", 0.0)
                    total_tokens_success += row["total_tokens"]
    
    # Summary
    print(f"\nBatch complete. Results in: {csv_path}")
    print("\nQuick summary:")
    print(f"Total test cases: {len(tests)}")
    print(f"Runs per case: {args.runs}")
    print(f"Output directory: {args.output_dir}")
    print(f"Processed {total_runs} total API calls")
    
    print("\n" + "=" * 60)
    print("Batch evaluation complete!")
    print(f"Results saved to: {csv_path}")
    print(f"Golden test cases: {len(tests)}")
    print(f"Runs per case: {args.runs}")
    print(f"Total API calls made: {total_runs}")
    
    pass_rate = (success_runs / total_runs * 100) if total_runs > 0 else 0
    print(f"Overall pass rate: {pass_rate:.1f}% ({success_runs}/{total_runs} runs)")
    
    if success_count > 0:
        avg_confidence = total_confidence / success_count
        avg_tokens = total_tokens_success / success_count
        print(f"Average confidence (successful runs): {avg_confidence:.3f}")
        print(f"Average total tokens (successful runs): {avg_tokens:.1f}")
    else:
        print("No successful runs → no average confidence/tokens available")
    
    gr_status = f"ENABLED (v{args.guardrail_version})" if args.guardrail_version else "DISABLED"
    print(f"Guardrail status: {gr_status}")
    
    print("Tip: Open the CSV and check the 'total_tokens' column for usage stats.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()