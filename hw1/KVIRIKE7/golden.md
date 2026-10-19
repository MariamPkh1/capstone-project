# HW1 golden questions · Score and zone for one applicant

Run on 19 October 2026, from `hw1/KVIRIKE7`, with `python -m src.scoring <subject=score ...>`. Data: `src/data/programs.json` (SAMPLE DATA, invented numbers, not real NAEC cutoffs). Unit tests: `python -m pytest hw1\KVIRIKE7` gave 15 passed.

| # | Question (input) | Expected | Actual | Pass? | How I ran it |
|---|---|---|---|---|---|
| 1 | `maths=160 english=170` | SAMPLE-CS = 650, zone realistic (cutoffs 610 to 655, safe starts at 660). Programs that need georgian or biology: unknown | SAMPLE-CS 650 realistic; SAMPLE-LAW, SAMPLE-BA, SAMPLE-BIO None unknown; SAMPLE-NEW 330 unknown | pass | `python -m src.scoring maths=160 english=170` |
| 2 | `maths=180 georgian=160 english=170 biology=150` | the four programs with cutoff history are safe; SAMPLE-NEW (no history) is unknown | SAMPLE-CS 710 safe; SAMPLE-LAW 650 safe; SAMPLE-BA 690 safe; SAMPLE-BIO 620 safe; SAMPLE-NEW 350 unknown | pass | `python -m src.scoring maths=180 georgian=160 english=170 biology=150` |
| 3 | `maths=250` (above the 0 to 200 scale) | message `Invalid score: maths: score 250 is outside 0-200`, exit code 1 | exactly that message, exit code 1 | pass | `python -m src.scoring maths=250`, then `echo $LASTEXITCODE` |

Raw output of question 1:

```
SAMPLE DATA - invented numbers for testing, NOT real NAEC cutoffs
SAMPLE-CS       650  realistic
SAMPLE-LAW     None  unknown
SAMPLE-BA      None  unknown
SAMPLE-BIO     None  unknown
SAMPLE-NEW      330  unknown
```

Raw output of question 2:

```
SAMPLE DATA - invented numbers for testing, NOT real NAEC cutoffs
SAMPLE-CS       710  safe
SAMPLE-LAW      650  safe
SAMPLE-BA       690  safe
SAMPLE-BIO      620  safe
SAMPLE-NEW      350  unknown
```

Raw output of question 3:

```
SAMPLE DATA - invented numbers for testing, NOT real NAEC cutoffs
Invalid score: maths: score 250 is outside 0-200
```

Exit code printed by `echo $LASTEXITCODE`: `1`.

Limit of this evidence: the cutoffs and the 0 to 200 scale are sample values, so these runs prove the logic, not the real NAEC results.
