# AI Reliability Lab – 30-Day PromptOps Bootcamp

Personal lab and documentation for the 30-Day AI Bootcamp focused on prompt engineering, reliability, observability, and AWS Bedrock integration.

## Progress Log

### Day 1 – LLM Foundations

Studied tokens, context windows, temperature, top_p. Wrote 1-page summary.

### Day 2 – Hallucinations & Failure Patterns

Documented 5 common LLM failure types with Bedrock examples.

### Day 3 – Baseline Prompt V1

Created and tested initial baseline prompt in Bedrock console.

### Day 4 – Prompt V2 (Role + Structure)

Improved prompt with role clarity and structure; compared vs V1.

### Day 5 – JSON Day (Structured Outputs)

Implemented native structured outputs via Converse API `outputConfig.textFormat` with JSON schema. Achieved near-100% valid JSON.

### Day 6 – Multi-Run Testing & Golden Set

Ran V1–V3 multiple times; created golden test set (8–10 cases); logged determinism and token usage.

### Day 7 – Week 1 Findings

Wrote Week 1 report highlighting impact of Bedrock structured outputs on JSON success rate.

### Day 8–10 – API Setup & Observability

Set up Python script with latency/token logging to CSV; built evaluation spreadsheet.

### Day 11 – Prompt Injection Testing

Tested prompt injection attacks; logged Bedrock content filter behavior.

### Day 12 – Guardrail Instructions

Added guardrail instructions to prompt; compared outcomes with/without Bedrock Guardrails.

### Day 13–14 – Validation & Reporting

Enhanced validation script for JSON output; wrote Week 2 report.

### Day 15 – Batch Evaluation Harness

Built batch evaluation harness using Bedrock Converse API with structured JSON outputs, multi-run testing, metrics logging, and 100% pass rate on golden set.

**Final status:** Scalable, reliable eval script with 100% pass rate (40/40 runs), token/latency tracking, and observability. Ready for Week 3 automation and reliability experiments.

**Key files:**

- `scripts/batch_eval_v3.py`
- `evaluation/no_guardrail_working/batch_metrics.csv` (100% pass results)

**Next:** Create relaxed guardrail version (low prompt-attack sensitivity) and test guarded vs unguarded behavior.

Day 15 complete – strong reliability foundation established! 🚀
