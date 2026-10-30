"""Offline-first LLM client switch (Java analogy: interface + Spring profiles).

Default provider is `fake`. Live OpenAI is optional and uses the current
Responses API (`client.responses.create`), never the sunset Assistants API.
"""

from .base import LLMClient, LLMResponse, Usage
from .factory import get_client, responses_create_kwargs
from .fake import FakeLLM

__all__ = [
    "FakeLLM",
    "LLMClient",
    "LLMResponse",
    "Usage",
    "get_client",
    "responses_create_kwargs",
]
