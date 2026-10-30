# Five-minute demo script (simulated)

Speak this while you share a terminal. Do not skip the honesty lines. Nothing here sends email, posts a GitHub review, or writes a wiki page.

## 0:00 — Clone and sync (30 s)

```bash
uv sync --locked --group dev
echo %LLM_PROVIDER%          :: Windows cmd, expect empty or fake
echo $LLM_PROVIDER           # macOS / Linux / WSL
```

Say: "Graded work is `LLM_PROVIDER=fake`. I did not commit a key."

## 0:30 — Ask with citations (90 s)

```bash
uv run docsdesk v1
```

Point at the RAG turn: the answer mentions refunds, `cites=` is not zero, the JSON line has `request_id` and `cost_usd`.

Say: "Retrieval is our numpy index over an original Spring fixture, not the model browsing GitHub."

## 2:00 — Approval gate (90 s)

If you have a second terminal:

```bash
uv run python -c "from docsdesk.v1 import DocsDeskV1; from docsdesk.triage import INCIDENT_REFUND_500; d=DocsDeskV1(); r=d.investigate(INCIDENT_REFUND_500, approved=False); print(r.status, r.tool_names)"
```

Point at `denied` and `propose_page`. Then show the approved path already printed by `docsdesk v1`.

Say: "This is simulated. `would_write` is a flag. No page was created."

## 3:30 — Eval gate and cost (60 s)

```bash
uv run docsdesk eval-v1
uv run docsdesk cost-report
```

Point at ≥30 cases, `capstone gate pass`, and the dated pricing source.

## 4:30 — Threats and stop (30 s)

```bash
uv run docsdesk portfolio
```

Name one residual (novel injection phrasing, unknown secrets, or a default `approved=True`). Stop. Do not open Docker Desktop unless someone asks, and then say CI never builds the image.

## Troubleshooting during a live demo

| Symptom | Windows | macOS / Linux |
|---|---|---|
| `python` not found | `py -3.12` or `uv run python`; avoid Store stub | `uv run python` / `python3` |
| `uv` missing after install | Restart the terminal; check PATH | `source $HOME/.local/bin/env` |
| Unicode garbage in JSON | Windows Terminal; `PYTHONUTF8=1` | usually fine |
| Port 8000 busy | `netstat -ano \| findstr :8000` | `lsof -i :8000` |
| Demo tries to call OpenAI | `set LLM_PROVIDER=fake` | `export LLM_PROVIDER=fake` |
