"""Billed input for replayed or stored chains (solution)."""

from __future__ import annotations


def billed_input(turn_sizes: list[int]) -> int:
    """Each turn pays for the running sum of prompt sizes (replay *or* stored)."""
    total = 0
    running = 0
    for size in turn_sizes:
        running += size
        total += running
    return total
