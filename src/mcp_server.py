"""Abiturienti as an MCP server: the same tools as src/tools/, usable by any MCP host.

Run it over stdio (what Claude Code, Cursor and VS Code launch):
    python -m src.mcp_server

Each tool module registers its own MCP tool, with a signature built from the same type
aliases as its contract. tests/test_mcp.py checks that both doors stay identical.
"""
from __future__ import annotations

from mcp.server import MCPServer

from .tools import MODULES

mcp = MCPServer("abiturienti", instructions="Georgian university admissions: programs, cutoffs, zones "
                                            "and priority-list checks. Every number comes from our data, never guess one.")
for module in MODULES:
    module.register(mcp)


if __name__ == "__main__":
    mcp.run()
