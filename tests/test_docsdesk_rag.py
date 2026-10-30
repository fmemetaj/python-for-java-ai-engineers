"""DocsDesk v0.4 RAG over the original payments-api Spring fixture."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from course_kit.loader import repo_root
from docsdesk.corpus import load_corpus_chunks
from docsdesk.rag import RagDesk, dump_embedding_fixture, load_payments_index
from docsdesk.retrieval_eval import run_retrieval_eval


def test_corpus_is_original_spring_fixture() -> None:
    chunks = load_corpus_chunks()
    stems = {chunk.stem for chunk in chunks}
    assert "PaymentController" in stems
    assert "refunds" in stems
    assert any(chunk.is_code and "@PostMapping" in chunk.text for chunk in chunks)


def test_precomputed_embeddings_exist() -> None:
    path = repo_root() / "data" / "embeddings" / "payments-api.json"
    assert path.is_file()
    index = load_payments_index(fixture=path)
    assert len(index) > 0


def test_rag_retrieves_refunds() -> None:
    desk = RagDesk(k=5, hybrid=True)
    hits = desk.retrieve("How do I refund a captured payment?")
    stems = [str(hit.get("stem")) for hit in hits]
    assert "refunds" in stems[:5]
    answer = desk.ask("How do I refund a captured payment?")
    assert answer.citations
    retrieved_ids = {str(hit["chunk_id"]) for hit in hits}
    assert {cite.chunk_id for cite in answer.citations} <= retrieved_ids


def test_retrieval_eval_meets_gate() -> None:
    report = run_retrieval_eval(provider="fake", k=5)
    failed = [case.id for case in report.cases if case.recall_at_k < 1.0]
    assert report.recall_at_k >= 0.8, failed
    assert report.groundedness >= 0.8
    assert report.ok
    assert "recall@5" in report.summary()


def test_live_provider_is_opt_in() -> None:
    previous = os.environ.get("LLM_PROVIDER")
    os.environ["LLM_PROVIDER"] = "openai"
    try:
        with pytest.raises(RuntimeError, match="fake"):
            run_retrieval_eval()
    finally:
        if previous is None:
            os.environ.pop("LLM_PROVIDER", None)
        else:
            os.environ["LLM_PROVIDER"] = previous


def test_docsdesk_eval_entrypoint(capsys: pytest.CaptureFixture[str]) -> None:
    from docsdesk.__main__ import main

    assert main(["eval"]) == 0
    captured = capsys.readouterr()
    assert "recall@5" in captured.out
    assert "groundedness" in captured.out


def test_rebuild_fixture_roundtrip(tmp_path: Path) -> None:
    path = dump_embedding_fixture(tmp_path / "payments-api.json")
    assert path.is_file()
    index = load_payments_index(fixture=path)
    assert len(index) == len(load_corpus_chunks())
