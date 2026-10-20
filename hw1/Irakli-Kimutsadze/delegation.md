# Delegation Log . check_ordering . Irakli Kimutsadze

## What I delegated
Rung 3 (write code from spec, I review): I gave Claude the feature
description, rules and the prompt from the assignment, and asked for
ordering.py plus pytest tests.

## Thing 1 the agent got wrong - spec mismatch
My first prompt did not include spec.md. Claude's first version used a
"category" key instead of "zone", and its warning message did not name the
programs, so it broke AC2. I only found out when I shared the spec and
golden screenshots and the mismatch became visible. Claude then rewrote the
function to use "zone", name both programs in the message, and use the test
names from golden.md.

## Thing 2 the agent got wrong - workflow advice
Claude told me to commit files straight to main. The submission checklist
says hw1/ must be merged through a pull request, not pushed directly. Claude
had not seen the checklist, and I had not shown it until later. I caught it
when I read the checklist against what I had done. I reverted my direct
commits, restored my files onto a new branch (hw1-irakli-v2) and opened a
pull request instead.

## Verification
I ran pytest in a Codespace after restoring the files on the new branch.
All 9 tests passed.

## What I learned
Give the AI the full spec and the checklist up front, not after the first
attempt. Tests for what the function must NOT do (realistic above safe must
not warn) matter as much as tests for what it should do. I also shouldn't
trust workflow advice from the AI without checking it against the
assignment's own rules.