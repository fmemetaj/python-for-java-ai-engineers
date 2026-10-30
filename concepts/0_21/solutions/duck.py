"""Behaviour over declared type (solution)."""

from __future__ import annotations


def line_count(obj: object) -> int:
    """If obj has line_count(), call it. Else if it has .lines, return len(obj.lines).

    Otherwise raise TypeError.
    """
    count = getattr(obj, "line_count", None)
    if callable(count):
        result = count()
        if not isinstance(result, int):
            raise TypeError("line_count() must return int")
        return result
    lines = getattr(obj, "lines", None)
    if lines is not None:
        return len(lines)
    raise TypeError(f"{type(obj).__name__} has no line_count() or lines")


def can_stream(obj: object) -> bool:
    """True when obj has a callable read attribute."""
    read = getattr(obj, "read", None)
    return callable(read)
