"""Drop citations that were not retrieved."""

from __future__ import annotations

from collections.abc import Sequence


def cite_only_retrieved(proposed_ids: Sequence[str], retrieved_ids: Sequence[str]) -> list[str]:
    """Return proposed ids that appear in retrieved_ids, preserving proposed order."""
    raise NotImplementedError
