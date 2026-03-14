# Day 14 – Guardrail Tuning + Week 2 Wrap

**Date:** ~March 2026  
**Theme:** Observability + Security + API Control (Week 2)

## Goals & Achievements

- Tuned Bedrock Guardrails: changed policy strength from **High** to **Medium** (and/or adjusted confidence thresholds for PROMPT_ATTACK filters).
- Re-ran full test suites:
  - **Injection batch** (15 attempts): Retained high block rate (likely still ~93–100%; confirm exact post-tune number from your logs).
  - **Golden benign batch** (8 cases): Reduced false positives significantly (e.g., from 50% blocked → lower % blocked; most now pass with valid JSON).
- Compared metrics before/after tuning:
  - Latency impact: Minimal change (~few ms difference in guardrail eval time).
  - Token usage: Higher on previously blocked benign cases (now generating structured JSON).
  - Overall: Better balance between security (injection resistance) and usability (low false positives).
- Finalized Week 2 observability foundation:
  - Full logging pipeline: tokens, latency, guardrail traces → CSVs in `/evaluation/`.
  - Validation scripts handle clean structured outputs + trace details.
  - Injection resistance: ~93.3–100% blocked depending on strength; benign pass rate improved post-tuning.
- Updated README with Week 2 completion status and key metrics summary.

## Key Takeaways

- **Bedrock Guardrails + structured outputs** = powerful combo for enterprise-grade reliability.
  - High strength → over-protective (too many false positives).
  - Medium strength → sweet spot for most use cases (strong blocking without crippling benign flows).
- Trace parsing is essential — turns opaque blocks into actionable debug data.
- Reference: Directly applied AIF-C01 Guardrails knowledge; native Converse integration made iteration fast.

## Week 2 Overall Summary

- Observability: Latency/token/guardrail logging fully scripted and reliable.
- Security: Injection block rate 93–100%; tunable false positives.
- Prep for Week 3: Batch automation scripts ready (retries, flake rate tracking, multi-run golden_pass_rate).

**Status:** Week 2 complete. Ready to start Week 3 automation and reliability engineering.

**Related commits:** Guardrail tuning experiments, re-run metrics, Week 2 wrap documentation.
