# 7.6 Threat model and known limitations   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_06/tests/test_skip.py` passes. **Still recommended.**

Official docs: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (version numbers change; read the current project page). DocsDesk files: `docsdesk.portfolio.threat_rows`, `docsdesk.security`.

## 1. Concept

A **threat model** lists what can go wrong, what you already mitigate, and what residual risk you still accept. A **limitations** list says what the fake cannot teach and what this repo will not do (no real deploy, no email, no GitHub review).

## 2. Intuition

Five rows for v1.0:

1. Prompt injection (direct + indirect in retrieved docs)
2. Data leakage (secrets in answers or logs)
3. Excessive agency (write tools without a human)
4. Cost runaway (no budget, no step cap)
5. Supply-chain / lock-in (hosted file_search vs your index)

Each row has a mitigation **and** a residual.

## 3. Why it exists

Green tests do not mean "safe in production". Interviewers will poke the gate. If you cannot name a residual, you have a brochure, not a model.

### The Java analogy that misleads you

SQL injection has a parser that separates code from data. An LLM does not: instructions, retrieved docs, and user text share one token stream. Treating `IGNORE PREVIOUS INSTRUCTIONS` like `'; DROP TABLE` misses *indirect* injection inside a chunk you retrieved (Module 6).

A STRIDE workshop is closer, but still assumes you control the interpreter.

## 4. Step-by-step examples

**Example 1 — classify.** "Ignore previous instructions" → `prompt-injection`.

**Example 2 — leakage.** Redact known secrets. Unknown secrets remain.

**Example 3 — agency.** `approved=False` denies `propose_page`. A default `True` would undo the row.

**Example 4 — limitations.** Must mention FakeLLM/FakeEmbedder **and** that CI does not deploy/docker-build.

**Example 5 — honesty.** `would_write` is not a wiki page. Do not write "we shipped to prod" in the README.

```bash
uv run python concepts/7_06/examples.py
```

## 5. Common pitfalls

- Mitigations without residuals ("we block injection" — with which phrases?).
- Copying OWASP titles without tying them to DocsDesk code.
- Calling the Dockerfile a production hardening guide. It is a sketch.

## 6. Exercises

1. **Guided:** `classify_threat`, `threat_ids`.
2. **Open:** `lists_limitations`.

```bash
uv run pytest concepts/7_06
```

- Hint 1: look for `inject`, `secret`/`api key`/`leak`, `approve`/`write tool`, `budget`/`spend`.
- Hint 2: join the limitation strings and search for `fake` plus `deploy` or `docker`.
- Solution: `solutions/threats.py`, `solutions/limits.py`.

## 7. Check

1. Why is SQL injection a misleading analog?
2. Name one residual for prompt injection in this repo.
3. What does `propose_page` actually do?
4. Does CI `docker build`?

## Setup / troubleshooting

- Injection fixtures: `data/evals/docsdesk_injection.json`.
- Never paste real keys into limitation examples. Use `course-test-secret-value`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run docsdesk portfolio` prints threats and limitations. Put that section in your README unchanged in spirit.

**What you learned:** five threats with residuals; limitations that admit the fake and skip deploy.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
