# 4.2 Cosine similarity and normalization   [NEW — no Java equivalent] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_02/tests/test_skip.py` passes. **Still recommended.**

Official docs: [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html), [numpy.dot](https://numpy.org/doc/stable/reference/generated/numpy.dot.html).

## 1. Concept

**Cosine similarity** is the cosine of the angle between two vectors: `dot(a, b) / (|a| |b|)`. It is 1 when they point the same way, 0 when orthogonal, −1 when opposite. **L2 normalization** divides a vector by its Euclidean length so cosine becomes a plain dot product.

## 2. Intuition

Length (how many times a word appears) should not dominate "are these about the same thing?". Cosine ignores length and keeps the direction. After L2-norm, every embedding sits on a unit sphere.

```
a = [3, 0]   |a| = 3
b = [1, 0]   |b| = 1
cosine = 1     (same direction)

c = [0, 2]     cosine(a, c) = 0  (right angle)
```

## 3. Why it exists

Euclidean distance (`sqrt(sum((a-b)^2))`) treats a long document vector as far from a short query even when they point the same way. Search engines that use embeddings almost always rank by cosine (or dot product of normalized vectors). Java `Math.hypot` / Euclidean distance in a kNN loop is the closest analog, and it is the wrong default for text.

### The Java analogy that misleads you

`equals` / `hashCode` are identity. Cosine is a *graded* score. `Arrays.compare` is lexicographic, not geometric. Do not `==` two float vectors from a live model.

## 4. Step-by-step examples

**Example 1 — parallel unit vectors.** `cosine([1, 0], [1, 0]) == 1`.

**Example 2 — orthogonal.** `cosine([1, 0], [0, 1]) == 0`.

**Example 3 — opposite.** `cosine([1, 0], [-1, 0]) == -1`.

**Example 4 — L2-normalize.** `[3, 4]` becomes `[0.6, 0.8]` because 3-4-5. Zero vectors stay zero; cosine with a zero is 0.0 (no false "perfect match").

**Example 5 — top-k.** Given a query and a matrix of rows, return the k highest cosines. This is brute-force search (next lesson wraps it in an index).

```bash
uv run python concepts/4_02/examples.py
```

The fake cannot teach approximate nearest neighbor (HNSW) recall loss. Graded tests check *your* formula.

## 5. Common pitfalls

- Forgetting to normalize before using a raw dot product as cosine.
- Truncating live embeddings without re-normalizing.
- Using `==` on floats; use a tolerance (`numpy.allclose`).
- `k=0` or a wider matrix than the query dim.

## 6. Exercises

1. **Guided:** `cosine_similarity(a, b)` including zeros and shape checks.
2. **Open:** `l2_normalize` and `topk_indices(query, matrix, k)`.

```bash
uv run pytest concepts/4_02
```

- Hint 1: `float(numpy.dot(a, b) / (norm(a) * norm(b)))`; 0.0 if either norm is 0.
- Hint 2: `numpy.argsort(-scores)[:k]`.
- Solution: `solutions/cosine.py`, `solutions/ranking.py`.

## 7. Check

1. Cosine of a vector with itself (non-zero)?
2. Why normalize before storing in an index?
3. What should cosine([0,0], [1,0]) return in this course?
4. Predict: top-k on three rows, k=2 — how many pairs?

## Setup / troubleshooting

- `numpy.linalg.norm` is in the locked numpy wheel — no extra package.
- If pyright complains about `NDArray`, you are on numpy 2.x (this repo).
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk ranks payment-api chunks by cosine, then reports recall@5.

**What you learned:** cosine is an angle; normalization makes it a dot product; top-k is sort of scores.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
