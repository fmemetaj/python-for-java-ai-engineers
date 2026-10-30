"""@deco is deco(fn) — a real call, not metadata."""

from __future__ import annotations

from functools import wraps


def banner(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return f"[{fn(*args, **kwargs)}]"

    return wrapped


@banner
def greet() -> str:
    return "DocsDesk"


assert greet() == "[DocsDesk]"
assert greet.__name__ == "greet"
print("0.26 examples ok")
