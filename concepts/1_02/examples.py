"""pyproject.toml holds ranges; uv.lock freezes exact versions."""

from __future__ import annotations

from pathlib import Path

root = Path(__file__).resolve().parents[2]
assert (root / "pyproject.toml").is_file()
assert (root / "uv.lock").is_file()
text = (root / "pyproject.toml").read_text(encoding="utf-8")
assert "requires-python" in text
print("1.2 examples ok")
