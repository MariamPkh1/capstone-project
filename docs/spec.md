# Abiturienti · Spec v0

## What it is

A Georgian web app for university applicants after the national exams.
It answers three questions:

1. **I have my scores. Where can I get in, and in what order should I list programs?**
2. **What universities and programs exist in Georgia?**
3. **I don't know what I want. Can you help me figure it out?**

The core insight: most applicants don't lose a place because their score is low.
They lose it because they list programs in the wrong order. The NAEC system goes
down your list and stops at the first program you qualify for — so a less-wanted
program placed above a more-wanted one costs you the better place.

---

## Principles

- **Python computes, the LLM only explains.** Scores, cutoffs, and zones come
  from deterministic code and the database. The LLM never calculates a score or
  states a cutoff from memory.
- **Show ranges, not promises.** Cutoffs vary year to year. Show the 3-year
  range and a confidence level.
- **Never rule anything out.** No "you can't get into X". Only "this is risky,
  put safe options below it".
- **Verify the rules first.** Write down the exact NAEC scoring and admission
  rules in `RULES.md`, with source links, before writing any code.

---

## Users

Georgian high-school graduates (abiturientebi) who have sat the national exams
and are filling the NAEC priority list — typically 17–19 years old, under time
pressure, high stakes. Secondary: parents helping their child choose.

---

## Success criteria

1. A user enters scores and gets a correctly zoned program list in under 3 seconds.
2. The LLM explanation never states a cutoff number that differs from the
   database value.
3. 9 of 10 golden questions pass (correct zone, correct ordering advice).

---

## Modules

| Module | Route | Phase |
|---|---|---|
| Calculator + Chat | `/calculator` | 1–2 (MVP) |
| Catalog | `/explore` | 3 |
| Quiz (optional) | `/quiz` | 4 |

---

### Module 1 · Calculator + Chat (MVP)

The calculator and chat are one continuous flow, not two separate screens.

**Step 1 — Calculator**

1. User enters exam subject scores (real or estimated from a practice test).
2. Backend computes the competitive score per program using subject coefficients
   from the database — pure Python, no LLM.
3. Each program is placed in a zone by comparing the score against the last
   3 years of cutoffs:
   - **Safe** — score clearly above the cutoff range
   - **Realistic** — score inside or just above the range
   - **Reach** — score below the range, but worth listing high
4. The LLM generates a short plain-language explanation of the list — why each
   program is in its zone, what the ordering logic is.
5. Warnings fire when: too few safe options (target 8–10), or a safe program
   is ranked above a reach program.
6. Export as plain text or PDF with NAEC codes, ready to paste into the NAEC portal.

**Step 2 — Chat refines the list**

The chat picks up where the calculator left off. The ranked list is the starting
context. The user can push back in natural language:

- "I can't move to Tbilisi" → deprioritize Tbilisi programs, re-explain
- "I'm not sure I want engineering" → ask why, suggest related fields
- "What if I retake and get 10 more points in maths?" → recompute and compare
- "I only want programs with grants" → filter and re-rank

The LLM never recomputes scores — it calls tools that requery the database with
new constraints, then explains the new result. The user ends with a list they
actually agree with, not just one the algorithm produced.

---

### Module 2 · Catalog

- University list and profile pages (5 universities, all programs)
- Program search with filters: field, city, language, tuition, cutoff range,
  grant availability
- Program page: subjects and coefficients, seats, tuition, 3-year score
  histogram, "check with my scores" button
- Compare 2–3 programs side by side

---

### Module 3 · Quiz (optional)

A lightweight entry point for students who don't have scores yet, or genuinely
don't know what field they want. Not required — students who already know their
scores and preferences skip this entirely.

- 10–15 questions measuring field interests and work environment preferences
  (based on RIASEC)
- Scoring is plain arithmetic, no LLM
- Result feeds into the chat as additional context: "based on your quiz, you
  leaned toward social sciences — here are programs in that direction
  with your score range"
- If a student starts the chat without scores and without a quiz result, the
  chat runs a short 3–5 question conversational mini-quiz instead

---

## Acceptance criteria

- **AC1** `POST /api/calculator/score` with valid scores returns
  `{program_id, competitive_score, zone}` for every program in the database.
- **AC2** Zone assignment matches manual calculation for all programs in the
  2026 golden set (pytest, deterministic).
- **AC3** `GET /api/programs?field=&city=&language=` returns only programs
  matching all supplied filters; missing filter means no constraint.
- **AC4** Every LLM call logs `model, tokens_in, tokens_out, cost_usd,
  latency_ms` to the application log.
- **AC5** p95 latency of `/api/calculator/score` stays under 500 ms
  (no LLM in this path).
- **AC6** Chat tool calls always fetch numbers from the database; the LLM
  response must not contain a cutoff value absent from the tool result.

---

## Context list

What the LLM must see to do its job — nothing else:

| Context | Where it lives | Used by |
|---|---|---|
| Competitive score + zone per program | computed by Django view, passed in prompt | Calculator explainer |
| Program name, university, tuition, seats | database query result | Calculator explainer |
| Cutoff range (min, max, year) | database query result | Calculator explainer |
| Active filters / user constraints | session, passed in system prompt | Chat |
| Tool call results | returned by Django tool executor | Chat |
| Quiz result summary (if taken) | session, passed in system prompt | Chat |

User history, full program descriptions, and university marketing text
are out of scope until after MVP.

---

## Napkin math

**Calculator explainer** (LLM explanation of the priority list):
50 req/day × (500 tokens in × $0.75 + 200 tokens out × $3.75) / 1M × 30 ≈ **$1.40/month**

**Chat**:
100 req/day × (2,000 tokens in × $0.75 + 300 tokens out × $3.75) / 1M × 30 ≈ **$7.90/month**

Model: `google/gemini-2.5-flash` via OpenRouter.
Total well under $15/month at early traffic. Revisit at 1,000 req/day.

---

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite + TypeScript |
| Backend | Django + Django REST Framework |
| Scoring logic | Pure Python module inside Django, no ORM dependency, fully unit-tested |
| Database | PostgreSQL |
| LLM calls | OpenRouter via `openai` SDK, all calls through one `llm.py` module |
| Deploy | Django on Railway, frontend on Vercel |

No graph database. No agent framework. No MCP server.
Chat uses OpenRouter function calling — tool definitions are plain Python dicts,
tool execution is a Django function, no external orchestration library needed.

---

## Data model
university(id, name_ka, name_en, city, accredited)
program(id, university_id, naec_code, name_ka, name_en, degree, language, tuition, seats, grant_seats)
program_subject(program_id, subject, required, coefficient)
admission_stat(program_id, year, min_score, grant_cutoff, applicants)


Every API response carries `data_version` and `rules_version` so the frontend
can show a "data last updated" notice.

---

## Universities in scope (5)

TSU · Ilia State · GTU · Freeuni · KIU

All programs from each university that appear in the NAEC 2024–2026 statistics.
No manual curation — if it is in the NAEC data, it is in the database.

---

## Data sources

- NAEC applicant handbook and admission statistics (PDF, public).
  Parse with `pdfplumber` → CSV → fix by hand → load into PostgreSQL.
  Test the parser on one university table before loading everything.
- University websites for `name_en` and program descriptions (MVP universities only).

---

## Design

- Monochrome plus one red accent
  - Background `#FFFFFF`, section bands `#F5F4F2`, borders `#E5E3E0`
  - Text `#111111` / `#6B6864` / `#9C9895`
  - Accent `#C8322C` (hover `#A8251F`)
- Red appears only on primary buttons, the user's own score, and headline numbers
- Zones shown by fill density, not color: filled circle (safe), half-filled
  (realistic), outline (reach)
- Flat cards, 1px borders, no shadows. Sentence case, tabular numerals.
- No illustrations, mascots, or stock photos — real data is the decoration

---

## Phases

| Phase | Work | Weeks |
|---|---|---|
| 0 | `RULES.md`, NAEC parser, PostgreSQL schema, data quality tests, seed data for 5 universities | 1 |
| 1 | Calculator: scoring module, DRF API, zone logic, golden set tests | 2–3 |
| 2 | Calculator UI + LLM explainer + chat refinement flow | 4–5 |
| 3 | Catalog: university + program pages, search, filters, comparison | 6–7 |
| 4 | Quiz (optional entry point), session profile, connect to chat | 8 |
| 5 | Golden set CI gate, validation against real 2026 cases, deploy, Demo Day prep | 9–10 |

---

## First slice (Lab 2)

**Criteria:** AC1, AC2
**Done when:** `pytest tests/test_calculator.py` passes locally and in CI for
all programs of one university (Freeuni) with 2024 cutoff data.
**Not in this slice:** UI, LLM explainer, chat, catalog, quiz, export.

---

## Risks

- **PDF parsing** — NAEC tables are inconsistently formatted across years.
  Test `pdfplumber` on one table before committing to the full pipeline.
- **Scoring rules change** — Coefficients and rules vary by year and program
  type. Every rule in `RULES.md` needs a source link and a year tag.
- **High stakes for users** — A wrong zone costs a real person a university
  place. The tool shows options and confidence levels, never verdicts.
  The methodology page must be written before launch.
- **LLM hallucinating cutoffs** — AC6 exists for this reason. The system prompt
  must forbid the model from stating numbers not in the tool result.

---

## Out of scope

- Accounts and authentication
- RSVP or application submission
- Real-time NAEC portal integration
- MCP server or agent framework
- Neo4j / graph database
- Streaming chat responses (add in Week 6 if time allows)
- Labour market signals (Geostat, jobs.ge)
- Georgian language UI (planned post-MVP)
- Universities beyond the 5 in scope
- Full 40-question quiz (10–15 is enough)
- Mandatory quiz before calculator (quiz is always optional)
- Push notifications or email
