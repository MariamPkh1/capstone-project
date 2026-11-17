# AGENTS.md · Abiturienti

*Instructions for AI coding agents working in this repo. Keep it current; agents read this first.*

## What this project is
Abiturienti is a Georgian web app for university applicants after the national exams. It takes a
student's exam scores, places each program in a zone (safe, realistic, reach) against the last three
years of cutoffs, and helps them order the NAEC priority list. **Python computes, the model only
explains:** scores, cutoffs and zones come from code and data, never from the model. Spec: `docs/spec.md`.

## Stack
- Language: Python 3.12
- Today: plain Python modules in `src/`, tools exposed through an MCP server (`src/mcp_server.py`)
- Planned: Django + DRF backend, React + Vite frontend, PostgreSQL (`docs/spec.md`, Tech stack)
- Model access: OpenRouter · default model: `google/gemini-2.5-flash` (`docs/decisions/0002-openrouter-gemini-flash.md`)
- Data: program and cutoff data in the repo, opened read-only by the code

## How to run
```
pip install -r requirements.txt
python -m src.mcp_server
pytest -q
```

## Conventions
- Secrets come from environment variables. Never write a key into a file.
- Every model call goes through `src/llm.py`, which reads and logs `usage`.
- New features ship with at least one golden question in `/evals`; every tool has a golden file in `evals/tools/`.
- Every change goes through a pull request; nothing is pushed straight to `main`.
- Tool arguments are validated against the contract before the tool runs; a failure goes back to the model as an error and nothing runs.

## You may
- Create and edit files in `src/`, `tests/`, `docs/`, `evals/`
- Propose dependency changes (ask before adding)

## You may not
- Touch `.env`, CI config, or anything in `secrets/`
- Delete or weaken tests to make them pass
- Call paid APIs in loops without a cap
- Let the model state a score, cutoff or zone that did not come from code

## Never
- Never put a user, student or account id in a tool's arguments
- Never add a tool that deletes or sends without asking first
