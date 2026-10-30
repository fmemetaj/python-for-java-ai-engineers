"""Derive max input and clamp requested output."""

from __future__ import annotations


def max_input_for(window: int, reserved_output: int) -> int:
    """Largest input that still leaves reserved_output room."""
    raise NotImplementedError


def clamp_output(requested: int, max_output: int) -> int:
    """Clip requested output into [0, max_output]."""
    raise NotImplementedError
