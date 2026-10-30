"""Assemble retrieved chunks into a prompt context (solution)."""

from __future__ import annotations

from collections.abc import Sequence


def assemble_context(chunks: Sequence[dict[str, str]], *, budget: int) -> str:
    """Join '[chunk_id]\\ntext' blocks until budget. Keep at least the first that fits."""
    parts: list[str] = []
    used = 0
    for chunk in chunks:
        block = f"[{chunk['chunk_id']}]\n{chunk['text']}"
        extra = len(block) + (2 if parts else 0)
        if parts and used + extra > budget:
            break
        parts.append(block)
        used += extra
    return "\n\n".join(parts)
