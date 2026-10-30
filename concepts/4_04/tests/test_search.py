import pytest
from course_kit.loader import load_concept_module
from course_kit.rag import FakeEmbedder

search = load_concept_module("4_04", "search")


def test_nearest_neighbor() -> None:
    embedder = FakeEmbedder(dim=16)
    index = search.InMemoryIndex(dim=16)
    index.add("auth:0", embedder.embed("Bearer JWT token"), payload={"stem": "authentication"})
    index.add("hooks:0", embedder.embed("HMAC-SHA256 webhook"), payload={"stem": "webhooks"})
    hits = index.search(embedder.embed("Bearer JWT"), k=1)
    ident = hits[0].get("id") or hits[0].get("chunk_id")
    assert ident == "auth:0"
    assert hits[0]["score"] > 0


def test_dim_mismatch() -> None:
    index = search.InMemoryIndex(dim=4)
    with pytest.raises(ValueError):
        index.add("x:0", [1.0, 0.0])
