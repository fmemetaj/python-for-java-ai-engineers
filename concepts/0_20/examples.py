"""super() follows the MRO, not 'the superclass' in the Java sense."""

from __future__ import annotations


class Tool:
    def tag(self) -> str:
        return "tool"


class Search(Tool):
    def tag(self) -> str:
        return "search:" + super().tag()


assert Search().tag() == "search:tool"
assert Search.__mro__[0].__name__ == "Search"
print("0.20 examples ok")
