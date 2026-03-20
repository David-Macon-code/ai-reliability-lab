* Day 19 — Exact-match scoring & quality metrics  
  * Added `match_score` (0–3) & `match_percentage` columns (parsed vs expected fields)  
  * Added average match % to summary (successful runs only)  
  * Fixed fallback safety & indentation → real golden inputs used, no crashes  
  * Golden set test: 100% pass rate, perfect 3.0 / 100.0% match on all 24 runs  

  Consolidated Day 19 Results Table (golden set, 24 calls)

  | Metric                        | Value          | Notes                                      |
  |-------------------------------|----------------|--------------------------------------------|
  | Total API calls               | 24             | 8 tests × 3 runs                           |
  | Pass rate                     | 100.0%         | All runs passed flake checks               |
  | Avg confidence                | ~0.95–1.0      | High & consistent on real bios             |
  | Avg match score               | 3.0            | All three fields (name, age, city) matched |
  | Avg match percentage          | 100.0%         | Perfect extraction vs expected             |
  | Avg total tokens              | ~300           | Consistent with previous runs              |
  | Avg latency                   | ~2–3s          | Stable, no spikes                          |

  Quick Insights:  
  * 100% match on golden set — model extracts name, age, city perfectly against expected  
  * Fallback safety prevents blank message crashes; debug logs show real inputs used  
  * Scoring works on both golden (high match) and adversarial (0% match without expected)  
  * Harness now tracks confidence + exact quality + leaks + retries  

  Next: Temperature sweep on failing tests (e.g. test 8), more subtle adversarial attacks, cost estimation per call  

  Commit: Day 19 complete – exact-match scoring integrated & tested (100% match on golden set)
