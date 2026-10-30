"""*args, **kwargs, and call-site unpacking."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def join_fields(*fields: str, sep: str = ",") -> str:
    return sep.join(fields)


def with_defaults(name: str, **options: object) -> dict[str, object]:
    return {"name": name, **options}


def apply_unpacked(
    fn: Callable[..., Any], args: tuple[object, ...], kwargs: dict[str, object]
) -> object:
    return fn(*args, **kwargs)


assert join_fields("ERROR", "disk", "full") == "ERROR,disk,full"
assert join_fields("ERROR", "disk", sep="|") == "ERROR|disk"
assert with_defaults("docsdesk", timeout=5) == {"name": "docsdesk", "timeout": 5}
assert apply_unpacked(join_fields, ("a", "b"), {"sep": "-"}) == "a-b"
print("0.8 examples ok")
