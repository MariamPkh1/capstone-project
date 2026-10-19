# Feature Spec . check_ordering . Irakli Kimutsadze

## Goal
Given a student's priority list with zone labels, detect dangerous orderings
where a Reach program is listed above a Safe program.

## Users
The Abiturienti backend validation layer, called before returning the
priority list so warnings can be shown in the UI.

## Acceptance criteria
- AC1: if any "reach" has rank < any "safe", valid is False and a warning
  is added for that pair.
- AC2: each warning has keys "type" ("reach_above_safe") and "message"
  (naming both programs and their ranks).
- AC3: no reach-above-safe pair -> {"valid": True, "warnings": []}.
- AC4: list with one or zero programs -> valid = True always.
- AC5: realistic above safe does NOT trigger a warning.
- AC6: ALL reach-safe pairs are reported, not just the first.

## Context
Pure Python. No LLM, no database, no API key.
Zones were already assigned by compute_zone(). Does not reassign zones.

## Out of scope
- Suggesting a corrected order (the LLM chat's job)
- Flagging realistic above safe (out of scope for MVP)
- Checking whether the list has enough safe programs
