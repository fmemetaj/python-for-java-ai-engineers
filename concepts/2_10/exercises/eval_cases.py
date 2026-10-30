"""First offline eval: exact match on fake answers."""

from __future__ import annotations


def grade_case(expected: str, actual: str) -> bool:
    """True when the fake answer equals the golden string."""
    raise NotImplementedError


def run_eval(cases: list[tuple[str, str]], answers: list[str]) -> dict[str, int]:
    """Return passed/failed counts comparing answers[i] to cases[i][1]."""
    raise NotImplementedError
