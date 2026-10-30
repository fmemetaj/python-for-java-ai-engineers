import pytest
from course_kit.loader import load_concept_module

gate = load_concept_module("7_04", "gate")


def test_bar() -> None:
    assert gate.meets_capstone_bar(44, 44) is True
    assert gate.meets_capstone_bar(29, 29) is False
    assert gate.meets_capstone_bar(44, 43) is False
    assert gate.meets_capstone_bar(30, 30, min_cases=30) is True


def test_bad_counts() -> None:
    with pytest.raises(ValueError):
        gate.meets_capstone_bar(10, 11)
    with pytest.raises(ValueError):
        gate.meets_capstone_bar(-1, 0)
    with pytest.raises(ValueError):
        gate.meets_capstone_bar(10, 10, min_cases=0)
