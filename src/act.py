"""Function calling: the model asks for a tool, our code decides whether it runs.

call_tool() checks, in order: is the tool offered to this caller, do the arguments pass the
contract, then runs it. Arguments are validated against the contract before the tool runs;
a failure goes back to the model as an error and nothing runs. The caller's identity is never
a tool argument: it comes from the session and is passed in here.

call_tool() never raises. Whatever happens becomes a dict the model can read and one line in
logs/tools.jsonl.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .tools import Tool, ToolFailure

TOOL_LOG = Path(os.environ.get("ABITURIENTI_TOOL_LOG", "logs/tools.jsonl"))


def brief(e: ValidationError) -> str:
    """A validation error the model can act on: which field, what was wrong. No stack trace."""
    return "; ".join(f"{'.'.join(map(str, x['loc'])) or 'arguments'}: {x['msg']}" for x in e.errors())


def call_tool(call: dict, allowed: dict[str, Tool], caller: str | None) -> dict:
    t0 = time.perf_counter()
    tool = allowed.get(call["name"])
    if tool is None:                                                     # 1 · not offered to this caller
        return _log(call, t0, error=f"no tool named {call['name']!r} is available")
    try:
        args = tool.args.model_validate_json(call["arguments"] or "{}")  # 2 · the contract, checked
    except ValidationError as e:
        return _log(call, t0, error=f"invalid arguments: {brief(e)}")
    try:
        out = tool.run(args, caller=caller) if tool.writes else tool.run(args)   # 3 · identity from us
    except ToolFailure as e:                                             # expected: not found, no data
        return _log(call, t0, error=str(e))
    return _log(call, t0, result=out.model_dump(mode="json"))            # 4 · the result, as data


def _log(call: dict, t0: float, result: dict | None = None, error: str | None = None) -> dict:
    """One line per call. The caller is deliberately not logged: no personal data in logs."""
    line = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tool": call["name"],
            "arguments": call["arguments"], "ok": error is None, "error": error,
            "latency_ms": round((time.perf_counter() - t0) * 1000, 1)}
    TOOL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TOOL_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return {**line, "result": result}
