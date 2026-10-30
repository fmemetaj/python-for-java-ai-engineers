"""RAG pipeline over the payments-api fixture. Offline FakeLLM + FakeEmbedder."""

from __future__ import annotations

from docsdesk.rag import RagDesk, assemble_context, citations_from_hits

desk = RagDesk(k=5, hybrid=True)
hits = desk.retrieve("How do I refund a captured payment?")
stems = [str(hit.get("stem")) for hit in hits]
assert "refunds" in stems

context = assemble_context(hits, budget=1800)
assert "[" in context
assert "refund" in context.lower()

answer = desk.ask("How do I refund a captured payment?")
assert "captured" in answer.answer.lower() or "refund" in answer.answer.lower()
assert answer.citations
assert {cite.chunk_id for cite in answer.citations} <= {str(hit["chunk_id"]) for hit in hits}

cites = citations_from_hits(hits[:1])
assert cites[0].chunk_id == hits[0]["chunk_id"]

print("4.5 examples ok")
