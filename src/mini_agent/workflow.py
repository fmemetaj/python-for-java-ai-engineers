"""Agent-shaped orchestration; actions are simulated and require approval."""
import asyncio
from .models import ReplyProposal, Ticket
from .tools import classify_ticket, fake_customer_context, fake_knowledge_base_lookup

async def prepare_reply(ticket: Ticket) -> ReplyProposal:
    category = classify_ticket(ticket)
    advice, context = await asyncio.gather(fake_knowledge_base_lookup(category), fake_customer_context(ticket.id))
    return ReplyProposal(ticket_id=ticket.id, category=category, suggested_reply=f"{context}: {advice}")

def simulate_send(proposal: ReplyProposal, *, approved: bool) -> dict[str, bool | int]:
    # No network call and no real user notification, even when approved.
    return {"ticket_id": proposal.ticket_id, "sent": bool(approved)}
