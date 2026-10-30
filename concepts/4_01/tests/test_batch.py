import numpy as np
from course_kit.loader import load_concept_module

batch = load_concept_module("4_01", "batch")


def test_empty_matrix() -> None:
    mat = batch.embed_many([], dim=8)
    assert mat.shape == (0, 8)


def test_stack_and_unit_rows() -> None:
    mat = batch.embed_many(["hello", "world"], dim=8)
    assert mat.shape == (2, 8)
    for row in mat:
        assert abs(float(np.linalg.norm(row)) - 1.0) < 1e-9
