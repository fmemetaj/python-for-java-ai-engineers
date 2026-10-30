import pytest
from course_kit.loader import load_concept_module

hints = load_concept_module("0_23", "hints")


def test_as_ints() -> None:
    assert hints.as_ints(["1", "2", "10"]) == [1, 2, 10]
    with pytest.raises(ValueError):
        hints.as_ints(["1", "x"])


def test_first() -> None:
    assert hints.first(["a", "b"]) == "a"
    assert hints.first([7]) == 7
    with pytest.raises(ValueError):
        hints.first([])


def test_hints_do_not_block_wrong_runtime_types() -> None:
    # The interpreter does not type-check. A static tool would flag this call.
    assert hints.first([1, "x"]) == 1  # type: ignore[list-item]
