# Pattern Journal · KVIRIKE7 · Weeks 5 to 7

## Week 5 · Tool Contract · 2026-11-24
**Where I used it:** `class ZonePrograms(Contract):` in `src/tools/zone_programs.py`. Because `Contract` enforces `extra="forbid"`, golden case `a1`—where the model attempts to pass an extra `zone: "safe"` field—is rejected with `"invalid arguments"` at validation time before `zone_programs()` ever runs.

**What I noticed:** The model never gets to decide the zone; it can only pass `scores` and optional `codes`, and Python calculates the actual result via `scoring.zone()`. Using the same `Codes` type alias in both `ZonePrograms` and `register()` also guarantees that the MCP tool schema and the function-calling schema stay identical. When I first ran `pytest tests/test_tool_golden.py -v -k KVIRIKE7` before registering the tool, all five golden cases (`k1`, `k2`, `k3`, `b1`, and `a1`) failed with `no tool named 'zone_programs' is available`. Once I wired up `TOOLS` and implemented `zone_programs`, all five cases—along with the full 28-test suite—passed.

**Do differently:** Right now, `zone_programs` raises `ToolFailure` on the first unknown program code it hits. Next time, I would collect every unknown code in `args.codes` and report them all in a single error message so the model can fix the entire list in one retry instead of failing one code at a time.

## Week 6 · Session State · 2026-11-24
**Where I used it:** `zone_programs(args: ZonePrograms)` accepts only the validated contract and holds zero internal state—the student's exam scores are passed in on every call, and nothing is persisted between invocations.

**What I noticed:** Keeping the tool completely stateless makes it deterministic: the same inputs always produce the exact same `ZoneResult`, which made writing and debugging the five golden cases straightforward. If the app needs to remember a student's scores across turns, that state belongs in the session layer rather than inside `zone_programs`, with the session injecting `scores` into each call so the tool stays pure.

**Do differently:** I would store the student's validated exam scores once in the session state and inject them automatically into tool calls, rather than forcing the model to re-send the full `scores` dictionary on every turn.

## Week 7 · Supervised Autonomy Loop · 2026-11-24
**Where I saw it:** An agent loop can call `zone_programs` repeatedly—for instance, checking multiple candidate program lists—without human intervention because it is strictly read-only and idempotent. In `src/tools/base.py`, this is encoded both in the `Tool` dataclass (`writes: bool = False`) and in the MCP metadata via `READS` (`read_only_hint=True, destructive_hint=False, idempotent_hint=True`).

**The one action in Abiturienti that must wait for a person's yes:** Submitting or modifying the applicant's official ranked program list (such as saving or locking in final university program preferences for NAEC registration). Every Abiturienti tool built so far only reads, whereas submitting or changing an application ranking alters real-world state (`writes=True`) and carries irreversible admissions consequences for the student, so it must require a signed-in user and explicit confirmation before executing.
