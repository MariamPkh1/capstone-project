"""`check_priority_list` · HW2 · owner: Irakli-Kimutsadze"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .. import data, scoring
from ..contracts import Contract, ProgramCode, Scores
from .base import READS, Tool, ToolFailure, mcp_run

# Shared by the contract (part 1) and the MCP door (part 4), so both describe it the same way.
Codes = Annotated[list[ProgramCode], Field(min_length=1, max_length=20,
                                           description="Program codes in the student's order, first choice first")]


# 1 · the contract: extra="forbid" comes from Contract. No zone, user, student or account field.
class CheckPriorityList(Contract):
    """Checks a student's priority list against their scores. Warns when a safe program is ranked above a reach program, and when no program is safe. Reads only."""

    codes: Codes
    scores: Scores


class Row(BaseModel):
    rank: int
    code: str
    zone: Literal["safe", "realistic", "reach", "unknown"]


class Warning(BaseModel):
    type: Literal["safe_above_reach", "no_safe"]
    message: str


class PriorityCheck(BaseModel):
    valid: bool
    rows: list[Row]
    warnings: list[Warning]


# 2 · the function: takes the validated contract only
def check_priority_list(args: CheckPriorityList) -> PriorityCheck:
    # Expected failure 1: a duplicate code
    seen: set[str] = set()
    for code in args.codes:
        if code in seen:
            raise ToolFailure(f"{code} appears more than once. NAEC lists each program once; "
                              "remove the duplicate and call again.")
        seen.add(code)

    # Expected failure 2: an unknown code. Data comes only through src/data.py.
    rows: list[Row] = []
    for rank, code in enumerate(args.codes, start=1):
        program = data.program(code)
        if program is None:
            raise ToolFailure(f"There is no program {code}. Call requery_programs to find real codes.")
        score = scoring.competitive_score(args.scores, program["subjects"])
        cutoffs = [stat["min_score"] for stat in program["stats"]]
        rows.append(Row(rank=rank, code=code, zone=scoring.zone(score, cutoffs)))

    warnings: list[Warning] = []

    # NAEC stops at the first program the student qualifies for, so a safe program
    # ranked above a reach program hides the reach one.
    for i, upper in enumerate(rows):
        if upper.zone != "safe":
            continue
        for lower in rows[i + 1:]:
            if lower.zone == "reach":
                warnings.append(Warning(
                    type="safe_above_reach",
                    message=(f"{upper.code} (safe, rank {upper.rank}) is above "
                             f"{lower.code} (reach, rank {lower.rank}). "
                             f"NAEC would stop at {upper.code}; move {lower.code} above it.")))

    if not any(row.zone == "safe" for row in rows):
        warnings.append(Warning(
            type="no_safe",
            message="No program on this list is safe. Add at least one safe program at the bottom."))

    return PriorityCheck(valid=not warnings, rows=rows, warnings=warnings)


# 3 · the registry entry
TOOLS = [Tool("check_priority_list", CheckPriorityList, check_priority_list)]


# 4 · the MCP door: same argument names, same types
def register(mcp) -> None:
    @mcp.tool(name="check_priority_list", annotations=READS, description=CheckPriorityList.__doc__)
    def _check_priority_list(codes: Codes, scores: Scores) -> PriorityCheck:
        return mcp_run(check_priority_list, CheckPriorityList(codes=codes, scores=scores))
