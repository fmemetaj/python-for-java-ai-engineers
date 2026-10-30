"""Behaviour over declared type."""

from __future__ import annotations


def line_count(obj: object) -> int:
    """If obj has line_count(), call it. Else if it has .lines, return len(obj.lines).

    Otherwise raise TypeError.
    """
    raise NotImplementedError


def can_stream(obj: object) -> bool:
    """True when obj has a callable read attribute."""
    raise NotImplementedError
