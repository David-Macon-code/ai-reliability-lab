# RAG Basics & Bedrock Notes

## Core Concepts

- **Embeddings**: Convert text to dense vectors capturing semantic meaning
- **RAG (Retrieval-Augmented Generation)**: Retrieve relevant context → augment prompt → reduce hallucinations
- **Bedrock Knowledge Bases**: Fully managed RAG solution
  - Ingest documents (S3) → automatic chunking + embedding (Titan Embeddings)
  - Vector store (managed, uses OpenSearch under hood)
  - Retrieve → augment prompt in Converse API

## Titan Embeddings G1

- Model ID: `amazon.titan-embed-text-v2:0` (or v1 for older)
- Dimensions: 1024 (v2) or 1536 (v1)
- Pricing: ~$0.0001 per 1K tokens (very cheap)
- Use `InvokeModel` API (not Converse) for embeddings

## RAG Flow in Bedrock

1. Ingest docs to Knowledge Base (S3 → chunk → embed → index)
2. Query: Embed user question → retrieve top-k chunks
3. Augment prompt: "Use this context: {retrieved} \nQuestion: {user}"
4. Call Converse with augmented prompt + structured output

## Cost Notes

- Embeddings: cheap (~$0.0001/1K tokens)
- Retrieval: free (managed)
- LLM calls: same as normal Converse (tokens + model rates)
- Savings vs pure LLM: fewer hallucinations → fewer retries/tokens

## Next Steps

- Create toy Knowledge Base (5–10 bios/facts in S3)
- Test Titan Embeddings call
- Compare hallucination rate with/without RAG

Resources:

- Course: Building Generative AI Applications Using Amazon Bedrock
- Docs: <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>

## Local vs SageMaker Studio Experience (Day 22)

- Completed Module 5 locally after SageMaker was slow/buggy (2 restarts needed)
- Same notebooks ran faster/more reliably on laptop Jupyter
- Cost: $0 compute vs. billed Studio instance time
- Takeaway: For Bedrock API prototyping (InvokeModel, Converse, Knowledge Bases), local Jupyter is often better
- Generated sample output: [sales.csv](sales.csv)

## Course Completion – Building Generative AI Applications Using Amazon Bedrock

- Completed: March 22, 2026
- Certificate awarded to David Macon
- Key modules focused on: Knowledge Bases, Titan Embeddings integration, RAG workflows
- Hands-on labs run locally on laptop Jupyter (faster/more reliable than SageMaker Studio)
- Sample output from Module 5: [sales.csv](../sales.csv)

## Titan Embeddings v2 Test Results (Local Jupyter)

- Model: amazon.titan-embed-text-v2:0
- Dimension: 1024
- Sample texts embedded successfully
- Cosine similarity example:
  - Text 1 vs Text 3 (location overlap): ~0.XX (high, as expected)
  - Notebook: [Day22_Titan_Embeddings_Test.ipynb](../Day22_Titan_Embeddings_Test.ipynb)

## Bedrock Access Limitation (March 22, 2026)

- On-demand Converse / InvokeModel blocked for major models (Claude 4.5 family, Llama 3.1, Mistral, Titan variants)
- "Account not authorized" on batch inference — requires support case
- Submitted support request for review (use case: personal AI bootcamp / RAG prototyping)
- Lesson: AWS Bedrock often requires manual approval for new accounts on advanced features


## Day 23: Manual RAG Simulation (Baseline vs Expected)

| Query                              | Baseline Result (no context) | Expected Answer (from toy_dataset.txt) | Improvement Potential |
|------------------------------------|------------------------------|----------------------------------------|-----------------------|
| Who is Sophia Chen...              | api_failed (throughput block) | Sophia Chen is 31 and lives in Seattle, Washington. She develops AI applications. | High (generation would succeed with context) |
| What is Fuquay-Varina known for?   | api_failed                   | Fuquay-Varina is a growing town in Wake County, North Carolina, near Raleigh. It is known for its family-friendly community and parks. | High |
| What is Dr. Raj Patel's profession?| api_failed                   | Dr. Raj Patel is a university professor specializing in computer science. | High |

## Day 24 – Prompt Engineering Best Practices for Amazon Bedrock (Completed March 23–24, 2026)

Certificate awarded.

### Key Bedrock-Specific Takeaways

- Role prompting: Use clear roles (e.g., "You are an expert data extractor") to improve accuracy on Claude models.
- Structured outputs: Leverage `outputConfig` with JSON schema for guaranteed valid JSON (near 100% success on supported models like Sonnet 4.5).
- Temperature & top_p tuning: Start with temperature=0.0 for deterministic extraction; increase slightly (0.2–0.5) for creative tasks.
- Chain-of-thought: Explicitly instruct "Think step by step" for reasoning-heavy queries.
- Few-shot examples: Include 1–3 examples in prompt for better entity extraction consistency.
- Guardrail instructions: Combine with Bedrock Guardrails for injection defense without heavy prompting.
- Model-specific quirks: Claude models respond best to detailed instructions; avoid overly verbose prompts on Haiku.
- Cost-aware prompting: Keep prompts concise to minimize token usage (Haiku excels here).

Notebook reference: [Day24_Prompt_Engineering_Notes.ipynb] (create if needed)

Next: Batch job submission (awaiting support clearance) and hallucination comparison.

## Guardrails on RAG

- Apply Bedrock Guardrails at the Knowledge Base or Converse level to block prompt injection and PII leakage.
- Recommended: Content filters for toxic/harmful content + sensitive data redaction for extraction tasks.
- In our toy setup: Guardrails would prevent refusals on fictional data while still protecting real PII.
- Future improvement: Combine Guardrails with structured outputs for safer RAG pipelines.

