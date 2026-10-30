"""No checked exceptions. Chain with `raise ... from`."""

from __future__ import annotations


class ParseError(Exception):
    pass


def parse_level(line: str) -> str:
    if not line.strip():
        raise ParseError("empty")
    return line.split()[0]


try:
    parse_level("")
except ParseError as exc:
    chained = ValueError("bad log")
    chained.__cause__ = exc
    assert chained.__cause__ is exc
print("0.24 examples ok")
