"""Agent-shaped orchestration; approval is simulated without sending a message."""

import asyncio

from .models import ReplyProposal, Ticket
from .tools import classify_ticket, fake_customer_context, fake_knowledge_base_lookup


async def prepare_reply(ticket: Ticket) -> ReplyProposal:
    category = classify_ticket(ticket)
    advice, context = await asyncio.gather(
        fake_knowledge_base_lookup(category), fake_customer_context(ticket.id)
    )
    return ReplyProposal(
        ticket_id=ticket.id,
        category=category,
        suggested_reply=f"{context}: {advice}",
    )


def simulate_send(proposal: ReplyProposal, *, approved: bool) -> dict[str, bool | int]:
    """Pure in-memory exercise; 'would_send' is hypothetical, not a delivery receipt."""
    return {
        "ticket_id": proposal.ticket_id,
        "approved": bool(approved),
        "would_send": bool(approved),
    }
