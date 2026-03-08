# ai-reliability-lab

**30-Day AI Reliability Lab**  
Applying NOC engineering discipline to LLM reliability using **AWS Bedrock**.

This is a hands-on, self-directed project where I treat large language models like production infrastructure: rigorous testing, observability, iteration, and failure-mode analysis.

Focus: Prompt engineering, golden evaluations, injection resistance, structured outputs, and observability — all built on the **Bedrock Converse API** with Claude 4.5 family models.

## Why This Project?

As a former NOC engineer pivoting into AI, I'm bringing systems reliability thinking to generative AI. The goal is to build production-grade habits early: no flaky playground experiments — only testable, observable, repeatable results.

## Tech Stack & Key Features

- Python + boto3 (Converse API)
- AWS Bedrock: Claude Sonnet 4.5 (native json_schema constrained decoding)
- Temperature 0.0 for determinism
- Golden test sets + adversarial injection testing
- Token/latency/CSV metrics logging
- Toggleable test modes (golden vs injection)

## Progress Highlights (as of March 2026)

| Day/Week | Status   | Key Outcome                                                                                                                         |
| -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Week 1   | Complete | 100% JSON success with native structured outputs (no parsing hacks)                                                                 |
| Day 12   | Complete | Guardrails integrated (100% prompt attack blocks); see evaluation/week2_guardrails.md for results/comparison                        |

See full results in `/evaluation/` (v3_results.json, metrics CSVs).

## Skills Demonstrated

- Native structured JSON enforcement via Bedrock Converse `outputConfig.textFormat` (token-level constrained decoding → ~100% compliance)
- Prompt injection resistance testing & mitigation
- boto3 Converse API automation with usage/token/latency logging
- Golden set evaluation, pass rate tracking, and test toggling
- Observability mindset applied to LLMs (like NOC monitoring)

## How to Run / Explore

1. Ensure AWS credentials with `bedrock:Converse` permission and model access enabled.
2. Install deps: `pip install boto3`
3. Run the main script: `python scripts/v3_json_test.py`
   - Toggle `IS_INJECTION_TEST` in the script for golden vs adversarial mode
4. Check outputs: `/evaluation/v3_results.json` and `/evaluation/v3_metrics_log.csv`

## Next Steps (Planned)

- Day 13: Integrate Bedrock Guardrails (`guardrailConfig`) + re-test injections
- Model comparison (Sonnet vs Haiku vs others)
- Toy RAG with Titan Embeddings + Bedrock Knowledge Bases

MIT Licensed — feel free to fork or reference.

Questions/comments? Reach out on X: [@1DavidInAtl](https://x.com/1DavidInAtl)
