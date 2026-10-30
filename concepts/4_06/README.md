# 4.6 Retrieval evals (recall@k, groundedness)   [NEW — no Java equivalent] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_06/tests/test_skip.py` passes. **Still recommended.**

## 1. Concept

**Retrieval evals** measure the *search* step, not the model's prose. **recall@k** asks: of the documents that should have been found, how many appear in the top-k hits? **Groundedness** asks: did every citation come from those hits (and does the quote appear in the context)?

## 2. Intuition

JUnit `assertEquals` on the answer string is the wrong gate (Module 3). Here the gold label is a *document stem* (`refunds`, `authentication`). If `refunds` is not in the top 5, the generator never had a chance.

```
gold stems     = {refunds}
retrieved[:5]  = [payments, refunds, errors, ...]
recall@5       = 1.0

citations      = [refunds:0]   retrieved ids = {refunds:0, payments:1}
groundedness   = 1.0
```

## 3. Why it exists

A fluent wrong answer is worse than a clumsy right one. Recall tells you to fix chunking or the index. Groundedness tells you to fix citation filtering. Splitting those scores is how you debug RAG without arguing with the model.

### The Java analogy that misleads you

JUnit / pytest on HTTP status codes looks like an eval. It is not: live generation is probabilistic (3.5). Retrieval on `FakeEmbedder` *is* deterministic, so recall@k can be a CI gate. Do not "fix" a red recall by switching `LLM_PROVIDER=openai`.

## 4. Step-by-step examples

**Example 1 — perfect recall.** Gold `{refunds}` in top-5 → 1.0.

**Example 2 — miss.** Gold `{PaymentController}` but only prose stems → 0.0. That is the naive chunker splitting the Java fence.

**Example 3 — partial.** Two gold stems, one hit → 0.5.

**Example 4 — groundedness.** Citation id not in retrieved ids → 0.0 even if the sentence is true.

**Example 5 — DocsDesk report.** `uv run docsdesk eval` prints mean recall@5 and groundedness over `data/evals/docsdesk_m4.json`.

```bash
uv run python concepts/4_06/examples.py
```

The fake cannot teach live embedding drift. Graded tests check *your* formulas.

## 5. Common pitfalls

- Computing recall on the generated sentence instead of retrieved stems.
- Using precision when the spec asked for recall (false positives vs misses).
- Empty gold → define 0.0, do not divide by zero.
- Raising k until recall is 1.0 without a groundedness check (you just stuffed the prompt).

## 6. Exercises

1. **Guided:** `recall_at_k(retrieved, gold, k)`.
2. **Open:** `groundedness(citation_ids, retrieved_ids)` and show structure-aware retrieval beats a naive size split on the Java controller question.

```bash
uv run pytest concepts/4_06
```

- Hint 1: `|gold ∩ retrieved[:k]| / |gold|`.
- Hint 2: `|citations ∩ retrieved| / |citations|`; empty citations → 0.0. Naive prefixes are `text[:40]` per file.
- Solution: `solutions/recall.py`, `solutions/grounded.py`.

## 7. Check

1. If recall@5 is 0, should you first tweak the prompt or the chunker?
2. Can groundedness be 1.0 while the answer is still wrong?
3. Why is FakeEmbedder a legal CI gate here?
4. Predict: gold two stems, top-5 contains one → recall?

## Setup / troubleshooting

```bash
uv run docsdesk eval
# or: uv run python -m docsdesk eval
```

Keep `LLM_PROVIDER=fake`. More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** Module checkpoint fails if mean recall@5 or groundedness drops below 0.8 on the committed gold set.

**What you learned:** recall measures retrieval; groundedness measures citation honesty; neither is `assertEquals` on prose.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
