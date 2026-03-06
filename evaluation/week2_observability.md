# Week 2 – Observability Baseline

- 8 golden cases evaluated using Bedrock Converse + native json_schema
- 100% valid JSON outputs
- 100% exact match after aligning expected full_name titles
- Avg latency: ~2.14 s
- Avg total tokens: 309.8
- CSV logging: evaluation/v3_metrics_log.csv
- Results: evaluation/v3_results.json

## Week 2 - Observability & Metrics Baseline

## Overview

- Model: Claude Sonnet 4.5 (global.anthropic.claude-sonnet-4-5-20250929-v1:0)
- API: Bedrock Converse with native json_schema structured outputs
- Golden set: 8 cases (100% pass rate after aligning expected full_name titles)
- Runs analyzed: 5 full batch executions (40 total calls)
- Key metrics tracked: per-example latency, tokens (input/output/total), golden match rate
- Files: `v3_metrics_log.csv`, `v3_results.json`

## Aggregate Stats (Across 5 Runs, 40 Calls)

| Metric                  | Average   | Min    | Max    | Std Dev | Notes                        |
|-------------------------|-----------|--------|--------|---------|------------------------------|
| Latency (all cases)     | ~2.09 s   | 1.43 s | 5.20 s | ~0.6 s  | Includes cold-start          |
| Latency (cases 2–8)     | ~1.83 s   | 1.43 s | 3.53 s | ~0.3 s  | Very consistent after warm   |
| Total Tokens            | 309.8     | 302    | 316    | ~4.5    | Extremely stable             |
| Golden Pass Rate        | 100.0%    | -      | -      | -       | All 8 cases match exactly    |

## Per-Case Latency Breakdown (Averages from 5 Runs)

|Case ID|Avg Latency (s)|Min (s)|Max (s)|Std Dev (s)|Observation|
|---|---|---|---|---|---|
|1|**3.92**|3.13|5.20|0.83|Consistent cold-start outlier (+~2.1s penalty)|
|2|1.78|1.68|2.01|0.12|Stable|
|3|1.74|1.59|1.93|0.13|Stable|
|4|1.90|1.54|1.96|0.15|Stable|
|5|1.72|1.43|1.99|0.20|Stable|
|6|1.74|1.55|1.96|0.14|Stable|
|7|2.17|1.73|3.53|0.67|One spike (likely transient)|
|8|1.78|1.64|1.90|0.10|Very stable|

## Key Observations

- **Cold-start effect** dominates case 1 latency: first Converse call in each script execution pays a 2–3s penalty due to Bedrock serverless backend warming up model resources.
- After the first call, latency stabilizes in the **1.5–2.0s** range — excellent for on-demand inference.
- Token counts show **near-zero variance** (always ~309–310 total), confirming reliable structured output enforcement.
- Occasional spikes (e.g., case 7 in one run) are normal transient queueing/network behavior.

## Lessons Learned

- First-call latency is higher but subsequent calls are fast and predictable — typical for Bedrock on-demand.
- Potential mitigation: add a lightweight warm-up call before the main loop (non-critical for now).
- Metrics logging (CSV + summary print) provides strong observability foundation for future experiments (injections, Guardrails, model swaps).

## Next Steps

- Test prompt injection resilience (Day 11)
- Integrate Bedrock Guardrails (Day 12)
- Compare Haiku 4.5 variant for speed/cost

Last updated: March 05, 2026
