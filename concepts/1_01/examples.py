"""uv is SDKMAN + Maven in one tool."""

from __future__ import annotations

import sys
from pathlib import Path

COMMANDS = {
    "install-python": "uv python install",
    "sync-locked": "uv sync --locked",
    "run-tests": "uv run pytest",
    "run-script": "uv run python",
}

assert COMMANDS["sync-locked"] == "uv sync --locked"
root = Path(__file__).resolve().parents[2]
assert (root / "pyproject.toml").is_file()
assert sys.executable
print("1.1 examples ok")
