"""DocsDesk ticket object. Fill in the bodies."""

from __future__ import annotations


class Ticket:
    def __init__(self, ticket_id: int, subject: str) -> None:
        """Store ticket_id and subject on the instance."""
        raise NotImplementedError

    def label(self) -> str:
        """Return '#<id> <subject>'."""
        raise NotImplementedError


def make_ticket(ticket_id: int, subject: str) -> Ticket:
    """Construct a Ticket."""
    raise NotImplementedError


def is_private_name(name: str) -> bool:
    """True for a single-underscore alias (_cache), False for dunder (__init__)."""
    raise NotImplementedError
