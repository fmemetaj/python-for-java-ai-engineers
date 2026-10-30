"""Open: cap the loop and format citations."""

from __future__ import annotations

from course_kit.hosted import HostedTurn, RetrievalHit


def run_two_steps(question: str, hits: list[RetrievalHit]) -> list[HostedTurn]:
    """[first_turn, second_turn]. Do not call step 2."""
    raise NotImplementedError


def citation_line(turn: HostedTurn) -> str:
    """'cited: id1,id2' or 'cited: none'."""
    raise NotImplementedError
