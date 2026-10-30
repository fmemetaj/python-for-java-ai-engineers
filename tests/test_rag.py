"""course_kit.rag: fake embeddings, cosine, chunking, index, hybrid — all offline."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from course_kit.rag import (
    FakeEmbedder,
    VectorIndex,
    bm25_scores,
    chunk_preserving_fences,
    chunk_structured,
    cosine_similarity,
    fuse_scores,
    get_embedder,
    l2_normalize,
    token_hash_embed,
    top_k,
)


def test_fake_embedder_is_deterministic_and_unit() -> None:
    vec = token_hash_embed("Bearer JWT", dim=16)
    assert vec.shape == (16,)
    assert abs(float(np.linalg.norm(vec)) - 1.0) < 1e-9
    assert np.allclose(vec, FakeEmbedder(dim=16).embed("Bearer JWT"))


def test_get_embedder_fake_default() -> None:
    embedder = get_embedder("fake")
    assert isinstance(embedder, FakeEmbedder)


def test_get_embedder_openai_is_opt_in() -> None:
    with pytest.raises(RuntimeError, match="embeddings.create"):
        get_embedder("openai")


def test_cosine_and_topk() -> None:
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)
    assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0
    ranked = top_k([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], k=1)
    assert ranked[0][0] == 0
    unit = l2_normalize([3.0, 4.0])
    assert np.allclose(unit, [0.6, 0.8])


def test_fences_stay_atomic() -> None:
    text = "intro\n\n```java\n@PostMapping\n```\n\noutro"
    kept = chunk_preserving_fences(text, max_chars=12, overlap=0, path="PaymentController.md")
    code = [c for c in kept if c.is_code]
    assert len(code) == 1
    assert "@PostMapping" in code[0].text
    assert code[0].text.count("```") == 2


def test_structured_keeps_heading() -> None:
    chunks = chunk_structured("# Refunds\n\nPartial refunds are allowed.\n", path="refunds.md")
    assert chunks
    assert chunks[0].heading == "Refunds"


def test_index_roundtrip(tmp_path: Path) -> None:
    embedder = FakeEmbedder(dim=8)
    index = VectorIndex(dim=8)
    index.add("a:0", embedder.embed("refund captured"), payload={"stem": "refunds"})
    path = tmp_path / "emb.json"
    index.save(path)
    loaded = VectorIndex.load(path)
    hits = loaded.search(embedder.embed("refund captured"), k=1)
    assert hits[0]["chunk_id"] == "a:0"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["model"] == "fake-hash-v1"


def test_bm25_and_fuse() -> None:
    scores = bm25_scores("refund", ["auth token", "refund captured", "hmac"])
    assert scores[1] > scores[0]
    fused = fuse_scores([0.0, 1.0], [3.0, 3.0], alpha=1.0)
    assert fused[1] > fused[0]
