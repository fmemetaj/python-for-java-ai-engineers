"""Reasons not to wrap a known pipeline in an agent loop."""

from __future__ import annotations

KNOWN_PIPELINE = "known_pipeline"
NO_TOOL_CHOICE = "model_does_not_pick_tools"
COST = "extra_tool_rounds_cost_tokens"


def reasons_not_to_use_agent(*, steps_known: bool, model_picks_tools: bool) -> list[str]:
    """Return the applicable reasons from a small allow-list of strings."""
    reasons: list[str] = []
    if steps_known:
        reasons.append(KNOWN_PIPELINE)
    if not model_picks_tools:
        reasons.append(NO_TOOL_CHOICE)
    if steps_known or not model_picks_tools:
        reasons.append(COST)
    return reasons
