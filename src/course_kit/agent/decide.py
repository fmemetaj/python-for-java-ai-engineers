"""Workflow vs agent vs a single LLM call.

A workflow is a path *you* wrote. An agent is a loop where the *model*
picks the next tool. Official Responses function calling:
https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

from typing import Literal

Orchestration = Literal["workflow", "agent", "single_call"]


def classify_orchestration(
    *,
    steps_known: bool,
    model_picks_tools: bool,
    needs_model: bool = True,
) -> Orchestration:
    """Return which control-flow style fits the task.

    * ``single_call`` — one prompt in, one message out (classify, extract).
    * ``workflow`` — you ordered the steps (RAG: retrieve then answer).
    * ``agent`` — the model may call tools zero-to-N times based on observations.
    """
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
    """True only when the model must choose tools and the path can branch."""
    if not needs_model:
        return False
    return bool(model_picks_tools and branching and not steps_known)
