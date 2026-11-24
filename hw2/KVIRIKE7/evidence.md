# HW2 · Evidence · `zone_programs` · KVIRIKE7

## The five golden cases
`evals/tools/KVIRIKE7.yaml`, run by `tests/test_tool_golden.py` in the CI job `test`, which the branch rule on `main` requires.

| # | Type | Call | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| k1 | normal | scores georgian 80, maths 90, history 75; codes [TSU-LAW] | ok, TSU-LAW 247.5, safe | <copy from output> | yes |
| k2 | normal | scores georgian 70, biology 80, english 60; codes [ILIA-BIO] | ok, 290.0, unknown | <copy> | yes |
| k3 | normal | codes [TSU-ART] | refused: no program TSU-ART, requery_programs | <copy> | yes |
| b1 | bad-input | scores maths "1e2" | refused: invalid arguments, scores.maths | <copy> | yes |
| a1 | adversarial | extra field zone: safe | refused: invalid arguments, zone | <copy> | yes |

Raw output:
(paste the output of: python -m pytest tests/test_tool_golden.py -v -k KVIRIKE7)

## The red run: proof the gate blocks
Branch `hw2-KVIRIKE7-red` changed `extra="forbid"` to `extra="ignore"` in `src/contracts.py`. Pull request #<number>, closed without merging.
- Red run: <link to the failed Actions run>
- Failing cases: a1<, plus the other tests that failed>. The merge box said the required check failed.
- Screenshot: <attach or link the merge-box screenshot>

**What it taught me.** <one honest paragraph in your own words. Include that other owners' tests failed too, so one line in Contract protects every tool.>

## The green run
Product pull request #18, merged 2026-11-25: <link to the green Actions run>.