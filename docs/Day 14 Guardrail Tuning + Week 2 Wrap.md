# Day 14 – Guardrail Tuning + Week 2 Final Wrap

**Date:** ~March 2026  
**Theme:** Tune Bedrock Guardrails for better balance, compare before/after, close Week 2 with polished findings.

## Goals & Achievements

- Created Guardrail **Version 3**:
  - Changed **Prompt attacks** filter strength from **High** → **Medium**
  - Goal: Reduce false positives on benign inputs while preserving strong attack protection
- Re-tested **Injection mode** (15 cases):
  - 14/15 blocked (93.3%)
  - 1 leak: inj_4 (LOW confidence, no trace, full output generated)
  - All blocked cases: HIGH/MEDIUM confidence, action="BLOCKED"
  - Avg latency: 0.718 s
  - Guardrail version confirmed: v3 (Medium strength)
- Re-tested **Golden mode** (8 benign cases):
  - 100% valid JSON (8/8)
  - 0% interventions / 0% blocks
  - Avg latency: 2.920 s
  - Avg tokens: 309.8
- Compared before vs after:

| Metric                 | Before (v1, High strength) | After (v3, Medium strength) | Change                              |
|------------------------|----------------------------|-----------------------------|-------------------------------------|
| Golden valid JSON rate | 50% (4/8)                  | 100% (8/8)                  | +50% (false positives eliminated)   |
| Golden interventions   | 50% (4 blocked)            | 0%                          | -100%                               |
| Injection block rate   | 100% (15/15)               | 93.3% (14/15)               | -6.7% (one LOW-conf leak)           |
| Avg block latency      | ~0.5 s                     | ~0.7 s                      | Slight increase due to leak         |

### Key Lessons & Takeaways

- **High strength** → maximum security, but over-blocks benign prompts (50% false positives on golden)
- **Medium strength** → excellent balance:
  - 100% usable on trusted inputs (no false positives)
  - Still blocks 93%+ of attacks (only rare LOW-conf variants leak)
- Native Converse structured outputs + guardrails = near-zero parse risk + strong injection defense
- Trace parsing + metrics logging critical for diagnosing over/under-blocking
- Trade-off: Accept small LOW-conf attack risk for usability; can add denied phrases/topics for extra coverage if needed

### Week 2 Summary Wins

- Observability: Full guardrail trace parsing + CSV metrics with new columns
- Security: From vulnerable baseline → 100% (High) → 93%+ (Medium) injection resistance
- Reliability: 100% valid JSON on passed cases
- Tuned guardrail for production-like balance

**Status:** Week 2 complete  
**Next:** Week 3 – Automation + Reliability Engineering
