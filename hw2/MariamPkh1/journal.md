# Pattern Journal · MariamPkh1 · Weeks 5 to 7


## Week 5 · Tool Contract · 24 November 2026

**Where I used it:** my HW2 tool `requery_programs`. I wrote the five golden cases first and ran them before the tool existed: all five failed with "no tool named requery_programs". The adversarial case asks for a 2027 cutoff, which is our risk 1, and now the contract refuses it (`Year` accepts only 2024 to 2026) before any lookup runs.
**What I noticed:** the tool-frame PR passed locally with `python -m pytest` but went red in CI, which runs plain `pytest`: the tests could not import `src`. One line in `pytest.ini` (`pythonpath = .`) fixed it. "Green on my laptop" was not the same check as "green in CI".
**Do differently:** run the exact command CI runs before pushing.

## Week 6 · Session State · <date>

**Where I used it:** [one real place: a line in our code, a test, or the lab exercise]
**What I noticed:** [ ]
**Do differently:** [ ]

## Week 7 · Supervised Autonomy Loop · <date>

**Where I saw it:** [one real place from the lab or lecture]
**The one action in Abiturienti that must wait for a person's yes:** [for example: saving or exporting the final priority list the student will paste into the NAEC portal. Reading programs, zoning and checking a list can run in a loop]
**Do differently:** [ ]
