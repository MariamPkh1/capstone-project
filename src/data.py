"""Program and cutoff data, read only.

Least privilege: this module is the only code that opens the data file, it opens it for
reading, and it has no function that writes. Tools get plain copies, never the file itself.
Today the data is a JSON file of SAMPLE numbers; the spec's PostgreSQL replaces it later,
behind the same three functions, with a read-only database user.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DATA_FILE = Path(os.environ.get("ABITURIENTI_DATA", Path(__file__).resolve().parents[1] / "data" / "programs.json"))


def _load() -> dict:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def programs() -> list[dict]:
    return _load()["programs"]


def program(code: str) -> dict | None:
    return next((p for p in programs() if p["code"] == code), None)


def data_label() -> str:
    return _load()["data_label"]
