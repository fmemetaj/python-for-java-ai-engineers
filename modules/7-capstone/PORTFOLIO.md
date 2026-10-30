# Portfolio / README guide

Copy this outline when you publish **your** brief (own-repo, pr-review, or log-triage). Keep graded CI on the payments-api fixture even if your public write-up uses another corpus.

## Title

DocsDesk v1.0 — &lt;brief id&gt; — Python for Java AI Engineers capstone

## Objective (4 sentences)

What it answers, who it is for, that it runs offline on FakeLLM, that writes are simulated.

## Architecture

Link [architecture.md](architecture.md) or paste the mermaid diagram. Name the seven layers. State the Java analog *and* where it breaks (the model proposes tools; you still cap and approve).

## How to run (clean clone)

```bash
uv python install 3.12
uv sync --locked --group dev
uv run python scripts/doctor.py --offline
uv run docsdesk v1
uv run docsdesk eval-v1
uv run docsdesk cost-report
```

Windows: `uv run python`, not the Microsoft Store stub. macOS/Linux: prefer `uv run python` over a leftover `python3` that is not 3.11–3.13. WSL: stay entirely in Linux; do not mix a Windows `.venv`.

Optional HTTP (not in CI, loopback only):

```bash
uv sync --locked --group prod
uv run --with uvicorn uvicorn docsdesk.service:create_app --factory --host 127.0.0.1 --port 8000
```

Never bind `0.0.0.0`. Never bake `OPENAI_API_KEY` into an image.

## Eval report

Paste `uv run docsdesk eval-v1` (fake). The bar is ≥30 cases, 100% on FakeLLM. If you optionally run a live key, report the rate and **claim no threshold**.

## Cost report

Paste `uv run docsdesk cost-report`. Keep the price date (`data/pricing.yaml`, retrieved 2026-10-30 from [OpenAI pricing](https://platform.openai.com/docs/pricing)). Do not hard-code USD in this paragraph.

## Threat model

The five rows from `docsdesk.portfolio.threat_rows` (injection, leakage, excessive agency, cost runaway, supply-chain), each with a residual.

Cite [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) as the current project page, not a memorized year.

## Known limitations

- FakeLLM / FakeEmbedder are not production models.
- Approval is an in-process boolean, not an IdP.
- FastAPI is optional; CI uses TestClient.
- `deploy/Dockerfile` is a sketch; CI does not build it.
- `propose_page` does not send email, open a ticket, or write a wiki page.
- No Assistants API.

## Five-minute demo

Follow [DEMO.md](DEMO.md). Say the word **simulated** when the write tool runs.

## Self-assessment

The ten boxes in the [module README](README.md). Tick them before you share the link.
