# 0001 · SQL retrieval over vector search

**Date:** 2026-10-19  
**Status:** accepted  
**Deciders:** Mariam Pkhaladze, Kvirike Gabunia, Irakli Kimutsadze

## Context

The Abiturienti calculator needs to retrieve admission statistics (cutoffs, coefficients, seats) to ground the LLM explanation and the chat tool calls. Two approaches were considered: a vector search index over program descriptions, and direct SQL queries against a structured PostgreSQL table.

## Decision

We use SQL queries against PostgreSQL for all retrieval. There is no vector index.

## Reasons

- Admission data is **structured and exact** — cutoff scores, coefficients, and seat counts are numbers, not prose. SQL returns the exact rows needed; a vector index would rank by semantic similarity when we need deterministic lookup.
- The highest-risk failure for this product is the LLM stating a wrong number. SQL retrieval guarantees the model receives the exact value from the database. A vector search could surface the wrong program or the wrong year's row.
- The data volume is small: roughly 300 programs across 5 universities. Putting all rows in the prompt would cost 6× more per request. SQL lets us pass only the rows the scoring module selected (under 50 per request), keeping prompt size under 1,000 tokens.
- The team has Django and PostgreSQL experience. A vector index (pgvector, Pinecone, or Chroma) would add operational complexity with no benefit for this use case.

## Trade-offs accepted

If we add free-text features later (program descriptions, university policies), a hybrid approach with a small document index may be worth revisiting. We will note this in `docs/spec.md` under future scope.
