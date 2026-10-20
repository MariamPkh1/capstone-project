# Pattern Journal · KVIRIKE7 · Weeks 1 to 4

*One entry per week: the pattern, one place I saw or used it, one thing I would do differently.*

## Week 1 · The Autonomy Ladder (Delegation and Verification)

**Where I used it:** in HW1 I wrote my own version of the feature first, then asked Claude for a version and compared the two. I treated Claude's code as a draft at rung 3: I ran the tests and the golden questions myself and probed it by hand before keeping it. **What I noticed:** all 15 tests passed and the code still had a bug, because the tests never touched the command line. Only my own odd inputs (`maths=1e2`) found it, so the checking is the real work, not the drafting. **Do differently:** decide before I start which inputs I will try by hand, instead of waiting until the tests are green.

## Week 2 · Spec Before Code

**Where I used it:** the HW1 spec has seven acceptance criteria, each one decidable by a test, including error cases (invalid scores, missing subjects, no cutoff data). **What I noticed:** the bug I found was in a part the spec never described, the format of values on the command line. There was no criterion, so there was no test. The spec was the gap, not the code. **Do differently:** write a criterion for every way the user can type input, not only for the functions behind it.
