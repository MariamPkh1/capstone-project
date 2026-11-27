# Pattern Journal . Irakli Kimutsadze . Weeks 5-7

## Week 5 . Tool Contract

Pattern: Tool Contract

Where I saw it: In my check_priority_list tool, the program codes are checked before the tool runs. A code has to match a fixed pattern, so when my test sent one with SQL inside, the tool refused it straight away as invalid arguments. The tool also has no zone field, so the model can ask but my own code decides the zone. In my red run I removed the pattern, and that test failed, which showed me how much one line protects.

What I would do differently: I would write the bad-input tests first and watch them fail before asking the AI for code. I would also check the spec's direction rule first, because my HW1 check warned reach above safe, when the real problem is safe above reach.

## Week 6 . Session State

Pattern: Session State

Where I saw it: My tool keeps no memory on purpose. Every call gets the full list and the scores, and my tests use `caller: null`, so nothing about a person or an earlier turn is saved. This means there is nothing to leak or forget to delete.

What I would do differently: If the chat ever remembers a student's scores, I would first write down who can read it, how long it lives and how it is deleted, and test it with two different users before building it.

## Week 7 . Supervised Autonomy Loop

Pattern: Supervised Autonomy Loop

Where I saw it: I marked my tool as a read tool, because it only checks an order and changes nothing. Asking twice gives the same answer, so a loop can call it without a person's yes. The one step that must wait for a person's yes is loading the parsed NAEC data into the database, because a wrong cutoff would enter silently and is much harder to undo than a check.

What I would do differently: I would label every tool read or consequential from the start, and add a test that calls a tool twice with the same input to make sure the second call is harmless.
