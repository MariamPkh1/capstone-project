# 0003 · Zone rule: highest cutoff plus 5 for safe, below the lowest for reach

**Date:** 2026-11-24  
**Status:** proposed (accepted when all three of us approve the tool-frame pull request)  
**Deciders:** Mariam Pkhaladze, Kvirike Gabunia, Irakli Kimutsadze

## Context

HW1 gave us two zone rules, and both passed their own tests:

- **Mariam's:** safe if the score is above the highest cutoff of the last three years; reach if it is more than 10 below the lowest; realistic in between.
- **Kvirike's:** safe if the score is at least the highest cutoff plus 5; reach if it is below the lowest; realistic in between.

The calculator, `zone_programs` and `check_priority_list` must all use the same rule, so we pick one and put it in `src/scoring.py`.

## Decision

Kvirike's rule, with `MARGIN = 5`:

| Zone | Rule |
|---|---|
| reach | score < lowest cutoff |
| realistic | lowest cutoff ≤ score < highest cutoff + 5 |
| safe | score ≥ highest cutoff + 5 |
| unknown | no cutoff history, or a required subject is missing |

## Reasons

- **It errs on the careful side.** A student who only just beats last year's highest cutoff is not safe: cutoffs move by more than a few points between years. Mariam's rule would call that student safe, and a wrong "safe" is the error that costs a place.
- **Below the lowest cutoff is a reach, full stop.** Mariam's rule called a score up to 10 below the lowest cutoff realistic, which tells a student a program is likely when no year has ever admitted that score.
- **It already handles the edge cases** we need: no cutoff history and a missing subject both give `unknown`, never a guess.

## Trade-offs accepted

Fewer programs come out as safe, so the "too few safe options" warning fires more often. That is the warning we want students to see. Golden g1 (247.5 against 195 to 215) is safe under both rules, so it does not change.
