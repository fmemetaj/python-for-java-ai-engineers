"""Threads overlap waits; they do not multiply CPU cores for Python bytecode."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor


def label(item: str) -> str:
    return item.upper()


with ThreadPoolExecutor(max_workers=2) as pool:
    out = list(pool.map(label, ["a", "b", "c"]))
assert out == ["A", "B", "C"]
print("0.28 examples ok")
