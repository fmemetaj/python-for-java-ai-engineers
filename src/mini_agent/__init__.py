"""Mini agent-shaped helpdesk simulation (no LLM or real send operation)."""

from .models import Ticket, ReplyProposal
from .tools import classify_ticket
from .workflow import prepare_reply, simulate_send

__all__ = ["Ticket", "ReplyProposal", "classify_ticket", "prepare_reply", "simulate_send"]
