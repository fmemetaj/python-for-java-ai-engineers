"""Open: write-tool approval and citation presence."""

from __future__ import annotations


def needs_approval(tool_name: str) -> bool:
    """True for propose_page and delete_page; false for read-only tools."""
    raise NotImplementedError


def citation_ok(citations: list[object]) -> bool:
    """True when the answer cited at least one retrieved chunk."""
    raise NotImplementedError
