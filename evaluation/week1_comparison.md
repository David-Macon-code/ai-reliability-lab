# Week 1 Comparison: V3 Native Structured Outputs

## V3 Batch Results on Golden Test Set

- **Cases tested**: 8  
- **Valid JSON**: 8/8 (100%)  
- **Exact match to expected**: 7/8 (87.5%)  
- **Average tokens**: 343.5  
- **Average latency**: ~2.17 seconds  

The single mismatch (ID 3) was semantic — the model included "Dr." in full_name, while the expected output did not. All outputs were perfectly valid JSON thanks to Bedrock's `outputConfig.textFormat` with json_schema.

### Summary Table

| ID | Bio Snippet                          | Valid JSON | Matches Expected | Tokens | Latency (s) |
|----|--------------------------------------|------------|------------------|--------|-------------|
| 1  | Albert Smith is a 34-year-old...     | Yes        | Yes              | 348    | 1.9         |
| 2  | Maria Gonzalez, 28, from Miami...    | Yes        | Yes              | 348    | 2.21        |
| 3  | Dr. Raj Patel is 45 years old...     | Yes        | No               | 350    | 2.08        |
| 4  | Sophia Chen works as a data analyst... | Yes      | Yes              | 340    | 1.94        |
| 5  | James O'Connor, a 52-year-old...     | Yes        | Yes              | 343    | 2.59        |
| 6  | Elena Rossi is a graphic designer... | Yes        | Yes              | 344    | 1.74        |
| 7  | Ahmed Khan, 38, lives in Denver...   | Yes        | Yes              | 334    | 2.95        |
| 8  | Lisa Thompson is 40 years old...     | Yes        | Yes              | 341    | 1.87        |

**Key Observation**  
Bedrock's native structured outputs delivered perfect schema compliance across varied bios (titles, reordered fields, extra details). The mismatch highlights the importance of precise golden set definitions (e.g., decide if honorifics belong in full_name).

**Tokens & Latency**  
Consistent and low-cost — ideal for production entity extraction.

**Next Steps**  
Run similar batch/manual tests on V1 (baseline prompt) and V2 (structured prompt) to compare validity %, parsing issues, and reliability. Expect lower JSON validity on V1/V2 without enforcement.

Full raw results: [v3_results.json](v3_results.json)
