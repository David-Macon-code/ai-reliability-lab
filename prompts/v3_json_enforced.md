# Prompt V3 – Strict JSON Enforced

**Task**  
Extract person info (full name, age, city, job title) from bio as JSON.

**Prompt text** (used in Bedrock Playground):
```You are a precise data extractor. Extract exactly these fields from the bio: full name, age, city, job title.
Bio: Albert Smith is a 34-year-old software engineer living in Springfield. He works at a cloud consulting firm and enjoys gaming on the weekends.
Return ONLY the JSON object. No explanations, no markdown, no extra text.```

**JSON Schema** (pasted into system prompt):
```json
{
  "type": "object",
  "properties": {
    "full_name": {"type": "string", "description": "Full name of the person"},
    "age": {"type": "integer", "description": "Age as number, null if missing"},
    "city": {"type": "string", "description": "City they live in"},
    "job_title": {"type": "string", "description": "Job title or main profession"}
  },
  "required": ["full_name", "age", "city", "job_title"],
  "additionalProperties": false
}
```Test settings

Model: Anthropic Claude Sonnet 4.5
Temperature: 0.0
Method: Prompt + schema in system prompt (playground)
Runs: 3

Outputs (all runs identical):```
{
  "full_name": "Albert Smith",
  "age": 34,
  "city": "Springfield",
  "job_title": "software engineer"
}
**Variance observed:** None — identical outputs across all runs (expected at temperature 0.0).
```Comparison to V1/V2

Preamble: Eliminated
Format: Strict, valid JSON (parseable with json.loads)
Reliability: 100% in tests; native Converse API would guarantee via constrained decoding
Variance: None observed```
### Native Bedrock Structured Outputs via Converse API (Full Win)

**Method:** boto3 `converse()` with `outputConfig.textFormat = {"type": "json_schema", ...}` → token-level constrained decoding  
**Inference Profile ID:** `global.anthropic.claude-sonnet-4-5-20250929-v1:0` (global cross-Region for reliable on-demand access)  
**Temperature:** 0.0  
**Prompt:** Minimal extraction instruction + bio (heavy "ONLY JSON" phrasing not required thanks to native enforcement)  
**Schema:** Same as playground (required fields: full_name, age, city, job_title; additionalProperties: false)  
**Runs:** At least 1 successful (repeat 3–5× for variance check — expect identical outputs at temp=0)  
**Output (all runs):**  
```json
{
  "full_name": "Albert Smith",
  "age": 34,
  "city": "Springfield",
  "job_title": "software engineer"
}
**Token Usage (first boto3 run):**
- Input: 354
- Output: 26
- Total: 380
**Key Portfolio Demonstration:**
- Implemented native Bedrock structured JSON outputs using `outputConfig.textFormat` with json_schema → achieved guaranteed schema compliance without prompt hacks or post-processing.
- Successfully navigated inference profile routing (`global.` prefix) for latest Claude 4.5 models.
- Logged real invocation metrics (tokens) for observability.
