# Fundamentals deliverables

[cost: mock] [last verified: 2026-10-30, Python 3.11–3.13]

## Module 0A — `log_stats.py`

A typed analyzer for a UTF-8 log file. DocsDesk will reuse this later. Implement `fundamentals/log_stats.py` after concepts 0.1–0.15.

```bash
uv run pytest fundamentals/test_log_stats.py
```

Open files with `encoding="utf-8"` (Windows default encodings otherwise corrupt non-ASCII lines). The fixture is `sample.log`.

## Module 0B — `tool_registry.py`

A `Protocol`-typed tool map with decorator registration — the same idea as `src/mini_agent/registry.py`. Implement `fundamentals/tool_registry.py` after concepts 0.16–0.29.

```bash
uv run pytest fundamentals/test_tool_registry.py
```

Type hints are editor guidance; Pydantic still validates `Ticket` at the boundary. The decorator **runs** at import/definition time — it is not a Java annotation.
