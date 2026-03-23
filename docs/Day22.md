# Day 22 – RAG Foundations & Bedrock Reality Check (March 22, 2026)

## Status Summary

| Item                                      | Status      | Details / Output |
|-------------------------------------------|-------------|------------------|
| AWS Bedrock RAG course                    | **Completed** | Certificate awarded. Labs run locally (faster, no cost, more reliable than SageMaker Studio). |
| Titan Embeddings v2 test                  | **Completed** | 1024 dims, batch + cosine similarity. Notebook: [Day22_Titan_Embeddings_Test.ipynb](../Day22_Titan_Embeddings_Test.ipynb) |
| Toy dataset & S3 upload                   | **Completed** | `toy_dataset.txt` + sample 10-K PDF in `rag-s3-dmac` bucket. |
| Knowledge Base creation & sync            | **Completed** | ID: `8OOQBDOPXT`. Retrieval confirmed (chunks returned). |
| Retrieval test                            | **Working** | Chunks returned from KB on queries. |
| Generation / answer production            | **Blocked** | All models (Claude Haiku/Sonnet 4.5, Llama 3.1, Mistral, Titan variants) refuse or are invalid for on-demand Converse/InvokeModel. Safety refusal on extraction queries; throughput restrictions on others. |
| Workaround plan                           | **Set for Day 23** | Pivot to Batch Inference (async, cheaper, bypasses on-demand gates). |

## Key Lessons Learned

- Local Jupyter + boto3 is superior for Bedrock prototyping (zero compute cost, no restarts, full control).
- Bedrock Knowledge Bases are easy to set up and sync from S3.
- Retrieval works reliably.
- Generation is gated: on-demand Converse/InvokeModel heavily restricted (throughput / legacy / safety refusals).
- "John Doe" and similar extraction patterns trigger aggressive Claude refusals — even with explicit "do not refuse" prompts and fictional data.
- Next: Batch Inference to get generated answers and complete the RAG loop.

## Repo Highlights

- Notebooks: Titan test, Sonnet vs Haiku visuals
- Files: `toy_dataset.txt` in S3
- KB: Synced & ready
- README: Model comparison + cost charts

Day 22 bagged — real RAG pipeline proven, AWS gating documented.
