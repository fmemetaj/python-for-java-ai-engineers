"""Fake hosted file_search vs DocsDesk's owned RAG — offline comparison."""

from __future__ import annotations

from dataclasses import dataclass

from course_kit.hosted import (
    RetrievalHit,
    StackDecision,
    choose_stack,
    decision_record,
    lock_in_flags,
    next_hosted_turn,
    overlap_rate,
)

from .rag import RagDesk

HOSTED_HITS = (
    RetrievalHit(
        chunk_id="hosted-auth",
        source="hosted:payments-api/authentication.md",
        text="Clients send Authorization: Bearer <token>.",
        score=0.91,
    ),
    RetrievalHit(
        chunk_id="hosted-refund",
        source="hosted:payments-api/refunds.md",
        text="Refund a captured payment with POST /payments/{id}/refunds.",
        score=0.88,
    ),
)


@dataclass(frozen=True)
class HostedComparison:
    question: str
    own_ids: tuple[str, ...]
    hosted_ids: tuple[str, ...]
    overlap: float
    decision: StackDecision
    record: dict[str, object]
    hosted_text: str


def fake_file_search(question: str) -> list[RetrievalHit]:
    """Keyword routing over canned hosted hits. Not a live tool call."""
    lowered = question.lower()
    if "refund" in lowered:
        return [HOSTED_HITS[1], HOSTED_HITS[0]]
    if "auth" in lowered or "bearer" in lowered or "token" in lowered:
        return [HOSTED_HITS[0]]
    return list(HOSTED_HITS)


def compare_retrieve(question: str, *, own_recall: float = 0.8) -> HostedComparison:
    rag = RagDesk()
    own = rag.retrieve(question, k=5)
    own_ids = tuple(str(hit.get("chunk_id", "")) for hit in own)
    hosted = fake_file_search(question)
    hosted_ids = tuple(hit.chunk_id for hit in hosted)
    overlap = overlap_rate(list(own_ids), list(hosted_ids))
    decision = choose_stack(
        own_recall=own_recall,
        hosted_available=True,
        can_export=True,
        can_eval=True,
        overlap=overlap,
    )
    flags = lock_in_flags(vendor_chunking=True, exportable=False, billed_separately=True)
    turn = next_hosted_turn(1, question, hosted)
    return HostedComparison(
        question=question,
        own_ids=own_ids,
        hosted_ids=hosted_ids,
        overlap=overlap,
        decision=decision,
        record=decision_record(decision, flags=flags),
        hosted_text=turn.text,
    )
