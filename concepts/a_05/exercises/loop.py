"""Guided: two-step fake hosted tool loop."""

from __future__ import annotations

from course_kit.hosted import HostedTurn, RetrievalHit


def first_turn(question: str, hits: list[RetrievalHit]) -> HostedTurn:
    """Step 0: a completed file_search_call."""
    raise NotImplementedError


def second_turn(question: str, hits: list[RetrievalHit]) -> HostedTurn:
    """Step 1: a message with citations from the hits."""
    raise NotImplementedError
