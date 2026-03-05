import boto3
import json
import time
import csv
from datetime import datetime
import os

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

# === LOAD GOLDEN TEST SET ===
golden_path = os.path.join("evaluation", "golden_test.json")
with open(golden_path, 'r', encoding='utf-8') as f:
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
    id_ = case.get('id', 'unknown')
    bio = case['bio']
    expected = case['expected']

    user_message = f"""Extract exactly these fields from the bio: full name, age, city, job title.

Bio: {bio}

Return ONLY the JSON object. No explanations, no markdown."""

    start_time = time.perf_counter()   # higher precision than time.time()

    try:
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

        matches = (
            normalize_name(parsed.get("full_name")) == normalize_name(expected.get("full_name")) and
            parsed.get("age") == expected.get("age") and
            (parsed.get("city") or "").strip().lower() == (expected.get("city") or "").strip().lower() and
            (parsed.get("job_title") or "").strip().lower() == (expected.get("job_title") or "").strip().lower()
        )

        results.append({
            "id": id_,
            "bio_snippet": bio[:60] + "..." if len(bio) > 60 else bio,
            "valid_json": True,
            "matches_expected": matches,
            "output": parsed,
            "tokens_total": usage.get('totalTokens'),
            "latency_sec": round(latency_sec, 3)
        })

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

        print(f"Processed {id_} | latency {latency_sec:.3f}s | tokens {usage.get('totalTokens')}")

    except Exception as e:
        latency_sec = time.perf_counter() - start_time
        results.append({
            "id": id_,
            "error": str(e),
            "valid_json": False,
            "latency_sec": round(latency_sec, 3)
        })
        print(f"Error on {id_}: {str(e)}")

# === SAVE RESULTS ===
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Quick summary stats
if results:
    latencies = [r['latency_sec'] for r in results if 'latency_sec' in r]
    total_tokens_list = [r.get('tokens_total', 0) for r in results if 'tokens_total' in r]
    
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"Average latency: {avg_latency:.3f} seconds")
    
    if total_tokens_list:
        avg_tokens = sum(total_tokens_list) / len(total_tokens_list)
        print(f"Average total tokens: {avg_tokens:.1f}")
    
    pass_rate = sum(1 for r in results if r.get('matches_expected', False)) / len(results) * 100
    print(f"Golden pass rate: {pass_rate:.1f}% ({int(pass_rate/100 * len(results))}/{len(results)} cases)")

print(f"\nBatch complete.")
print(f"Results saved to: {results_file}")
print(f"Metrics logged to: {CSV_LOG_PATH}")
print(f"Processed {len(results)} / {len(golden_data)} cases")