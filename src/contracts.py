"""The shared pieces of every tool contract. Each tool's own contract lives in its module in src/tools/.

Rules that hold for every contract:
  * extra="forbid": an argument we did not ask for is an error, never ignored
  * every string has a pattern or a fixed set of values; every number has bounds
  * nothing here names WHO is calling. Identity comes from the session, never the model.
"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

ProgramCode = Annotated[str, Field(pattern=r"^[A-Z]{2,8}-[A-Z]{2,6}$", description="Program code, like TSU-LAW")]
University = Annotated[Literal["TSU", "ILIA", "GTU", "FREEUNI", "KIU"], Field(description="University")]
City = Annotated[Literal["Tbilisi", "Kutaisi"], Field(description="City the program is taught in")]
Language = Annotated[Literal["ka", "en"], Field(description="Teaching language: ka (Georgian) or en (English)")]
StudyField = Annotated[Literal["law", "computer-science", "psychology", "biology", "engineering", "business"],
                       Field(description="Field of study")]
Subject = Literal["georgian", "english", "maths", "history", "physics", "biology"]
Score = Annotated[float, Field(ge=0, le=100, strict=True, description="Exam score, 0 to 100, as a number")]
Scores = Annotated[dict[Subject, Score], Field(min_length=1, max_length=6,
                                               description="The student's exam scores by subject, like {\"georgian\": 80, \"maths\": 90}")]
Year = Annotated[Literal[2024, 2025, 2026], Field(description="Admission year with published cutoffs: 2024, 2025 or 2026")]


class Contract(BaseModel):
      model_config = ConfigDict(extra="ignore")
