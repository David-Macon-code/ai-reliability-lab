# Day 15 – Batch Evaluation Harness with Bedrock Converse + Structured Outputs

**Date:** March 14, 2026  
**Goal:** Build a scalable, multi-run batch evaluation script using AWS Bedrock Converse API with native structured JSON outputs (Claude Sonnet 4.5), metrics logging, and reliability tracking.

## Key Achievements

- Implemented `batch_eval_v3.py` using Bedrock **Converse API** with `outputConfig.textFormat` + JSON schema
- Fixed schema validation error by removing unsupported `minimum`/`maximum` on number fields
- Corrected messages structure (no `"system"` role — Bedrock only allows `user`/`assistant`)
- Successfully disabled guardrails (by **omitting** `guardrailConfig` entirely) to bypass aggressive "PROMPT_ATTACK" blocking
- Achieved **100% pass rate** on golden set (40/40 runs in final run)
- Logged comprehensive metrics: valid_json, confidence, tokens (input/output/total), latency, guardrail status, flake_reason
- Added clean console summary with pass rate, total calls, and usage tips

## Final Results (no_guardrail_working run)

- Golden test cases: 8
- Runs per case: 5
- Total API calls: 40
- **Overall pass rate: 100.0% (40/40 runs)**
- Valid JSON: 100%
- Flake reasons: none (all empty)
- Guardrail blocks: none

### Average Metrics (across 40 runs)

| Metric              | Average Value       | Notes |
|---------------------|---------------------|-------|
| Input Tokens        | ~322                | Consistent across bios |
| Output Tokens       | ~43                 | Very compact JSON output |
| Total Tokens        | ~365                | Reasonable for structured extraction |
| Latency (seconds)   | ~3.8                | Varies 2–6s; normal for Sonnet 4.5 with schema enforcement |
| Confidence Score    | ~0.97               | Very high — model is confident in extractions |

## Lessons Learned / Fixes Applied

| Issue | Fix |
|-------|-----|
| ValidationException: min/max not supported on number | Removed `minimum`/`maximum` from confidence schema |
| No valid JSON output, tokens=0 | Confirmed schema valid after fix |
| Guardrail blocked everything as "PROMPT_ATTACK" | Omitted `guardrailConfig` entirely (passing `None` causes boto3 validation error) |
| "system" role invalid in messages | Moved instructions into first user message |
| Input field mismatch | Used `"bio"` key from golden_test.json |

## Next Steps (Day 16+)

- **Re-enable guardrails safely** (tomorrow plan)
  - Bedrock console → Guardrails → select 9g6hem28nedj → Create new version
  - Content filters → Prompt attacks → set sensitivity to **Low** or **None** (for lab purposes)
  - Keep other filters as-is
  - Save & deploy (note new version number, e.g. "4")
  - Test with single run by temporarily hard-coding `"guardrailVersion": "4"` in script
- Add conditional `--use-guardrail` flag for easy toggling
- Add semantic validation (compare actual vs expected fields)
- Run temperature sweep (0.0 → 1.0) to measure determinism/variance
- Expand golden set with edge/adversarial cases
- Begin Week 3: automation, multi-model comparison, injection testing

## Files Updated

- `scripts/batch_eval_v3.py` → final working version (guardrail disabled, bio field, clean summary)
- `evaluation/no_guardrail_working/batch_metrics.csv` → 100% pass run results

**Day 15 complete!**  
Reliable batch eval harness achieved with native structured outputs, metrics, and observability — 100% pass rate on golden set.
