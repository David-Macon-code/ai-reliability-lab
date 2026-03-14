# Week 2 Completion – Observability + Security + API Control

**Dates:** ~March 5–9, 2026  
**Theme:** Monitor AI like a NOC monitors systems. Leverage Bedrock Guardrails for security, build programmatic observability, and tune for production balance.

## Quick Recap: Week 1 – LLM Foundations + Controlled Prompt Testing

- Studied tokens, context windows, temperature/top_p, hallucinations, and common failure modes.
- Created and iterated on Prompt V1 → V2 → V3 (baseline → role clarity → native structured outputs via Converse API json_schema).
- Achieved **~100% valid JSON** on V3 using Bedrock's structured outputs feature (no heavy prompt engineering needed).
- Built initial golden test set (8 cases) and ran comparisons.
- Key win: Native structured outputs made JSON reliability near-perfect when the model generates output.

## Week 2 Summary & Achievements

Focused on observability, security via Bedrock Guardrails, and API-level control.

### Major Milestones

- Enhanced validation script (`v3_json_test.py`) to parse and log full guardrail traces (intervened, filter_type, action, latency_ms, confidence).
- Fixed CSV logging with `csv.DictWriter` → consistent headers + all guardrail columns.
- Ran extensive before/after testing on golden (benign) and injection (attack) sets.
- Tuned Guardrail from **Version 1 (High strength)** → **Version 3 (Medium strength)**.
- Documented trade-offs with clear metrics.

### Before vs After Guardrail Tuning

| Metric                          | Before (v1, High strength)    | After (v3, Medium strength) | Change / Notes                          |
|---------------------------------|-------------------------------|-----------------------------|-----------------------------------------|
| **Golden valid JSON rate**      | 50% (4/8)                     | **100% (8/8)**              | Eliminated all false positives          |
| **Golden interventions/blocks** | 50% (4 blocked, all LOW conf) | **0%**                      | Benign inputs fully usable              |
| **Injection block rate**        | **100% (15/15)**              | 93.3% (14/15)               | One LOW-conf leak (inj_4)               |
| **Avg block latency**           | ~0.5 s                        | ~0.7 s                      | Slight increase due to leak             |
| **Guardrail detection**         | 100% on attacks               | 93.3% (14/15)               | Still catches MEDIUM/HIGH conf reliably |
| **Avg guardrail latency**       | ~250–280 ms                   | ~250–300 ms                 | Consistent overhead                     |

### Key Lessons

- **Native structured outputs** + Guardrails = production-grade combo: near-zero parse failures + strong injection protection.
- **High strength** → maximum security but over-blocks benign prompts (50% false positives).
- **Medium strength** → excellent balance: 100% usable benign inputs, still blocks 93%+ of attacks (only rare LOW-conf variants leak).
- Trace parsing + metrics logging essential for diagnosing over/under-blocking and guiding tuning.
- Trade-off: Small increase in LOW-confidence attack risk for dramatic usability improvement; can mitigate with denied phrases/topics if needed.

### Week 2 Status

**Complete** — hardened foundations achieved.  
Scripts now observability-aware, guardrail tuned, metrics populated, and trade-offs documented.

## Overview of Remaining Plan (Weeks 3–4)

### Week 3 – Automation + Reliability Engineering

- Theme: Batch scripting, reliability testing, error handling, and scaling runs.
- Key tasks:
  - Build full automation scripts (multi-model, multi-run batches).
  - Add retry logic, error classification, and pass/fail thresholds.
  - Track reliability metrics (e.g., flake rate, retry success).
  - Optimize for token/cost efficiency.

### Week 4 – RAG + Cost Optimization + Enterprise Framing

- Theme: Introduce toy RAG, compare hallucination rates, optimize costs, frame for enterprise use.
- Key tasks:
  - Study embeddings/RAG basics (Bedrock Knowledge Bases + Titan Embeddings).
  - Build toy RAG pipeline (local or Bedrock embeddings).
  - Compare hallucination rates (vanilla vs RAG).
  - Model comparison (Sonnet 4.5 vs Haiku 4.5 vs others).
  - Cost analysis + optimization techniques.
  - Final polish, documentation, and repo wrap-up.

**Overall Project Goal:** By end of 30 days, have a production-grade PromptOps workflow on Bedrock: reliable structured outputs, tuned security, observability, automation, RAG integration, and cost awareness.

Week 2 delivered strong progress on security and observability. Ready for Week 3 automation push.
