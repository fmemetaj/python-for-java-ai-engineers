"""Control-flow helpers used by a tiny DocsDesk status parser."""

from __future__ import annotations


def label_status(code: int) -> str:
    """Map 200→ok, 400/404→client, 500→server, anything else→other."""
    raise NotImplementedError


def sum_to(n: int) -> int:
    """Return 1 + 2 + ... + n. Use a for-in over range."""
    raise NotImplementedError


def first_error(levels: list[str]) -> str | None:
    """Return 'ERROR' if it appears, otherwise None."""
    raise NotImplementedError
