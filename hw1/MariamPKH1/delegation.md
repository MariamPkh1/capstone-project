# Delegation Log · compute_zone · Mariam Pkhaladze

## What I delegated

Rung 3 (Write code from spec, I review): I gave Claude the full function
signature, the zone logic rules (safe / realistic / reach with the 10-point
boundary), and all six acceptance criteria from spec.md. I asked it to write
`src/scoring.py` and `src/tests/test_scoring.py` without touching any other
files in the repo.

## First attempt — what came back wrong

The first version used `>=` instead of `>` for the safe zone boundary:

```python
if competitive_score >= max_cutoff:
    zone = "safe"
```

This classifies a score exactly equal to the highest cutoff as safe, which is
wrong. A student whose score matches last year's maximum cutoff is on the
boundary — realistic at best, not a clear safe. I caught this by reading AC2
("strictly greater than") against the code line by line. I then added a test
with `score == max_cutoff` (g boundary test) which failed, confirming the bug.

## How I fixed it

I pointed Claude to the exact line and quoted AC2. It corrected the operator
to `>`. I re-ran `pytest hw1/MariamPKH1` — all tests passed including the
boundary case.

## Second issue — floating point in output

The initial version returned `competitive_score` as a raw float. On some
inputs this produced values like `247.50000000000003` due to floating-point
arithmetic. AC1 says the result must be rounded to 1 decimal place. I caught
it by printing the g1 output before writing golden.md. Fixed with
`round(..., 1)` around the sum.

## What I learned

Reading each acceptance criterion against the code line by line — not just
running the tests — catches boundary errors that happy-path tests miss.
The `>=` vs `>` bug would have passed every test I wrote first, because none
of them tested the exact boundary value. Writing the boundary test first,
then checking whether it passed, was the verification step that made the
difference.
