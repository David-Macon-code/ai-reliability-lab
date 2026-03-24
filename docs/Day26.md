## Day 26 – Manual RAG vs Baseline (Local Simulation)

| Query                                      | Baseline (no context)      | Expected Answer (from KB chunks / toy_dataset.txt) | Notes |
|--------------------------------------------|----------------------------|----------------------------------------------------|-------|
| Who is Sophia Chen and where does she live?| api_failed (throughput block) | Sophia Chen is 31 and lives in Seattle, Washington. She develops AI applications and is passionate about sustainable technology. | RAG would provide correct context |
| What is Fuquay-Varina known for?           | api_failed                 | Fuquay-Varina is a growing town in Wake County, North Carolina, near Raleigh. It is known for its family-friendly community and parks. | RAG would pull local knowledge |
| What is Dr. Raj Patel's profession?        | api_failed                 | Dr. Raj Patel is a university professor specializing in computer science. | RAG would return accurate profession |
| Where is Maria Gonzalez from and what does she do? | api_failed            | Maria Gonzalez, 28, is from Miami, Florida. She is a marketing specialist. | RAG would give correct origin and job |
| Summarize the AnyCompany 10-K financial highlights | api_failed            | The financial statements include notes... AnyCompany Financial has a strong reputation... | RAG pulls directly from PDF |

**Observation**: Baseline fails completely due to on-demand restriction. Manual RAG would succeed if generation were available, as relevant chunks are being retrieved.
