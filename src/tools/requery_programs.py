"""`requery_programs` · HW2 · owner: MariamPkh1

The chat's requery-with-filters tool: "I can't move to Tbilisi", "only programs with grants".
It returns programs and their published cutoffs straight from the data, and never computes a
zone or states a number of its own. That is risk 1 (the hallucinated cutoff) turned into a
mitigation: a year we have no data for, like 2027, is refused by the contract before any lookup.
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

from .. import data
from ..contracts import City, Contract, Language, StudyField, University, Year
from .base import READS, Tool, ToolFailure, mcp_run

MaxTuition = Annotated[int, Field(ge=0, le=20000, description="Highest yearly tuition in GEL, 0 to 20000")]


class RequeryPrograms(Contract):
    """Programs that match the student's filters, with each program's published cutoffs. Reads only; it never computes a zone."""
    city: City | None = None
    field: StudyField | None = None
    language: Language | None = None
    university: University | None = None
    grants_only: bool = False
    max_tuition: MaxTuition | None = None
    year: Year | None = None


class Cutoff(BaseModel):
    year: int
    min_score: float


class ProgramMatch(BaseModel):
    code: str
    name: str
    university: str
    city: str
    language: str
    tuition: int
    grant_seats: int
    cutoffs: list[Cutoff]


class RequeryResult(BaseModel):
    data_label: str
    count: int
    programs: list[ProgramMatch]


def requery_programs(args: RequeryPrograms) -> RequeryResult:
    filters = {"city": args.city, "field": args.field, "language": args.language, "university": args.university}
    found = []
    for p in data.programs():
        if any(wanted is not None and p[key] != wanted for key, wanted in filters.items()):
            continue
        if args.grants_only and p["grant_seats"] == 0:
            continue
        if args.max_tuition is not None and p["tuition"] > args.max_tuition:
            continue
        cutoffs = [Cutoff(**s) for s in p["stats"] if args.year is None or s["year"] == args.year]
        found.append(ProgramMatch(code=p["code"], name=p["name"], university=p["university"], city=p["city"],
                                  language=p["language"], tuition=p["tuition"], grant_seats=p["grant_seats"],
                                  cutoffs=cutoffs))
    if not found:
        raise ToolFailure("No program matches these filters. Drop one filter, for example max_tuition or city, and call again.")
    return RequeryResult(data_label=data.data_label(), count=len(found), programs=found)


TOOLS = [Tool("requery_programs", RequeryPrograms, requery_programs)]


def register(mcp) -> None:
    """Add this module's tools to the MCP server."""
    @mcp.tool(name="requery_programs", annotations=READS, description=RequeryPrograms.__doc__)
    def _requery_programs(city: City | None = None, field: StudyField | None = None, language: Language | None = None,
                          university: University | None = None, grants_only: bool = False,
                          max_tuition: MaxTuition | None = None, year: Year | None = None) -> RequeryResult:
        return mcp_run(requery_programs, RequeryPrograms(city=city, field=field, language=language, university=university,
                                                         grants_only=grants_only, max_tuition=max_tuition, year=year))
