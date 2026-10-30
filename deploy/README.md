# Optional DocsDesk container (concept 6.6)

This folder is **not** used in CI. Docker Desktop / the Docker engine is optional.
Graded FastAPI tests use an in-process TestClient (no port, no image).

Never put `OPENAI_API_KEY` in the Dockerfile, `.dockerignore` exceptions, or an image.
Default `LLM_PROVIDER=fake`.

## Run locally (loopback only)

```bash
docker build -f deploy/Dockerfile -t docsdesk:local .
docker run --rm -p 127.0.0.1:8000:8000 docsdesk:local
```

The image CMD prints how to start uvicorn. To serve:

```bash
docker run --rm -p 127.0.0.1:8000:8000 docsdesk:local \
  python -c "print('use uvicorn on 127.0.0.1 from a venv instead of this sketch')"
```

Prefer the venv path from concept 6.6:

```bash
uv sync --locked --group prod
uv run --with uvicorn uvicorn docsdesk.service:create_app --factory --host 127.0.0.1 --port 8000
```

If port 8000 is busy: Windows `netstat -ano | findstr :8000`, macOS/Linux `lsof -i :8000`, then pick `--port 8001`.
Do not publish `0.0.0.0` for this course. Do not deploy to a real host.
