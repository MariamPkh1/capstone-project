"""Competitive score and zone. Python computes these; the model only explains them.

The zone rule is decision 0003 (docs/decisions/0003-zone-rule.md):
  reach      the score is below the lowest cutoff of the last three years
  realistic  at or above the lowest, but less than the highest plus MARGIN
  safe       at least the highest cutoff plus MARGIN
  unknown    the program has no cutoff history, or the applicant lacks a required subject
"""
from __future__ import annotations

MARGIN = 5


def competitive_score(scores: dict[str, float], subjects: dict[str, float]) -> float | None:
    """Sum of coefficient x score, rounded to one decimal. None if a required subject is missing."""
    if any(subject not in scores for subject in subjects):
        return None
    return round(sum(coefficient * scores[subject] for subject, coefficient in subjects.items()), 1)


def zone(score: float | None, cutoffs: list[float], margin: float = MARGIN) -> str:
    if score is None or not cutoffs:
        return "unknown"
    if score < min(cutoffs):
        return "reach"
    if score < max(cutoffs) + margin:
        return "realistic"
    return "safe"
