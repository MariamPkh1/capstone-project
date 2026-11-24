"""The MCP door: every tool in TOOLS is served by the MCP server with the same arguments."""
import asyncio

import pytest
from mcp import Client

from src.mcp_server import mcp
from src.tools import TOOLS


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as c:
        return {t.name: t for t in (await c.list_tools()).tools}


def strip(schema):
    return {k: {kk: vv for kk, vv in v.items() if kk != "title"} for k, v in schema.get("properties", {}).items()}


def test_same_tools_through_both_doors():
    assert set(run(listed())) == set(TOOLS)


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_both_doors_describe_the_arguments_identically(name):
    mcp_schema = run(listed())[name].input_schema
    fc_schema = TOOLS[name].schema()["function"]["parameters"]
    assert strip(mcp_schema) == strip(fc_schema)
    assert set(mcp_schema.get("required", [])) == set(fc_schema.get("required", []))


@pytest.mark.parametrize("name", sorted(TOOLS))
def test_read_tools_are_annotated_read_only(name):
    assert run(listed())[name].annotations.read_only_hint is not TOOLS[name].writes
