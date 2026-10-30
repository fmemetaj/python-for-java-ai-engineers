"""Retrieval evals: recall@k and groundedness. Offline on the payments-api fixture."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from course_kit.loader import repo_root

from .rag import RagDesk, assemble_context

EVAL_FILE = Path("data") / "evals" / "docsdesk_m4.json"


@dataclass
class RetrievalCaseResult:
    id: str
    question: str
    recall_at_k: float
    grounded: float
    retrieved: list[str] = field(default_factory=list)


@dataclass
class RetrievalReport:
    recall_at_k: float
    groundedness: float
    k: int
    cases: list[RetrievalCaseResult]
    provider: str = "fake"

    @property
    def ok(self) -> bool:
        return self.recall_at_k >= 0.8 and self.groundedness >= 0.8

    def summary(self) -> str:
        return (
            f"recall@{self.k}={self.recall_at_k:.2f} "
            f"groundedness={self.groundedness:.2f} "
            f"provider={self.provider}"
        )


def load_retrieval_cases(path: Path | None = None) -> list[dict[str, Any]]:
    eval_path = path if path is not None else repo_root() / EVAL_FILE
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    if not isinstance(cases, list) or len(cases) < 8:
        raise ValueError("retrieval eval set must contain at least 8 cases")
    return cases


def recall_at_k(retrieved_stems: list[str], gold_stems: list[str], *, k: int) -> float:
    if not gold_stems:
        return 0.0
    top = set(retrieved_stems[:k])
    hits = sum(1 for stem in gold_stems if stem in top)
    return hits / len(gold_stems)


def groundedness_score(citation_ids: list[str], retrieved_ids: list[str]) -> float:
    if not citation_ids:
        return 0.0
    retrieved = set(retrieved_ids)
    return sum(1 for item in citation_ids if item in retrieved) / len(citation_ids)


def _squash(text: str) -> str:
    return " ".join(text.lower().split())


def quote_supported(quote: str, context: str) -> bool:
    needle = _squash(quote)
    return bool(needle) and needle in _squash(context)


def run_retrieval_eval(
    *,
    provider: str | None = None,
    k: int = 5,
    desk: RagDesk | None = None,
) -> RetrievalReport:
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").strip().lower() or "fake"
    if name != "fake":
        raise RuntimeError(
            "Live retrieval eval is optional. Keep LLM_PROVIDER=fake for graded work. "
            "Never commit keys. Generation would use client.responses.create; "
            "embeddings would use client.embeddings.create — never Assistants."
        )
    cases = load_retrieval_cases()
    rag = desk if desk is not None else RagDesk(k=k, hybrid=True)
    results: list[RetrievalCaseResult] = []
    for case in cases:
        question = str(case["question"])
        gold = [str(item) for item in case["gold_stems"]]
        hits = rag.retrieve(question, k=k)
        stems = [str(hit.get("stem") or Path(str(hit.get("path", ""))).stem) for hit in hits]
        ids = [str(hit.get("chunk_id", "")) for hit in hits]
        rec = recall_at_k(stems, gold, k=k)
        answer = rag.ask(question)
        cite_ids = [cite.chunk_id for cite in answer.citations]
        ground = groundedness_score(cite_ids, ids)
        context = assemble_context(hits)
        if answer.citations and not all(
            quote_supported(cite.quote, context) for cite in answer.citations
        ):
            ground = min(ground, 0.0)
        results.append(
            RetrievalCaseResult(
                id=str(case["id"]),
                question=question,
                recall_at_k=rec,
                grounded=ground,
                retrieved=stems,
            )
        )
    mean_recall = sum(item.recall_at_k for item in results) / len(results)
    mean_ground = sum(item.grounded for item in results) / len(results)
    return RetrievalReport(
        recall_at_k=mean_recall,
        groundedness=mean_ground,
        k=k,
        cases=results,
        provider="fake",
    )


def print_report(report: RetrievalReport) -> None:
    print("DocsDesk retrieval eval (fake, precomputed embeddings)")
    print(f"recall@{report.k}       {report.recall_at_k:.2f}")
    print(f"groundedness   {report.groundedness:.2f}")
    print(f"provider       {report.provider}  cost: mock")
    for case in report.cases:
        print(
            f"  {case.id:<6} recall={case.recall_at_k:.2f} "
            f"grounded={case.grounded:.2f} retrieved={','.join(case.retrieved)}"
        )
