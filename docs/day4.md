# Day 4 – Prompt V2 Creation (Role + Structure)

**Date:** ~March 2026  
**Theme:** LLM Foundations + Controlled Prompt Testing (Week 1)

## Goals & Achievements

- Created Prompt V2: Added role clarity (e.g., "You are an entity extractor...") and structured instructions (e.g., "Output in JSON format with keys: name, age, city").
- Compared outputs vs. V1 on 3–5 test cases.
- Logged differences in `/evaluation/week1_comparison.md`.
  - V1: Unstructured text, harder to parse.
  - V2: More consistent, but still occasional invalid JSON (e.g., missing keys).

## Key Findings

- Improvements: Coherence up ~20%; JSON validity ~70% (manual parsing).
- Issues: Model sometimes ignored format instructions at higher temperature.

## Next

- Day 5: Upgrade to V3 with native structured outputs.

**Status:** Day 4 complete.  
**Related Artifacts:** /prompts/v2_structured.md, /evaluation/week1_comparison.md
