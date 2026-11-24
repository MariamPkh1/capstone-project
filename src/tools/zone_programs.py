"""`zone_programs` · HW2 · owner: KVIRIKE7"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .. import data, scoring
from ..contracts import Contract, ProgramCode, Scores
from .base import READS, Tool, ToolFailure, mcp_run

# One shared type, used by the contract AND the MCP door, so both describe it identically.
Codes = Annotated[
    list[ProgramCode],
    Field(min_length=1, max_length=20, description="Program codes to zone; leave out for every program"),
]


# 1 · the contract
class ZonePrograms(Contract):
    """Competitive score and zone (safe, realistic, reach, unknown) for each program, from the student's exam scores. Reads only."""

    scores: Scores
    codes: Codes | None = None


# result models: exactly the fields from the spec
class ProgramZone(BaseModel):
    code: str
    name: str
    competitive_score: float | None
    zone: Literal["safe", "realistic", "reach", "unknown"]
    cutoff_min: float | None
    cutoff_max: float | None


class ZoneResult(BaseModel):
    data_label: str
    programs: list[ProgramZone]


# 2 · the function
def zone_programs(args: ZonePrograms) -> ZoneResult:
    if args.codes is None:
        chosen = data.programs()
    else:
        chosen = []
        for code in args.codes:
            found = data.program(code)
            if found is None:
                raise ToolFailure(f"There is no program {code}. Call requery_programs to find real codes.")
            chosen.append(found)

    rows = []
    for p in chosen:
        cutoffs = [s["min_score"] for s in p["stats"]]
        score = scoring.competitive_score(args.scores, p["subjects"])
        rows.append(ProgramZone(
            code=p["code"],
            name=p["name"],
            competitive_score=score,
            zone=scoring.zone(score, cutoffs),
            cutoff_min=min(cutoffs) if cutoffs else None,
            cutoff_max=max(cutoffs) if cutoffs else None,
        ))
    return ZoneResult(data_label=data.data_label(), programs=rows)


# 3 · the registry entry
TOOLS = [Tool("zone_programs", ZonePrograms, zone_programs)]


# 4 · the MCP door: same argument names, same types
def register(mcp) -> None:
    @mcp.tool(name="zone_programs", annotations=READS, description=ZonePrograms.__doc__)
    def _zone_programs(scores: Scores, codes: Codes | None = None) -> ZoneResult:
        return mcp_run(zone_programs, ZonePrograms(scores=scores, codes=codes))