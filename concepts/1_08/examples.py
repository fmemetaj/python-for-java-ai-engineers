"""pytest: plain assert, fixtures by name, parametrize."""

from __future__ import annotations

cases = [("auth",), ("tickets",)]
assert cases[0][0] == "auth"
print("1.8 examples ok")
