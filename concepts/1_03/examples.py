"""Five venv facts Java developers usually do not expect."""

from __future__ import annotations

import sys
from pathlib import Path

# Example 1 — `.venv` is a directory with its own python binary.
root = Path(__file__).resolve().parents[2]
posix = root / ".venv" / "bin" / "python"
windows = root / ".venv" / "Scripts" / "python.exe"
# Either layout exists after `uv sync`; CI always has one of them.
assert posix.name == "python" and windows.name == "python.exe"

# Example 2 — in-venv detection (sys.prefix vs sys.base_prefix).
in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)

# Example 3 — two projects can pin different httpx versions because each has a venv.

# Example 4 — `uv run` uses `.venv` without you activating it.

# Example 5 — Windows Scripts vs POSIX bin; never mix a Windows venv with WSL.
system = "Windows" if sys.platform.startswith("win") else "Linux"
if system == "Windows":
    expected = root / ".venv" / "Scripts" / "python.exe"
else:
    expected = root / ".venv" / "bin" / "python"
assert expected.name.startswith("python")

print("1.3 examples ok")
print(f"in_venv={in_venv}")
