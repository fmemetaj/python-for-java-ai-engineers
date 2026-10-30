"""DocsDesk tools: definitions, allow-list, argument validation, approval.

Java analog: interface dispatch + Bean Validation + Spring Security.
Read-only tools run without approval. Unknown names are blocked.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from pydantic import BaseModel, ValidationError

from .client import DocsClient
from .models import GetEndpointSpecArgs, SearchDocsArgs
from .settings import Settings

READ_ONLY_TOOLS = frozenset({"search_docs", "get_endpoint_spec"})
WRITE_TOOLS = frozenset({"delete_page"})
ALLOWED_TOOLS = READ_ONLY_TOOLS

SEARCH_DOCS_TOOL: dict[str, object] = {
    "type": "function",
    "name": "search_docs",
    "description": "Search internal DocsDesk pages by keyword.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Keyword to match slug, title, or body."},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True,
}

GET_ENDPOINT_SPEC_TOOL: dict[str, object] = {
    "type": "function",
    "name": "get_endpoint_spec",
    "description": "Return the HTTP method, path, and summary for one API endpoint.",
    "parameters": {
        "type": "object",
        "properties": {
            "method": {"type": "string", "description": "HTTP method such as GET."},
            "path": {"type": "string", "description": "Path template such as /tickets/{id}."},
        },
        "required": ["method", "path"],
        "additionalProperties": False,
    },
    "strict": True,
}

TOOL_SPECS: tuple[dict[str, object], ...] = (SEARCH_DOCS_TOOL, GET_ENDPOINT_SPEC_TOOL)

_ARG_MODELS: dict[str, type[BaseModel]] = {
    "search_docs": SearchDocsArgs,
    "get_endpoint_spec": GetEndpointSpecArgs,
}


class ToolBlockedError(ValueError):
    """Raised when a tool name is not on the allow-list."""


class ApprovalRequiredError(PermissionError):
    """Raised when a write tool is invoked without an explicit approval."""


def needs_approval(name: str) -> bool:
    return name in WRITE_TOOLS


def parse_arguments(raw: str) -> dict[str, Any]:
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ValueError("tool arguments must be a JSON object")
    return loaded


def validate_args(name: str, raw: str | Mapping[str, Any]) -> BaseModel:
    model = _ARG_MODELS.get(name)
    if model is None:
        raise ToolBlockedError(f"unknown tool {name!r}")
    payload: Mapping[str, Any]
    if isinstance(raw, str):
        payload = parse_arguments(raw)
    else:
        payload = raw
    return model.model_validate(payload, strict=True)


class ToolRunner:
    """Execute allow-listed tools with validation, approval, and idempotency."""

    def __init__(
        self,
        docs: DocsClient | None = None,
        *,
        allow: frozenset[str] | None = None,
        approved: bool = False,
    ) -> None:
        self._docs = docs if docs is not None else DocsClient(Settings.offline())
        self._owns_docs = docs is None
        self._allow = allow if allow is not None else ALLOWED_TOOLS
        self.approved = approved
        self._idempotency: dict[str, str] = {}

    def close(self) -> None:
        if self._owns_docs:
            self._docs.close()

    def __enter__(self) -> ToolRunner:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def invoke(
        self,
        name: str,
        raw_args: str | Mapping[str, Any],
        *,
        idempotency_key: str | None = None,
        approved: bool | None = None,
    ) -> str:
        if name not in self._allow:
            raise ToolBlockedError(f"tool {name!r} is not allow-listed")
        gate = self.approved if approved is None else approved
        if needs_approval(name) and not gate:
            raise ApprovalRequiredError(f"tool {name!r} requires approval")
        if idempotency_key and idempotency_key in self._idempotency:
            return self._idempotency[idempotency_key]
        validated = validate_args(name, raw_args)
        result = self._dispatch(name, validated)
        if idempotency_key:
            self._idempotency[idempotency_key] = result
        return result

    def invoke_handled(self, name: str, raw_args: str) -> str:
        """Loop-safe invoke: validation failures become JSON error payloads."""
        try:
            return self.invoke(name, raw_args)
        except (
            ToolBlockedError,
            ApprovalRequiredError,
            ValidationError,
            ValueError,
            KeyError,
        ) as exc:
            return json.dumps({"error": type(exc).__name__, "detail": str(exc)})

    def _dispatch(self, name: str, args: BaseModel) -> str:
        handlers: dict[str, Callable[[BaseModel], str]] = {
            "search_docs": self._search_docs,
            "get_endpoint_spec": self._get_endpoint_spec,
        }
        handler = handlers.get(name)
        if handler is None:
            raise ToolBlockedError(f"no handler for {name!r}")
        return handler(args)

    def _search_docs(self, args: BaseModel) -> str:
        assert isinstance(args, SearchDocsArgs)
        pages = self._docs.search_pages(args.query)
        payload = [page.model_dump() for page in pages]
        return json.dumps(payload)

    def _get_endpoint_spec(self, args: BaseModel) -> str:
        assert isinstance(args, GetEndpointSpecArgs)
        spec = self._docs.get_endpoint_spec(args.method, args.path)
        return spec.model_dump_json()
