"""Port a Java loop+Map aggregation to comprehensions."""

from __future__ import annotations


def error_messages(rows: list[dict[str, str | int]]) -> list[str]:
    """Messages of rows whose level is ERROR, in input order."""
    raise NotImplementedError


def index_by_id(rows: list[dict[str, str | int]]) -> dict[int, str]:
    """Map id → message. Later rows with the same id win."""
    raise NotImplementedError


def unique_levels(rows: list[dict[str, str | int]]) -> set[str]:
    """The set of level strings."""
    raise NotImplementedError
