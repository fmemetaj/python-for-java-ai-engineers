# Optional local image for concept 6.6. CI does not build or run this file.
# Never bake secrets. Default provider is fake. Bind loopback on the host.
# Official Python image: https://hub.docker.com/_/python

FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LLM_PROVIDER=fake \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN useradd --create-home --uid 10001 docsdesk

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN pip install --no-cache-dir . \
    && pip install --no-cache-dir "fastapi>=0.115,<1"

USER docsdesk

EXPOSE 8000

# This image does not start a server. Learners who opt in run uvicorn on
# 127.0.0.1 themselves (see deploy/README.md). CI never docker-builds this.
CMD ["python", "-m", "docsdesk.service"]
