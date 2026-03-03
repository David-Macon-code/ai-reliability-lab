# Day 1 Summary: Tokens, Context Windows, Temperature, Top_p

## Tokens
- The smallest unit LLMs process (roughly 4 characters ≈ 1 token in English; ~0.75 words).  
- Bedrock responses include usage stats: inputTokenCount, outputTokenCount, totalTokenCount.  
- Critical for tracking cost, avoiding truncation, and observability in production.

## Context Window
- Maximum tokens allowed in one request (prompt + output combined).  
- Claude Sonnet 4.5 on Bedrock: Up to ~200K tokens — allows long contexts/docs/RAG without forgetting.  
- Like RAM on a server: Bigger window = better for complex tasks, but higher token usage.

## Temperature & Top_p Experiments (Bedrock Playground – Claude Sonnet 4.5)
- **Temp 0.0** (top_p default): Outputs showed minor variations across 3 identical runs (different robot names, actions, endings, but consistent story structure).  
  - Not 100% deterministic due to backend/GPU factors in Claude models—no seed parameter available.  
- **Temp 1.0**: Stories varied wildly (different plots, details, tones).  
- **Top_p 0.1 vs 0.95**: Low top_p = very focused/similar outputs; high = more diverse/creativity.  
- Note: For Claude 4.5+, set only temperature **or** top_p (not both) to avoid issues.

## Takeaways for Reliability Lab
- Low temperature (0.0–0.2) + Bedrock's native structured outputs will minimize variance for JSON tasks.  
- Logging token usage and output drift will be key in Week 1 batch tests.  
- This reinforces treating LLMs as probabilistic infrastructure, not deterministic code.
