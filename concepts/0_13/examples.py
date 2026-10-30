"""List, dict, and set comprehensions over DocsDesk log rows."""

from __future__ import annotations


def error_messages(rows: list[dict[str, str | int]]) -> list[str]:
    return [str(row["message"]) for row in rows if row["level"] == "ERROR"]


def index_by_id(rows: list[dict[str, str | int]]) -> dict[int, str]:
    return {int(row["id"]): str(row["message"]) for row in rows}


def unique_levels(rows: list[dict[str, str | int]]) -> set[str]:
    return {str(row["level"]) for row in rows}


rows = [
    {"id": 1, "level": "INFO", "message": "started"},
    {"id": 2, "level": "ERROR", "message": "disk full"},
    {"id": 3, "level": "ERROR", "message": "timeout"},
]
assert error_messages(rows) == ["disk full", "timeout"]
assert index_by_id(rows)[2] == "disk full"
assert unique_levels(rows) == {"INFO", "ERROR"}
print("0.13 examples ok")
