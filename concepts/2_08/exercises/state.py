"""Billed input for replayed or stored chains."""

from __future__ import annotations


def billed_input(turn_sizes: list[int]) -> int:
    """Each turn pays for the running sum of prompt sizes (replay *or* stored)."""
    raise NotImplementedError
