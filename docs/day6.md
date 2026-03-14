# Day 6 – Multi-Run Testing + Golden Set

**Date:** ~March 2026  
**Theme:** LLM Foundations + Controlled Prompt Testing (Week 1)

## Goals & Achievements

- Ran each prompt version (V1–V3) 5 times via script (V3 using structured API).
- Logged determinism variance and token usage from response['usage'].
  - V1/V2: Higher variance at temperature>0; V3: Perfect determinism at 0.0.
- Created golden test set: 8–10 cases in `/evaluation/golden_test.json`.
- Ran V1–V3 on subset: Logged JSON validity % (V1 ~65%, V2 ~85%, V3 ~100%).

## Key Findings

- Structured outputs shine: 100% validity, lower tokens than prompted formats.
- Variance low overall; hallucinations minimal on golden cases.

## Next

- Day 7: Compile Week 1 report.

**Status:** Day 6 complete.  
**Related Artifacts:** /evaluation/golden_test.json, /evaluation/v3_metrics_log.csv (partial)
