## Week 3: Reliability Engineering Complete

**Theme Recap**  
Treated the LLM like a distributed system component — automated batch evals, added resilience (retries), classified flakes, quantified pass rates, and prepared cost observability.

**Key Achievements**

- Batch runner (`3_attempt_retry_logic_V5.py`): CLI args, per-run CSV logging, all columns (tokens, latency, confidence, flake_reason, guardrail_intervened, retry_count, match %)
- Retry: 3-attempt exponential backoff
- Determinism sweep (Day 18): 100% pass across temp=0.0/0.3/0.7 on adversarial/benign tests — zero flake increase
- Failure classification: guardrail_block, low_confidence, json_parse_error, empty response, api_failed
- Guardrail sweeps (v3 Medium, v4 Low): success drops from 91.7% → 16.7%, block rate 83–100%, ~82% cost savings ($0.0422 → $0.0076 for 36 runs)
- Observability: full summary with total interventions, block rate, blocked runs, latency total/avg, cost estimation
- No false positives in no-guardrail mode — metrics now 100% reliable

**Biggest Wins**

- Guardrails deliver massive cost reduction by blocking early (82% savings)
- Extraction remains perfect (100% exact-match) on passes
- High determinism on Claude Sonnet 4.5 — temperature barely affects flake rate

**Surprises**

- Low (v4) and Medium (v3) block nearly identically on this adversarial set
- Some successes still show intervened=True (partial blocks/redactions)

**Repo Highlights**

- scripts/3_attempt_retry_logic_V5.py — mature harness
- evaluation/: CSVs for no-GR + v4 + v3
- docs/: Day21.md with comparison table

**Ready for Week 4**  
Batch script + golden/adversarial sets are primed for RAG injection (toy dataset, Titan Embeddings, hallucination comparison).

Week 3: Complete ✅
