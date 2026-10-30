"""Guided: two-step fake hosted tool loop."""

from __future__ import annotations

from course_kit.hosted import HostedTurn, RetrievalHit, next_hosted_turn


def first_turn(question: str, hits: list[RetrievalHit]) -> HostedTurn:
    """Step 0: a completed file_search_call."""
    return next_hosted_turn(0, question, hits)


def second_turn(question: str, hits: list[RetrievalHit]) -> HostedTurn:
    """Step 1: a message with citations from the hits."""
    return next_hosted_turn(1, question, hits)
