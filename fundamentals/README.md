# Module 0A deliverable — `log_stats.py`

[cost: mock] [last verified: 2026-10-30, Python 3.11–3.13]

A typed analyzer for a UTF-8 log file. DocsDesk will reuse this later. Implement `fundamentals/log_stats.py` after concepts 0.1–0.15.

```bash
uv run pytest fundamentals/test_log_stats.py
```

Open files with `encoding="utf-8"` (Windows default encodings otherwise corrupt non-ASCII lines). The fixture is `sample.log`.
