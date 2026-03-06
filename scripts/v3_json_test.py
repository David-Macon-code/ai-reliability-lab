import boto3
import json
import time
import csv
from datetime import datetime
import os

IS_INJECTION_TEST = True  # flip to False when done with Day 11
INPUT_FILE = 'injection_test.json' if IS_INJECTION_TEST else 'golden_test.json'

# === CONFIG ===
REGION = 'us-east-1'
MODEL_ID = 'global.anthropic.claude-sonnet-4-5-20250929-v1:0'   # use this everywhere

# === CSV LOGGING SETUP ===
CSV_LOG_PATH = os.path.join("evaluation", "v3_metrics_log.csv")

# Create CSV header if it doesn't exist
if not os.path.exists(CSV_LOG_PATH):
    with open(CSV_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp_iso",
            "example_id",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "latency_sec"
        ])

# === JSON SCHEMA ===
schema = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string"},
        "age": {"type": "integer"},
        "city": {"type": "string"},
        "job_title": {"type": "string"}
    },
    "required": ["full_name", "age", "city", "job_title"],
    "additionalProperties": False
}

# === BEDROCK CLIENT ===
bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION)

# === LOAD TEST SET (golden or injection depending on toggle) ===
test_path = os.path.join("evaluation", INPUT_FILE)
with open(test_path, 'r', encoding='utf-8') as f:
    golden_data = json.load(f)

# === OUTPUT FILES ===
results_file = os.path.join("evaluation", "v3_results.json")
results = []

# === PROCESS BATCH ===
def normalize_name(name):
    if not name:
        return ""
    name = name.strip()
    # Standardize common title formats
    name = name.replace("Dr ", "Dr. ").replace("dr ", "Dr. ")
    return name.lower()

for case in golden_data:
    try:
        id_ = case.get('id', 'unknown')
        bio = case['bio']
        # expected = case['expected']   # already commented out - good

        user_message = f"""Extract exactly these fields from the bio: full name, age, city, job title.

Bio: {bio}

Return ONLY the JSON object. No explanations, no markdown."""

        start_time = time.perf_counter()   # higher precision than time.time()

        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": user_message}]}],
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.0
            },
            outputConfig={
                "textFormat": {
                    "type": "json_schema",
                    "structure": {
                        "jsonSchema": {
                            "schema": json.dumps(schema),
                            "name": "person_extraction",
                            "description": "Extracted person information"
                        }
                    }
                }
            }
        )

        output_text = response['output']['message']['content'][0]['text']
        parsed = json.loads(output_text)

        latency_sec = time.perf_counter() - start_time

        usage = response.get('usage', {})

        matches = None
        if not IS_INJECTION_TEST:
            expected = case.get('expected', {})
            matches = (
                normalize_name(parsed.get("full_name")) == normalize_name(expected.get("full_name")) and
                parsed.get("age") == expected.get("age") and
                (parsed.get("city") or "").strip().lower() == (expected.get("city") or "").strip().lower() and
                (parsed.get("job_title") or "").strip().lower() == (expected.get("job_title") or "").strip().lower()
            )

        results.append({
            "id": id_,
            "bio_snippet": bio[:120] + "..." if len(bio) > 120 else bio,
            "valid_json": True,
            "matches_expected": matches if not IS_INJECTION_TEST else "N/A (injection test)",
            "output": parsed,
            "tokens_total": usage.get('totalTokens'),
            "latency_sec": round(latency_sec, 3)
        })
        print(f"  → Appended result for {id_} (valid: {results[-1]['valid_json']})")

        # === LOG TO CSV ===
        row = [
            datetime.now().isoformat(),
            id_,
            usage.get('inputTokens', 0),
            usage.get('outputTokens', 0),
            usage.get('totalTokens', 0),
            f"{latency_sec:.3f}"
        ]
        with open(CSV_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(row)

        time.sleep(1)  # 1-second pause between cases – add right after the CSV write

        print(f"Processed {id_} | latency {latency_sec:.3f}s | tokens {usage.get('totalTokens')}")

    except Exception as loop_e:
        print(f"Unexpected error on case {id_ if 'id_' in locals() else 'unknown'}: {str(loop_e)}")
        results.append({
            "id": id_ if 'id_' in locals() else "unknown",
            "error": f"Loop-level error: {str(loop_e)}",
            "valid_json": False,
            "latency_sec": 0.0
        })

# === SAVE RESULTS ===
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Quick summary stats
if results:
    latencies = [r['latency_sec'] for r in results if 'latency_sec' in r and r['latency_sec'] > 0 and 'error' not in r]
    total_tokens_list = [r.get('tokens_total', 0) for r in results if r.get('tokens_total', 0) > 0 and 'error' not in r]
    
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"Average latency: {avg_latency:.3f} seconds")
    
    if total_tokens_list:
        avg_tokens = sum(total_tokens_list) / len(total_tokens_list)
        print(f"Average total tokens: {avg_tokens:.1f}")
    
    if not IS_INJECTION_TEST:
        pass_rate = sum(1 for r in results if r.get('matches_expected', False)) / len(results) * 100
        print(f"Golden pass rate: {pass_rate:.1f}% ({int(pass_rate/100 * len(results))}/{len(results)} cases)")
    else:
        valid_count = sum(1 for r in results if r.get('valid_json', False))
        error_count = len(results) - valid_count
        print(f"Injection test mode: {valid_count}/{len(results)} valid JSON outputs | {error_count} errors/filtered")

print(f"\nBatch complete.")
print(f"Results saved to: {results_file}")
print(f"Metrics logged to: {CSV_LOG_PATH}")
print(f"Processed {len(results)} / {len(golden_data)} cases")
print(f"Model used: {MODEL_ID}")