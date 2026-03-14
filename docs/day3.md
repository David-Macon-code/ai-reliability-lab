# Day 3 – Prompt V1 Creation (Baseline)

**Date:** ~March 2026  
**Theme:** LLM Foundations + Controlled Prompt Testing (Week 1)

## Goals & Achievements

- Created baseline Prompt V1 for the core task (e.g., entity extraction from text).
- Saved as `/prompts/v1_baseline.md`.
- Tested in Bedrock console (Converse mode) for initial feel.
  - Model: anthropic.claude-sonnet-4-5-20250929-v1:0
  - Quick tests: 3–5 examples; outputs were coherent but unstructured (no enforced JSON).
  - Noted inconsistencies: Occasional hallucinations or off-topic responses.

## Key Findings

- Baseline prompt provides a starting point but lacks structure—JSON parsing failed ~40% on manual checks.
- Token usage: Avg ~150–200 per response (from console estimates).

## Next

- Day 4: Enhance to V2 with role and structure.

**Status:** Day 3 complete.  
**Related Artifacts:** /prompts/v1_baseline.md
