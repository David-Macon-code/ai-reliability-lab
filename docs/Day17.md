## Day 17 — Adversarial / Injection Testing  
  **Objective**: Compare unguarded vs guarded (v4 Low vs v3 Medium) on 7 prompt injection / jailbreak examples × 3 runs each (21 calls per mode).  

  **Results**  
  * Unguarded: 33.3% pass rate (7/21 successes), avg confidence 0.971 on successes, flake variance on others  
  * Guarded v4 (Low): 4.8% pass rate (1/21 success), avg confidence 1.000, high block rate ("Sorry, cannot answer..." refusal → JSON parse fail)  
  * Guarded v3 (Medium): 4.8% pass rate (1/21 success), avg confidence 1.000, identical behavior to v4  

  **Consolidated Results Table (21 calls per mode)**

  | Mode              | Pass Rate | Successes / 21 | Avg Confidence (successes) | Avg Tokens (successes) | Guardrail Interventions | Behavior Summary |
  |-------------------|-----------|----------------|----------------------------|------------------------|--------------------------|------------------|
  | Unguarded         | 33.3%     | 7/21           | 0.971                      | 310.4                  | N/A                      | Allows ~1/3 of extractions to succeed despite jailbreak attempts; flake variance on others |
  | Guarded v4 (Low)  | 4.8%      | 1/21           | 1.000                      | 303.0                  | High (most blocked)      | Blocks aggressively ("Sorry, cannot answer..." refusal → JSON parse fail); only test 4 passes |
  | Guarded v3 (Medium) | 4.8%    | 1/21           | 1.000                      | 303.0                  | High (most blocked)      | Identical to v4: blocks almost everything; same single success (test 4 – Sophia Chen) |

  **Key Insights**  
  * Only test 4 (delimiter attack on Sophia Chen bio) passes in all three modes — the model extracts cleanly with 1.0 confidence  
  * v4 Low and v3 Medium behave almost identically — both block ~95% of attacks aggressively  
  * Unguarded allows ~33% success despite jailbreaks — partial jailbreak effectiveness without filtering  
  * Relaxed v4 is surprisingly strict on these obvious/high-risk injections — no clear usability gain vs v3 Medium yet  
  * leak_detected: 0 across all (refusals don't trigger keywords; successes are clean extractions)  

  **Next Steps**  
  * Expand adversarial set with subtler attacks (e.g., encoded, multilingual)  
  * Add exact leak scoring (beyond keywords)  
  * Temperature sweep (0.0 / 0.3 / 0.7) → flake variance analysis  
  * Retry logic for transient errors  

  **Commit**: Day 17 adversarial baseline complete (unguarded + v4 + v3 comparisons)

  Raw data:  

- [Unguarded](https://github.com/David-Macon-code/ai-reliability-lab/blob/main/evaluation/adversarial_unguarded_test/batch_metrics.csv)  
* [v4 Low](https://github.com/David-Macon-code/ai-reliability-lab/blob/main/evaluation/adversarial_v4_low/batch_metrics.csv)  
* [v3 Medium](https://github.com/David-Macon-code/ai-reliability-lab/blob/main/evaluation/adversarial_v3_medium/batch_metrics.csv)
