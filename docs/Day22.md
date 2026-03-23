# Day 22 – RAG Basics & Bedrock Foundations (March 22, 2026)

## Status Overview

| Item                                      | Status      | Details / Output |
|-------------------------------------------|-------------|------------------|
| Building Generative AI Applications Using Amazon Bedrock course | **Completed** | Certificate awarded to David Macon. Labs run locally (faster, no cost, more reliable than SageMaker Studio). |
| Haiku modelId testing                     | **Completed** | Full guardrail sweep (none/low/medium, 3 runs each on adversarial). Charts & README updated. |
| Jupyter notebook setup                    | **Completed** | Local JupyterLab validated as superior for Bedrock prototyping. |
| Titan Embeddings v2 test                  | **Completed** | Single & batch embedding successful (1024 dims). Cosine similarity tested. Notebook: [Day22_Titan_Embeddings_Test.ipynb](../Day22_Titan_Embeddings_Test.ipynb) |
| rag_notes.md                              | **In progress** | Started with Titan variants, RAG flow, cost notes, local vs Studio experience. |
| Toy dataset creation & S3 upload          | **Completed** | `toy_dataset.txt` created + uploaded to `rag-s3-dmac` (along with sample 10-K PDF). |
| Knowledge Base creation & sync            | **Completed** | KB ID: `8OOQBDOPXT`. Retrieval confirmed (chunks returned). |
| Generation / answer production            | **Blocked** | On-demand Converse & InvokeModel restricted for all tested models (Claude 3.5/4.5, Llama 3.1, Mistral, Titan variants). Pivoting to Batch Inference on Day 23. |

## Key Takeaways

- Local Jupyter + boto3 is often superior to SageMaker Studio for Bedrock RAG prototyping (zero compute cost, faster, no restarts).
- Titan Embeddings v2 works reliably locally (1024 dimensions, cosine similarity shows semantic closeness).
- Bedrock Knowledge Bases are easy to set up and sync from S3.
- On-demand generation via Converse/InvokeModel heavily restricted in this account (throughput / legacy gating).
- Next: Use Batch Inference to bypass restrictions and get generated answers.

## Repo Updates

- Notebooks: Titan test, comparison visuals
- Files: `toy_dataset.txt` uploaded to S3
- KB: Created & synced
- README: Sonnet vs Haiku charts + cost bars added
