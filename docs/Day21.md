## Day 21 — Week 3 Wrap-Up: Reliability Engineering Complete



**Major Wins**

- Proved that Guardrails can deliver ~82% cost reduction while preserving perfect extraction quality on passes — a huge reliability + economics win.
- Built a production-grade batch evaluation harness that reliably quantifies LLM reliability, flake rates, guardrail effectiveness, and cost impact
- Demonstrated ~82% cost savings with Bedrock Guardrails on adversarial prompts — massive real-world value for PromptOps / AIF-C01
- Achieved 100% exact-match accuracy on all successful extractions across configs — structured outputs are rock-solid
- Eliminated false positives in no-guardrail metrics — intervention counts now 100% accurate
- Full observability in a clean console summary: success rate, confidence, match %, latency (avg + total), interventions, block rate, blocked runs, cost estimation

**Accomplishments**

- Re-ran full sweeps (--runs 3) across no-guardrail, Low (v4), and Medium (v3) configs
- Guardrails dropped success rate from 91.7% → 16.7%, blocked ~83% of attempts early
- Cost reduced from $0.0422 → $0.0076 (~82% savings) — guardrails prevent expensive completions
- Extraction quality remained perfect (100% exact-match, ~0.975 avg confidence) on passes
- Latency increased slightly (~0.3–0.6s) due to guardrail trace/evaluation overhead
- v3 Medium and v4 Low showed nearly identical blocking behavior on this adversarial set

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


**Final Polish & Fixes**

- Added total guardrail interventions (all runs), block rate %, blocked runs count, visual separators in summary
- Fixed false positives in no-guardrail mode: `intervened` defaults to `False`, guarded by `args.guardrail_version` in success/failure branches
- No more incorrect intervention counts when no guardrail is active

**Next**

- Haiku modelId testing.
- Setup Jupyter notebook
- Week 4: RAG basics, Titan Embeddings G1, toy dataset retrieval
