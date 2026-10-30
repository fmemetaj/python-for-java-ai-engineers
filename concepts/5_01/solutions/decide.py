"""Classify a task as workflow, agent, or single_call."""

from __future__ import annotations

from typing import Literal

Orchestration = Literal["workflow", "agent", "single_call"]


def classify_orchestration(
    *,
    steps_known: bool,
    model_picks_tools: bool,
    needs_model: bool = True,
) -> Orchestration:
    """Return which control-flow style fits the task."""
    if not needs_model:
        return "workflow"
    if model_picks_tools:
        return "agent"
    if steps_known:
        return "workflow"
    return "single_call"


def should_use_agent(
    *,
    steps_known: bool,
    model_picks_tools: bool,
    branching: bool,
    needs_model: bool = True,
) -> bool:
    """True only when the model must choose tools on a branching, unknown path."""
    if not needs_model:
        return False
    return bool(model_picks_tools and branching and not steps_known)
