"""Three eval checks: exact match, schema, rubric (substring)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def grade_exact(expected: str, actual: str) -> bool:
    """True when the strings are equal (FakeLLM golden answers)."""
    return expected == actual


def grade_schema(validate: Callable[[Any], object], payload: Any) -> bool:
    """True when validate(payload) does not raise."""
    try:
        validate(payload)
    except Exception:
        return False
    return True


def grade_rubric(text: str, needles: Sequence[str]) -> bool:
    """True when every needle appears in text (case-insensitive)."""
    lowered = text.lower()
    return all(needle.lower() in lowered for needle in needles)
