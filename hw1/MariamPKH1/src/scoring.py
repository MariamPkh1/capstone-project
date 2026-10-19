"""
compute_zone: given exam scores, subject coefficients, and historical cutoff
data, return the competitive score and zone for one program.

Run tests: pytest hw1/MariamPKH1
"""


def compute_zone(
    subject_scores: dict,
    coefficients: dict,
    cutoff_stats: list,
) -> dict:
    """
    Compute a student's competitive score for one program and assign a zone.

    Args:
        subject_scores: subject name -> score, e.g. {"georgian": 80, "math": 90}
        coefficients:   subject name -> coefficient, e.g. {"georgian": 1.5, "math": 1.0}
        cutoff_stats:   list of {"year": int, "min_score": float}, one entry per year

    Returns:
        {"competitive_score": float, "zone": "safe" | "realistic" | "reach"}

    Raises:
        ValueError: if a subject in coefficients is not present in subject_scores
    """
    for subject in coefficients:
        if subject not in subject_scores:
            raise ValueError(f"Missing score for subject: {subject}")

    competitive_score = round(
        sum(subject_scores[subj] * coeff for subj, coeff in coefficients.items()),
        1,
    )

    cutoffs = [entry["min_score"] for entry in cutoff_stats]
    max_cutoff = max(cutoffs)
    min_cutoff = min(cutoffs)

    if competitive_score > max_cutoff:
        zone = "safe"
    elif competitive_score >= min_cutoff - 10:
        zone = "realistic"
    else:
        zone = "reach"

    return {"competitive_score": competitive_score, "zone": zone}
