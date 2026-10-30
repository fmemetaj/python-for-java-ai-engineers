"""Built-in types: equality, identity, None, unbounded int."""

from __future__ import annotations


def same_identity(left: object, right: object) -> bool:
    return left is right


def same_value(left: object, right: object) -> bool:
    return left == right


def none_label(value: object) -> str:
    return "missing" if value is None else "present"


assert same_value("DocsDesk", "DocsDesk") is True
assert same_identity(None, None) is True
assert none_label(None) == "missing"
assert none_label("") == "present"
assert (10**100).bit_length() > 64
one = 1
assert int(True) == one
assert True is not one

print("0.4 examples ok")
