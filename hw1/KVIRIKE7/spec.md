# HW1 spec · Score and zone for one applicant

*Abiturienti · individual feature · one page.*
*Run (from the repo root): `python -m pip install -r hw1/KVIRIKE7/src/requirements.txt && python -m pytest hw1/KVIRIKE7`*
*Try it: `cd hw1/KVIRIKE7 && python -m src.scoring maths=160 english=170`*
*Data in `src/data/programs.json` is SAMPLE data, invented for testing. It is not real NAEC data.*

## Goal

Given an applicant's exam scores, return for every program in the data file its competitive score and a zone (safe, realistic, reach or unknown), using the program's subject coefficients and its past cutoffs. No database, no network, no model call.

## Users

Georgian school graduates filling the NAEC priority list. The Abiturienti calculator will call this module later; for HW1 it is used from the command line and from tests.

## Acceptance criteria

1. `competitive_score(scores, program)` returns the sum of coefficient × score over the program's subjects. Maths ×3 and English ×1 with maths 180 and English 160 returns 700.
2. `zone(score, cutoffs, margin=5)` returns `reach` if score < min(cutoffs), `realistic` if min(cutoffs) <= score < max(cutoffs) + margin, and `safe` if score >= max(cutoffs) + margin. The boundaries are tested.
3. `evaluate(scores, programs)` returns one `{program_id, competitive_score, zone}` per program, in the same order as the input.
4. If the applicant has no score for a subject a program needs, that program returns `competitive_score: None` and zone `unknown`, with no exception.
5. A score that is not a number (including `True`) or is outside 0 to `score_max` (200 in the data file) raises `InvalidScore` whose message names the subject. The command line prints `Invalid score: ...` and exits with code 1.
6. A program with an empty cutoff list returns zone `unknown`.
7. 200 programs evaluate in under 50 ms, with no network and no model call.

## Context the agent needs

- `src/data/programs.json`: `score_max` and, per program, `program_id`, `subjects` (subject to coefficient) and `cutoffs` (past minimum scores).
- `AGENTS.md` at the repo root: conventions and test command.
- This file.

## Out of scope

Chat, LLM explanation, catalog, quiz, PDF export, database, list-ordering warnings, grant cutoffs, real NAEC data.

## Napkin math

No model call in this feature, so the cost is zero per request.

## Risks

- A wrong zone could mislead a real applicant. The module only labels zones; it never says "you cannot get in".
- The weighted-sum formula, the 0 to 200 scale and the margin of 5 are assumptions taken from the team spec and chosen as defaults. They must be checked against the official NAEC rules before any real use.
- The sample cutoffs are invented. If they were mistaken for real data, users could be misled, so the data file labels itself as sample and the command line prints that label on every run.
