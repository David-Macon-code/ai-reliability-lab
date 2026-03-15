# Day 15 – Batch Evaluation Harness with Bedrock Converse + Structured Outputs

**Date:** March 14, 2026  
**Goal:** Build a scalable, multi-run batch evaluation script using AWS Bedrock Converse API with native structured JSON outputs (Claude Sonnet 4.5), guardrails, metrics logging, and reliability tracking.

## Key Achievements

- Implemented `batch_eval_v3.py` using Bedrock **Converse API** with `outputConfig.textFormat` + JSON schema
- Fixed schema validation error by removing unsupported `minimum`/`maximum` on number fields
- Corrected messages structure (no `"system"` role — Bedrock only allows `user`/`assistant`)
- Successfully disabled guardrails (by **omitting** `guardrailConfig` entirely) to bypass aggressive "PROMPT_ATTACK" blocking
- Achieved **100% pass rate** on golden set (40/40 runs in final run)
- Logged comprehensive metrics: valid_json, confidence, tokens (input/output/total), latency, guardrail status, flake_reason
- Added console summary with pass rate, total calls, and usage tips

## Final Results (no_guardrail_working run)

- Golden test cases: 8
- Runs per case: 5
- Total API calls: 40
- **Overall pass rate: 100.0% (40/40 runs)**
- Confidence scores: consistently high (typically 0.95–1.0)
- Valid JSON: 100%
- Tokens per call: ~320 input / ~40–50 output (total ~360–370)
- Latency: ~2–6 seconds per call (normal for structured decoding)

## Lessons Learned / Fixes Applied

| Issue | Fix |
|-------|-----|
| ValidationException: min/max not supported on number | Removed `minimum`/`maximum` from confidence schema |
| No valid JSON output, tokens=0 | Confirmed schema valid after fix; added system prompt in user message |
| Guardrail blocked everything as "PROMPT_ATTACK" | Omitted `guardrailConfig` entirely (passing `None` causes boto3 validation error) |
| "system" role invalid in messages | Moved instructions into first user message |
| Input field mismatch | Used `"bio"` key from golden_test.json |

## Next Steps (Day 16+)

- Create new guardrail version with **low** or **none** sensitivity for "Prompt attacks"
  - Bedrock console → Guardrails → select 9g6hem28nedj → Create new version → relax prompt attack filter → deploy (e.g. version 4)
  - Test with hard-coded version number or add `--use-guardrail` flag
- Add semantic validation (compare actual vs expected fields)
- Run temperature sweep (0.0 → 1.0) to measure determinism
- Expand golden set with adversarial / edge cases
- Begin Week 3: automation, multi-model comparison, injection testing

## Files Updated

- `scripts/batch_eval_v3.py` → final working version (guardrail disabled, bio field, clean summary)
- `evaluation/no_guardrail_working/batch_metrics.csv` → 100% pass run results

**Day 15 complete!**  
Reliable batch eval harness achieved with native structured outputs, metrics, and observability. Ready for deeper reliability engineering.

Commit: Day 15: Finalized batch harness – 100% pass rate, guardrail disabled, full metrics logging
