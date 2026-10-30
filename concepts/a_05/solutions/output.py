"""Open: cap the loop and format citations."""

from __future__ import annotations

from course_kit.hosted import HostedTurn, RetrievalHit, next_hosted_turn


def run_two_steps(question: str, hits: list[RetrievalHit]) -> list[HostedTurn]:
    """[first_turn, second_turn]. Do not call step 2."""
    return [next_hosted_turn(0, question, hits), next_hosted_turn(1, question, hits)]


def citation_line(turn: HostedTurn) -> str:
    """'cited: id1,id2' or 'cited: none'."""
    if not turn.citations:
        return "cited: none"
    return "cited: " + ",".join(turn.citations)
