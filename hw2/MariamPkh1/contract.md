# HW2 · Tool contract · `requery_programs` · MariamPkh1

Run the five cases: `python -m pytest tests/test_tool_golden.py -v -k MariamPkh1`

Code on `main`: [`src/tools/requery_programs.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/tools/requery_programs.py) (contract `RequeryPrograms`, the function, the `TOOLS` entry, `register()` for MCP) · shared types in [`src/contracts.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/contracts.py) · gates in [`src/act.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/act.py) · MCP server [`src/mcp_server.py`](https://github.com/MariamPkh1/capstone-project/blob/main/src/mcp_server.py) · cases [`evals/tools/MariamPkh1.yaml`](https://github.com/MariamPkh1/capstone-project/blob/main/evals/tools/MariamPkh1.yaml). Product pull request: [#9](https://github.com/MariamPkh1/capstone-project/pull/9).

**In one sentence, for the model:** Programs that match the student's filters, with each program's published cutoffs. Reads only; it never computes a zone.

| | |
|---|---|
| **Effect** | reads |
| **Undo** | nothing to undo: no state changes |
| **Idempotent?** | yes: the same arguments always give the same result |
| **Offered to** | everyone, visitors included. It needs no identity, so offering it widely costs nothing |
| **Identity from** | not needed. The contract has no user, student or account field |
| **Touches** | `data/programs.json`, read only, through `src/data.py` (the only module that opens it, and it has no write function) |
| **Must never** | state a cutoff that is not in the data, or compute a zone. Zones belong to `src/scoring.py` |

**Read or consequential (Lab 7).** It is a read tool: it changes nothing, so a loop may call it as often as it likes without asking a person first.

**Inputs.** Every string is a fixed set of values, the one number has bounds, unknown fields are refused (`extra="forbid"` on `Contract`).

| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| `city` | string or null | `Tbilisi`, `Kutaisi` | City the program is taught in |
| `field` | string or null | `law`, `computer-science`, `psychology`, `biology`, `engineering`, `business` | Field of study |
| `language` | string or null | `ka`, `en` | Teaching language |
| `university` | string or null | `TSU`, `ILIA`, `GTU`, `FREEUNI`, `KIU` | University |
| `grants_only` | boolean | default false | Only programs with grant seats |
| `max_tuition` | integer or null | 0 to 20000 | Highest yearly tuition in GEL |
| `year` | integer or null | `2024`, `2025`, `2026` only | Admission year with published cutoffs |

**Result.** `data_label` (says the numbers are sample data), `count`, and `programs`: each with `code`, `name`, `university`, `city`, `language`, `tuition`, `grant_seats`, and `cutoffs` (a list of `year` and `min_score`, only for the requested year if one is given). No internal ids.

**Expected failures.**

| When | Message the model reads |
|---|---|
| no program matches | No program matches these filters. Drop one filter, for example max_tuition or city, and call again. |
| a value outside the contract (e.g. city Batumi) | invalid arguments: city: Input should be 'Tbilisi' or 'Kutaisi' |
| a year without data (e.g. 2027) | invalid arguments: year: Input should be 2024, 2025 or 2026 |

**Tests and golden cases.** All five in `evals/tools/MariamPkh1.yaml`, run in CI by `tests/test_tool_golden.py`.

| Case | Expect | Where |
|---|---|---|
| m1 · `city: Kutaisi` | runs, `count: 2` | `evals/tools/MariamPkh1.yaml` |
| m2 · `field: law, grants_only: true, year: 2026` | runs, `count: 1` | same |
| m3 · `city: Kutaisi, field: law` | refused: "No program matches… drop one filter" | same |
| b1 · invalid arguments: `city: Batumi` | refused before the tool runs | same |
| a1 · adversarial: `year: 2027` | refused before any lookup | same |
| not offered to this caller | n/a: a read tool, offered to everyone | `tests/test_act.py` tests the gate itself |
| identity in the arguments | refused by `extra="forbid"` | `tests/test_act.py::test_unknown_field_is_refused` |
| both doors describe the same arguments | identical schemas | `tests/test_mcp.py` |

**Log line.** `logs/tools.jsonl` records the time, the tool, the arguments, ok or the error, and the latency. There is no caller field: the tool never receives one, so no personal data reaches the log.
