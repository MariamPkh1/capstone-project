"""What every tool is made of. Each tool module in src/tools/ builds on these."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel

from ..contracts import Contract

# Every Abiturienti tool so far only reads. A tool that changes something needs its own annotations.
READS = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


class ToolFailure(Exception):
    """An expected failure. The message goes back to the model, so make it say what to do next."""


@dataclass(frozen=True)
class Tool:
    name: str
    args: type[Contract]
    run: Callable[..., BaseModel]
    writes: bool = False                  # True: changes the world, needs a signed-in caller

    def schema(self) -> dict:
        """What the model sees: name, description and JSON Schema, all from the contract."""
        return {"type": "function", "function": {
            "name": self.name, "description": self.args.__doc__.strip(),
            "parameters": self.args.model_json_schema()}}


def mcp_run(fn, args: Contract):
    """Run a tool for the MCP door: expected failures reach the host as readable errors."""
    try:
        return fn(args)
    except ToolFailure as e:
        raise ToolError(str(e)) from e
