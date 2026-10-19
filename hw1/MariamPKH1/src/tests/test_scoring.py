import pytest
from src.scoring import compute_zone

CUTOFFS_3Y = [
    {"year": 2024, "min_score": 195},
    {"year": 2023, "min_score": 200},
    {"year": 2022, "min_score": 192},
]

COEFFICIENTS = {"georgian": 1.5, "math": 1.0, "history": 0.5}


# ── AC1 + AC2: safe zone ───────────────────────────────────────────────────

def test_safe_zone():
    # 80*1.5 + 90*1.0 + 75*0.5 = 120 + 90 + 37.5 = 247.5
    # max cutoff = 200 → 247.5 > 200 → safe
    result = compute_zone(
        subject_scores={"georgian": 80, "math": 90, "history": 75},
        coefficients=COEFFICIENTS,
        cutoff_stats=CUTOFFS_3Y,
    )
    assert result["competitive_score"] == 247.5
    assert result["zone"] == "safe"


# ── AC1 + AC4: reach zone ─────────────────────────────────────────────────

def test_reach_zone():
    # 55*1.5 + 60*1.0 + 50*0.5 = 82.5 + 60 + 25 = 167.5
    # min cutoff = 192 → 167.5 < 192 - 10 = 182 → reach
    result = compute_zone(
        subject_scores={"georgian": 55, "math": 60, "history": 50},
        coefficients=COEFFICIENTS,
        cutoff_stats=CUTOFFS_3Y,
    )
    assert result["competitive_score"] == 167.5
    assert result["zone"] == "reach"


# ── AC1 + AC3: realistic zone ─────────────────────────────────────────────

def test_realistic_zone():
    # 60*1.5 + 70*1.0 + 60*0.5 = 90 + 70 + 30 = 190.0
    # min cutoff = 192, max cutoff = 200
    # 190 <= 200 (not safe) and 190 >= 182 (192 - 10) → realistic
    result = compute_zone(
        subject_scores={"georgian": 60, "math": 70, "history": 60},
        coefficients=COEFFICIENTS,
        cutoff_stats=CUTOFFS_3Y,
    )
    assert result["competitive_score"] == 190.0
    assert result["zone"] == "realistic"


# ── AC5: missing subject raises ValueError ────────────────────────────────

def test_missing_subject_raises_error():
    with pytest.raises(ValueError, match="history"):
        compute_zone(
            subject_scores={"georgian": 80, "math": 90},
            coefficients=COEFFICIENTS,
            cutoff_stats=[{"year": 2024, "min_score": 195}],
        )


# ── AC6: single year of cutoff data ──────────────────────────────────────

def test_single_year_cutoff():
    # 80*1.5 + 90*1.0 = 120 + 90 = 210.0
    # only cutoff: 195 → 210 > 195 → safe
    result = compute_zone(
        subject_scores={"georgian": 80, "math": 90},
        coefficients={"georgian": 1.5, "math": 1.0},
        cutoff_stats=[{"year": 2024, "min_score": 195}],
    )
    assert result["competitive_score"] == 210.0
    assert result["zone"] == "safe"


# ── AC2: boundary — score exactly equal to max cutoff is NOT safe ─────────

def test_score_equal_to_max_cutoff_is_realistic():
    # score exactly 200 (= max cutoff) → not strictly greater → realistic
    # need: score = 200, min=192 → 200 >= 182 and 200 <= 200 → realistic
    result = compute_zone(
        subject_scores={"georgian": 80, "math": 80},
        coefficients={"georgian": 1.5, "math": 0.625},
        cutoff_stats=CUTOFFS_3Y,
    )
    # 80*1.5 + 80*0.625 = 120 + 50 = 170 — adjust
    # simpler: one subject, coefficient 1.0, score exactly 200
    result = compute_zone(
        subject_scores={"georgian": 200},
        coefficients={"georgian": 1.0},
        cutoff_stats=CUTOFFS_3Y,
    )
    assert result["competitive_score"] == 200.0
    assert result["zone"] == "realistic"
