"""Why a bill triples when you replay conversation state (solution)."""

from __future__ import annotations


def billed_input_tokens(turn_prompt_sizes: list[int], *, replay: bool) -> int:
    """Stored state is billed like replay: each turn pays for the chain so far."""
    del replay  # previous_response_id still bills prior input tokens.
    total = 0
    running = 0
    for size in turn_prompt_sizes:
        running += size
        total += running
    return total


def bill_tripled_because_replay(total_replay: int, first_turn: int) -> bool:
    """True when replaying made later turns cost more than the first prompt alone."""
    return first_turn > 0 and total_replay >= 3 * first_turn
