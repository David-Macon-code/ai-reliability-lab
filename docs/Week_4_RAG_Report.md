# Week 4 RAG Report – Building Reliable Retrieval-Augmented Generation with Amazon Bedrock  

**David Macon**  
**March 25, 2026**

## Overview

During Week 4 of the 30-Day AI Bootcamp, I focused on implementing Retrieval-Augmented Generation (RAG) using Amazon Bedrock. The goal was to move beyond theoretical prompting into a practical, production-aware RAG pipeline, including embeddings, Knowledge Bases, cost optimization, and reliability testing.

## Key Accomplishments

- **Completed core Bedrock RAG training**  
  Earned certificates in:
  - Building Generative AI Applications Using Amazon Bedrock
  - Building cost-effective RAG applications with Amazon Bedrock Knowledge Bases and Amazon S3 Vectors
  - Prompt Engineering Best Practices for Amazon Bedrock Models
  - Amazon Bedrock Getting Started
  - Developing Generative Artificial Intelligence Solutions
  - Designing Secure Retrieval Augmented Generation (RAG) Applications with AWS
  - Essentials of Prompt Engineering
  - Foundations of Prompt Engineering

- **Built and deployed a working Knowledge Base**  
  - Created `toy_dataset.txt` and uploaded it with `AnyCompany_financial_10K.pdf` to S3 bucket `rag-s3-dmac`
  - Provisioned Bedrock Knowledge Base (`8OOQBDOPXT`) using Titan Embeddings v2
  - Successfully tested retrieval — chunks are consistently returned from both toy data and the 10-K document

- **Validated Titan Embeddings locally**  
  - Tested `amazon.titan-embed-text-v2:0` with batch embedding and cosine similarity
  - Demonstrated semantic closeness between related Fuquay-Varina texts

- **Implemented manual RAG workaround**  
  - Due to on-demand generation restrictions (Converse / InvokeModel blocked for Claude, Llama, Mistral, and Titan models), I built a manual RAG pipeline:
    - Retrieve chunks via Bedrock `retrieve` API
    - Augment prompts with retrieved context
    - Run through local batch script for metrics
  - Documented baseline (no context) vs manual RAG simulation

- **Documented real-world AWS constraints**  
  - Identified on-demand throughput and model access limitations
  - Opened support case #177423331600991 for batch inference authorization
  - Prepared `batch_queries.jsonl` and S3 structure for future batch jobs

## Lessons Learned

- Retrieval from Bedrock Knowledge Bases works reliably once synced.
- On-demand generation can be heavily restricted in new or upgraded accounts — Batch Inference is the practical production path.
- "John Doe" style placeholder names can trigger aggressive safety refusals in Claude models.
- Manual RAG (retrieve + prompt augmentation) is a viable workaround during gating periods.
- Cost optimization and Guardrails must be considered early in RAG design.

## Next Steps

- Submit batch inference job once support case is cleared
- Complete full hallucination comparison (baseline vs RAG)
- Final Week 4 polish and portfolio packaging

This week demonstrated both the power and the practical challenges of building RAG applications on AWS Bedrock. The experience reinforced the importance of reliability engineering, cost awareness, and adaptability when working with real cloud constraints.

**Repository**: <https://github.com/David-Macon-code/ai-reliability-lab>
