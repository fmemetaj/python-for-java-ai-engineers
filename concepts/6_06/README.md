# 6.6 Advanced: FastAPI service + container   [Analog: Spring Boot app + jar/container] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/6_06/tests/test_skip.py` passes. **Optional** (🟣). Docker is optional and is **skipped in CI**.

Official docs: [FastAPI](https://fastapi.tiangolo.com/), [uvicorn settings](https://www.uvicorn.org/settings/). Code: `src/docsdesk/service.py`, sketch: `deploy/Dockerfile`.

## 1. Concept

DocsDesk as an HTTP service: `GET /health` (no model) and `POST /ask` (ProductionDesk). That is a Spring Boot `@RestController` analog. The **container** is a sketch so you see what *not* to bake in (keys, `0.0.0.0` in CI). Graded tests never bind a port.

## 2. Java version

```java
public class BootDemo {
    public static String health() {
        return "ok";
    }
    public static void main(String[] args) {
        System.out.println(health());
    }
}
```

A real app would be `@RestController` + `java -jar` + a distroless image. Health must not call the LLM.

## 3. Python version

```python
from docsdesk.service import create_app, health_payload, validate_question

assert health_payload()["status"] == "ok"
assert validate_question("How do clients authenticate?")

# Optional extra: uv sync --locked --group prod
# from fastapi.testclient import TestClient
# client = TestClient(create_app())  # in-process, no port
```

| Java | Python |
| --- | --- |
| `@RestController` + `@GetMapping("/health")` | FastAPI `@app.get("/health")` |
| `java -jar app.jar` | `uvicorn docsdesk.service:create_app --factory` |
| Actuator `/health` | `health_payload` — **no model call** |
| Container USER + no secrets in image | `deploy/Dockerfile` (`USER docsdesk`, `LLM_PROVIDER=fake`) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Bind `0.0.0.0` in prod | This course uses **127.0.0.1** | Accidental LAN exposure in a lesson |
| Bake `application.yml` secrets | `.env` is gitignored; Dockerfile must not `ENV OPENAI_API_KEY=` | Keys in the image history |
| Health = "I can call the DB" | Health must not call FakeLLM *or* OpenAI | `/health` becomes a paid, flaky probe |
| Docker required in CI | CI **skips** `docker build` | Red CI on machines without Docker Desktop |

## 5. Exercise

Implement `health` (no model) and `validate_question` (reject blank).

```bash
uv run pytest concepts/6_06
```

- Hint 1: health is `{"status": "ok", "provider": "fake"}`.
- Hint 2: `question.strip()` must be non-empty or `ValueError`.
- Solution: `solutions/service.py`.

Optional local server (not CI, loopback only):

```bash
uv sync --locked --group prod
uv run --with uvicorn uvicorn docsdesk.service:create_app --factory --host 127.0.0.1 --port 8000
```

If 8000 is busy: Windows `netstat -ano | findstr :8000`; macOS/Linux `lsof -i :8000`; then `--port 8001`. Docker Desktop must be running on Windows/macOS; on Linux you need permission to talk to the daemon. CI does not build `deploy/Dockerfile`.

## 6. Check

1. Why must `/health` not call the model?
2. What goes wrong if the Dockerfile copies `.env`?
3. Does CI bind port 8000?
4. Predict: `POST /ask` with `{"question": "  "}` — 422 or 200?

## Setup / troubleshooting

- **FastAPI extra:** `uv sync --locked --group prod`. Without it, TestClient tests skip; the exercise still grades.
- **Docker:** optional. Never `docker push` for this course. Never deploy to a real service.
- **Env vars:** Windows `set LLM_PROVIDER=fake`; PowerShell `$env:LLM_PROVIDER="fake"`; macOS/Linux `export LLM_PROVIDER=fake`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `tests/test_docsdesk_service.py` uses TestClient when FastAPI is installed. `tests/test_docsdesk_prod.py` reads the Dockerfile and asserts no baked key.

**What you learned:** Spring Boot analog as FastAPI; health without LLM; containers are optional and must not ship secrets.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
