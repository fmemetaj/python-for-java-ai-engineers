"""`with` always runs teardown — that is the point."""

from __future__ import annotations

from contextlib import contextmanager


@contextmanager
def flag():
    state = {"open": True}
    try:
        yield state
    finally:
        state["open"] = False


with flag() as seen:
    assert seen["open"] is True
assert seen["open"] is False
print("0.25 examples ok")
