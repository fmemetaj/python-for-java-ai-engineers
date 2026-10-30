"""Inheritance, super(), and MRO names (solution)."""

from __future__ import annotations


class Tool:
    def tag(self) -> str:
        return "tool"


class Search(Tool):
    def tag(self) -> str:
        """Return 'search:' plus the parent tag via super()."""
        return "search:" + super().tag()


class Mixin:
    def tag(self) -> str:
        return "mixin"


class SearchWithMixin(Mixin, Search):
    pass


def mro_names(cls: type) -> list[str]:
    """Return [c.__name__ for c in cls.__mro__]."""
    return [item.__name__ for item in cls.__mro__]
