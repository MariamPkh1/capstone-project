# HW2 · Tool Contract · `zone_programs` · KVIRIKE7

Test command: `python -m pytest tests/test_tool_golden.py -v -k KVIRIKE7`

| Row | Answer |
|---|---|
| Name | zone_programs |
| What it does | Competitive score and zone (safe, realistic, reach, unknown) per program, from the student's exam scores. Python decides the zone; the model only explains it. |
| Effect | reads |
| Undo | nothing to undo: no state changes |
| Idempotent? | yes: the same arguments give the same result |
| Offered to | everyone, visitors included; it needs no identity |
| Identity from | not needed. The contract has no user, student or account field |
| Touches | data/programs.json, read only, through src/data.py |
| Must never | accept a zone from the model; state a cutoff that is not in the data; guess a zone when a subject or the cutoff history is missing |

**Read tool, not a consequential one.** It changes nothing, so an agent loop may call it without a person's yes.

## Links (on main)
- Tool: https://github.com/MariamPkh1/capstone-project/blob/main/src/tools/zone_programs.py
- Contract base: https://github.com/MariamPkh1/capstone-project/blob/main/src/contracts.py
- MCP door: https://github.com/MariamPkh1/capstone-project/blob/main/src/mcp_server.py
- Golden cases: https://github.com/MariamPkh1/capstone-project/blob/main/evals/tools/KVIRIKE7.yaml

## Inputs
| Argument | Type | Constraint | Description the model reads |
|---|---|---|---|
| scores | Scores | 1 to 6 subjects from the fixed list; each a number 0 to 100 (strict: "1e2", true refused) | The student's exam scores by subject |
| codes | list[ProgramCode] or None | 1 to 20 codes, each matching ^[A-Z]{2,8}-[A-Z]{2,6}$; None means every program | Program codes to zone |

Input formats (from the spec): 90 and 87.5 accepted; "90", "1e2", true refused; -5 and 101 refused; {} refused; unknown subject refused; a subject the program needs missing → runs, that program's zone is unknown.

## Result
`data_label`, `programs`: each with `code`, `name`, `competitive_score` (or null), `zone` (safe, realistic, reach, unknown), `cutoff_min`, `cutoff_max`.

## Expected failures
- Unknown code → `There is no program TSU-ART. Call requery_programs to find real codes.`
- Invalid arguments (wrong type, extra field, bad pattern) → refused by the contract before the tool runs: "invalid arguments" plus the field name.

## The five cases
| id | type | why |
|---|---|---|
| k1 | normal | golden g1, the core output; 247.5 against 195 to 215 is safe |
| k2 | normal | a program with no cutoff history is unknown, never guessed |
| k3 | normal | an unknown program code; the message sends the model to requery_programs |
| b1 | bad-input | a score sent as text ("1e2") is refused, not parsed |
| a1 | adversarial | the model sets an extra `zone` field; it is refused, Python decides zones |

## Log line
`logs/tools.jsonl` records the time, tool, arguments, ok or error, and latency. There is no caller field: the tool never receives one.