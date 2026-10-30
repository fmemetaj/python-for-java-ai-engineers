"""Mini agent-shaped helpdesk simulation (no LLM or real send operation)."""

from .models import Ticket, ReplyProposal
from .registry import FunctionTool, Tool, ToolRegistry
from .tools import classify_ticket, registry
from .workflow import prepare_reply, simulate_send

__all__ = [
    "Ticket",
    "ReplyProposal",
    "FunctionTool",
    "Tool",
    "ToolRegistry",
    "classify_ticket",
    "prepare_reply",
    "registry",
    "simulate_send",
]
