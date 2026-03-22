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
