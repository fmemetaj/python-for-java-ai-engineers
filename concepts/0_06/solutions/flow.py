"""Control-flow helpers (solution)."""

from __future__ import annotations


def label_status(code: int) -> str:
    """Map 200→ok, 400/404→client, 500→server, anything else→other."""
    if code == 200:
        return "ok"
    if code in {400, 404}:
        return "client"
    if code == 500:
        return "server"
    return "other"


def sum_to(n: int) -> int:
    """Return 1 + 2 + ... + n. Use a for-in over range."""
    total = 0
    for number in range(1, n + 1):
        total += number
    return total


def first_error(levels: list[str]) -> str | None:
    """Return 'ERROR' if it appears, otherwise None."""
    for level in levels:
        if level == "ERROR":
            return level
    return None
