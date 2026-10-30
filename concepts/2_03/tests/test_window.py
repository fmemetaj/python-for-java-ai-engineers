import pytest
from course_kit.loader import load_concept_module

window = load_concept_module("2_03", "window")


def test_remaining() -> None:
    assert window.remaining_budget(100, 40, 20) == 40


def test_overflow_raises() -> None:
    with pytest.raises(ValueError):
        window.remaining_budget(10, 8, 5)


def test_would_overflow() -> None:
    assert window.would_overflow(10, [3, 3], 5) is True
    assert window.would_overflow(10, [3, 3], 4) is False
