"""Open: grade one suite case; all-true means the suite passed."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def grade_case(
    case: dict[str, Any],
    *,
    looks_like_injection: Callable[[str], bool],
    redact_secrets: Callable[[str, Sequence[str]], str],
) -> bool:
    """Return True when the case behaved as ``expect``.

    Kinds: direct (blocked), benign (allowed), leak (redacted), indirect
    (strip lines that look like injection; leftover text must be clean).
    """
    raise NotImplementedError


def suite_ok(results: Sequence[bool]) -> bool:
    """True when every result is True and the sequence is non-empty."""
    raise NotImplementedError
