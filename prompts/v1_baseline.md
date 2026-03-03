# Prompt V1 – Baseline (Free-form Extraction)

**Task**  
Extract structured person information from a bio text: full name, age, city, and job title / main profession.

**Prompt text** (exact text used):'''Extract structured person information from the following bio text: name, age, city, and job title.

Full name
Age
City they live in
Job title or main profession

Bio: Albert Smith is a 34-year-old software engineer living in Springfield. He works at a cloud consulting firm and enjoys gaming on the weekends.'''

**Test settings**  
- Model: Anthropic Claude Sonnet 4.5 (Bedrock Playground)  
- Temperature: 0.0 (for maximum determinism)  
- Top P: Default / blank  
- Date: March 03, 2026  
- Runs: 3 identical prompts (chat cleared between each)

**Outputs** (all 3 runs identical):'''Based on the bio text, here is the extracted information:
Full name: Albert Smith
Age: 34
City they live in: Springfield
Job title or main profession: Software engineer'''
**Observations & Analysis**  
- **Determinism**: 100% identical across all 3 runs — no variance at temperature=0.0  
- **Format**: Free-form bullet list with a polite introductory sentence ("Based on the bio text, here is the extracted information:")  
- **Accuracy**: Extraction was correct and complete (no hallucinations, no missing fields)  
- **Strengths**: Clear, readable, and reliable even in baseline form  
- **Weaknesses**:  
  - Includes unnecessary preamble text → not suitable for automated parsing (e.g., JSON downstream)  
  - No strict structure enforced (bullets could vary in wording/order if prompt changes slightly)  
  - Not machine-readable for scripts (Week 2 observability / validation scripts)  

**Next in the Plan**  
- Day 4: Prompt V2 — Add role clarity ("You are a precise data extractor") + explicit output structure (remove preamble, enforce consistent format)  
- Day 5: Prompt V3 — Enforce strict JSON output using Bedrock Converse API structured outputs (native schema enforcement for 100% reliability)

**Why this baseline matters**  
This free-form version serves as our control: reliable but not production-ready. We'll measure improvements in consistency, parseability, and token efficiency across versions.
