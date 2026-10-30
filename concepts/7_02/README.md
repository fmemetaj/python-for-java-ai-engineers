# 7.2 Architecture of DocsDesk v1.0   [Analog: Spring Boot layered architecture] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_02/tests/test_skip.py` passes.

Official docs: [FastAPI](https://fastapi.tiangolo.com/) (optional HTTP). DocsDesk files: `docsdesk.v1.DocsDeskV1`, `docsdesk.service.create_app`.

## 1. Concept

DocsDesk v1.0 is **one process** with layers: optional HTTP → injection check → budget/cache → RAG → agent + approval → JSON logs → eval gate. Same idea as a Spring Boot app with web / service / repository — different objects.

## 2. Java version

```java
public class ArchitectureDemo {
    public static String[] layers() {
        return new String[] {"web", "service", "repository"};
    }
    public static void main(String[] args) {
        String[] names = layers();
        System.out.println(String.join(",", names));
    }
}
```

A `@RestController` does not talk to JDBC. It calls a service. The service calls a repository.

## 3. Python version

```python
from docsdesk.portfolio import architecture_layers
from docsdesk.v1 import DocsDeskV1

assert architecture_layers() == ["http", "security", "budget", "rag", "agent", "observe", "evals"]
with DocsDeskV1() as desk:
    result = desk.ask("How do clients authenticate?")
```

| Java | Python |
| --- | --- |
| `@RestController` | optional FastAPI (`create_app`) |
| `@Service` | `DocsDeskV1.ask` / `investigate` |
| Spring Security filter | `classify_prompt` before the model |
| `@Cacheable` / Caffeine | `TtlCache` |
| Micrometer + MDC | `request_id` ContextVar + JSON log |
| surefire fail-the-build | `run_v1_eval` CI gate |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Package-by-layer forever | One facade class composing existing modules | Copy-pasting RagDesk into a new package "for cleanliness" |
| Bind `0.0.0.0` in Docker | Loopback only in this course | Accidental LAN exposure of a fake desk |
| Assistants API as "the agent layer" | Sunset; Responses + your loop | Following a 2024 blog post |
| One `@SpringBootTest` that boots Tomcat | TestClient, no port | CI hanging on port 8000 |

## 5. Exercise

Return the seven layer names in order, and look up an index.

```bash
uv run pytest concepts/7_02
```

- Hint 1: `http` is first (optional), `evals` is last (the gate).
- Hint 2: RAG is *before* the agent — retrieve, then maybe investigate.
- Solution: `solutions/layers.py`.

## 6. Check

1. Why is `http` optional?
2. Which layer runs *before* any FakeLLM call on `ask`?
3. Predict: if you skip `budget`, what production failure returns?
4. Does CI `docker build` the sketch in `deploy/`?

## Setup / troubleshooting

- FastAPI: `uv sync --locked --group prod`. Tests use Starlette TestClient. Do not bind a port in CI.
- Port 8000 only if you opt into uvicorn: Windows `netstat -ano | findstr :8000`; macOS/Linux `lsof -i :8000`. Bind `127.0.0.1`.
- Docker Desktop (Windows/macOS) or the engine (Linux) is optional. CI skips it.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `modules/7-capstone/architecture.md` is the diagram you show in an interview. The code that matches it is `DocsDeskV1`.

**What you learned:** v1.0 is a Spring-style layered *composition*, not six leftover CLIs.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
