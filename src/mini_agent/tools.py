"""Deterministic classification and fake asynchronous tool."""

import asyncio

from .models import Ticket
from .registry import ToolRegistry

registry = ToolRegistry()


def classify_ticket(ticket: Ticket) -> str:
    content = f"{ticket.subject} {ticket.body}".lower()
    if any(x in content for x in ("login", "log in", "sign in", "password", "account access")):
        return "access"
    if any(x in content for x in ("invoice", "billing", "payment")):
        return "billing"
    return "general"


async def fake_knowledge_base_lookup(category: str) -> str:
    await asyncio.sleep(0.01)
    return {
        "access": "Try resetting your password.",
        "billing": "Please check your billing portal.",
        "general": "Our team will review your request.",
    }[category]


async def fake_customer_context(ticket_id: int) -> str:
    await asyncio.sleep(0.01)
    return f"Ticket #{ticket_id}"


@registry.register("classify")
def classify_payload(payload: str) -> str:
    """Sync Tool-protocol wrapper around :func:`classify_ticket`."""
    subject = payload[:80] if len(payload) >= 2 else "na"
    body = payload if len(payload) >= 3 else "n/a"
    return classify_ticket(Ticket(id=1, subject=subject, body=body))


@registry.register("kb_hint")
def kb_hint(category: str) -> str:
    """Sync excerpt of the fake knowledge-base lookup (no I/O)."""
    return {
        "access": "Try resetting your password.",
        "billing": "Please check your billing portal.",
        "general": "Our team will review your request.",
    }.get(category, "Our team will review your request.")
