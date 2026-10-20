from ordering import check_ordering


def P(rank, name, zone):
    return {"rank": rank, "name": name, "zone": zone}


# ---- golden questions ----
def test_reach_above_safe():  # g1
    programs = [
        P(1, "GTU Engineering", "reach"),
        P(2, "TSU Law", "safe"),
        P(3, "Ilia Business", "realistic"),
    ]
    assert check_ordering(programs) == {
        "valid": False,
        "warnings": [{
            "type": "reach_above_safe",
            "message": "GTU Engineering (Reach, rank 1) is listed above TSU Law (Safe, rank 2)",
        }],
    }


def test_correct_order():  # g2
    programs = [
        P(1, "TSU Law", "safe"),
        P(2, "Ilia Business", "realistic"),
        P(3, "GTU Engineering", "reach"),
    ]
    assert check_ordering(programs) == {"valid": True, "warnings": []}


def test_single_item():  # g3
    assert check_ordering([P(1, "TSU Law", "reach")]) == {"valid": True, "warnings": []}


# ---- extra coverage ----
def test_empty_list():
    assert check_ordering([]) == {"valid": True, "warnings": []}


def test_all_pairs_reported():  # AC6
    programs = [
        P(1, "R1", "reach"), P(2, "R2", "reach"),
        P(3, "S1", "safe"), P(4, "S2", "safe"),
    ]
    result = check_ordering(programs)
    assert result["valid"] is False
    assert {w["message"] for w in result["warnings"]} == {
        "R1 (Reach, rank 1) is listed above S1 (Safe, rank 3)",
        "R1 (Reach, rank 1) is listed above S2 (Safe, rank 4)",
        "R2 (Reach, rank 2) is listed above S1 (Safe, rank 3)",
        "R2 (Reach, rank 2) is listed above S2 (Safe, rank 4)",
    }
    assert len(result["warnings"]) == 4


def test_realistic_above_safe_no_warning():  # AC5 (negative test)
    result = check_ordering([P(1, "Ilia Business", "realistic"), P(2, "TSU Law", "safe")])
    assert result == {"valid": True, "warnings": []}


def test_realistic_does_not_mask_reach_violation():
    programs = [P(1, "R", "reach"), P(2, "T", "realistic"), P(3, "S", "safe")]
    assert len(check_ordering(programs)["warnings"]) == 1


def test_input_order_does_not_matter():
    programs = [P(2, "S", "safe"), P(1, "R", "reach")]
    assert check_ordering(programs)["valid"] is False


def test_zone_case_insensitive():
    assert check_ordering([P(1, "R", "Reach"), P(2, "S", "SAFE")])["valid"] is False
