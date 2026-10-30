"""DocsDesk — a docs HTTP client that grows module by module.

Module 1: settings, redacting logs, httpx + retries, Pydantic JSON, fake LLM.
Module 2: answer from a pasted doc, print tokens and USD, multi-turn session.
Everything essential runs offline (`LLM_PROVIDER=fake`, fixture HTTP transport).
"""

from .client import DocsClient
from .logging_setup import RedactingFilter, configure_logging
from .models import DocPage
from .session import DeskSession, Turn, default_session, load_instructions
from .settings import Settings

__all__ = [
    "DeskSession",
    "DocPage",
    "DocsClient",
    "RedactingFilter",
    "Settings",
    "Turn",
    "configure_logging",
    "default_session",
    "load_instructions",
]
