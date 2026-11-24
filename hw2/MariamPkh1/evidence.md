# HW2 · Evidence · `requery_programs` · MariamPkh1

## The five golden cases

`evals/tools/MariamPkh1.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires. "Actual" is copied from running each case through `call_tool()` on 24 November 2026.

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| m1 | normal | `requery_programs(city="Kutaisi")` | runs, 2 programs | KIU-CS and KIU-MGMT, each with cutoffs for 2024, 2025, 2026 | pass |
| m2 | normal | `requery_programs(field="law", grants_only=true, year=2026)` | runs, 1 program | TSU-LAW, with the 2026 cutoff only | pass |
| m3 | normal | `requery_programs(city="Kutaisi", field="law")` | refused, says to drop a filter | "No program matches these filters. Drop one filter, for example max_tuition or city, and call again." | pass |
| b1 | bad-input | `requery_programs(city="Batumi")` | refused before the tool runs | "invalid arguments: city: Input should be 'Tbilisi' or 'Kutaisi'" | pass |
| a1 | adversarial | `requery_programs(field="law", year=2027)` | refused before any lookup | "invalid arguments: year: Input should be 2024, 2025 or 2026" | pass |

**Boundary first.** I added the five cases before the tool existed and ran them. All five failed, because the tool was not in the registry yet:

```
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m1] FAILED   [ 20%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m2] FAILED   [ 40%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m3] FAILED   [ 60%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:b1] FAILED   [ 80%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:a1] FAILED   [100%]
```

After the tool, `python -m pytest tests/test_tool_golden.py -v -k MariamPkh1`:

```
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m1] PASSED   [ 20%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m2] PASSED   [ 40%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:m3] PASSED   [ 60%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:b1] PASSED   [ 80%]
tests/test_tool_golden.py::test_tool_golden_case[MariamPkh1:a1] PASSED   [100%]
======================= 5 passed, 1 deselected in 1.03s =======================
```

**The MCP door.** Through an in-memory MCP client, the server lists `requery_programs` with `read_only_hint: true`. `city: Kutaisi` returns 2 programs. `year: 2027` is refused by the SDK before the function runs. That message is longer than ours: it includes an internal class name and a pydantic link, which is the SDK's own text, not something our code adds.

## The red run: proof the gate blocks

Branch `hw2-MariamPkh1-red` changed one line in `src/tools/requery_programs.py`: `year: Year | None = None` became `year: int | None = None`. Pull request [#10](https://github.com/MariamPkh1/capstone-project/pull/10), closed without merging.

- Red run: https://github.com/MariamPkh1/capstone-project/actions/runs/45453699577/job/138657327105?pr=10
- Result: `2 failed, 19 passed`. The failures were `test_tool_golden_case[MariamPkh1:a1]` and `test_both_doors_describe_the_arguments_identically[requery_programs]`.
- The merge box said "All checks have failed" and "Merging is blocked", with the required `test` check marked failed.

**What it taught me.**  Without the `Year` type, the 2027 request was not refused. The tool answered `count: 1` with TSU-LAW and an empty `cutoffs` list. Nothing crashed and nothing looked wrong, which is exactly the danger: a model reading "TSU Law, 2027, count 1" could easily say the program is open in 2027 and guess a cutoff, which is our risk 1. So the data lookup does not protect us; only the contract does. The second failure surprised me: the MCP door still used `Year`, so the two doors disagreed, and the both-doors test caught a weakening I had made in only one place.

## The green run

Product pull request [#9](https://github.com/MariamPkh1/capstone-project/pull/9), merged 24 November 2026: https://github.com/MariamPkh1/capstone-project/actions/runs/45450232427/job/138644986803?pr=9 (`21 passed`, including all five cases).
