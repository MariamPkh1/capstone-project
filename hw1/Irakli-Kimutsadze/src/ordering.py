def _zone(p):
    return str(p.get("zone", "")).strip().lower()


def check_ordering(programs: list) -> dict:
    """Warn about every (reach, safe) pair where the reach is ranked above the safe.

    Lower rank number = listed higher. Realistic programs never trigger warnings.
    """
    programs = programs or []
    reaches = [p for p in programs if _zone(p) == "reach"]
    safes = [p for p in programs if _zone(p) == "safe"]

    warnings = []
    for r in reaches:
        for s in safes:
            if r["rank"] < s["rank"]:
                warnings.append({
                    "type": "reach_above_safe",
                    "message": (
                        f"{r.get('name', '')} (Reach, rank {r['rank']}) is listed above "
                        f"{s.get('name', '')} (Safe, rank {s['rank']})"
                    ).strip(),
                })

    return {"valid": not warnings, "warnings": warnings}
