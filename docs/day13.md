# Day 13 – Validation Script Enhancements + Week 2 Reporting Kickoff

**Date:** ~March 2026  
**Theme:** Observability + Security + API Control (Week 2)

## Goals & Achievements

- Enhanced `v3_json_test.py` to programmatically parse and log Bedrock Guardrail trace details from Converse API responses:
  - `guardrail_intervened` (bool)
  - `guardrail_filter_type` (e.g., "PROMPT_ATTACK")
  - `guardrail_action` (e.g., "BLOCKED")
  - `guardrail_latency_ms` (~240–300 ms typical)
  - `guardrail_confidence` (LOW / MEDIUM / HIGH)
- Switched CSV logging to `csv.DictWriter` for consistent headers and reliable appending (no more mismatched columns).
- Ran injection batch (`IS_INJECTION_TEST = True`):
  - **15/15 cases blocked (100%)**
  - All classified as PROMPT_ATTACK
  - Confidence mix: mostly HIGH, some MEDIUM/LOW
  - Avg end-to-end latency: ~0.437 s (quick early fails due to blocking)
  - Tokens: 0 on all blocked cases (no generation occurred)
- Ran golden benign batch (`IS_INJECTION_TEST = False`):
  - **50% pass rate** (4/8 valid JSON outputs)
  - **50% blocked** due to LOW-confidence PROMPT_ATTACK false positives
- Started drafting Week 2 findings:
  - Documented over-blocking issue on safe inputs
  - Highlighted value of automated trace parsing for debugging and future alerting/SLO tracking

## Key Findings

- Native structured outputs (json_schema mode) deliver **100% valid JSON** when Guardrails allow generation.
- Guardrails (High strength) → perfect injection blocking, but introduce **50% false positives** on golden benign cases.
- Trace parsing now auto-logs intervention details → huge win for observability and reliability engineering.

## Next (Day 14)

- Tune Guardrail policy: lower from High to Medium strength / adjust confidence thresholds.
- Re-run both injection and golden batches to compare before/after metrics.
- Finalize Week 2 completion report with updated tables and takeaways.

**Status:** Day 13 complete  
**Related commits:** Guardrail trace parsing added, CSV logging fixed with DictWriter
