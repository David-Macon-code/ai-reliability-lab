# AI Reliability Lab – 30-Day PromptOps Execution on AWS Bedrock

<div align="center">

[![AWS Certified AI Practitioner (AIF-C01)](https://images.credly.com/size/110x110/images/4d4693bb-530e-4bca-9327-de07f3aa2348/image.png)](https://www.credly.com/badges/745adead-31ea-4399-99ff-35ff787966c8/public_url)

**AWS Certified AI Practitioner (AIF-C01)**  
Issued March 11, 2026 | Valid until March 2029  

</div>

A personal lab I created following a structured 30-day plan to build reliable, observable, secure LLM workflows using **AWS Bedrock** (Converse API with native structured outputs, Guardrails, observability, etc.).

Directly applying cert knowledge on responsible AI, content filtering, Bedrock services, and Guardrails to Weeks 1–2 results (e.g., tuned Guardrails blocking 93%+ injections with 0% false positives on golden benign tests).

**Current Status (as of March 11, 2026)**

| Week | Status          | Key Outcomes                                                                 |
|------|-----------------|------------------------------------------------------------------------------|
| 1    | ✅ Complete     | LLM foundations, V1–V3 prompts, native structured outputs → **~100% JSON validity**, golden set created |
| 2    | ✅ Complete     | Observability pipeline, Bedrock Guardrails tuned (Medium) → **93.3% injection blocks**, **100% golden pass** |

- Week 1 – : LLM foundations, prompt iteration (V1 → V3), native structured outputs achieved ~100% JSON validity.
- Week 2 – : Observability (guardrail trace parsing + metrics CSV), security tuning (Guardrail v3 – Medium strength), before/after testing.
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

### Week 1

- **[Week 1 Findings](./docs/week1_findings.md)** — Completed LLM foundations, prompt iterations (V1–V3), and native structured outputs; achieved ~100% JSON validity and created golden test set.

### Week 1 Overview: LLM Foundations + Controlled Prompt Testing

| Category              | Key Activities & Outcomes                                                                 | Result / Metric                  |
|-----------------------|-------------------------------------------------------------------------------------------|----------------------------------|
| Core Concepts         | Studied tokens, context windows, temperature, top_p, hallucinations & failure patterns   | 1-page summary + 5 failure types documented |
| Prompt Iterations     | V1 (baseline), V2 (role + structure), V3 (native json_schema structured outputs)         | V3: ~100% valid JSON             |
| Testing & Evaluation  | Multi-run comparisons, determinism logging, golden test set creation (8–10 cases)        | Golden set saved; V3 perfect determinism at temp=0.0 |
| Major Win             | Leveraged Bedrock Converse API native structured outputs (Claude 4.5 family)             | Eliminated "JSON hardest" problem; 100% schema compliance |

- **[Day 1](./docs/day1_summary.md)** — Studied tokens, context windows, temperature, and top_p; summarized core inference concepts.
- **[Day 2](./docs/day2_failures.md)** — Documented 5 common LLM failure modes, including Bedrock-specific content filtering edge cases.
- **[Day 3](./docs/day3.md)** — Created and console-tested baseline Prompt V1 for the core entity extraction task.
- **[Day 4](./docs/day4.md)** — Developed Prompt V2 with role clarity and structure; compared outputs against V1.
- **[Day 5](./docs/day5.md)** — Implemented Prompt V3 using Bedrock's native structured outputs (json_schema); achieved ~100% valid JSON.
- **[Day 6](./docs/day6.md)** — Ran multi-version tests, logged token usage/determinism, and built the golden test set (8–10 cases).
- **[Day 7](./docs/week1_findings.md)** — Compiled Week 1 Findings Report with JSON success rate table highlighting structured outputs impact.

### Week 2

- **[Week 2 Findings](./docs/week2_completion.md)** — Built observability (latency/token/trace logging), integrated & tuned Bedrock Guardrails (Medium strength); delivered 93.3% injection blocks + 100% golden benign pass.

### Week 2 Overview: Observability + Security + API Control

| Category              | Key Activities & Outcomes                                                                 | Result / Metric                          |
|-----------------------|-------------------------------------------------------------------------------------------|------------------------------------------|
| Observability Setup   | Full boto3 Converse scripting, latency (timeit), token usage logging, CSV output         | Latency ~0.4–0.6s, tokens tracked per run |
| Injection Testing     | Prompt injection attacks (DAN, HACKED, XSS, etc.) on V3 prompt                           | Day 11: 100% defeated (5/5)             |
| Guardrails Integration| Added guardrailConfig (Medium strength), trace parsing, pre/post tuning comparison       | 93.3% injection blocks (14/15), 100% golden benign pass |
| Security Tuning       | Reduced false positives from High → Medium strength; logged trace details (confidence, latency) | From 50% false positives → 0% on golden |
| Overall Reliability   | Combined structured outputs + Guardrails + observability pipeline                        | Production-viable security + usability balance |

- **[Day 8](./docs/day8.md)** — Set up full boto3 Converse API scripting with latency and token observability logging.
- **[Day 9](./docs/day9.md)** — Expanded batch testing; logged precise latency/token metrics to CSV for golden runs.
- **[Day 10](./docs/day10.md)** — Built basic validation script and eval spreadsheet; scored initial golden pass rates.
- **[Day 11](./docs/day11.md)** — Tested 5 prompt injections (DAN, HACKED, etc.); 100% defeated with no leaks, golden 100% pass.
- **[Day 12](./docs/day12.md)** — Integrated Bedrock Guardrails via guardrailConfig; re-tested and tuned for 93.3% injection blocks + 100% golden pass.
- **[Day 13](./docs/day13.md)** — Enhanced validation script to parse guardrail traces; confirmed 100% injection blocks but 50% false positives pre-tuning.
- **[Day 14](./docs/day14.md)** — Finalized guardrail tuning, compared metrics, and wrapped Week 2 with improved observability + security baseline.

### Week 3

- **[Week 3 In Progress]** — Batch scripts, retry logic, flake tracking, cost notes

- **[Day 15](docs/Day15.md)** — Implemented Bedrock Converse batch runner with native structured outputs, metrics tracking, and perfect 40/40 pass rate on golden tests

- **[Day 16](docs/Day16.md)** — Established stable Bedrock Converse baseline with native structured outputs on Claude Sonnet 4.5 inference profile; achieved 100% golden pass rate (160/160 runs unguarded); deployed relaxed guardrail v4 (Low prompt attacks); added toggle flag (--guardrail-version); confirmed 100% pass + zero interventions on benign set with v4 guarded run; captured scaled metrics (avg conf 0.962, avg tokens ~296); Week 3 reliability harness locked in.

- **[Day 17](docs/Day17.md)** — Conducted adversarial injection testing on 7 jailbreak/prompt attack examples × 3 runs each (21 calls per mode); unguarded achieved 33.3% pass rate (7/21); both v4 Low and v3 Medium guarded modes achieved 4.8% pass rate (1/21) with high blocking; confirmed identical strict behavior between v4 and v3 on obvious attacks; leak_detected zero across all; Week 3 security/usability comparison baseline established.

### Current Setup Highlights

- Model: anthropic.claude-sonnet-4-5-20250929-v1:0 (via inference profile)
- Guardrail: 9g6hem28nedj v3 (Medium strength on Prompt attacks)
- Scripts: scripts/v3_json_test.py (golden/injection toggles, trace parsing, CSV logging)
- Outputs: /evaluation/v3_metrics_log.csv , /evaluation/v3_results.json

### Next Steps (Day 17+)

- Expand adversarial set with subtler / edge-case attacks (encoded, multilingual, indirect jailbreaks)  
- Add exact leak scoring (compare parsed output vs expected → flag hallucinations / leaks)  
- Run temperature sweep (0.0 / 0.3 / 0.7) on select benign + adversarial tests → measure flake rate & confidence variance  
- Implement retry logic (3 attempts + exponential backoff on transient errors like ThrottlingException)  
- Compare cost & latency across unguarded / v4 Low / v3 Medium on larger runs  
- Explore semantic validation (cosine similarity on embeddings of parsed vs expected)

Built with AWS Bedrock + Claude 4.5 family – ongoing PromptOps learning lab.

**Final status:** Scalable, reliable eval script with 100% pass rate (40/40 runs), token/latency tracking, and observability. Ready for Week 3 automation and reliability experiments.

**Key files:**

- **[batch_eval_v3.py](scripts/batch_eval_v3.py)** — main batch evaluation script with Converse API, guardrail toggle, adversarial/golden switching, and metrics logging  
- **[batch_metrics.csv](evaluation/no_guardrail_final/batch_metrics.csv)** — 100% pass baseline results (unguarded, Day 16)  
- **[adversarial_test.json](evaluation/adversarial_test.json)** — 7 injection/jailbreak examples used in Day 17 adversarial testing  
- **[batch_metrics.csv examples](evaluation/)** — recent adversarial results:  
-**[Unguarded](evaluation/adversarial_unguarded_test/batch_metrics.csv) (33.3% pass)**
-**[v4 Low](evaluation/adversarial_v4_low/batch_metrics.csv) (4.8% pass)**
-**[v3 Medium](evaluation/adversarial_v3_medium/batch_metrics.csv) (4.8% pass)**

**Next:** Temperature sweep (0.0 / 0.3 / 0.7) for flake variance, retry logic on transient errors, expanded adversarial set, exact-match scoring against expected fields.

**Day 17 complete – 100% benign pass, adversarial shows security/usability trade-offs (33.3% vs 4.8%).**

* AWSBedrock #PromptOps #ResponsibleAI #AIFC01*

* License

[MIT license](#MIT-1-ov-file)
