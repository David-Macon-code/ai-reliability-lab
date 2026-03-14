# Week 1 Findings Report  

**30-Day PromptOps Execution Checklist – AWS Bedrock**

**Theme:** LLM Foundations + Controlled Prompt Testing  

**Date completed:** ~March 2026 (Week 1)  

**Key Activities & Outcomes:**

- Studied core inference concepts: tokens, context windows (esp. Claude 4.5 family: 200k+ tokens), temperature, top_p — documented in personal notes.
- Documented 5 common failure modes: hallucinations, prompt injection, sycophancy, context loss, content filtering false positives (Bedrock-specific).
- Prompt versions:
  - V1: Baseline task prompt → inconsistent structure, ~60-70% JSON validity on manual tests.
  - V2: Added role + clear instructions → improved coherence but still parsing failures.
  - V3: Leveraged native structured outputs (Converse API + json_schema in outputConfig) → **~100% valid JSON** across 5+ test runs (no post-processing needed).
- Golden test set created: 8–10 cases in `/evaluation/golden_test.json`.
- Ran each version 5× → V3 showed perfect determinism at temperature=0.0, token usage logged via response['usage'].
- **Major win:** Bedrock's token-level constrained decoding (GA for Claude 4.5 models) eliminates the "JSON hardest" problem — reliability jump from ~70% to 100%.

**JSON Success Rate Table:**

| Prompt Version | JSON Validity % | Avg Tokens | Notes |
|----------------|-----------------|------------|-------|
| V1 (baseline)  | ~65%            | ~180       | Manual parsing often failed |
| V2 (structured prompt) | ~85%     | ~210       | Better but still occasional escapes |
| V3 (json_schema) | **100%**      | ~160-190   | Guaranteed valid; no retries needed |

**Conclusion:** Native structured outputs are production-ready and transformative for entity extraction / structured tasks on Bedrock. Minimal prompt engineering required for format enforcement.
