"""What pytest is allowed to assert."""

from __future__ import annotations


def assert_strategy(target: str) -> str:
    """Return 'behavior' or 'forbidden' for a test target.

    Targets you will see: 'cost', 'usage_shape', 'live_wording', 'json_schema'.
    """
    raise NotImplementedError
