## Day 16 – Reliability Engineering Baseline (March 16, 2026)

**Goal**: Establish a stable evaluation harness using Bedrock Converse API with native structured outputs, add guardrail toggle, run scaled baselines (unguarded + guarded), and confirm 100% golden pass rate on benign inputs.

### Key Achievements

- **Guardrail v4 created & deployed**  
  - ID: `9g6hem28nedj`  
  - Version: **4** (deployed March 16, 2026 14:09 EDT)  
  - Configuration: Prompt attacks / jailbreak sensitivity set to **Low** (other filters unchanged)

- **Guardrail toggle fully implemented**  
  - Arg: `--guardrail-version` (e.g. `--guardrail-version 4` or omit for disabled)  
  - Conditional `guardrailConfig` in Converse call  
  - Summary prints guardrail status (ENABLED vX or DISABLED)

- **Baseline runs – Unguarded (no guardrail)**  
  - Model: `global.anthropic.claude-sonnet-4-5-20250929-v1:0` (inference profile)  
  - Runs: 160 total (8 golden tests × 20 runs)  
  - Pass rate: **100.0%** (160/160 runs)  
  - Avg confidence (successful): **0.962**  
  - Avg total tokens: **~296**  
  - Avg latency: ~2.0–3.0s (stable)  
  - flake_reason: None across all runs

- **Baseline runs – Guarded (v4 Low sensitivity)**  
  - Same golden set, `--guardrail-version 4`  
  - Pass rate: **100.0%** on benign inputs  
  - Guardrail interventions: **0** (`guardrail_intervened = False` everywhere)  
  - No false positives on clean bios → confirms relaxed version preserves usability

- **Script & pipeline improvements**  
  - Native structured outputs working reliably (json_schema enforced)  
  - Real golden inputs used (`bio` field) instead of dummy fallback  
  - Aggregate metrics in summary (confidence, tokens)  
  - Debug prints added (can be toggled or logged to file later)  
  - Fixed multiple Bedrock validation issues: inference profile, schema constraints, temperature+top_p conflict, duplicate counters, scoping errors

### Metrics Snapshot (Unguarded – 160 runs)

| Metric                        | Value          | Notes                                      |
|-------------------------------|----------------|--------------------------------------------|
| Total API calls               | 160            | 8 tests × 20 runs                          |
| Pass rate                     | 100.0%         | All runs passed flake checks               |
| Avg confidence                | 0.962          | High & consistent on real bios             |
| Avg total tokens              | ~296           | Input ~200 + output ~96 typical            |
| Latency range                 | ~1.7–3.7 s     | Occasional higher due to cold starts       |
| flake_reason                  | None           | No low-confidence or guardrail issues      |

### Next Steps (Day 17 / Week 3)

- Run adversarial/injection test set (unguarded vs v4 vs v3) → measure block rates
- Temperature sweep (0.0 / 0.3 / 0.7) → analyze confidence & flake variance
- Add retry logic for transient errors (ThrottlingException, etc.)
- Implement exact-match scoring against `"expected"` fields in golden_test.json

**Status**: Day 16 complete — stable baseline established with unguarded + guarded (v4) comparisons on benign data. Ready for deeper reliability experiments.

Commit: "Day 16 COMPLETE: 100% golden pass, guardrail toggle + v4 deployed, scaled baselines captured"
