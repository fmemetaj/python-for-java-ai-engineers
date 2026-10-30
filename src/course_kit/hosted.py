"""Hosted Responses tools vs an owned retrieval pipeline.

Official docs: https://platform.openai.com/docs/guides/tools
file_search: https://platform.openai.com/docs/guides/tools-file-search
web_search: https://platform.openai.com/docs/guides/tools-web-search

Graded work never calls hosted tools. Fake results are canned JSON. Concept
4.7 already flagged lock-in; this module is the decision procedure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HOSTED_TOOL_NAMES = ("web_search", "file_search")
StackChoice = Literal["own", "hosted", "hybrid"]


@dataclass(frozen=True)
class RetrievalHit:
    chunk_id: str
    source: str
    text: str
    score: float


@dataclass(frozen=True)
class HostedToolCall:
    """One scripted hosted-tool turn (not a function_call Item)."""

    type: str
    call_id: str
    status: str = "completed"


@dataclass(frozen=True)
class HostedTurn:
    kind: Literal["tool", "message"]
    call: HostedToolCall | None = None
    text: str = ""
    citations: tuple[str, ...] = ()


@dataclass(frozen=True)
class StackDecision:
    choice: StackChoice
    reason: str
    overlap: float
    own_recall: float
    can_export: bool
    can_eval: bool


def overlap_rate(own_ids: list[str], hosted_ids: list[str]) -> float:
    """Jaccard overlap of retrieved ids. Empty either side → 0.0."""
    own = set(own_ids)
    hosted = set(hosted_ids)
    if not own or not hosted:
        return 0.0
    return len(own & hosted) / len(own | hosted)


def choose_stack(
    *,
    own_recall: float,
    hosted_available: bool,
    can_export: bool,
    can_eval: bool,
    overlap: float,
) -> StackDecision:
    """Prefer the owned pipeline when you can measure it.

    hosted wins only as a prototype when you have no corpus yet.
    hybrid is for "keyword gaps the vector index misses" — not a default.
    """
    if own_recall < 0.0 or own_recall > 1.0 or overlap < 0.0 or overlap > 1.0:
        raise ValueError("rates must be in [0, 1]")
    if can_eval and own_recall >= 0.6:
        return StackDecision(
            choice="own",
            reason="owned pipeline meets recall and is eval-able in CI",
            overlap=overlap,
            own_recall=own_recall,
            can_export=can_export,
            can_eval=can_eval,
        )
    if hosted_available and not can_eval:
        return StackDecision(
            choice="hosted",
            reason="no owned eval yet; hosted is a prototype, not a CI gate",
            overlap=overlap,
            own_recall=own_recall,
            can_export=can_export,
            can_eval=can_eval,
        )
    if hosted_available and own_recall < 0.6 and overlap < 0.5:
        return StackDecision(
            choice="hybrid",
            reason="owned recall is weak and hosted hits barely overlap",
            overlap=overlap,
            own_recall=own_recall,
            can_export=can_export,
            can_eval=can_eval,
        )
    return StackDecision(
        choice="own",
        reason="keep the owned pipeline; hosted lock-in is not justified",
        overlap=overlap,
        own_recall=own_recall,
        can_export=can_export,
        can_eval=can_eval,
    )


def next_hosted_turn(step: int, question: str, hits: list[RetrievalHit]) -> HostedTurn:
    """Two-step fake: tool call, then a cited message. Cap at two steps."""
    del question
    if step < 0:
        raise ValueError("step must be >= 0")
    if step == 0:
        return HostedTurn(
            kind="tool",
            call=HostedToolCall(type="file_search_call", call_id="fs_1", status="completed"),
        )
    if step == 1:
        citations = tuple(hit.chunk_id for hit in hits[:3])
        text = hits[0].text if hits else "No hosted hits."
        return HostedTurn(kind="message", text=text, citations=citations)
    raise ValueError("hosted fake stops after the message turn")


def lock_in_flags(
    *, vendor_chunking: bool, exportable: bool, billed_separately: bool
) -> dict[str, bool]:
    return {
        "vendor_chunking": vendor_chunking,
        "exportable": exportable,
        "billed_separately": billed_separately,
        "ci_honest": exportable and not vendor_chunking,
    }


def decision_record(
    decision: StackDecision,
    *,
    flags: dict[str, bool],
) -> dict[str, object]:
    """A short ADR-shaped dict you can paste into a portfolio README."""
    return {
        "choice": decision.choice,
        "reason": decision.reason,
        "own_recall": decision.own_recall,
        "overlap": decision.overlap,
        "can_export": decision.can_export,
        "can_eval": decision.can_eval,
        "flags": dict(flags),
        "api": "responses",
        "assistants": False,
    }
