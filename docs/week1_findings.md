# Week 1 Findings Report – LLM Foundations + Bedrock Structured Outputs

**Background**  
Former NOC Engineer leveraging AWS Certified AI Practitioner (AIF-C01) knowledge to build reliable LLM pipelines with AWS Bedrock Converse API.

**Key Activities (Days 1–6)**
- Studied tokens, context windows, inference params, hallucinations.
- Iterated prompts V1 → V2 → V3.
- Achieved prompt-based JSON enforcement in playground.
- Implemented **native structured outputs** via `outputConfig.textFormat` + json_schema (GA Feb 2026 for Claude 4.5 family).
- Handled global inference profile routing for on-demand access.
- Created 8-case golden test set with varied bios.
- Ran batch evaluation on V3 → logged validity, matches, tokens, latency.

**Major Wins**
- Native Bedrock structured outputs delivered **100% valid JSON** across 8 diverse cases (vs. prompt-only methods' typical 90–98%).
- Token usage ~344 avg, latency ~2.17 s avg — efficient for entity extraction.
- Demonstrated enterprise-grade reliability: constrained decoding eliminates parsing failures.

**Lessons Learned**
- Semantic differences (e.g., "Dr. Raj Patel" vs "Raj Patel") require explicit rules in prompts / golden sets.
- Inference profile requirement (`global.`) is critical for latest Claude models — common gotcha.

**Next (Week 2 Preview)**
- Add observability: latency CSV, token tracking over runs.
- Test prompt injection + Bedrock Guardrails.
- Compare V1 & V2 validity % on same golden set.

**Skills Demonstrated**
- boto3 Converse API + native json_schema for guaranteed structured output.
- Golden test set creation & batch evaluation scripting.
- GitHub repo organization + markdown documentation.

Commit: [link to this week's commits]
