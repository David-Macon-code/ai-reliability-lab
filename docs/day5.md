# Day 5 – JSON Day (V3 with Structured Outputs)

**Date:** ~March 2026  
**Theme:** LLM Foundations + Controlled Prompt Testing (Week 1)

## Goals & Achievements

- Created Prompt V3: Leveraged Bedrock's native structured outputs via Converse API (json_schema in outputConfig).
- Used recommended model: anthropic.claude-sonnet-4-5-20250929-v1:0.
- Starter schema adapted (e.g., properties: name, age, city, confidence; required: name, confidence).
- Python snippet implemented in /scripts/v3_json_test.py for testing.
- Tested 5+ examples: 100% valid JSON (guaranteed by token-level decoding).
- Documented rare failures: Minor schema compilation delay on first call (~1–2s).

## Key Findings

- Major upgrade: No need for heavy prompt engineering—API enforces format.
- Success rate: ~100% valid JSON; parsed directly with json.loads().
- Token usage: ~160–190 per response.

## Next

- Day 6: Multi-run testing and golden set.

**Status:** Day 5 complete.  
**Related Artifacts:** /scripts/v3_json_test.py
