# HW1 delegation log · Score and zone for one applicant

**Date:** 2026-10-19 · **Tool:** Claude (claude.ai chat) · **Rung on the Autonomy Ladder:** 3 (I wrote my own version first and kept it out of the repo. Claude then wrote the version that is submitted. I compared the two, ran the tests and golden questions myself, and probed it by hand before keeping it.)

**What I delegated.** I gave Claude the course brief (`MILESTONE-1.md`), the lecturer's example folder and our team spec, and asked it to pick one small feature from the capstone's first slice and build it. It wrote the scoring and zone module, the pytest file, the sample data and drafts of `spec.md` and the golden questions. The code in `src/` is Claude's version. I created the files on GitHub, ran everything on my own computer and wrote the final documents from real results. I had written my own version first, and I compared it with Claude's before deciding what to keep.

**What it got wrong.**
1. *Plan.* The first plan put the tests directly in `src/`. The lecturer's example uses `src/tests/` with `__init__.py` files. We caught it by comparing against `Lab-3/examples/hw1-example` before any code was committed.
2. *Code.* The command line parser only turned a value into a number when it contained a dot. So `maths=1e2` (which is 100, a valid score) was rejected with the message "must be a number". All 15 tests passed, because they tested `evaluate()` and never the command line. I found it by trying odd inputs by hand (`maths=1e3`). The fix converts every value with `float()` and turns whole numbers into integers. I added two tests, and now 17 pass.
3. *Assumptions.* Claude chose the 0 to 200 score scale, the plain weighted-sum formula and a margin of 5 for "safe". The data is invented and labelled SAMPLE. I have not yet checked these against the official NAEC rules, and the spec lists this as a risk.
4. *Process.* Claude's first instructions were confusing, and an empty `scoring.py` ended up committed directly to `main` before I had made the branch. I left it, and filled it in on the branch `hw1-KVIRIKE7`, so the pull request carries the content.

**How I verified.** I ran `python -m pytest hw1\KVIRIKE7` myself (15 passed, then 17 after the fix). I ran the three golden questions from the command line and pasted the real outputs into `golden.md`. I probed two extra inputs by hand, which is how bug 2 was found. I also compared Claude's version with the one I had written myself.

**What I would change next time.** State the accepted input formats of the command line in the spec, so there is a criterion and a test for them. Start from a branch instead of `main`.
