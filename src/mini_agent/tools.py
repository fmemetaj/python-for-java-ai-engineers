"""Deterministic classification and fake asynchronous tool."""
import asyncio
from .models import Ticket

def classify_ticket(ticket: Ticket) -> str:
    content = f"{ticket.subject} {ticket.body}".lower()
    if any(x in content for x in ("login", "log in", "sign in", "password", "account access")):
        return "access"
    if any(x in content for x in ("invoice", "billing", "payment")):
        return "billing"
    return "general"

async def fake_knowledge_base_lookup(category: str) -> str:
    await asyncio.sleep(0.01)
    return {"access": "Try resetting your password.", "billing": "Please check your billing portal.", "general": "Our team will review your request."}[category]

async def fake_customer_context(ticket_id: int) -> str:
    await asyncio.sleep(0.01)
    return f"Ticket #{ticket_id}"
