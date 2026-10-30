"""If it quacks, call it — no shared interface type required at runtime."""

from __future__ import annotations


class Fileish:
    def read(self) -> str:
        return "docs"


class NotAFile:
    pass


assert callable(getattr(Fileish(), "read", None))
assert not callable(getattr(NotAFile(), "read", None))
print("0.21 examples ok")
