"""Why a bill triples when you replay conversation state."""

from __future__ import annotations


def billed_input_tokens(turn_prompt_sizes: list[int], *, replay: bool) -> int:
    """If replay, each turn resends the sum of all prompts so far.

    turn_prompt_sizes is the *new* user text on each turn (tokens).
    Replay billed input on turn i is sum(sizes[:i+1]); total billed is the sum of those.
    If not replay (impossible-free stored state — still billed the same per official docs),
    return the same total: stored state is not a discount.
    """
    raise NotImplementedError


def bill_tripled_because_replay(total_replay: int, first_turn: int) -> bool:
    """True when replaying made later turns cost more than the first prompt alone."""
    raise NotImplementedError
