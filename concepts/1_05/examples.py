"""ruff is Checkstyle/Spotless; pyright is javac-for-hints, not runtime."""

from __future__ import annotations

assert True  # pyright would flag `count: int = "1"`; the interpreter would not
print("1.5 examples ok")
