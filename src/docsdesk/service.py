"""Optional FastAPI wrapper around ProductionDesk. Java analog: Spring Boot + jar.

The HTTP layer is optional (concept 6.6). Graded tests use Starlette's in-process
TestClient — no bound port, no Docker, no network. Docker is a separate sketch
in ``deploy/`` and is skipped in CI.

Install: ``uv sync --locked --group prod``.
Docs: https://fastapi.tiangolo.com/
"""

from __future__ import annotations

import importlib
from typing import Any

from .production import ProductionDesk


def health_payload() -> dict[str, str]:
    """Liveness body. Must not call the model (like Spring Actuator /health)."""
    return {"status": "ok", "provider": "fake"}


def validate_question(question: str) -> str:
    text = question.strip()
    if not text:
        raise ValueError("question must be non-empty")
    return text


def fastapi_available() -> bool:
    try:
        importlib.import_module("fastapi")
    except ImportError:
        return False
    return True


def create_app(desk: ProductionDesk | None = None) -> Any:
    """Build a FastAPI app. Raises RuntimeError if the optional extra is missing."""
    try:
        fastapi = importlib.import_module("fastapi")
    except ImportError as exc:
        raise RuntimeError(
            "FastAPI is optional. Install with: uv sync --locked --group prod"
        ) from exc
    FastAPI = fastapi.FastAPI
    HTTPException = fastapi.HTTPException
    app = FastAPI(title="DocsDesk", version="0.6")
    holder = desk if desk is not None else ProductionDesk()

    @app.get("/health")
    def health() -> dict[str, str]:
        return health_payload()

    @app.post("/ask")
    def ask(body: dict[str, Any]) -> dict[str, Any]:
        raw = body.get("question")
        if not isinstance(raw, str):
            raise HTTPException(status_code=422, detail="question must be a string")
        try:
            question = validate_question(raw)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        result = holder.ask(question)
        return {
            "answer": result.answer,
            "request_id": result.request_id,
            "cost_usd": result.cost_usd,
            "cached": result.cached,
            "blocked": result.blocked,
            "model": result.model,
        }

    return app


def main() -> int:
    print("DocsDesk HTTP API is optional and is not started by CI.")
    print("In-process tests use FastAPI TestClient (no port).")
    print(
        "To run locally (not in CI, loopback only): "
        "uv sync --locked --group prod && "
        "uv run --with uvicorn uvicorn docsdesk.service:create_app --factory "
        "--host 127.0.0.1 --port 8000"
    )
    print("Never bind 0.0.0.0 in this course. Never bake OPENAI_API_KEY into an image.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
