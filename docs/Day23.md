# Day 23 – Batch Prep + Cost-Effective RAG Course (March 23, 2026)

## Completed Items

| Item                                      | Status      | Details / Output |
|-------------------------------------------|-------------|------------------|
| Batch input JSONL creation & S3 upload    | **Completed** | `batch_queries.jsonl` (3 queries) created and uploaded to `rag-s3-dmac/batch-input/` |
| Building cost-effective RAG applications with Amazon Bedrock Knowledge Bases and Amazon S3 Vectors | **Completed** | Certificate awarded to David Macon. Notes added to rag_notes.md (S3 Vectors for up to 90% storage cost reduction while maintaining performance). |
| Retrieval test (chunks from KB)           | **Working** | Successful retrieve calls – chunks returned from `toy_dataset.txt` and `AnyCompany_financial_10K.pdf` for safe queries. |

## Key Takeaways (from completed items)

- Batch input ready for inference job submission (awaiting support case clearance #177423331600991).
- Cost-effective RAG course completed – key insight: S3 Vectors dramatically lower storage costs for Knowledge Bases.
- Retrieval from KB is reliable and returning relevant content (no refusals in retrieve phase).

## Next (deferred / pending)

- Submit batch job once support clears
- Hallucination comparison (baseline vs RAG)
- Remaining Skill Builder courses (Prompt Engineering, Getting Started, RAG Lab)

