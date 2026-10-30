"""Multi-turn DocsDesk session: pasted doc in, tokens and USD out.

Default client is FakeLLM (Responses-shaped). `previous_response_id` still
bills prior input tokens — server-side state is not free context.
https://platform.openai.com/docs/guides/migrate-to-responses
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from course_kit.cost import cost_usd, format_cost
from course_kit.llm import FakeLLM, LLMResponse, Usage, get_client

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "answer_from_doc.v1.txt"
PROMPT_VERSION = "answer_from_doc.v1"


def load_instructions(path: Path | None = None) -> str:
    prompt_path = path if path is not None else PROMPT_FILE
    return prompt_path.read_text(encoding="utf-8").strip()


@dataclass(frozen=True)
class Turn:
    question: str
    answer: str
    usage: Usage
    cost: float
    response_id: str
    prompt_version: str = PROMPT_VERSION

    def summary(self) -> str:
        return (
            f"{self.answer}\n"
            f"[tokens in={self.usage.input_tokens} out={self.usage.output_tokens} "
            f"cached={self.usage.cached_tokens} | {format_cost(self.cost)} | "
            f"prompt={self.prompt_version}]"
        )


class DeskSession:
    """Keep a multi-turn session over one pasted document. Offline by default."""

    def __init__(
        self,
        document: str,
        *,
        client: FakeLLM | None = None,
        model: str = "gpt-4.1-mini",
        store: bool = True,
    ) -> None:
        self.document = document
        self.model = model
        self.store = store
        self.prompt_version = PROMPT_VERSION
        self.instructions = load_instructions()
        self._client = client if client is not None else FakeLLM()
        self.turns: list[Turn] = []
        self._previous_id: str | None = None

    def ask(self, question: str) -> Turn:
        prompt = f"Document:\n{self.document}\n\nQuestion: {question}"
        response: LLMResponse = self._client.complete(
            prompt,
            instructions=self.instructions,
            previous_response_id=self._previous_id,
            store=self.store,
            model=self.model,
        )
        amount = cost_usd(response.usage, self.model)
        turn = Turn(
            question=question,
            answer=response.output_text,
            usage=response.usage,
            cost=amount,
            response_id=response.id,
        )
        self.turns.append(turn)
        if self.store:
            self._previous_id = response.id
        return turn


def default_session(document: str) -> DeskSession:
    """Build a session using `get_client()` so LLM_PROVIDER=fake stays the default."""
    client = get_client()
    if not isinstance(client, FakeLLM):
        raise RuntimeError("DocsDesk Module 2 graded path requires LLM_PROVIDER=fake")
    return DeskSession(document, client=client)
