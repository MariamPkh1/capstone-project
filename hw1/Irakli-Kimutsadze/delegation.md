# Delegation Log . check_ordering . Irakli Kimutsadze

## What I delegated
Rung 3 (write code from spec, I review): I gave Claude the feature
description, rules and the prompt from the assignment, and asked for
ordering.py plus pytest tests.

## First attempt - what came back wrong
My first prompt did not include the spec.md details. Claude's first
version used a "category" key instead of "zone", and its warning
message did not include program names, so it did not match AC2.

## How I fixed it
I gave Claude the spec and golden questions. It rewrote the function to
use "zone", include program names in the message, and use the test names
from golden.md (test_reach_above_safe, test_correct_order,
test_single_item).

## Verification
I committed the files to GitHub and ran pytest in a Codespace.
All 9 tests passed.

## What I learned
Giving the AI the full spec up front gives better results than a short
prompt. Tests for what the function must NOT do (realistic above safe
must not warn) matter as much as tests for what it should do.
