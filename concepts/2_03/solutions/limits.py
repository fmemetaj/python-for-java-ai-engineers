"""Derive max input and clamp requested output (solution)."""

from __future__ import annotations


def max_input_for(window: int, reserved_output: int) -> int:
    """Largest input that still leaves reserved_output room."""
    if window <= 0 or reserved_output < 0:
        raise ValueError("invalid window or reserved_output")
    return window - reserved_output


def clamp_output(requested: int, max_output: int) -> int:
    """Clip requested output into [0, max_output]."""
    if max_output < 0:
        raise ValueError("max_output must be >= 0")
    if requested < 0:
        return 0
    return min(requested, max_output)
