# Golden Questions · compute_zone · Mariam Pkhaladze

## How to run
From the repo root:
  pytest hw1/MariamPKH1 -v

---

## g1 · Safe zone — score clearly above all cutoffs

**Input:**
```
subject_scores = {"georgian": 80, "math": 90, "history": 75}
coefficients   = {"georgian": 1.5, "math": 1.0, "history": 0.5}
cutoff_stats   = [{"year": 2024, "min_score": 195},
                  {"year": 2023, "min_score": 200},
                  {"year": 2022, "min_score": 192}]
```

**Expected:** `{"competitive_score": 247.5, "zone": "safe"}`

Calculation: 80×1.5 + 90×1.0 + 75×0.5 = 120 + 90 + 37.5 = 247.5.
Max cutoff across 3 years = 200. 247.5 > 200 → safe.

**Actual:** `{"competitive_score": 247.5, "zone": "safe"}`

**Result:** PASS

**Command:** `pytest hw1/MariamPKH1/src/tests/test_scoring.py::test_safe_zone -v`

---

## g2 · Reach zone — score well below all cutoffs

**Input:**
```
subject_scores = {"georgian": 55, "math": 60, "history": 50}
coefficients   = {"georgian": 1.5, "math": 1.0, "history": 0.5}
cutoff_stats   = [{"year": 2024, "min_score": 195},
                  {"year": 2023, "min_score": 200},
                  {"year": 2022, "min_score": 192}]
```

**Expected:** `{"competitive_score": 167.5, "zone": "reach"}`

Calculation: 55×1.5 + 60×1.0 + 50×0.5 = 82.5 + 60 + 25 = 167.5.
Min cutoff = 192. 167.5 is 24.5 points below → more than 10 → reach.

**Actual:** `{"competitive_score": 167.5, "zone": "reach"}`

**Result:** PASS

**Command:** `pytest hw1/MariamPKH1/src/tests/test_scoring.py::test_reach_zone -v`

---

## g3 · Missing subject — raises ValueError, not a silent crash

**Input:**
```
subject_scores = {"georgian": 80, "math": 90}   # history is missing
coefficients   = {"georgian": 1.5, "math": 1.0, "history": 0.5}
cutoff_stats   = [{"year": 2024, "min_score": 195}]
```

**Expected:** `ValueError` with a message that names the missing subject ("history")

**Actual:** `ValueError: Missing score for subject: history`

**Result:** PASS

**Command:** `pytest hw1/MariamPKH1/src/tests/test_scoring.py::test_missing_subject_raises_error -v`
