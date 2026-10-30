"""Allow-lists, argument validation, approval gates, and idempotency."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def is_allowed(name: str, allow: frozenset[str]) -> bool:
    """True when the tool name is on the allow-list."""
    raise NotImplementedError


def validate_search_args(payload: Mapping[str, Any]) -> str:
    """Return the query string. Reject non-str or empty query (raise ValueError)."""
    raise NotImplementedError


def run_if_approved(name: str, *, write_tools: frozenset[str], approved: bool) -> bool:
    """True when the call may proceed. Write tools require approved=True."""
    raise NotImplementedError


def call_once(cache: dict[str, str], key: str, fn: Callable[[], str]) -> str:
    """Idempotency: return the cached result for key, otherwise call fn and store it."""
    raise NotImplementedError
