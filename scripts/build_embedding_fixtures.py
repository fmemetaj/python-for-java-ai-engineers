"""Rebuild data/embeddings/payments-api.json from FakeEmbedder (offline)."""

from __future__ import annotations

from docsdesk.rag import dump_embedding_fixture


def main() -> int:
    path = dump_embedding_fixture()
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
