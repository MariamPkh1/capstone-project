# Pattern Journal · Mariam Pkhaladze · Weeks 1–4

*One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

---

## Week 1 · The Autonomy Ladder

**Where I used it:** In Lab 1 I asked Claude to critique our Abiturienti spec v0. I was at rung 2 — the agent suggested, I decided. It proposed adding a "user history" field to the context list so the LLM could personalise answers. I rejected it because nothing in our core feature (the calculator) uses past sessions — it would have been context noise, not context signal.

**What I noticed:** The agent defaulted to more context, not less. Every suggestion it made added something. The Autonomy Ladder made me ask "which rung am I on right now?" before accepting, which forced me to actually evaluate the suggestion instead of just merging it.

**What I would do differently:** Write the rung into the prompt next time — "you are at rung 2, propose only, do not write files." Without that instruction, Claude moved toward rung 3 on its own and started generating code I had not asked for.

---

## Week 2 · Spec Before Code

**Where I used it:** Writing the acceptance criteria for the Abiturienti calculator. My first draft said "returns the correct zone for a student's scores." That is not testable — a script cannot decide pass or fail without asking me what "correct" means. I rewrote it as AC2: "zone is safe when competitive_score > max(min_score) across all years in cutoff_stats." Now a test can check it without my input.

**What I noticed:** The boundary cases — exactly equal to the cutoff, one year of data versus three — only appeared when I tried to make every criterion decidable by a script. The spec found the bugs before the code existed.

**What I would do differently:** Write the error criteria first. AC5 (missing subject raises ValueError) was the last one I added and almost the most important — it is the one that stops a silent wrong answer from reaching a student.

---

## Week 3 · Uncertainty-Aware UX

**Where I used it:** The zone system in Abiturienti is uncertainty-aware by design. Instead of saying "your cutoff is 195," the calculator uses three years of cutoffs and classifies the student's position as safe, realistic, or reach. The 10-point realistic band exists specifically because we do not know which year's cutoff will apply next year.

**What I noticed:** The LLM explanation layer receives the zone label plus the 3-year range, not a single number. This means the model cannot say "you need 195" — it can only say "you are above the range for the last three years." That constraint came directly from the uncertainty-aware principle: show ranges, not promises.

**What I would do differently:** I would define the realistic boundary (the 10 points) in a named constant or a config value from the start, not hardcoded in the zone logic. If the threshold changes, it should change in one place.

---

## Week 4 · Grounded Generation

**Where I used it:** Running the three golden questions for HW1 made the grounded generation principle concrete. g3 tests that the function raises a ValueError when a subject is missing — meaning the downstream LLM explanation can only ever receive a fully computed score, never a partial one. The LLM is grounded in the output of `compute_zone()`, which is deterministic. It cannot invent a score or a zone from memory because it never sees raw scores at all.

**What I noticed:** The golden set is what makes grounding verifiable. Without g3, I would not have a written record that the guard against bad input actually works. The evidence rule from Lab 4 applies here: a claim that the system is grounded is not the same as a committed test result showing it.

**What I would do differently:** Write the refusal golden question (g5 in the team's evals/golden.yaml) earlier. Knowing what the system must refuse helps define what it must accept, and that boundary is easier to specify before writing any code than after.
