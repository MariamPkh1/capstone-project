import time

import pytest

from src.scoring import (InvalidScore, competitive_score, evaluate, load_data,
                         main, zone)

CS = {"program_id": "P", "subjects": {"maths": 3, "english": 1}}


def test_competitive_score_weighted_sum():  # AC1
    assert competitive_score({"maths": 180, "english": 160}, CS) == 700


def test_missing_subject_gives_none():  # AC4
    assert competitive_score({"maths": 180}, CS) is None


@pytest.mark.parametrize("score, expected", [
    (599, "reach"),       # just below the lowest cutoff
    (600, "realistic"),   # exactly the lowest cutoff
    (654, "realistic"),   # inside the range plus margin
    (655, "safe"),        # exactly highest cutoff + margin 5
])
def test_zone_boundaries(score, expected):  # AC2
    assert zone(score, [600, 620, 650], margin=5) == expected


def test_no_cutoffs_is_unknown():  # AC6
    assert zone(700, []) == "unknown"


def test_evaluate_one_result_per_program_in_order():  # AC3
    data = load_data()
    out = evaluate({"maths": 180, "georgian": 160, "english": 170,
                    "biology": 150}, data["programs"], data["score_max"])
    assert [r["program_id"] for r in out] == [p["program_id"] for p in data["programs"]]
    assert set(out[0]) == {"program_id", "competitive_score", "zone"}


def test_evaluate_unknown_when_subject_missing():  # AC4
    data = load_data()
    out = evaluate({"maths": 180, "english": 170}, data["programs"])
    law = next(r for r in out if r["program_id"] == "SAMPLE-LAW")
    assert law == {"program_id": "SAMPLE-LAW", "competitive_score": None, "zone": "unknown"}


@pytest.mark.parametrize("bad", ["abc", None, True, -1, 201])
def test_invalid_score_raises(bad):  # AC5
    with pytest.raises(InvalidScore, match="maths"):
        evaluate({"maths": bad}, [CS], score_max=200)


def test_speed_200_programs():  # AC7
    programs = [CS] * 200
    start = time.perf_counter()
    evaluate({"maths": 180, "english": 160}, programs)
    assert time.perf_counter() - start < 0.05


def test_cli_accepts_scientific_notation(capsys):  # found by hand: "1e2" was rejected
    assert main(["maths=1e2", "english=100"]) == 0
    assert "SAMPLE-CS" in capsys.readouterr().out


def test_cli_rejects_out_of_range_scientific_notation(capsys):
    assert main(["maths=1e3"]) == 1
    assert "outside 0-200" in capsys.readouterr().out
  
