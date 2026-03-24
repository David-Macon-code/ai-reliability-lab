# Day 24 – Prompt Engineering Best Practices

## Completed Items

| Item | Status | Details |
|------|--------|---------|
| Prompt Engineering Best Practices for Amazon Bedrock Models | **Completed** | Certificate awarded to David Macon. |
| rag_notes.md updates | **Completed** | Added Bedrock-specific prompting takeaways (role prompting, structured outputs, temperature tuning, chain-of-thought, few-shot examples, guardrail integration). |

## Key Takeaways from Course

- Role prompting significantly improves consistency on Claude models.
- Structured outputs via `outputConfig` with JSON schema achieve near-100% valid JSON on supported models.
- Temperature 0.0 for deterministic extraction tasks; 0.2–0.5 for creative reasoning.
- Chain-of-thought ("Think step by step") helps with complex queries.
- Few-shot examples boost entity extraction accuracy.
- Combine with Bedrock Guardrails for injection defense without heavy prompting.
- Cost-aware prompting: Keep prompts concise — Haiku benefits most from brevity.

Next: Batch inference job (awaiting support case #177423331600991) and hallucination comparison.

Day 24 bagged.
