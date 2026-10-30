"""Open: write-tool approval and citation presence."""

from __future__ import annotations

_WRITE = frozenset({"propose_page", "delete_page"})


def needs_approval(tool_name: str) -> bool:
    """True for propose_page and delete_page; false for read-only tools."""
    return tool_name in _WRITE


def citation_ok(citations: list[object]) -> bool:
    """True when the answer cited at least one retrieved chunk."""
    return len(citations) >= 1
