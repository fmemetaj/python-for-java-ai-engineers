import numpy as np
import pytest
from course_kit.loader import load_concept_module

embed = load_concept_module("4_01", "embed")


def test_dim_and_norm() -> None:
    vec = embed.token_hash_embed("Bearer JWT", dim=8)
    assert vec.shape == (8,)
    assert abs(float(np.linalg.norm(vec)) - 1.0) < 1e-9


def test_deterministic() -> None:
    a = embed.token_hash_embed("refund", dim=16)
    b = embed.token_hash_embed("refund", dim=16)
    assert np.allclose(a, b)


def test_empty_is_unit() -> None:
    vec = embed.token_hash_embed("", dim=8)
    assert vec[0] == 1.0
    assert np.allclose(vec[1:], 0.0)


def test_rejects_tiny_dim() -> None:
    with pytest.raises(ValueError):
        embed.token_hash_embed("x", dim=1)
