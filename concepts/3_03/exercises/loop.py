"""One step of the tool-call loop: pair outputs by call_id."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def loop_is_done(output_items: Sequence[Any]) -> bool:
    """True when no item is a function_call (message-only response)."""
    raise NotImplementedError


def collect_outputs(
    calls: Sequence[Any],
    execute: Callable[[str, str], str],
) -> list[dict[str, str]]:
    """For each call, run execute(name, arguments) and build function_call_output items."""
    raise NotImplementedError


def mismatched_call_id(calls: Sequence[Any], outputs: Sequence[dict[str, str]]) -> str | None:
    """Return a call_id that has no matching output, else None."""
    raise NotImplementedError
