"""A tiny agent loop: status, cap, approval. You implement the machine."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

Status = Literal["done", "capped", "denied"]


def next_status(has_tool_call: bool, *, step: int, max_steps: int) -> Status | Literal["tool"]:
    """Return 'done', 'capped', or 'tool' for the next action."""
    if not has_tool_call:
        return "done"
    if step >= max_steps:
        return "capped"
    return "tool"


def should_stop(status: str) -> bool:
    """True for terminal statuses."""
    return status in {"done", "capped", "denied"}


def run_capped_loop(
    complete: Callable[[], Any],
    execute: Callable[[str, str], str],
    *,
    max_steps: int,
    write_tools: frozenset[str] | None = None,
    approved: bool = False,
) -> dict[str, Any]:
    """Run complete() until done, capped, or denied."""
    writes = write_tools if write_tools is not None else frozenset()
    names: list[str] = []
    text = ""
    step = 0
    while step < max_steps:
        step += 1
        response = complete()
        text = getattr(response, "output_text", "") or ""
        calls = list(getattr(response, "function_calls", ()) or ())
        if not calls:
            return {"status": "done", "steps": step, "tool_names": names, "output_text": text}
        for call in calls:
            name = str(getattr(call, "name", ""))
            arguments = str(getattr(call, "arguments", "{}"))
            names.append(name)
            if name in writes and not approved:
                return {
                    "status": "denied",
                    "steps": step,
                    "tool_names": names,
                    "output_text": "",
                }
            execute(name, arguments)
    return {"status": "capped", "steps": step, "tool_names": names, "output_text": text}
