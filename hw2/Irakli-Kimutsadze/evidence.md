# HW2 · Evidence · `check_priority_list` · Irakli-Kimutsadze

## The five golden cases

`evals/tools/Irakli-Kimutsadze.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires.

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| i1 | normal | `codes: [FREEUNI-BA, TSU-LAW]` | ok, `valid: true` | ok, `valid: true` | PASSED |
| i2 | normal | `codes: [TSU-LAW, FREEUNI-BA]` | ok, `valid: false` | ok, `valid: false` | PASSED |
| i3 | normal | `codes: [TSU-LAW, TSU-LAW]` | refused: "appears more than once", "remove the duplicate" | refused with that message | PASSED |
| b1 | bad-input | `codes: []` | refused: "invalid arguments", `codes` | refused by the contract | PASSED |
| a1 | adversarial | `codes: ["TSU-LAW'; DROP TABLE program;--"]` | refused: "invalid arguments", `codes.0` | refused by the pattern on `ProgramCode` | PASSED |

Raw output:

```
$ python -m pytest tests/test_tool_golden.py -v -k Irakli-Kimutsadze
collected 11 items / 6 deselected / 5 selected

tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i1] PASSED   [ 20%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i2] PASSED   [ 40%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i3] PASSED   [ 60%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:b1] PASSED   [ 80%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:a1] PASSED   [100%]

5 passed, 6 deselected in 0.95s
```

Full suite on `main`: `python -m pytest -q` gave `28 passed`.

## The direction of the warning

My HW1 `check_ordering()` warned on reach above safe. That is the wrong way round. NAEC goes down the list and stops at the first program the student qualifies for, so a safe program ranked above a reach program hides the reach one. The spec (Module 1, step 5) says a safe program must not be ranked above a reach program, so reach belongs at the top and safe at the bottom. `check_priority_list` warns on safe above reach. Golden case i1 (reach first, safe last) is valid and i2 (safe first) is flagged. Golden g3 in the team's golden set asks the old question and still needs fixing.

## The red run: proof the gate blocks

Branch `hw2-Irakli-Kimutsadze-red` removed the `pattern` from `ProgramCode` in `src/contracts.py`. Pull request #17, closed without merging.

- Red run: https://github.com/MariamPkh1/capstone-project/actions/runs/45474184466/job/138729874857
- Failing cases: `Irakli-Kimutsadze:a1` (1 failed, 4 passed, 6 deselected). The merge box said the required check failed and merging was blocked.

Raw output of the red run, run locally before pushing:

```
$ python -m pytest tests/test_tool_golden.py -v -k Irakli-Kimutsadze
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i1] PASSED   [ 20%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i2] PASSED   [ 40%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:i3] PASSED   [ 60%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:b1] PASSED   [ 80%]
tests/test_tool_golden.py::test_tool_golden_case[Irakli-Kimutsadze:a1] FAILED   [100%]

E   AssertionError: error was: There is no program TSU-LAW'; DROP TABLE program;--. Call requery_programs to find real codes.
E   assert 'invalid arguments' in "there is no program tsu-law'; drop table program;--. call requery_programs to find real codes."

1 failed, 4 passed, 6 deselected in 0.85s
```

Proof from the terminal that merging was blocked (`gh pr view --json mergeable,mergeStateStatus,statusCheckRollup` on PR #17): `mergeStateStatus: "BLOCKED"`, and the `test` check in workflow `CI` has `conclusion: "FAILURE"`.

**What it taught me.** I removed one line, the `pattern` on `ProgramCode` in `src/contracts.py`, and only case `a1` went red while my other four cases stayed green. The SQL string `TSU-LAW'; DROP TABLE program;--` was no longer refused as invalid arguments. It slipped past the contract and reached the lookup, where only the unknown-code check stopped it with "There is no program ...". The tool still refused it, so a person trying it by hand might have thought nothing was wrong, but my test expected "invalid arguments", so CI caught the missing first defence and the merge box said BLOCKED. For me the lesson is that the contract has to refuse bad input before any code runs, and that a later check catching it is luck, not a replacement. It also showed me that one shared line protects every tool that uses `ProgramCode`, so weakening it in one place affects all of them.

## The green run

Product pull request #16, merged 2026-11-24: https://github.com/MariamPkh1/capstone-project/actions/runs/45468450221/job/138709574744
