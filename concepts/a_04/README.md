# A.4 Hosted file_search vs own RAG   [Analog: managed OpenSearch vs self-hosted Lucene] [cost: mock] [~50 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_04/tests/test_skip.py` passes.

Official docs: [file_search](https://platform.openai.com/docs/guides/tools-file-search), [Tools](https://platform.openai.com/docs/guides/tools). Concept 4.7 already flagged lock-in; this lesson is the **decision**. Helpers: `course_kit.hosted`.

## 1. Concept

**Hosted file_search** is a Responses *tool* that retrieves over files stored on the vendor. **Owned RAG** is Module 4: FakeEmbedder + numpy + pytest recall@k. When you can measure recall, owned is the default. Hosted is a prototype, not a CI gate.

## 2. Java version

```java
public class HostedVsOwnDemo {
    public static String choose(boolean canEval, double ownRecall) {
        if (canEval && ownRecall >= 0.6) {
            return "own";
        }
        return "hosted";
    }
    public static void main(String[] args) {
        System.out.println(choose(true, 0.8));
        System.out.println(choose(false, 0.0));
    }
}
```

Managed OpenSearch vs a Lucene jar you ship: same split — convenience versus a contract you can test.

## 3. Python version

```python
from course_kit.hosted import choose_stack, overlap_rate

overlap_rate(["a", "b"], ["b", "c"])  # 1/3
choose_stack(own_recall=0.8, hosted_available=True, can_export=True, can_eval=True, overlap=0.1)
```

| Java / search | Python (this course) |
| --- | --- |
| Self-hosted Lucene | `RagDesk` + fixture vectors |
| Amazon OpenSearch managed | Hosted `file_search` tool |
| You control analyzers | Vendor chunking (opaque) |
| You export the index | Often **not** exportable |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| "Managed ES is still Lucene" | Hosted file_search is a tool with vendor chunking | Recall@k tests that cannot run |
| Index dump / snapshot | Many hosted stores are not exportable | Lock-in discovered at renewal |
| One cluster for prod+test | Graded work must not call hosted | CI that needs a paid vector store |
| BM25 analog from 4.7 | This lesson picks a **stack** | Hybrid as a default without overlap data |

## 5. Exercise

Jaccard overlap, then `pick_stack` (`own` / `hosted` / `hybrid`).

```bash
uv run pytest concepts/a_04
```

- Hint 1: empty either id list → overlap `0.0`.
- Hint 2: `can_eval` and `own_recall >= 0.6` → `own`.
- Solution: `solutions/compare.py`, `solutions/stack.py`.

## 6. Check

1. When is hosted the honest default?
2. Why is managed OpenSearch only a partial analog?
3. Predict: own_recall=0.8, can_eval=True → choice?
4. Can CI measure vendor chunking?
5. Does this lesson call live `file_search`?

## Setup / troubleshooting

- `uv run docsdesk hosted` prints the comparison on FakeEmbedder.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk v1.0 keeps owned RAG; hosted stays a prototype flag in the ADR (A.6).

**What you learned:** owned RAG is CI-honest; hosted file_search is lock-in unless you accept a prototype.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
