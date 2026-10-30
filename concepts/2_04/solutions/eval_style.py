"""What pytest is allowed to assert (solution)."""

from __future__ import annotations


def assert_strategy(target: str) -> str:
    """Return 'behavior' or 'forbidden' for a test target."""
    if target in {"cost", "usage_shape", "json_schema"}:
        return "behavior"
    if target == "live_wording":
        return "forbidden"
    raise ValueError(f"unknown target {target!r}")
