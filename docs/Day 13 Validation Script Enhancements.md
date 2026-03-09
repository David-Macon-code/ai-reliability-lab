# Day 13 – Validation Script Enhancements + Week 2 Reporting Kickoff

**Date:** ~March 2026  
**Theme:** Enhance observability by parsing Bedrock Guardrail traces programmatically and start drafting Week 2 findings.

## Goals & Achievements

- Enhanced `v3_json_test.py` to parse and log guardrail trace details:
  - `guardrail_intervened` (bool)
  - `guardrail_filter_type` (e.g., "PROMPT_ATTACK")
  - `guardrail_action` (e.g., "BLOCKED")
  - `guardrail_latency_ms` (~240–300 ms typical)
  - `guardrail_confidence` (LOW / MEDIUM / HIGH)
- Used `csv.DictWriter` for consistent headers and reliable appending
- Ran injection batch (IS_INJECTION_TEST = True):
  - 15/15 cases blocked (100%)
  - All PROMPT_ATTACK, confidence mix (mostly HIGH, some MEDIUM/LOW)
  - Avg latency: ~0.437 s (quick early fails)
  - Tokens: 0 on all blocked cases
- Ran golden batch (IS_INJECTION_TEST = False):
  - 50% pass rate (4/8 valid JSON)
  - 50% blocked on LOW-confidence PROMPT_ATTACK detections
- Started Week 2 findings draft:
  - Documented over-blocking on benign inputs (false positives)
  - Highlighted value of trace parsing for debugging

### Key Findings

- Native structured outputs → 100% valid JSON when not blocked
- Guardrail (High strength) → perfect on injections, but 50% false positives on golden
- Trace parsing now auto-logs intervention details → enables future alerting/SLO tracking

### Next (Day 14)

- Tune guardrail confidence threshold (High → Medium strength)
- Re-run both modes to compare before/after
- Finalize Week 2 report with metrics tables

**Status:** Day 13 complete  
**Commits:** Guardrail trace parsing added, CSV logging fixed with DictWriter
