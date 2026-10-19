# run: pytest hw1/MariamPKH1
# requires: Python 3.11+, pytest — install with: pip install pytest

# Feature Spec · compute_zone · Mariam Pkhaladze · MariamPKH1

## Goal

Given a student's exam subject scores, a program's subject coefficients, and
three years of admission cutoff data, compute the student's competitive score
for that program and classify it into a zone: safe, realistic, or reach.

This is the deterministic core of the Abiturienti calculator. A student enters
their scores once and receives a zone label for every program in the database.
The zone tells them where to place that program on their NAEC priority list.

## Users

The Abiturienti backend — called for each program in the database when a
student submits their scores via POST /api/calculator/score.

## Acceptance criteria

- AC1: competitive_score = sum(score × coefficient) for every subject in
  coefficients. Result is a float rounded to 1 decimal place.
- AC2: zone is "safe" when competitive_score > max(min_score) across all
  years in cutoff_stats.
- AC3: zone is "realistic" when competitive_score is within 10 points below
  min(min_score) across all years (i.e. min_score - 10 <= score <= max_score).
- AC4: zone is "reach" when competitive_score is more than 10 points below
  min(min_score) across all years.
- AC5: raises ValueError with a message naming the subject when a subject
  appears in coefficients but not in subject_scores.
- AC6: works correctly when cutoff_stats contains 1, 2, or 3 years of data.

## Context list

What the function receives — nothing else:

| Input | Type | Example |
|---|---|---|
| subject_scores | dict str→float | {"georgian": 80, "math": 90} |
| coefficients | dict str→float | {"georgian": 1.5, "math": 1.0} |
| cutoff_stats | list of dicts | [{"year": 2024, "min_score": 195}] |

## Out of scope

- Fetching coefficients or cutoffs from a database (the Django view's job)
- Formatting the zone label for display (the formatter's job)
- Handling more than one program at a time
- LLM explanation of the zone (a separate module)
