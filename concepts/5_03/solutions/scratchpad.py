"""Compress observations into a short scratchpad line."""

from __future__ import annotations

from collections.abc import Sequence


def scratchpad(observations: Sequence[str], *, max_chars: int) -> str:
    """Join with ' | '. If longer than max_chars, ellipsize with '...'."""
    joined = " | ".join(observations)
    if len(joined) <= max_chars:
        return joined
    if max_chars <= 3:
        return "." * max_chars
    return joined[: max_chars - 3].rstrip() + "..."
