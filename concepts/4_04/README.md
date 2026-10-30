# 4.4 Vector index / search   [Analog: Lucene / Elasticsearch index] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/4_04/tests/test_skip.py` passes.

Official docs: [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings) (store your own vectors). Elasticsearch kNN is the Java-side neighbor.

## 1. Concept

A **vector index** stores `(id, vector, payload)` and answers "nearest neighbors of this query vector". In this course it is a numpy matrix plus cosine top-k. Lucene/Elasticsearch inverted indexes store *terms*; a vector index stores *directions*.

## 2. Java version

```java
public class VectorIndexDemo {
    public static int topId(double[] q, double[][] docs) {
        int best = 0;
        double bestScore = q[0] * docs[0][0] + q[1] * docs[0][1];
        for (int i = 1; i < docs.length; i++) {
            double score = q[0] * docs[i][0] + q[1] * docs[i][1];
            if (score > bestScore) { bestScore = score; best = i; }
        }
        return best;
    }
    public static void main(String[] args) {
        System.out.println(topId(new double[]{1, 0}, new double[][]{{1, 0}, {0, 1}}));
    }
}
```

That loop is brute-force kNN (fine for DocsDesk's tiny corpus). Lucene's inverted index would instead walk posting lists for the query terms.

## 3. Python version

```python
index = VectorIndex(dim=64)
index.add("refunds:0", embedder.embed(chunk), payload={"text": chunk, "stem": "refunds"})
hits = index.search(embedder.embed(question), k=5)
# hits[0]["chunk_id"], hits[0]["score"]
```

| Java | Python |
| --- | --- |
| Lucene `DirectoryReader` | `VectorIndex` (numpy matrix) |
| Elasticsearch inverted index | cosine over rows |
| `ScoreDoc.doc` + `_source` | `chunk_id` + payload dict |
| kNN / HNSW plugin | brute-force `top_k` (this course) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Analyzer + BM25 always on | Dense search ignores unknown tokens | Query "give money back" still needs overlap with "refund" in the *fake* hasher; live models generalize |
| Schema mapping at index time | Payload is a dict you remember to fill | Missing `path` → cannot cite |
| Elasticsearch cluster | In-memory matrix | Restart loses the index unless you dump JSON |
| Term queries are exact | Cosine is graded | Taking only score==1 misses near matches |
| One shard per index | Mixing dims in one matrix | `ValueError: expected dim 64` |

When to use a real vector DB: the matrix no longer fits in RAM, or you need metadata filters pushed down (the same reason you stopped using a `HashMap` and started Elasticsearch).

## 5. Exercise

Implement `InMemoryIndex.add` and `search` returning `[{id, score}, ...]` sorted by cosine.

```bash
uv run pytest concepts/4_04
```

- Hint 1: store parallel lists (ids, rows). Search is `top_k` from 4.2.
- Hint 2: reject a vector whose length ≠ dim.
- Solution: `solutions/search.py`.

## 6. Check

1. What does Lucene store that a vector index does not?
2. Why dump `data/embeddings/payments-api.json`?
3. Predict: query `[1,0]` vs rows `[1,0]` and `[0,1]` — which id wins?
4. When is brute-force cosine no longer enough?

## Setup / troubleshooting

- Fixture load: `VectorIndex.load(path)` reads JSON floats. Rebuild with `uv run python scripts/build_embedding_fixtures.py`.
- numpy install: [troubleshooting](../../docs/setup/troubleshooting.md) (native wheels).
- `LLM_PROVIDER=fake` still required; the index does not call OpenAI.

**Real scenario:** DocsDesk searches the payments-api index, then feeds the hits to FakeLLM.

**What you learned:** a vector index is kNN over embeddings; Lucene is the inverted-index analog, not a drop-in.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
