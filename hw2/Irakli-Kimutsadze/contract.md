 HW2 · Tool Contract · `check_priority_list` · Irakli-Kimutsadze

**Run the tests:** `python -m pytest tests/test_tool_golden.py -v -k Irakli-Kimutsadze`

The student's priority list in order, plus their exam scores, goes in; warnings come out. The tool computes every zone itself through `src/scoring.py` and never trusts a zone from the model, so the contract has no zone field at all.

## Contract card

| Row | Answer |
|---|---|
| Effect | reads |
| Undo | nothing to undo: no state changes |
| Idempotent? | yes: the same arguments give the same result |
| Offered to | everyone, visitors included; it needs no identity |
| Identity from | not needed. The contract has no user, student or account field |
| Touches | `data/programs.json`, read only, through `src/data.py` |
| Must never | accept a zone from the model; state a cutoff that is not in the data; build a query from a raw string; warn the wrong way round (reach above safe) |

**Read tool, not a consequential one.** This tool changes nothing, so a loop may call it without a person's yes.

## Inputs

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `codes` | `list[ProgramCode]` | 1 to 20 codes, each matching `^[A-Z]{2,8}-[A-Z]{2,6}$` | Program codes in the student's order, first choice first |
| `scores` | `Scores` | 1 to 6 subjects from the fixed list; each a number 0 to 100 (strict: `"1e2"`, `true` refused) | The student's exam scores by subject |

The contract inherits `extra="forbid"` from `Contract`, so any extra argument (such as `zone`) is refused.

## Result

| Field | Meaning |
|---|---|
| `valid` | `true` when there are no warnings |
| `rows` | each with `rank`, `code`, `zone` (safe, realistic, reach, unknown) |
| `warnings` | each with `type` (`safe_above_reach`, `no_safe`) and `message` |

Warnings:

- `safe_above_reach`, for every safe program ranked above a reach one: "TSU-LAW (safe, rank 1) is above FREEUNI-BA (reach, rank 2). NAEC would stop at TSU-LAW; move FREEUNI-BA above it."
- `no_safe`, when nothing on the list is safe: "No program on this list is safe. Add at least one safe program at the bottom."

NAEC goes down the list and stops at the first program the student qualifies for, so reach programs belong at the top and safe ones at the bottom. The warning is for safe above reach.

## Expected failures

| Situation | Exact message |
|---|---|
| Duplicate code | "TSU-LAW appears more than once. NAEC lists each program once; remove the duplicate and call again." |
| Unknown code | "There is no program X. Call requery_programs to find real codes." |
| Invalid arguments (empty list, bad pattern, extra field) | refused by the contract before the tool runs: "invalid arguments" plus the field name |

## The five golden cases

File: `evals/tools/Irakli-Kimutsadze.yaml`

| # | Type | Call | Expected | Why |
|---|---|---|---|---|
| i1 | normal | `codes: [FREEUNI-BA, TSU-LAW]`, scores georgian 80, maths 90, history 75, english 10 | ok, `valid: true` | right order, reach first and safe last, gets no warning |
| i2 | normal | `codes: [TSU-LAW, FREEUNI-BA]`, same scores | ok, `valid: false` | a safe program above a reach one is flagged |
| i3 | normal | `codes: [TSU-LAW, TSU-LAW]` | refused: "appears more than once", "remove the duplicate" | NAEC lists each program once |
| b1 | bad-input | `codes: []` | refused: "invalid arguments", `codes` | an empty list never reaches the check |
| a1 | adversarial | `codes: ["TSU-LAW'; DROP TABLE program;--"]` | refused: "invalid arguments", `codes.0` | SQL smuggled into a code; the pattern stops it before any lookup |

With these scores FREEUNI-BA is a reach (230 against 240 to 262) and TSU-LAW is safe (247.5 against 195 to 215).

## Log line

`logs/tools.jsonl` records the time, tool, arguments, ok or error, and latency. There is no caller field: the tool never receives one.

## Links to my code on `main`

- Tool: [`src/tools/check_priority_list.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/tools/check_priority_list.py)
- Shared contract types: [`src/contracts.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/contracts.py)
- MCP door: [`src/mcp_server.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/mcp_server.py)
- Golden cases: [`evals/tools/Irakli-Kimutsadze.yaml`](https://github.com/MariamPkh1/capstone-project/blob/main/evals/tools/Irakli-Kimutsadze.yaml)
- Product pull request: #16
