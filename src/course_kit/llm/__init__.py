"""Offline-first LLM client switch (Java analogy: interface + Spring profiles).

Default provider is `fake`. Live OpenAI is optional and uses the current
Responses API (`client.responses.create`), never the sunset Assistants API.
"""

from .base import (
    ChatChoice,
    ChatCompletion,
    ChatMessage,
    ChatUsage,
    FunctionCall,
    LLMClient,
    LLMResponse,
    OutputItem,
    OutputMessage,
    OutputText,
    ReasoningItem,
    StreamEvent,
    Usage,
)
from .context import remaining_budget, trim_oldest, would_overflow
from .factory import chat_completions_create_kwargs, get_client, responses_create_kwargs
from .fake import FakeLLM
from .migrate import migrate_chat_body_to_responses
from .schema import (
    chat_response_format,
    function_call_output,
    json_schema_from_model,
    responses_text_format,
)
from .tokens import estimate_tokens

__all__ = [
    "ChatChoice",
    "ChatCompletion",
    "ChatMessage",
    "ChatUsage",
    "FakeLLM",
    "FunctionCall",
    "LLMClient",
    "LLMResponse",
    "OutputItem",
    "OutputMessage",
    "OutputText",
    "ReasoningItem",
    "StreamEvent",
    "Usage",
    "chat_completions_create_kwargs",
    "chat_response_format",
    "estimate_tokens",
    "function_call_output",
    "get_client",
    "json_schema_from_model",
    "migrate_chat_body_to_responses",
    "remaining_budget",
    "responses_create_kwargs",
    "responses_text_format",
    "trim_oldest",
    "would_overflow",
]
