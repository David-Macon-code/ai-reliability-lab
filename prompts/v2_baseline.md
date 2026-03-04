# Prompt V2 – Role Clarity + Structured Output

**Task**  
Same as V1: Extract person info (name, age, city, job title) from bio.

**Prompt text** (V2):
```You are a precise, no-nonsense data extractor. Your only job is to pull the requested fields from the bio text.

Extract the following information exactly as specified:
- Full name
- Age
- City
- Job title

Rules:
- Respond ONLY with the extracted fields in this exact format.
- Do not add any introductory text, explanations, conclusions, or extra words.
- Do not use markdown, bullets, or code blocks.
- Do not add periods at the end of lines unless part of the data.
- If a field is missing, write "Not found".

Bio: Albert Smith is a 34-year-old software engineer living in Springfield. He works at a cloud consulting firm and enjoys gaming on the weekends.

Output format must be:
Full name: [value]
Age: [value]
City: [value]
Job title: [value]```

**Improvements over V1**  
- Added role: "precise, no-nonsense data extractor"  
- Explicit rules to forbid preamble/extras  
- Defined exact output format (key: value lines)

**Test settings**  
- Model: Anthropic Claude Sonnet 4.5  
- Temperature: 0.0  
- Top P: Default  
- Runs: 3

**Outputs**:
```Full name: Albert Smith
Age: 34
City: Springfield
Job title: software engineer```

```Full name: Albert Smith
Age: 34
City: Springfield
Job title: software engineer```

```Full name: Albert Smith
Age: 34
City: Springfield
Job title: software engineer```

**Comparison to V1**  
- Preamble: Removed / still present?  
- Format consistency:  
- Variance:  
- Other improvements:  

**Next**  
Day 5: V3 – Strict JSON enforcement via prompt and Bedrock structured outputs.
