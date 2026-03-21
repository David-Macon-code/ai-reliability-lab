### Week 3 Completion: Reliability Engineering Sprint

Week 3 focused on treating the LLM like a distributed system component — shifting from exploratory testing to systematic, repeatable automation. The goal was to build a production-grade batch pipeline that runs unattended evals, surfaces flakes reliably, quantifies pass rates, and tracks cost/performance metrics for optimization.

**Major Wins**  

- Proved that Bedrock Guardrails deliver ~82% cost reduction on adversarial prompts while preserving perfect extraction quality (100% exact-match on passes) — a massive real-world reliability + economics win that directly showcases employability in PromptOps and AIF-C01-level AI workflows.

**Accomplishments**

- Built and polished a robust batch evaluation harness (`3_attempt_retry_logic_V5.py`) with CLI args, full CSV logging, retry logic (3 attempts with backoff), and detailed flake classification
- Ran temperature sweep (0.0 / 0.3 / 0.7) on adversarial/benign tests — 100% pass rate across all temps, zero meaningful flake increase, high determinism on Claude Sonnet 4.5
- Implemented multi-guardrail sweeps (v3 Medium, v4 Low) — success rate dropped from 91.7% → 16.7%, block rate 83–100%, ~82% cost savings ($0.0422 → $0.0076 for 36 runs)
- Added comprehensive observability: total interventions (all runs), block rate %, blocked runs, latency (avg + total), confidence, exact-match %, cost estimation
- Fixed false positives in no-guardrail mode — intervention counts now 100% accurate (0 when no guardrail active)

**Comparison Table (--runs 3, adversarial set)**

| Metric                          | No Guardrail | Low (v4) | Medium (v3) |
|---------------------------------|--------------|----------|-------------|
| Success Rate                    | 91.7%        | 16.7%    | 16.7%       |
| Total Guardrail Interventions   | 0            | 36       | 30          |
| Guardrail Block Rate            | 0.0%         | 100.0%   | 83.3%       |
| Blocked Runs                    | 3 (8.3%)     | 30 (83.3%) | 30 (83.3%)  |
| Avg Confidence (success)        | 0.964        | 0.975    | 0.975       |
| Avg Exact-Match % (success)     | 100.0%       | 100.0%   | 100.0%      |
| Avg Latency (success)           | 2.085s       | 2.713s   | 2.426s      |
| Total Estimated Cost            | $0.0422      | $0.0076  | $0.0076     |

**Insights**

- Guardrails dramatically reduce success on adversarial prompts (92% → 17%) by blocking early — huge cost saver (~82% reduction)
- Extraction quality remains perfect (100% exact-match, ~0.975 confidence) when passes occur
- Latency increases slightly (~0.3–0.6s) due to guardrail evaluation/trace overhead
- Low (v4) and Medium (v3) strengths show nearly identical blocking on this dataset — both highly effective here

**Final Polish**

- Enhanced summary with total guardrail interventions (all runs), block rate %, blocked runs count, visual separators
- Eliminated false positives in no-guardrail mode: `intervened` defaults to `False`, guarded by `args.guardrail_version` in success/failure branches
- No more incorrect counts when guardrail is disabled

**Next**
- Haiku modelId testing.
- Setup Jupyter notebook
- Week 4: RAG basics, Titan Embeddings G1, toy dataset retrieval

Week 3: Complete ✅
