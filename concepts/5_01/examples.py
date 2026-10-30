"""Workflow vs agent vs a single LLM call. Offline; no network."""

from __future__ import annotations

from course_kit.agent import classify_orchestration, should_use_agent

# Example 1 — one prompt, one message: not an agent.
assert (
    classify_orchestration(steps_known=True, model_picks_tools=False, needs_model=True)
    == "workflow"
)

# Example 2 — Module 4 RAG: you retrieve, then you answer.
assert (
    should_use_agent(
        steps_known=True,
        model_picks_tools=False,
        branching=False,
    )
    is False
)

# Example 3 — triage: the model may call search, spec, propose_page.
assert classify_orchestration(steps_known=False, model_picks_tools=True) == "agent"
assert (
    should_use_agent(
        steps_known=False,
        model_picks_tools=True,
        branching=True,
    )
    is True
)

# Example 4 — no model at all (pure HTTP fetch) is still a workflow.
assert classify_orchestration(steps_known=True, model_picks_tools=False, needs_model=False) == (
    "workflow"
)

# Example 5 — a classifier with no tools is a single call when the path is unknown
# but the model does not pick tools (extract an Incident JSON).
assert classify_orchestration(steps_known=False, model_picks_tools=False) == "single_call"

print("5.1 examples ok")
