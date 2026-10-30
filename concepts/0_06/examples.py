"""if/elif, range, match, and for/else."""

from __future__ import annotations


def label_status(code: int) -> str:
    match code:
        case 200:
            return "ok"
        case 400 | 404:
            return "client"
        case 500:
            return "server"
        case _:
            return "other"


def sum_to(n: int) -> int:
    total = 0
    for number in range(1, n + 1):
        total += number
    return total


def first_error(levels: list[str]) -> str | None:
    for level in levels:
        if level == "ERROR":
            return level
    else:
        return None


assert label_status(404) == "client"
assert sum_to(3) == 6
assert first_error(["INFO", "ERROR"]) == "ERROR"
assert first_error(["INFO"]) is None
print("0.6 examples ok")
