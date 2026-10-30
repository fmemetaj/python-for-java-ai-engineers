"""First offline eval: exact match on fake answers (solution)."""

from __future__ import annotations


def grade_case(expected: str, actual: str) -> bool:
    """True when the fake answer equals the golden string."""
    return expected == actual


def run_eval(cases: list[tuple[str, str]], answers: list[str]) -> dict[str, int]:
    """Return passed/failed counts comparing answers[i] to cases[i][1]."""
    if len(answers) != len(cases):
        raise ValueError("answers must align with cases")
    passed = 0
    failed = 0
    for case, actual in zip(cases, answers, strict=True):
        if grade_case(case[1], actual):
            passed += 1
        else:
            failed += 1
    return {"passed": passed, "failed": failed}
