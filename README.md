# AI Reliability Lab – 30-Day PromptOps Execution on AWS Bedrock

<div align="center">

![AWS Certified AI Practitioner Badge](https://images.credly.com/size/340x340/images/4d4693bb-530e-4bca-9327-de07f3aa2348/image.png)

**AWS Certified AI Practitioner (AIF-C01)**  
Issued March 11, 2026 | Valid until March 2029  
[View on Credly](https://www.credly.com/badges/745adead-31ea-4399-99ff-35ff787966c8/public_url)


**Milestone Achieved!** 🎉  
Passed **AWS Certified AI Practitioner (AIF-C01)** on March 11, 2026 — directly fueling better Guardrails, responsible AI practices, and Bedrock workflows in this lab.

</div>

A personal lab I created following a structured 30-day plan to build reliable, observable, secure LLM workflows using **AWS Bedrock** (Converse API with native structured outputs, Guardrails, observability, etc.).

Directly applying cert knowledge on responsible AI, content filtering, Bedrock services, and Guardrails to Weeks 1–2 results (e.g., tuned Guardrails blocking 93%+ injections with 0% false positives on golden benign tests).

**Current Status (as of March 11, 2026)**

- Week 1 – Complete: LLM foundations, prompt iteration (V1 → V3), native structured outputs achieved ~100% JSON validity.
- Week 2 – Complete: Observability (guardrail trace parsing + metrics CSV), security tuning (Guardrail v3 – Medium strength), before/after testing.
  - Golden benign: 100% pass rate (0% false positives after tuning)
  - Injections: 93.3% blocked (14/15), one LOW-conf leak
  - Key win: Balanced usability + strong attack protection (enhanced by AIF-C01 insights on Guardrails & responsible AI)

In progress: Week 3 – Automation + Reliability Engineering

## Progress Overview

| Week | Theme | Status | Key Outcomes |
| --- | --- | --- | --- |
| 1 | LLM Foundations + Prompt Testing | Complete | 100% structured JSON on V3, golden test set created |
| 2 | Observability + Security + API Control | Complete | Guardrail tuned (Medium strength), trace parsing + metrics logging, 100% golden pass, 93%+ injection blocks |
| 3 | Automation + Reliability Engineering | In progress | Batch scripts, retry logic, flake tracking, cost notes |
| 4 | RAG + Cost Optimization + Enterprise Framing | Planned | Toy RAG, hallucination compare, model swap, final polish |

### Detailed Reports

- [Week 1 Findings](/David-Macon-code/ai-reliability-lab/blob/main/docs/week1_findings.md)
- [Week 2 Completion – Observability + Security + API Control](/David-Macon-code/ai-reliability-lab/blob/main/docs/Week%202%20Completion%20%E2%80%93%20Observability%20+%20Security%20+%20API%20Control.md)
- [Day 13](/David-Macon-code/ai-reliability-lab/blob/main/docs/day13.md)
- [Day 14](/David-Macon-code/ai-reliability-lab/blob/main/docs/day14.md)

### Current Setup Highlights

- Model: anthropic.claude-sonnet-4-5-20250929-v1:0 (via inference profile)
- Guardrail: 9g6hem28nedj v3 (Medium strength on Prompt attacks)
- Scripts: scripts/v3_json_test.py (golden/injection toggles, trace parsing, CSV logging)
- Outputs: /evaluation/v3_metrics_log.csv , /evaluation/v3_results.json

### Next Steps (Week 3 Kickoff)

- Automate multi-run batches
- Add reliability features (retries with backoff, error classification)
- Track flake rate, token/cost aggregates per run category

Feel free to explore `/docs/` , `/scripts/` , and `/evaluation/` for details.

Built with AWS Bedrock + Claude 4.5 family – ongoing PromptOps learning lab.

# AWSBedrock #PromptOps #ResponsibleAI #AIFC01

## About

30-Day PromptOps / AI Reliability Lab – Applying NOC discipline to LLMs with AWS Bedrock

### Resources

[Readme](#readme-ov-file)

### License

[MIT license](#MIT-1-ov-file)
