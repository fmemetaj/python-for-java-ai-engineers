"""Assemble retrieved chunks into a prompt context."""

from __future__ import annotations

from collections.abc import Sequence


def assemble_context(chunks: Sequence[dict[str, str]], *, budget: int) -> str:
    """Join '[chunk_id]\\ntext' blocks until budget. Keep at least the first that fits."""
    raise NotImplementedError
