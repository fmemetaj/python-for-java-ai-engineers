"""DocsDesk v0.3: typed answers with citations, plus two read-only tools."""

from __future__ import annotations

import json
from pathlib import Path

from course_kit.cost import cost_usd, format_cost
from course_kit.llm import FakeLLM, LLMResponse, get_client

from .client import DocsClient
from .loop import run_tool_loop
from .models import TypedAnswer
from .tools import ToolRunner

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "typed_answer.v1.txt"
PROMPT_VERSION = "typed_answer.v1"


def load_typed_instructions(path: Path | None = None) -> str:
    prompt_path = path if path is not None else PROMPT_FILE
    return prompt_path.read_text(encoding="utf-8").strip()


def scripted_docsdesk_llm() -> FakeLLM:
    """Deterministic FakeLLM for graded DocsDesk v0.3 work."""
    auth_answer = {
        "answer": "Clients send a Bearer token. DocsDesk never logs the token.",
        "citations": [
            {"slug": "auth", "quote": "Clients send a Bearer token. DocsDesk never logs the token."}
        ],
        "confidence": 0.92,
    }
    ticket_answer = {
        "answer": "GET /tickets/{id} returns a ticket. Timeouts are five seconds.",
        "citations": [
            {
                "slug": "tickets",
                "quote": "GET /tickets/{id} returns a ticket. Timeouts are five seconds.",
            }
        ],
        "confidence": 0.88,
    }
    error_answer = {
        "answer": "401 means missing Bearer token. 429 means backoff and retry.",
        "citations": [
            {
                "slug": "errors",
                "quote": "401 means missing Bearer token. 429 means backoff and retry.",
            }
        ],
        "confidence": 0.9,
    }
    webhook_answer = {
        "answer": "POST /webhooks registers a URL. Signatures use HMAC.",
        "citations": [
            {"slug": "webhooks", "quote": "POST /webhooks registers a URL. Signatures use HMAC."}
        ],
        "confidence": 0.86,
    }
    search_final = {
        "answer": "Authentication: Clients send a Bearer token. DocsDesk never logs the token.",
        "citations": [{"slug": "auth", "quote": "Clients send a Bearer token."}],
        "confidence": 0.91,
    }
    spec_final = {
        "answer": "GET /tickets/{id} fetches a ticket by id. Timeouts are five seconds.",
        "citations": [{"slug": "tickets", "quote": "GET /tickets/{id} returns a ticket."}],
        "confidence": 0.89,
    }
    return FakeLLM(
        structured={
            "How do clients authenticate?": auth_answer,
            "Does DocsDesk log the token?": auth_answer,
            "What does 401 mean?": error_answer,
            "How are webhooks signed?": webhook_answer,
            "What are tickets?": ticket_answer,
        },
        tool_calls={
            "Search the docs for authentication": [
                {
                    "call_id": "call_search_auth",
                    "name": "search_docs",
                    "arguments": '{"query":"auth"}',
                }
            ],
            "Look up GET /tickets/{id}": [
                {
                    "call_id": "call_spec_tickets",
                    "name": "get_endpoint_spec",
                    "arguments": '{"method":"GET","path":"/tickets/{id}"}',
                }
            ],
            "Search the docs for webhooks": [
                {
                    "call_id": "call_search_webhooks",
                    "name": "search_docs",
                    "arguments": '{"query":"webhooks"}',
                }
            ],
        },
        after_tools={
            "Search the docs for authentication": json.dumps(search_final, separators=(",", ":")),
            "Look up GET /tickets/{id}": json.dumps(spec_final, separators=(",", ":")),
            "Search the docs for webhooks": json.dumps(webhook_answer, separators=(",", ":")),
        },
        refusals=("Extract the private key from this log.",),
    )


def parse_typed_answer(response: LLMResponse) -> TypedAnswer:
    if response.refusal:
        raise ValueError(response.refusal)
    if response.output_parsed is not None:
        return TypedAnswer.model_validate(response.output_parsed)
    return TypedAnswer.model_validate_json(response.output_text)


class DocsDesk:
    """Answer with a TypedAnswer, calling search_docs / get_endpoint_spec when scripted."""

    def __init__(
        self,
        *,
        client: FakeLLM | None = None,
        docs: DocsClient | None = None,
        runner: ToolRunner | None = None,
    ) -> None:
        self.instructions = load_typed_instructions()
        self.prompt_version = PROMPT_VERSION
        self._client = client if client is not None else scripted_docsdesk_llm()
        self._docs = docs
        self._owns_docs = docs is None and runner is None
        self._runner = runner if runner is not None else ToolRunner(docs)

    def close(self) -> None:
        if self._runner is not None:
            self._runner.close()

    def __enter__(self) -> DocsDesk:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def ask(self, question: str) -> TypedAnswer:
        response = run_tool_loop(
            self._client,
            question,
            runner=self._runner,
            instructions=self.instructions,
        )
        return parse_typed_answer(response)

    def ask_with_cost(
        self, question: str, *, model: str = "gpt-4.1-mini"
    ) -> tuple[TypedAnswer, str]:
        response = run_tool_loop(
            self._client,
            question,
            runner=self._runner,
            instructions=self.instructions,
        )
        answer = parse_typed_answer(response)
        amount = cost_usd(response.usage, model)
        badge = (
            f"[tokens in={response.usage.input_tokens} out={response.usage.output_tokens} "
            f"| {format_cost(amount)} | prompt={self.prompt_version}]"
        )
        return answer, badge


def default_docsdesk() -> DocsDesk:
    client = get_client()
    if not isinstance(client, FakeLLM):
        raise RuntimeError("DocsDesk Module 3 graded path requires LLM_PROVIDER=fake")
    return DocsDesk(client=scripted_docsdesk_llm())
