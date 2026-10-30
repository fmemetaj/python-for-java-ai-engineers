"""FastAPI sketch: health, validation, optional TestClient. No bound port."""

from __future__ import annotations

from course_kit.loader import repo_root
from docsdesk.service import create_app, fastapi_available, health_payload, validate_question

# Example 1 — health does not call a model.
body = health_payload()
assert body["status"] == "ok"
assert body["provider"] == "fake"

# Example 2 — empty questions are rejected before ProductionDesk.
assert validate_question("How do clients authenticate?") == "How do clients authenticate?"
try:
    validate_question("   ")
    raise AssertionError("blank question must fail")
except ValueError:
    pass

# Example 3 — Dockerfile sketch never bakes a key.
dockerfile = (repo_root() / "deploy" / "Dockerfile").read_text(encoding="utf-8")
assert "LLM_PROVIDER=fake" in dockerfile
assert "OPENAI_API_KEY=" not in dockerfile
assert "USER docsdesk" in dockerfile

# Example 4 — in-process TestClient when the optional extra is installed.
if fastapi_available():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    asked = client.post("/ask", json={"question": "How do clients authenticate?"})
    assert asked.status_code == 200
    payload = asked.json()
    assert "Bearer" in payload["answer"] or payload["blocked"] is False
    assert "request_id" in payload
    assert "cost_usd" in payload
    blank = client.post("/ask", json={"question": "  "})
    assert blank.status_code == 422

# Example 5 — create_app is a factory (uvicorn --factory); CI never binds 8000.
assert callable(create_app)

print("6.6 examples ok")
