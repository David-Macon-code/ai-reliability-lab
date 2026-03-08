# Week 2: Guardrails Integration & Injection Re-Testing (Day 12)

**Date:** March 8, 2026  
**Model:** `anthropic.claude-sonnet-4-5-20250929-v1:0` (global endpoint)  
**Guardrail:** ID `9g6hem28nedj`, Version `1` (self-owned, ARN: `arn:aws:bedrock:us-east-1:887395463602:guardrail/9g6hem28nedj`)  
**Script:** `scripts/v3_json_test.py` with `guardrailConfig` enabled  
**Test Mode:** `IS_INJECTION_TEST = False` (mixed batch: 4 golden/normal + 4 injection/adversarial cases)  
**Goal:** Integrate Bedrock Guardrails via `guardrailConfig` in Converse API → re-test prompt injections → compare to Day 11 (schema + prompt defense only)

## Guardrail Configuration Highlights

- **Enabled Policies** (console-configured):
  - Prompt attacks filter: HIGH strength
  - Content filters: Standard (hate, insults, sexual, violence, misconduct)
  - Other: Likely defaults (no custom denied topics or PII/regex added yet)
- **Converse API Integration**:

  ```python
  guardrail_config = {
      "guardrailIdentifier": "9g6hem28nedj",
      "guardrailVersion": "1",
      "trace": "enabled"  # Adds detailed trace.guardrail in response
  }
  # Passed in bedrock_runtime.converse(..., guardrailConfig=guardrail_config)
