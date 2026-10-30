"""Open: build the ADR-shaped dict. assistants must be False."""

from __future__ import annotations

from course_kit.hosted import StackDecision, decision_record


def make_record(decision: StackDecision, flags: dict[str, bool]) -> dict[str, object]:
    """choice, reason, rates, flags, api=responses, assistants=False."""
    return decision_record(decision, flags=flags)
