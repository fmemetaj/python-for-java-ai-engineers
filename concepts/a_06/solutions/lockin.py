"""Guided: lock-in flags for hosted retrieval."""

from __future__ import annotations

from course_kit.hosted import lock_in_flags


def flags(*, vendor_chunking: bool, exportable: bool, billed_separately: bool) -> dict[str, bool]:
    """Include ci_honest = exportable and not vendor_chunking."""
    return lock_in_flags(
        vendor_chunking=vendor_chunking,
        exportable=exportable,
        billed_separately=billed_separately,
    )
