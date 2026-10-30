"""A tiny agent loop: status, cap, approval. You implement the machine."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

Status = Literal["done", "capped", "denied"]


def next_status(has_tool_call: bool, *, step: int, max_steps: int) -> Status | Literal["tool"]:
    """Return 'done', 'capped', or 'tool' for the next action."""
    raise NotImplementedError


def should_stop(status: str) -> bool:
    """True for terminal statuses."""
    raise NotImplementedError


def run_capped_loop(
    complete: Callable[[], Any],
    execute: Callable[[str, str], str],
    *,
    max_steps: int,
    write_tools: frozenset[str] | None = None,
    approved: bool = False,
) -> dict[str, Any]:
    """Run complete() until done, capped, or denied.

    ``complete()`` returns an object with ``.function_calls`` (each having
    ``.name``, ``.arguments``, ``.call_id``) and ``.output_text``.
    """
    raise NotImplementedError
