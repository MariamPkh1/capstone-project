"""The gates in call_tool(), with a tiny tool defined here so they are tested before any real tool exists."""
import json

from src.act import call_tool
from src.contracts import Contract, ProgramCode
from src.tools import Tool, ToolFailure, tools_for
from pydantic import BaseModel


class Echo(Contract):
    """Echo a program code. Reads only."""
    code: ProgramCode


class Echoed(BaseModel):
    code: str


def echo(args: Echo) -> Echoed:
    if args.code == "NO-SUCH":
        raise ToolFailure("There is no program NO-SUCH. Call requery_programs to find a real code.")
    return Echoed(code=args.code)


ALLOWED = {"echo": Tool("echo", Echo, echo)}


def call(arguments, name="echo"):
    return call_tool({"id": "t", "name": name, "arguments": json.dumps(arguments)}, ALLOWED, None)


def test_valid_call_runs():
    out = call({"code": "TSU-LAW"})
    assert out["ok"] and out["result"] == {"code": "TSU-LAW"}


def test_tool_not_offered_is_refused():
    out = call({"code": "TSU-LAW"}, name="drop_table")
    assert not out["ok"] and "no tool named" in out["error"]


def test_invalid_arguments_never_reach_the_tool():
    out = call({"code": "../../.env"})
    assert not out["ok"] and out["error"].startswith("invalid arguments: code")


def test_unknown_field_is_refused():
    out = call({"code": "TSU-LAW", "student_id": "s123"})
    assert not out["ok"] and "student_id" in out["error"]


def test_expected_failure_reaches_the_model_as_text():
    out = call({"code": "NO-SUCH"})
    assert not out["ok"] and "Call requery_programs" in out["error"]


def test_broken_json_is_refused_not_raised():
    out = call_tool({"id": "t", "name": "echo", "arguments": "{not json"}, ALLOWED, None)
    assert not out["ok"] and out["error"].startswith("invalid arguments")


def test_visitor_is_never_offered_a_write_tool(monkeypatch):
    import src.tools as tools
    monkeypatch.setattr(tools, "TOOLS", {"w": Tool("w", Echo, echo, writes=True)})
    assert tools.tools_for(None) == {} and "w" in tools.tools_for("s123")
