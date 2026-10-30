# 4.1 Embeddings and vector spaces   [NEW — no Java equivalent] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_01/tests/test_skip.py` passes. **Still recommended.**

Official docs: [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings). numpy arrays: [numpy.ndarray](https://numpy.org/doc/stable/reference/arrays.ndarray.html).

## 1. Concept

An **embedding** is a list of numbers (a vector) that places a piece of text in a high-dimensional space so that *similar meaning* tends to land *nearby*. Retrieval compares vectors, not keywords.

## 2. Intuition

Imagine every paragraph as a point on a map. "refund a captured payment" and "POST /payments/{id}/refunds" should sit closer together than "refund" and "HMAC webhook signature". The map has tens or thousands of axes (the **dimension**). You never plot it; you measure angles.

```
"Bearer JWT"  →  FakeEmbedder  →  [0.12, -0.40, …]   (64 numbers, L2-normalized)
"HMAC-SHA256" →  FakeEmbedder  →  [0.05,  0.33, …]
```

This course's `FakeEmbedder` is a **hashing trick** (tokens → buckets with ±1). It is deterministic and offline. It is *not* a neural model. Live OpenAI uses `client.embeddings.create` with `text-embedding-3-small` (1536 dims by default). That is the Embeddings API, **not** Responses and **not** Assistants.

## 3. Why it exists

Keyword search fails when the question uses different words than the doc (`"how do I give the money back?"` vs `"refund"`). Embeddings give a score for *relatedness* without a shared token. Java would reach for Lucene analyzers and synonyms — useful, but still lexical. Vectors are a different index.

### The Java analogy that misleads you

`String.hashCode()` and `HashMap` look like "turn text into a number". They do not. A hash code is for buckets, not similarity: two near-synonyms almost never hash near each other. `MessageDigest` is the same trap. The hashing trick in `FakeEmbedder` *does* use hashes, but it accumulates **many** token hashes into a vector so overlapping tokens can be close. A single `hashCode` cannot.

## 4. Step-by-step examples

**Example 1 — a numpy vector.** `np.array([1.0, 0.0, 0.0])` has `shape (3,)` and `ndim == 1`. This is a `double[]`, not an `ArrayList<Double>`.

**Example 2 — dimension.** `FakeEmbedder(dim=8).embed("hello").shape == (8,)`. Changing `dim` is a new space; do not compare 8-D to 64-D.

**Example 3 — same text, same vector.** Embeddings from `FakeEmbedder` are deterministic. Tests can assert equality. A live model is close but not bit-identical.

**Example 4 — shared tokens pull together.** `"refund captured payment"` is closer (higher cosine, next lesson) to `"refund a captured payment"` than to `"HMAC-SHA256 webhook"`.

**Example 5 — empty text.** The fake embedder returns the first unit vector so you never store a silent zero that later looks like a match (cosine of zeros is defined as 0.0 in our helper, but a stored zero is still a bug).

**Example 6 — live vs fake (optional).** Graded work sets `LLM_PROVIDER=fake`. If you opt in, `client.embeddings.create(model="text-embedding-3-small", input=texts)` — never Assistants. Prices: `data/pricing.yaml` → `embeddings` (retrieved 2026-10-30). Generation in RAG still uses Responses (`client.responses.create`).

```bash
uv run python concepts/4_01/examples.py
```

The fake cannot teach a production embedding model's multilingual geometry or its bill. Graded tests check *your* hashing embedder and shapes.

## 5. Common pitfalls

- Treating an embedding as a summary you can read. The axes have no English labels.
- Mixing models or dimensions in one index.
- Truncating a live vector without re-normalizing ([OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings) `dimensions` parameter is the supported way to shorten).
- Calling Assistants or Responses for embeddings.
- Committing API keys. Copy `.env.example` → `.env` only for optional live calls.

## 6. Exercises

1. **Guided:** implement `token_hash_embed` (hashing trick, L2-normalized, dim ≥ 2).
2. **Open:** `embed_many` returns an `(n, dim)` matrix; every non-empty row has L2-norm ≈ 1.

```bash
uv run pytest concepts/4_01
```

- Hint 1: hash each token to a bucket and a ±1 sign; divide by `numpy.linalg.norm`.
- Hint 2: `numpy.stack` row vectors. Empty input → shape `(0, dim)`.
- Solution: `solutions/embed.py`, `solutions/batch.py`.

## 7. Check

1. Is an embedding a paragraph you can print, or a vector of floats?
2. Why is `String.hashCode()` a misleading analog?
3. Which API embeds text — Responses, Assistants, or Embeddings?
4. Predict: `embed("a")` vs `embed("a")` with FakeEmbedder — equal or not?
5. Why must CI keep `LLM_PROVIDER=fake`?

## Setup / troubleshooting

- **numpy wheels:** `uv sync --locked` should download a wheel for CPython 3.11–3.13 on Windows amd64, macOS x86_64/arm64, and Linux. If uv tries to *build* numpy, you are on an unusual platform or a mismatched arch (Apple Silicon running an x86_64 Python under Rosetta). Use `uv python install 3.12` for the native arch, then `uv sync --locked`.
- **Windows ARM64:** prefer an official numpy wheel; do not install Visual Studio just to compile numpy for this course.
- **macOS ARM:** `arch` should be `arm64`. "Bad CPU type" → native Terminal, not Rosetta.
- Graded work never calls the network. More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk indexes `data/corpus/payments-api` with `FakeEmbedder` and committed vectors in `data/embeddings/payments-api.json`.

**What you learned:** embeddings are dense vectors; the course fake is a hashing trick; live embeddings are optional and use a different API than Responses.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
