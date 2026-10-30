# 1.12 Retries with backoff   [Analog: Spring Retry / Resilience4j] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_12/tests/test_skip.py` passes.

DocsDesk implements a small retry helper (no extra library). Later, the optional OpenAI SDK retries 408/429/5xx on its own — that is a different client.

## 1. Concept

Retry **transient** failures: HTTP 429, 5xx, timeouts. Do **not** retry 400 or 404 (the request is wrong). Wait longer after each failure (**exponential backoff**) so a stampeding herd does not melt the mock — or a real — server.

## 2. Java version

```java
public class RetryDemo {
    static boolean retry(int status) {
        return status == 429 || status >= 500;
    }
    public static void main(String[] args) {
        System.out.println(retry(503));
        System.out.println(retry(404));
    }
}
```

Spring Retry would wrap the same predicate with `@Retryable` and a backoff policy.

## 3. Python version

```python
def should_retry(status_code: int) -> bool:
    return status_code == 429 or status_code >= 500


def backoff_seconds(attempt: int, base: float) -> float:
    return base * (2**attempt)  # 0 → base, 1 → 2base, 2 → 4base
```

`run_with_retry` calls `fn`, catches `TransientError`, sleeps, and gives up after `attempts`. Tests inject a `sleeper` so CI does not wait.

| Java | Python |
| --- | --- |
| `@Retryable(backoff = @Backoff(delay = 50, multiplier = 2))` | `run_with_retry(..., base_delay=0.05)` |
| `Retry-After` header | not parsed here (keep the helper small) |
| Resilience4j `RetryConfig` | a 20-line function you can read |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Retry all exceptions | Retry only transients | Retrying a 400 with a bad JSON body |
| `@Retryable` hides the loop | You see the loop | Forgetting to re-raise on the last attempt |
| Jitter on by default in some libs | This helper is deterministic | Fine for tests; add jitter before production load |
| Retry on the HTTP client bean | DocsDesk retries in `DocsClient.get_page` | Double retry if httpx *and* your helper both retry |

## 5. Exercise

Implement `should_retry`, `backoff_seconds`, and `run_with_retry`.

```bash
uv run pytest concepts/1_12
```

- Hint 1: 429 and `>= 500` only.
- Hint 2: `base * (2 ** attempt)` with `attempt` starting at 0. Sleep only when you will try again.
- Solution: `solutions/retry.py`.

## 6. Check

1. Why not retry HTTP 404?
2. What are the first three delays when `base=0.05`?
3. Where does DocsDesk inject a no-wait sleeper in tests?
4. Predict: three failures, `attempts=3` — does the sleeper run twice or three times?

## Setup / troubleshooting

- **CI time:** never `time.sleep(1)` in graded tests. Inject `sleeper`.
- **Live OpenAI (optional):** the official SDK already retries some 429/5xx. Do not stack unbounded retries on top without a cap.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** the mock docs service returns 500 twice, then 200. `tests/test_docsdesk.py` asserts two sleeps and a successful `DocPage`. No network, no jitter, no paid API.

**What you learned:** retry transients with exponential backoff; 4xx stays a hard failure.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
