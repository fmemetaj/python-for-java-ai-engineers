"""Retrieve → assemble context → answer with citations (DocsDesk v0.4).

Offline: FakeEmbedder + precomputed fixture vectors + scripted FakeLLM.
Generation uses Responses-shaped FakeLLM.complete, never Assistants.
"""

from __future__ import annotations

from pathlib import Path

from course_kit.loader import repo_root
from course_kit.llm import FakeLLM, LLMResponse
from course_kit.rag import FakeEmbedder, VectorIndex, hybrid_search
from course_kit.rag.embeddings import DEFAULT_DIM

from .corpus import load_corpus_chunks
from .models import RagAnswer, RagCitation

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "rag_answer.v1.txt"
PROMPT_VERSION = "rag_answer.v1"
EMBEDDING_FIXTURE = Path("data") / "embeddings" / "payments-api.json"


def load_rag_instructions(path: Path | None = None) -> str:
    prompt_path = path if path is not None else PROMPT_FILE
    return prompt_path.read_text(encoding="utf-8").strip()


def assemble_context(hits: list[dict[str, object]], *, budget: int = 1800) -> str:
    """Join retrieved chunks as labeled blocks until the character budget."""
    parts: list[str] = []
    used = 0
    for hit in hits:
        chunk_id = str(hit.get("chunk_id", ""))
        text = str(hit.get("text", "")).strip()
        block = f"[{chunk_id}]\n{text}"
        if used + len(block) + 2 > budget and parts:
            break
        parts.append(block)
        used += len(block) + 2
    return "\n\n".join(parts)


def citations_from_hits(hits: list[dict[str, object]], *, quote_len: int = 80) -> list[RagCitation]:
    out: list[RagCitation] = []
    for hit in hits:
        text = str(hit.get("text", "")).strip()
        quote = text[:quote_len].rstrip()
        if not quote:
            continue
        out.append(
            RagCitation(
                chunk_id=str(hit["chunk_id"]),
                path=str(hit.get("path", "")),
                quote=quote,
            )
        )
    return out


def scripted_rag_answers() -> dict[str, dict[str, object]]:
    """Deterministic answers keyed by question. Citations filled at ask time."""
    return {
        "How do clients authenticate?": {
            "answer": "Clients send Authorization: Bearer <jwt>. The JWT is HS256-signed.",
        },
        "How do I create a payment?": {
            "answer": "POST /payments with amountCents, currency, and an Idempotency-Key header.",
        },
        "How do I refund a captured payment?": {
            "answer": "POST /payments/{id}/refunds. Only captured payments can be refunded.",
        },
        "How are webhook signatures verified?": {
            "answer": "Verify X-Signature with HMAC-SHA256 over the raw body.",
        },
        "What does HTTP 409 mean?": {
            "answer": "409 Conflict: refund of a payment that is not captured, or a conflicting idempotency key.",
        },
        "Which Spring annotation maps POST /payments?": {
            "answer": "@PostMapping on PaymentController.create maps POST /payments.",
        },
        "What header carries the JWT?": {
            "answer": "The Authorization header carries the Bearer JWT.",
        },
        "What is the Idempotency-Key header for?": {
            "answer": "Repeat the same Idempotency-Key on POST /payments to retry without charging twice.",
        },
        "Are partial refunds allowed?": {
            "answer": "Yes. Partial refunds are allowed while remaining captured cents are greater than zero.",
        },
        "Which HMAC algorithm signs webhooks?": {
            "answer": "HMAC-SHA256. Reject the event if the hex digest does not match.",
        },
    }


def load_payments_index(
    *,
    fixture: Path | None = None,
    embedder: FakeEmbedder | None = None,
) -> VectorIndex:
    """Prefer committed fixture vectors; rebuild with FakeEmbedder if missing."""
    path = fixture if fixture is not None else repo_root() / EMBEDDING_FIXTURE
    if path.is_file():
        return VectorIndex.load(path)
    hasher = embedder if embedder is not None else FakeEmbedder(dim=DEFAULT_DIM)
    chunks = load_corpus_chunks()
    return VectorIndex.from_chunks(chunks, embedder=hasher)


class RagDesk:
    """DocsDesk retrieval-augmented answering over the payments-api corpus."""

    def __init__(
        self,
        *,
        index: VectorIndex | None = None,
        embedder: FakeEmbedder | None = None,
        client: FakeLLM | None = None,
        k: int = 5,
        hybrid: bool = True,
    ) -> None:
        self.embedder = embedder if embedder is not None else FakeEmbedder()
        self.index = index if index is not None else load_payments_index(embedder=self.embedder)
        self.k = k
        self.hybrid = hybrid
        self.instructions = load_rag_instructions()
        self.prompt_version = PROMPT_VERSION
        self._scripts = scripted_rag_answers()
        self._client = (
            client
            if client is not None
            else FakeLLM(structured={key: dict(value) for key, value in self._scripts.items()})
        )

    def retrieve(self, question: str, *, k: int | None = None) -> list[dict[str, object]]:
        take = k if k is not None else self.k
        vector = self.embedder.embed(question)
        if self.hybrid:
            return hybrid_search(question, self.index, vector, k=take)
        return self.index.search(vector, k=take)

    def ask(self, question: str) -> RagAnswer:
        hits = self.retrieve(question)
        context = assemble_context(hits)
        response = self._client.complete(
            question,
            instructions=f"{self.instructions}\n\n{context}",
        )
        return self._parse(question, response, hits)

    def _parse(
        self, question: str, response: LLMResponse, hits: list[dict[str, object]]
    ) -> RagAnswer:
        cites = citations_from_hits(hits[:2])
        if response.output_parsed is not None and "answer" in response.output_parsed:
            answer_text = str(response.output_parsed["answer"])
            return RagAnswer(answer=answer_text, citations=cites)
        if question in self._scripts:
            return RagAnswer(answer=str(self._scripts[question]["answer"]), citations=cites)
        text = response.output_text or "I do not know from the retrieved chunks."
        return RagAnswer(answer=text, citations=cites)


def dump_embedding_fixture(path: Path | None = None) -> Path:
    """Rebuild and write precomputed FakeEmbedder vectors for the corpus."""
    target = path if path is not None else repo_root() / EMBEDDING_FIXTURE
    target.parent.mkdir(parents=True, exist_ok=True)
    index = VectorIndex.from_chunks(load_corpus_chunks(), embedder=FakeEmbedder())
    index.save(target)
    return target
