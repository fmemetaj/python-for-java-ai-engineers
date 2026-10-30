"""Port a Java loop+Map aggregation to comprehensions (solution)."""

from __future__ import annotations


def error_messages(rows: list[dict[str, str | int]]) -> list[str]:
    """Messages of rows whose level is ERROR, in input order."""
    return [str(row["message"]) for row in rows if row["level"] == "ERROR"]


def index_by_id(rows: list[dict[str, str | int]]) -> dict[int, str]:
    """Map id → message. Later rows with the same id win."""
    return {int(row["id"]): str(row["message"]) for row in rows}


def unique_levels(rows: list[dict[str, str | int]]) -> set[str]:
    """The set of level strings."""
    return {str(row["level"]) for row in rows}
