"""The tool registry. One module per tool, so each owner edits only their own file.

To add a tool: write src/tools/<tool>.py with its contract, function, a TOOLS list and register(mcp),
then list the module in MODULES below.
"""
from __future__ import annotations

from . import check_priority_list, requery_programs, zone_programs
from .base import READS, Tool, ToolFailure, mcp_run

MODULES = [requery_programs, zone_programs, check_priority_list]
TOOLS: dict[str, Tool] = {t.name: t for m in MODULES for t in m.TOOLS}


def tools_for(caller: str | None) -> dict[str, Tool]:
    """Least privilege by construction: a visitor who is not signed in is never offered a write tool."""
    return {n: t for n, t in TOOLS.items() if caller or not t.writes}


__all__ = ["MODULES", "READS", "TOOLS", "Tool", "ToolFailure", "mcp_run", "tools_for"]
