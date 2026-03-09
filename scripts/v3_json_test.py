import boto3
import json
import time
import csv
from datetime import datetime
import os

# === CONFIG ===
REGION = 'us-east-1'
MODEL_ID = 'global.anthropic.claude-sonnet-4-5-20250929-v1:0'  # or fallback to region-specific if needed

# Guardrail config - prefer env vars for production/flexibility
GUARDRAIL_ID = os.getenv("BEDROCK_GUARDRAIL_ID", "9g6hem28nedj")
GUARDRAIL_VERSION = os.getenv("BEDROCK_GUARDRAIL_VERSION", "3")

guardrail_config = {
    "guardrailIdentifier": GUARDRAIL_ID,
    "guardrailVersion": GUARDRAIL_VERSION,
    "trace": "enabled"  # crucial for debugging
}

IS_INJECTION_TEST = True  # Flip to True for Day 12 injection re-test
INPUT_FILE = 'injection_test.json' if IS_INJECTION_TEST else 'golden_test.json'

# === CSV LOGGING SETUP ===
CSV_LOG_PATH = os.path.join("evaluation", "v3_metrics_log.csv")

# Create CSV header if it doesn't exist (added guardrail_intervened)
if not os.path.exists(CSV_LOG_PATH):
    with open(CSV_LOG_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp_iso",
            "example_id",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "latency_sec",
            "guardrail_intervened",
            "guardrail_filter_type",
            "guardrail_action",
            "guardrail_latency_ms",
            "guardrail_confidence"
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

# === LOAD TEST SET ===
test_path = os.path.join("evaluation", INPUT_FILE)
with open(test_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# === OUTPUT FILES ===
results_file = os.path.join("evaluation", "v3_results.json")
results = []

# === HELPER ===
def normalize_name(name):
    if not name:
        return ""
    name = name.strip()
    name = name.replace("Dr ", "Dr. ").replace("dr ", "Dr. ")
    return name.lower()

# === PROCESS BATCH ===
for case in test_data:
    try:
        case_id = case.get('id', 'unknown')
        bio = case['bio']

        user_message = f"""Extract exactly these fields from the bio: full name, age, city, job title.

Bio: {bio}

Return ONLY the JSON object. No explanations, no markdown."""

        start_time = time.perf_counter()

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
            },
            guardrailConfig=guardrail_config  # toggled via config above
        )

        intervened = False
        filter_type = None
        action = None
        gr_latency = 0.0
        confidence = None
        guardrail_details = {}  # for extra debug if needed

        if 'trace' in response and 'guardrail' in response['trace']:
            trace = response['trace']['guardrail']
            intervened = True
            
            # Handle inputAssessment (most common for prompt blocks)
            if 'inputAssessment' in trace and trace['inputAssessment']:
                # Get the first (usually only) assessment dict by its dynamic key
                assess_key = next(iter(trace['inputAssessment']))
                assess = trace['inputAssessment'][assess_key]
                
                # Content policy filters (e.g., PROMPT_ATTACK, HATE, etc.)
                if 'contentPolicy' in assess and 'filters' in assess['contentPolicy'] and assess['contentPolicy']['filters']:
                    f = assess['contentPolicy']['filters'][0]  # take first; extend to loop if multi
                    filter_type = f.get('type')
                    confidence = f.get('confidence')
                    action = f.get('action')  # e.g., BLOCKED, NONE
                
                # Invocation metrics for latency
                if 'invocationMetrics' in assess:
                    gr_latency = assess['invocationMetrics'].get('guardrailProcessingLatency', 0)
            
            # Optional: capture outputAssessment if response was partially generated before block
            if 'outputAssessment' in trace:
                # similar parsing if needed
                pass
            
            # Dump full trace for debugging rare cases
            guardrail_details = trace

        latency_sec = time.perf_counter() - start_time

        # Guardrail handling
        guardrail_intervened = False
        guardrail_trace = None
        guardrail_trace_summary = None

        if 'trace' in response and 'guardrail' in response.get('trace', {}):
            guardrail_trace = response['trace']['guardrail']
            if response.get('stopReason') == 'guardrail_intervened':
                guardrail_intervened = True
                print(f"  → Guardrail INTERVENED on {case_id}")
                print("  Guardrail trace:", json.dumps(guardrail_trace, indent=2))

            # Richer summary for results/logging
            guardrail_trace_summary = {
                "action": guardrail_trace.get("action"),
                "assessments": guardrail_trace.get("assessments", []),
                # Add more fields if needed (e.g. "topicPolicy", "outputAssessments")
            }

        # Output parsing
        if guardrail_intervened:
            output_text = None
            parsed = None
            valid_json = False
        else:
            output_text = response['output']['message']['content'][0]['text']
            try:
                parsed = json.loads(output_text)
                valid_json = True
            except json.JSONDecodeError:
                valid_json = False
                parsed = None

        usage = response.get('usage', {})

        # Golden matching (skip for injection tests)
        matches = None
        if not IS_INJECTION_TEST:
            expected = case.get('expected', {})
            if parsed:
                matches = (
                    normalize_name(parsed.get("full_name")) == normalize_name(expected.get("full_name")) and
                    parsed.get("age") == expected.get("age") and
                    (parsed.get("city") or "").strip().lower() == (expected.get("city") or "").strip().lower() and
                    (parsed.get("job_title") or "").strip().lower() == (expected.get("job_title") or "").strip().lower()
                )

        # Append to results
        results.append({
            "id": case_id,
            "bio_snippet": bio[:120] + "..." if len(bio) > 120 else bio,
            "valid_json": valid_json,
            "guardrail_intervened": guardrail_intervened,
            "guardrail_trace_summary": guardrail_trace_summary,
            "matches_expected": matches if not IS_INJECTION_TEST else "N/A (injection test)",
            "output": parsed,
            "tokens_total": usage.get('totalTokens'),
            "latency_sec": round(latency_sec, 3)
        })
        print(f"  → Appended result for {case_id} (valid: {valid_json}, intervened: {guardrail_intervened})")

        # === LOG TO CSV ===
        row = [
            datetime.now().isoformat(),
            case_id,
            usage.get('inputTokens', 0),
            usage.get('outputTokens', 0),
            usage.get('totalTokens', 0),
            f"{latency_sec:.3f}",
            str(guardrail_intervened).lower()
        ]
        with open(CSV_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(row)

        time.sleep(1)  # Rate limit safety

        print(f"Processed {case_id} | latency {latency_sec:.3f}s | tokens {usage.get('totalTokens')}")

    except Exception as e:
        print(f"Unexpected error on case {case_id if 'case_id' in locals() else 'unknown'}: {str(e)}")
        results.append({
            "id": case_id if 'case_id' in locals() else "unknown",
            "error": str(e),
            "valid_json": False,
            "guardrail_intervened": False,
            "latency_sec": 0.0
        })

# === SAVE RESULTS ===
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# === SUMMARY ===
if results:
    latencies = [r['latency_sec'] for r in results if r.get('latency_sec', 0) > 0 and 'error' not in r]
    total_tokens_list = [r.get('tokens_total', 0) for r in results if r.get('tokens_total', 0) > 0 and 'error' not in r]

    if latencies:
        print(f"Average latency: {sum(latencies) / len(latencies):.3f} seconds")
    if total_tokens_list:
        print(f"Average total tokens: {sum(total_tokens_list) / len(total_tokens_list):.1f}")

    if not IS_INJECTION_TEST:
        pass_rate = sum(1 for r in results if r.get('matches_expected', False)) / len(results) * 100
        print(f"Golden pass rate: {pass_rate:.1f}% ({int(pass_rate/100 * len(results))}/{len(results)} cases)")
    else:
        valid_count = sum(1 for r in results if r.get('valid_json', False))
        intervened_count = sum(1 for r in results if r.get('guardrail_intervened', False))
        error_count = len(results) - valid_count - intervened_count
        print(f"Injection test mode:")
        print(f"  Valid JSON: {valid_count}/{len(results)}")
        print(f"  Guardrail interventions: {intervened_count}")
        print(f"  Other errors: {error_count}")

print(f"\nBatch complete.")
print(f"Results saved to: {results_file}")
print(f"Metrics logged to: {CSV_LOG_PATH}")
print(f"Processed {len(results)} / {len(test_data)} cases")
print(f"Model used: {MODEL_ID}")
print(f"Guardrail used: {GUARDRAIL_ID} v{GUARDRAIL_VERSION}")