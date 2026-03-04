## V3 Native Structured Outputs – Batch Results on Golden Test Set

- Cases tested: 8
- Valid JSON: 8/8 (100%)
- Exact match to expected: 7/8 (87.5%)
- Average tokens: ~344
- Average latency: ~2.2 seconds

  ```json
  [
  {
    "id": 1,
    "bio_snippet": "Albert Smith is a 34-year-old software engineer li...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Albert Smith",
      "age": 34,
      "city": "Springfield",
      "job_title": "software engineer"
    },
    "tokens": 348,
    "latency_sec": 1.9
  },
  {
    "id": 2,
    "bio_snippet": "Maria Gonzalez, 28, from Miami, is a marketing spe...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Maria Gonzalez",
      "age": 28,
      "city": "Miami",
      "job_title": "marketing specialist"
    },
    "tokens": 348,
    "latency_sec": 2.21
  },
  {
    "id": 3,
    "bio_snippet": "Dr. Raj Patel is 45 years old and resides in Bosto...",
    "valid_json": true,
    "matches_expected": false,
    "output": {
      "full_name": "Dr. Raj Patel",
      "age": 45,
      "city": "Boston",
      "job_title": "cardiologist"
    },
    "tokens": 350,
    "latency_sec": 2.08
  },
  {
    "id": 4,
    "bio_snippet": "Sophia Chen works as a data analyst in Seattle. Ag...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Sophia Chen",
      "age": 31,
      "city": "Seattle",
      "job_title": "data analyst"
    },
    "tokens": 340,
    "latency_sec": 1.94
  },
  {
    "id": 5,
    "bio_snippet": "James O'Connor, a 52-year-old retired teacher from...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "James O'Connor",
      "age": 52,
      "city": "Chicago",
      "job_title": "retired teacher"
    },
    "tokens": 343,
    "latency_sec": 2.59
  },
  {
    "id": 6,
    "bio_snippet": "Elena Rossi is a graphic designer based in Austin....",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Elena Rossi",
      "age": 29,
      "city": "Austin",
      "job_title": "graphic designer"
    },
    "tokens": 344,
    "latency_sec": 1.74
  },
  {
    "id": 7,
    "bio_snippet": "Ahmed Khan, 38, lives in Denver and runs his own I...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Ahmed Khan",
      "age": 38,
      "city": "Denver",
      "job_title": "IT consultant"
    },
    "tokens": 334,
    "latency_sec": 2.95
  },
  {
    "id": 8,
    "bio_snippet": "Lisa Thompson is 40 years old. She is a project ma...",
    "valid_json": true,
    "matches_expected": true,
    "output": {
      "full_name": "Lisa Thompson",
      "age": 40,
      "city": "Atlanta",
      "job_title": "project manager"
    },
    "tokens": 341,
    "latency_sec": 1.87
  }
]
**Key Observation**  
Bedrock's `outputConfig.textFormat` with json_schema delivered perfect schema compliance across all varied bios (titles, reordered info, extra details). The single mismatch was semantic (inclusion of "Dr." in full_name), not structural — highlighting the value of clear expected definitions in golden sets.

**Tokens & Latency** (consistent and low-cost for production use).

**Next**: Run similar tests on V1 (baseline prompt) and V2 (structured prompt) via playground or script → compare validity % and reliability.
