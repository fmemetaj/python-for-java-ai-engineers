"""Collect and forward leftover arguments."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def join_fields(*fields: str, sep: str = ",") -> str:
    """Join the positional fields with sep (keyword-only after *fields)."""
    raise NotImplementedError


def with_defaults(name: str, **options: object) -> dict[str, object]:
    """Return a dict with name plus every keyword option."""
    raise NotImplementedError


def apply_unpacked(
    fn: Callable[..., Any], args: tuple[object, ...], kwargs: dict[str, object]
) -> object:
    """Call fn with the tuple unpacked positionally and the dict as keywords."""
    raise NotImplementedError
