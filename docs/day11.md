# Day 11 – Prompt Injection Testing

**Date:** ~March 2026  
**Theme:** Observability + Security + API Control (Week 2)

## Goals & Achievements

- Tested 5 prompt injection attempts: DAN, HACKED, hacked JSON, XSS, pirate.
- Logged results (Bedrock content filters behavior).
- Results: 5/5 defeated—100% valid JSON, no leaks.
- Golden set: 100% pass (no false positives at this stage).

## Key Findings

- Bedrock filters effective at default; all classified as attacks.
- No generation on blocked cases (0 tokens).
- Documented in /evaluation/ (e.g., injection_results.md at earlier commit).

## Next

- Day 12: Add guardrails.

**Status:** Day 11 complete.  
**Related Artifacts:** X post with video demo; /evaluation/v3_metrics_log.csv (injection runs)
