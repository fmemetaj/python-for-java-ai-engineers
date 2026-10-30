"""Classes bind names on an instance; there is no private keyword."""

from __future__ import annotations


class Ticket:
    def __init__(self, ticket_id: int, subject: str) -> None:
        self.ticket_id = ticket_id
        self.subject = subject
        self._cache: str | None = None

    def label(self) -> str:
        return f"#{self.ticket_id} {self.subject}"


t = Ticket(1, "Login")
assert t.label() == "#1 Login"
assert t._cache is None  # convention, not enforcement
print("0.16 examples ok")
