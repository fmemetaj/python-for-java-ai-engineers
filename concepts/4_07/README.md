# 4.7 Advanced: hybrid search + reranking   [Analog: Elasticsearch BM25 scoring] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_07/tests/test_skip.py` passes. **Optional** (🟣). Still in `course check m4`.

Official docs: [Elasticsearch BM25](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/relevance/bm25). Hosted `file_search` (lock-in) is a sidebar, not the graded path.

## 1. Concept

**Hybrid search** mixes a lexical score (BM25 — term frequency with inverse document frequency) with a vector score (cosine), then optionally **reranks** a shortlist. Elasticsearch has done BM25 for years; adding a kNN clause is the analog.

## 2. Java version

```java
public class HybridDemo {
    public static double fuse(double bm25, double cosine, double alpha) {
        return alpha * cosine + (1.0 - alpha) * bm25;
    }
    public static void main(String[] args) {
        System.out.println(fuse(0.8, 0.2, 0.5));
    }
}
```

In Elasticsearch you would `bool` a `match` query with a `knn` clause, or `rescore` the window. Min-max normalize each score before mixing, or BM25's raw magnitude swamps cosine's `[-1, 1]`.

## 3. Python version

```python
lexical = bm25_scores(query, [hit["text"] for hit in hits])
fused = fuse_scores(vector_scores, lexical, alpha=0.6)
# rerank_by_cosine(query_vec, shortlist, vectors, k=5)
```

| Java / ES | Python (this course) |
| --- | --- |
| BM25 `tf`, `idf`, `k1`, `b` | `bm25_scores` |
| `function_score` / weighted `bool` | `fuse_scores` (alpha on cosine) |
| `rescore` window | `rerank_by_cosine` |
| Hosted OpenAI `file_search` | Own pipeline + FakeEmbedder |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| BM25 scores are unbounded | Cosine is in [-1, 1] | Adding them raw lets BM25 win always |
| Analyzers lowercase + stem | Our tokenizer is regex `[a-z0-9]+` | `"POST"` and `"post"` match; `"give-back"` ≠ `"refund"` |
| Cluster query DSL | In-memory lists | Fine for the fixture; not a replacement for ES |
| Hosted file_search "just works" | Lock-in, extra $ , opaque chunking | Graded work never calls it |

**Hosted file_search vs own pipeline (cost and lock-in).** OpenAI's hosted retrieval is a Responses *tool*, billed separately, with vendor chunking you cannot unit-test. Own pipeline: FakeEmbedder + numpy + pytest recall@k. Use hosted later if you accept the bill and the black box — not in CI.

## 5. Exercise

Implement `bm25_scores`, `fuse_scores` (min-max, then `alpha * cosine + (1-alpha) * bm25`), and a tiny rerank.

```bash
uv run pytest concepts/4_07
```

- Hint 1: IDF `log(1 + (N - n + 0.5) / (n + 0.5))`; skip empty docs.
- Hint 2: if all BM25 values are equal, min-max is zeros — cosine still decides.
- Solution: `solutions/hybrid.py`.

## 6. Check

1. Why min-max before adding BM25 to cosine?
2. What does `alpha=1` mean?
3. Is file_search required for DocsDesk eval?
4. Predict: query token in only doc 2 — which BM25 score is larger?

## Setup / troubleshooting

Optional lesson. If BM25 is all zeros, your tokenizer dropped the query (`HMAC-SHA256` → `hmac`, `sha256`). More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk `RagDesk(hybrid=True)` fuses BM25 with cosine before answering.

**What you learned:** lexical + dense, scaled, then rerank; hosted file_search is optional lock-in.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
