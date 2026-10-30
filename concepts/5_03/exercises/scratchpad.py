"""Compress observations into a short scratchpad line."""

from __future__ import annotations

from collections.abc import Sequence


def scratchpad(observations: Sequence[str], *, max_chars: int) -> str:
    """Join with ' | '. If longer than max_chars, ellipsize with '...'."""
    raise NotImplementedError
