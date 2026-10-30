import pytest
from course_kit.loader import load_concept_module

budget = load_concept_module("6_04", "budget")


def test_remaining() -> None:
    assert budget.remaining(1.0, 0.4) == 0.6
    assert budget.remaining(0.2, 0.5) == 0.0
    with pytest.raises(ValueError):
        budget.remaining(1.0, -0.1)


def test_route_model() -> None:
    assert budget.route_model(1.0, 0.0001) == budget.DEFAULT
    assert budget.route_model(0.00005, 0.01) == budget.CHEAP
    with pytest.raises(RuntimeError):
        budget.route_model(0.0, 0.01)
