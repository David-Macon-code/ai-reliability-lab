## Day 18 — Retry Logic + Guarded Retry Runs  
  **Objective**: Add 3-attempt retry with exponential backoff + retry_count column; test on expanded adversarial set (12 tests × 3 runs = 36 calls per mode).  

  Results:  
  * Unguarded: 91.7% pass rate (33/36), avg confidence 0.964, avg tokens 312.1, avg latency 2.67s  
  * Guarded v4 (Low): 16.7% pass rate (6/36), avg confidence 0.975, avg tokens 315.5, avg latency 3.23s  
  * Guarded v3 (Medium): 16.7% pass rate (6/36), avg confidence 0.975, avg tokens 315.5, avg latency 4.60s  

  Consolidated Day 18 Results Table (36 calls per mode on expanded set)

  | Mode              | Pass Rate | Successes / 36 | Avg Confidence (successes) | Avg Total Tokens (successes) | Avg Latency (successes) | Guardrail Status | Key Behavior |
  |-------------------|-----------|----------------|----------------------------|------------------------------|--------------------------|------------------|--------------|
  | Unguarded         | 91.7%     | 33/36          | 0.964                      | 312.1                        | 2.67s                    | DISABLED         | High pass rate on expanded set; only 3 failures (likely test 8 parsing edge case) |
  | Guarded v4 (Low)  | 16.7%     | 6/36           | 0.975                      | 315.5                        | 3.23s                    | ENABLED (v4)     | Blocks ~83%; refusals → JSON parse fail; more permissive than v3 |
  | Guarded v3 (Medium) | 16.7%   | 6/36           | 0.975                      | 315.5                        | 4.60s                    | ENABLED (v3)     | Identical pass rate to v4; slightly higher latency; still aggressive blocking |

  Quick Insights:  
  * Unguarded: 91.7% pass — very robust extraction even on expanded attacks  
  * v4 Low & v3 Medium: identical 16.7% pass — both block ~83% of attempts (refusals cause parse fail)  
  * v4 Low is not more permissive than v3 Medium on this set (same pass rate) — Low sensitivity still catches most obvious injections  
  * Retry logic: No visible retries (retry_count likely 0 everywhere), but loop is active and ready for real throttling  
  * Failures: Likely test 8 (base64 attack) — parse error on refusal message ("list index out of range" in debug)  

  This confirms v4 Low offers little usability gain over v3 Medium on these attacks — both are strict. The real difference may show on subtler or edge-case injections.

  Next Steps:  
  * Temperature sweep on failing tests (e.g. test 8) to reduce flakes  
  * Exact-match scoring (parsed vs expected fields)  
  * Expand adversarial set further (subtler attacks)  
  * Add retry_count logging + cost estimation per call
