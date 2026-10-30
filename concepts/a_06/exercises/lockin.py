"""Guided: lock-in flags for hosted retrieval."""

from __future__ import annotations


def flags(*, vendor_chunking: bool, exportable: bool, billed_separately: bool) -> dict[str, bool]:
    """Include ci_honest = exportable and not vendor_chunking."""
    raise NotImplementedError
