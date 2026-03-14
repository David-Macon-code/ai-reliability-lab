# Week 2 Completion – Observability + Security + API Control  

**30-Day PromptOps Execution Checklist – AWS Bedrock**

**Theme:** Monitor AI like a NOC monitors systems  

**Date completed:** ~March 2026 (Week 2)  

**Key Activities & Outcomes:**

- Set up full API scripting with boto3 Converse: latency tracked via timeit, token usage/cost notes from response['usage'] → saved to `/evaluation/` CSVs.
- Prompt injection testing (Day 11): Classic attacks (DAN-style, role-reversal, etc.) → Bedrock content filters caught many at default, but some leaked at LOW confidence.
- Added guardrailConfig in Converse calls (Medium strength policy) → re-tested injections.
- Results: Golden benign prompts → 100% pass (0% false positives).  
  Injection attempts (15 total) → **93.3% blocked** (14/15), 1 LOW-confidence leak through.
- Validation scripts enhanced to parse clean JSON from structured outputs (no try/except soup needed).
- Observability: Built simple logging for trace, latency, tokens → ready for batch runs in Week 3.

**Security Takeaways:**

- Bedrock Guardrails + structured outputs = strong combo for injection resistance without heavy in-prompt defenses.
- Reference: AIF-C01 Guardrails module knowledge applied directly.

**Next:** Week 3 automation (batch processing, retries, flake rate tracking) will build on this foundation.
