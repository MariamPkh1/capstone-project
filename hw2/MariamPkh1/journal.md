# Pattern Journal · MariamPkh1 · Weeks 5 to 7


## Week 5 · Tool Contract · 24 November 2026

**Where I used it:** my HW2 tool `requery_programs`. I wrote the five golden cases first and ran them before the tool existed: all five failed with "no tool named requery_programs". The adversarial case asks for a 2027 cutoff, which is our risk 1, and now the contract refuses it (`Year` accepts only 2024 to 2026) before any lookup runs.
**What I noticed:** the tool-frame PR passed locally with `python -m pytest` but went red in CI, which runs plain `pytest`: the tests could not import `src`. One line in `pytest.ini` (`pythonpath = .`) fixed it. "Green on my laptop" was not the same check as "green in CI".
**Do differently:** run the exact command CI runs before pushing.

## Week 6 · Session State · 27 October 2026

**Where I used it:** in Lab 6 our team had to choose one thing Abiturienti should remember across turns. For us the obvious one is the student's exam scores and their current priority list, so the chat can keep refining the same list instead of asking for the scores again every turn. The lab's rule was "no store before a contract": write down what is stored, who can read it, how long it lives, and who can delete it, before writing any code.
**What I noticed:** the "never store" list matters more than what we keep. Scores are fine because the student types them in, but anything the model guessed about the student (for example "she probably wants Tbilisi") must not be saved as a fact. And deleting a row must never depend on the model.
**Do differently:** we have not built the state part in our repo yet. Next time I would write `docs/state-contract.md` first, the same way the golden cases came first in HW2.

## Week 7 · Supervised Autonomy Loop · 17 November 2026

**Where I saw it:** in Lab 7, the loop that takes a goal, runs a few tool calls on its own, stops after a fixed number of steps, and parks anything risky until a person says yes (`NEEDS_YES` and `confirm()`). My HW2 tool fits on the safe side: `requery_programs` only reads, so a loop can call it as many times as it needs without asking anyone.
**The one action in Abiturienti that must wait for a person's yes:** saving or exporting the final priority list that the student will paste into the NAEC portal. Reading programs, zoning them and checking the order can all run inside a loop, but the list the student actually submits must be their own decision.
**Do differently:** decide which tools are "read" and which are "consequential" before building the loop, not after, so the confirmation step is designed in from the start.
