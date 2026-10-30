"""DocsDesk ticket object (solution)."""

from __future__ import annotations


class Ticket:
    def __init__(self, ticket_id: int, subject: str) -> None:
        """Store ticket_id and subject on the instance."""
        self.ticket_id = ticket_id
        self.subject = subject

    def label(self) -> str:
        """Return '#<id> <subject>'."""
        return f"#{self.ticket_id} {self.subject}"


def make_ticket(ticket_id: int, subject: str) -> Ticket:
    """Construct a Ticket."""
    return Ticket(ticket_id, subject)


def is_private_name(name: str) -> bool:
    """True for a single-underscore alias (_cache), False for dunder (__init__)."""
    return name.startswith("_") and not name.startswith("__")
