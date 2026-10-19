"""Score and zone for one applicant. No database, no network, no model call."""
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "programs.json"


class InvalidScore(ValueError):
    """A score is not a number or is outside the scale."""


def load_data(path=DATA_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_scores(scores, score_max):
    for subject, value in scores.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidScore(f"{subject}: score must be a number, got {value!r}")
        if not 0 <= value <= score_max:
            raise InvalidScore(f"{subject}: score {value} is outside 0-{score_max}")


def competitive_score(scores, program):
    """Sum of coefficient * score. None if the applicant lacks a required subject."""
    total = 0
    for subject, coefficient in program["subjects"].items():
        if subject not in scores:
            return None
        total += coefficient * scores[subject]
    return total


def zone(score, cutoffs, margin=5):
    """reach / realistic / safe against the cutoff range. unknown if no data."""
    if score is None or not cutoffs:
        return "unknown"
    low, high = min(cutoffs), max(cutoffs)
    if score < low:
        return "reach"
    if score < high + margin:
        return "realistic"
    return "safe"


def evaluate(scores, programs, score_max=200, margin=5):
    validate_scores(scores, score_max)
    results = []
    for program in programs:
        score = competitive_score(scores, program)
        results.append({
            "program_id": program["program_id"],
            "competitive_score": score,
            "zone": zone(score, program.get("cutoffs", []), margin),
        })
    return results


def main(argv):
    scores = {}
    for arg in argv:
        subject, _, value = arg.partition("=")
        try:
            scores[subject] = float(value) if "." in value else int(value)
        except ValueError:
            scores[subject] = value  # let validation reject it
    data = load_data()
    print(data["data_label"])
    try:
        results = evaluate(scores, data["programs"], data["score_max"])
    except InvalidScore as err:
        print(f"Invalid score: {err}")
        return 1
    for r in results:
        print(f'{r["program_id"]:<12} {str(r["competitive_score"]):>6}  {r["zone"]}')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
