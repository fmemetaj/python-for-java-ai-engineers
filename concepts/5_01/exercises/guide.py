"""Reasons not to wrap a known pipeline in an agent loop."""

from __future__ import annotations


def reasons_not_to_use_agent(*, steps_known: bool, model_picks_tools: bool) -> list[str]:
    """Return the applicable reasons from a small allow-list of strings."""
    raise NotImplementedError
