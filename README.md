# AI Reliability Lab – 30-Day PromptOps Execution on AWS Bedrock

A Personal lab I created following a structured 30-day plan to build reliable, observable, secure LLM workflows using AWS Bedrock (Converse API, structured outputs, Guardrails, etc.).

![alt text](image.png)

**Current Status (as of March 9, 2026)**  
✅ **Week 1** – Complete: LLM foundations, prompt iteration (V1 → V3), native structured outputs achieved ~100% JSON validity.  
✅ **Week 2** – Complete: Observability (guardrail trace parsing + metrics CSV), security tuning (Guardrail v3 – Medium strength), before/after testing.  

- Golden benign: 100% pass rate (0% false positives after tuning)  
- Injections: 93.3% blocked (14/15), one LOW-conf leak  
- Key win: Balanced usability + strong attack protection  

🚧 **In progress:** Week 3 – Automation + Reliability Engineering  

## Progress Overview

| Week | Theme                              | Status     | Key Outcomes |
|------|------------------------------------|------------|--------------|
| 1    | LLM Foundations + Prompt Testing   | ✅ Complete | 100% structured JSON on V3, golden test set created |
| 2    | Observability + Security + API Control | ✅ Complete | Guardrail tuned (Medium strength), trace parsing + metrics logging, 100% golden pass, 93%+ injection blocks |
| 3    | Automation + Reliability Engineering | In progress | Batch scripts, retry logic, flake tracking, cost notes |
| 4    | RAG + Cost Optimization + Enterprise Framing | Planned | Toy RAG, hallucination compare, model swap, final polish |

### Detailed Reports

- [Week 1 Findings](./docs/week1_findings.md)  
- [Week 2 Completion – Observability + Security](./docs/Week%202%20Completion%20–%20Observability%20+%20Security%20+%20API%20Control.md)  
- [Day 13](./docs/day13.md)  
- [Day 14](./docs/day14.md)  

### Current Setup Highlights

- Model: `global.anthropic.claude-sonnet-4-5-20250929-v1:0` (inference profile)  
- Guardrail: `9g6hem28nedj` v3 (Medium strength on Prompt attacks)  
- Scripts: `scripts/v3_json_test.py` (golden/injection toggles, trace parsing, CSV logging)  
- Outputs: `/evaluation/v3_metrics_log.csv`, `/evaluation/v3_results.json`  

### Next Steps (Week 3 Kickoff)

- Automate multi-run batches  
- Add reliability features (retries, error classification)  
- Track flake rate and token/cost aggregates  

Feel free to explore `/docs/`, `/scripts/`, and `/evaluation/` for details.

Built with AWS Bedrock + Claude 4.5 family – ongoing PromptOps learning lab.
