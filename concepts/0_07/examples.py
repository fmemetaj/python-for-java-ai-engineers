"""Defaults, keyword arguments, and the mutable-default trap."""

from __future__ import annotations


def greet(name: str, prefix: str = "Hello") -> str:
    return f"{prefix}, {name}"


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    collected = [] if tags is None else list(tags)
    collected.append(tag)
    return collected


def broken_add_tag(tag: str, tags: list[str] = []) -> list[str]:
    tags.append(tag)
    return tags


assert greet("Ada") == "Hello, Ada"
assert greet("Ada", prefix="Hi") == "Hi, Ada"
assert add_tag("login") == ["login"]
assert add_tag("billing") == ["billing"]
assert add_tag("api", ["login"]) == ["login", "api"]
first = broken_add_tag("a")
second = broken_add_tag("b")
assert first is second
assert second == ["a", "b"]
print("0.7 examples ok")
