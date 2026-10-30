# 7.1 Capstone briefs — pick a product   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_01/tests/test_skip.py` passes. **Still recommended.**

Official docs: none for "pick a brief" — this is a product decision. DocsDesk files: `docsdesk.portfolio.BRIEFS`, `modules/7-capstone/README.md`.

## 1. Concept

A **capstone brief** is a one-page product contract: who it is for, which corpus it reads, which tools may write, and which artifacts you will show. Module 7 is not a new SDK. It is DocsDesk v1.0, defended as a portfolio.

## 2. Intuition

Three original options, one implementation in this repo (the payments-api fixture) so CI stays offline:

```
(a) own-repo     → point RAG at *your* public Java docs
(b) pr-review    → comment on a fixture diff (approval before "post")
(c) log-triage   → parse a log line, then the Module 5 agent loop
```

You ship **one**. The graded tests use (c)-shaped fixtures plus (a)-shaped RAG over `data/corpus/payments-api`. Nothing posts to GitHub. Nothing emails.

## 3. Why it exists

Hiring managers ask "show me a thing you built", not "show me a certificate". A brief stops you from gluing six module demos and calling it a product.

### The Java analogy that misleads you

A Jira ticket ("build the payments API") is a spec for *shipping software*. A capstone brief is a spec for *evidence*: eval report, cost per 100, threat model, five-minute demo. Closing the ticket is not the same as being able to defend the repo.

## 4. Step-by-step examples

**Example 1 — own-repo.** Public Spring README + Javadoc. Read-only tools. Swap the fixture corpus later; keep FakeEmbedder in CI.

**Example 2 — pr-review.** A committed diff fixture. `propose_page` analog is "submit review". The approval flag stays false until a human says yes. No `api.github.com` in graded work.

**Example 3 — log-triage.** `Incident` from Module 3, then `TriageDesk` from Module 5. `propose_page` is simulated (`would_write`).

**Example 4 — artifacts.** Six names: README, architecture, eval report, cost report, threat model, demo.

**Example 5 — unknown brief.** `choose_brief("secret-saas")` raises `KeyError`. Do not invent a fourth option that needs a paid API.

```bash
uv run python concepts/7_01/examples.py
```

## 5. Common pitfalls

- Treating the capstone as "run all previous notebooks again".
- Picking all three briefs and finishing none.
- Pointing graded tests at `LLM_PROVIDER=openai`.
- Committing `.env` because "the demo needs a key".
- Claiming the simulated review was posted.

## 6. Exercises

1. **Guided:** `list_briefs`, `choose_brief`.
2. **Open:** `required_artifacts` (the six rubric names).

```bash
uv run pytest concepts/7_01
```

- Hint 1: ids are `own-repo`, `pr-review`, `log-triage`.
- Hint 2: write_tools is False only for own-repo.
- Solution: `solutions/briefs.py`, `solutions/artifacts.py`.

## 7. Check

1. Why is a Jira ticket a misleading analog for a capstone brief?
2. Which brief is read-only?
3. Name the six artifacts.
4. Does graded work need a paid key?
5. What does `propose_page` actually write?

## Setup / troubleshooting

- `LLM_PROVIDER=fake` (default). A live key is optional and never committed.
- Windows: `set LLM_PROVIDER=fake`. PowerShell: `$env:LLM_PROVIDER="fake"`. macOS/Linux: `export LLM_PROVIDER=fake`.
- If `uv` is missing after install: restart the terminal (PATH). Windows Store `python` is the wrong interpreter — use `uv run python`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** `uv run course check m7` prints `v1 pass` only when DocsDesk v1.0 and the ≥30-case eval are green on fake.

**What you learned:** pick one brief; the rubric is evidence, not a certificate.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
