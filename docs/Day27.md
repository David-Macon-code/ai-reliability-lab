## Day 27 – Manual RAG Simulation 

**Note**: On-demand generation blocked by AWS (support case #177423331600991 pending). Using manual simulation with retrieved chunks.

| Query                                      | Baseline (no context)      | Expected RAG Answer (from KB chunks) | Improvement Potential |
|--------------------------------------------|----------------------------|--------------------------------------|-----------------------|
| Who is Sophia Chen and where does she live?| Blocked (throughput error) | Sophia Chen is 31 and lives in Seattle, Washington. She develops AI applications. | High – context provides accurate details |
| What is Fuquay-Varina known for?           | Blocked                    | Fuquay-Varina is a growing town in Wake County, North Carolina, near Raleigh. Known for family-friendly community and parks. | High |
| What is Dr. Raj Patel's profession?        | Blocked                    | Dr. Raj Patel is a university professor specializing in computer science. | High |
| Where is Maria Gonzalez from and what does she do? | Blocked               | Maria Gonzalez, 28, is from Miami, Florida. She is a marketing specialist. | High |
| Summarize the AnyCompany 10-K financial highlights | Blocked               | Financial statements include notes on position, operations, and cash flow. Strong reputation, wide range of products. | Medium – pulls directly from PDF |

**Conclusion**: Retrieval is working. Generation is blocked by AWS policy. Manual RAG would significantly reduce hallucinations and improve accuracy if generation were available.
