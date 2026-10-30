import pytest
from course_kit.loader import load_concept_module

scale = load_concept_module("7_05", "scale")


def test_scale() -> None:
    assert scale.cost_per_n(0.00004, 100) == pytest.approx(0.004)
    assert scale.cost_per_n(0.0, 100) == 0.0
    assert scale.cost_per_n(0.001, 0) == 0.0


def test_negative() -> None:
    with pytest.raises(ValueError):
        scale.cost_per_n(-0.01, 100)
    with pytest.raises(ValueError):
        scale.cost_per_n(0.01, -1)
