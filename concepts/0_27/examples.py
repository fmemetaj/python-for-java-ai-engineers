"""A file is a module; import looks on sys.path (uv run sets this up)."""

from __future__ import annotations

import mini_agent
from mini_agent.models import Ticket


assert mini_agent.__name__ == "mini_agent"
assert Ticket(id=1, subject="Help", body="Please").id == 1
print("0.27 examples ok")
