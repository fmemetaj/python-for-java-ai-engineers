"""src layout vs Maven src/main/java."""

from __future__ import annotations

from pathlib import Path

root = Path(__file__).resolve().parents[2]
assert (root / "src" / "docsdesk" / "__init__.py").is_file()
assert (root / "src" / "docsdesk" / "client.py").is_file()
print("1.4 examples ok")
