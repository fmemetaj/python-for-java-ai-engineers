"""Truthiness: empty/zero/None are falsy; non-empty strings are not."""

from __future__ import annotations


def keep_truthy(values: list[object]) -> list[object]:
    return [value for value in values if value]


def first_present(*values: object) -> object | None:
    for value in values:
        if value:
            return value
    return None


assert keep_truthy([0, "", "ok", [], {"id": 1}, None, "0"]) == ["ok", {"id": 1}, "0"]
assert first_present(None, "", 0, "ready") == "ready"
assert first_present(None, "", 0) is None
assert bool("0") is True
assert bool([]) is False

print("0.5 examples ok")
