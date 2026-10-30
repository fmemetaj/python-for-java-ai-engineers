"""One step of the tool-call loop: pair outputs by call_id."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any


def _is_function_call(item: Any) -> bool:
    item_type = item.get("type") if isinstance(item, dict) else getattr(item, "type", None)
    return item_type == "function_call"


def _call_id(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("call_id", ""))
    return str(getattr(item, "call_id", ""))


def _name(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("name", ""))
    return str(getattr(item, "name", ""))


def _arguments(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("arguments", "{}"))
    return str(getattr(item, "arguments", "{}"))


def loop_is_done(output_items: Sequence[Any]) -> bool:
    """True when no item is a function_call (message-only response)."""
    return not any(_is_function_call(item) for item in output_items)


def collect_outputs(
    calls: Sequence[Any],
    execute: Callable[[str, str], str],
) -> list[dict[str, str]]:
    """For each call, run execute(name, arguments) and build function_call_output items."""
    outputs: list[dict[str, str]] = []
    for call in calls:
        result = execute(_name(call), _arguments(call))
        outputs.append(
            {
                "type": "function_call_output",
                "call_id": _call_id(call),
                "output": result,
            }
        )
    return outputs


def mismatched_call_id(calls: Sequence[Any], outputs: Sequence[dict[str, str]]) -> str | None:
    """Return a call_id that has no matching output, else None."""
    seen = {item.get("call_id") for item in outputs}
    for call in calls:
        identifier = _call_id(call)
        if identifier not in seen:
            return identifier
    return None
