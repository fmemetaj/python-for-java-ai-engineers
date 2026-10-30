"""In-memory vector index. Offline FakeEmbedder."""

from __future__ import annotations

from course_kit.rag import FakeEmbedder, VectorIndex

embedder = FakeEmbedder(dim=16)
index = VectorIndex(dim=16)
index.add("auth:0", embedder.embed("Bearer JWT token"), payload={"stem": "authentication"})
index.add("hooks:0", embedder.embed("HMAC-SHA256 webhook signature"), payload={"stem": "webhooks"})
assert len(index) == 2

hits = index.search(embedder.embed("How do clients send a Bearer JWT?"), k=1)
assert hits[0]["chunk_id"] == "auth:0"
assert hits[0]["stem"] == "authentication"
assert hits[0]["score"] > 0

dumped = index.dump()
assert dumped["dim"] == 16
assert dumped["model"] == "fake-hash-v1"

print("4.4 examples ok")
