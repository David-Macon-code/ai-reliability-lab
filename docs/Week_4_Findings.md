# Week 4 Findings – RAG Foundations & Real-World AWS Constraints  

## Executive Summary

Week 4 focused on implementing Retrieval-Augmented Generation (RAG) using Amazon Bedrock. I successfully built a working Knowledge Base, validated retrieval, and prepared batch infrastructure. However, on-demand generation (Converse / InvokeModel) was heavily restricted, forcing a manual RAG simulation and pivot toward Batch Inference.

## Key Technical Achievements

- **Knowledge Base Implementation**  
  - Created and synced Bedrock Knowledge Base (`8OOQBDOPXT`) using Titan Embeddings v2  
  - Uploaded `toy_dataset.txt` + `AnyCompany_financial_10K.pdf` to S3 (`rag-s3-dmac`)  
  - Retrieval confirmed: relevant chunks returned for multiple queries

- **Embeddings & Retrieval Testing**  
  - Validated `amazon.titan-embed-text-v2:0` locally with batch embedding and cosine similarity  
  - Demonstrated semantic closeness on related Fuquay-Varina and person-specific queries

- **Manual RAG Workaround**  
  - Built baseline (no context) vs manual RAG (with pasted KB chunks) comparison using existing batch script  
  - Documented clear potential for improved accuracy and reduced hallucinations when generation is available

- **Batch Infrastructure**  
  - Created `batch_queries.jsonl` and uploaded to S3, ready for batch inference job submission

## Major Challenge Encountered

On-demand generation via Converse and InvokeModel was blocked for all tested models (Claude Haiku/Sonnet 4.5, Llama 3.1, Mistral, Titan variants) with "throughput not supported" or "invalid model identifier" errors.  
Support case #177423331600991 opened and acknowledged — awaiting authorization for batch access.

## Lessons Learned

- Retrieval from Bedrock Knowledge Bases is reliable once properly synced.
- "John Doe" style placeholder names can trigger aggressive safety refusals in Claude models.
- On-demand Converse is increasingly restricted in 2026; Batch Inference is the practical production path for high-volume or gated workloads.
- Manual RAG (retrieve + prompt augmentation) is a viable short-term workaround.
- Cost optimization and Guardrails must be designed in from the start for enterprise RAG.

## Skills Demonstrated

- End-to-end RAG pipeline construction with Bedrock Knowledge Bases
- Local embeddings testing and cosine similarity analysis
- Adaptation to cloud service limitations with manual workarounds
- Comprehensive documentation of both successes and production blockers

**Next Steps**: Submit batch inference job once support clears, complete full hallucination comparison, and finalize portfolio packaging.

Week 4 successfully completed despite real-world AWS constraints.
