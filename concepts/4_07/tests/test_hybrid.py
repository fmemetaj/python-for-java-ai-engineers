import pytest
from course_kit.loader import load_concept_module

hybrid = load_concept_module("4_07", "hybrid")


def test_bm25_prefers_matching_doc() -> None:
    docs = ["Bearer JWT", "refund captured payment", "HMAC webhook"]
    scores = hybrid.bm25_scores("refund captured", docs)
    assert scores[1] > scores[0]
    assert hybrid.bm25_scores("x", []) == []


def test_fuse_minmax() -> None:
    fused = hybrid.fuse_scores([0.0, 1.0], [10.0, 10.0], alpha=1.0)
    assert fused[1] > fused[0]
    with pytest.raises(ValueError):
        hybrid.fuse_scores([1.0], [1.0, 2.0], alpha=0.5)


def test_rerank() -> None:
    ids = hybrid.rerank_ids([1.0, 0.0], ["a", "b"], [[0.0, 1.0], [1.0, 0.0]], k=1)
    assert ids == ["b"]
