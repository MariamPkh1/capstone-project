"""The zone rule from decision 0003, at its boundaries."""
from src.scoring import competitive_score, zone

CUTOFFS = [195, 205, 215]


def test_golden_g1_score_and_zone():
    score = competitive_score({"georgian": 80, "maths": 90, "history": 75},
                              {"georgian": 1.5, "maths": 1.0, "history": 0.5})
    assert score == 247.5
    assert zone(score, CUTOFFS) == "safe"


def test_missing_subject_has_no_score():
    assert competitive_score({"georgian": 80}, {"georgian": 1.5, "maths": 1.0}) is None


def test_boundaries():
    assert zone(194.9, CUTOFFS) == "reach"
    assert zone(195, CUTOFFS) == "realistic"
    assert zone(219.9, CUTOFFS) == "realistic"
    assert zone(220, CUTOFFS) == "safe"


def test_no_history_or_no_score_is_unknown():
    assert zone(250, []) == "unknown"
    assert zone(None, CUTOFFS) == "unknown"
