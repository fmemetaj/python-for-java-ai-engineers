import numpy as np
from course_kit.loader import load_concept_module

ranking = load_concept_module("4_02", "ranking")


def test_l2_normalize_345() -> None:
    unit = ranking.l2_normalize([3.0, 4.0])
    assert np.allclose(unit, [0.6, 0.8])


def test_zero_stays_zero() -> None:
    assert np.allclose(ranking.l2_normalize([0.0, 0.0]), [0.0, 0.0])


def test_topk_order() -> None:
    matrix = [[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]]
    assert ranking.topk_indices([1.0, 0.0], matrix, 2) == [0, 2]
