"""Allow-lists, argument validation, approval gates, and idempotency."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def is_allowed(name: str, allow: frozenset[str]) -> bool:
    """True when the tool name is on the allow-list."""
    return name in allow


def validate_search_args(payload: Mapping[str, Any]) -> str:
    """Return the query string. Reject non-str or empty query (raise ValueError)."""
    query = payload.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    return query


def run_if_approved(name: str, *, write_tools: frozenset[str], approved: bool) -> bool:
    """True when the call may proceed. Write tools require approved=True."""
    if name in write_tools and not approved:
        return False
    return True


def call_once(cache: dict[str, str], key: str, fn: Callable[[], str]) -> str:
    """Idempotency: return the cached result for key, otherwise call fn and store it."""
    if key in cache:
        return cache[key]
    result = fn()
    cache[key] = result
    return result
