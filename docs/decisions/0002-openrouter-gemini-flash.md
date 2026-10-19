# 0002 · OpenRouter gateway with Gemini 2.5 Flash

**Date:** 2026-10-19  
**Status:** accepted  
**Deciders:** Mariam Pkhaladze, Kvirike Gabunia, Irakli Kimutsadze

## Context

The Abiturienti LLM explainer and chat need a model that is fast, cheap, and capable of following a strict system prompt (no inventing numbers). We needed to choose both the model and the access method.

## Decision

We call `google/gemini-2.5-flash` via the OpenRouter API, using the `openai` SDK with a custom base URL. All calls go through a single `llm.py` module.

## Reasons

**Model choice — Gemini 2.5 Flash:**
- Input cost: $0.15 / 1M tokens; output: $0.60 / 1M tokens. At our projected load (150 req/day) this is under $10/month including chat.
- Flash-tier latency is acceptable for the explanation step (user is reading a ranked list while it generates).
- Context window (1M tokens) is far beyond what we need; no risk of hitting limits.

**Gateway choice — OpenRouter:**
- One API key, one SDK, access to multiple model families. If Gemini is unavailable or raises prices, we switch the `model` string in `llm.py` without touching any other code.
- The `openai` SDK is already familiar to the team and handles retries and timeouts.
- OpenRouter provides per-call cost metadata, which `llm.py` logs to `logs/usage.jsonl` for the token budget section of the Design Review.

**Single `llm.py` module:**
- All model calls go through one file. Logging, error handling, and the model ID are in one place. No code outside `llm.py` constructs a model call directly.

## Trade-offs accepted

OpenRouter adds a small per-call margin (~10%) over calling Google directly. We accept this for the provider-switching flexibility and the unified logging. We will revisit at 1,000 req/day.
