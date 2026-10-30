import pytest
from course_kit.loader import load_concept_module

cosine = load_concept_module("4_02", "cosine")


def test_parallel() -> None:
    assert cosine.cosine_similarity([1.0, 0.0], [2.0, 0.0]) == pytest.approx(1.0)


def test_orthogonal() -> None:
    assert cosine.cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_opposite() -> None:
    assert cosine.cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == pytest.approx(-1.0)


def test_zero() -> None:
    assert cosine.cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_shape_mismatch() -> None:
    with pytest.raises(ValueError):
        cosine.cosine_similarity([1.0], [1.0, 0.0])
