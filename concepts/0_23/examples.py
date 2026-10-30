"""Hints are not javac. Pydantic (0.19) is what validates at the boundary."""

from __future__ import annotations


def double(n: int) -> int:
    return n + n


assert double(2) == 4
# This call is a type error for pyright, but the interpreter still runs it:
assert double("ab") == "abab"  # type: ignore[arg-type]
print("0.23 examples ok")
