# 6.3 Performance: async concurrency, caching, timeouts   [Analog: Caffeine/@Cacheable, thread pools] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/6_03/tests/test_skip.py` passes.

Official docs: [asyncio.gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather), [httpx timeouts](https://www.python-httpx.org/advanced/timeouts/). DocsDesk: `docsdesk.cache.TtlCache`.

## 1. Concept

Three knobs that keep DocsDesk snappy **without** extra model calls: a **TTL cache** (Caffeine analog), a **timeout** (WebClient `responseTimeout`), and **concurrent I/O** via `asyncio.gather`. `gather` is cooperative concurrent I/O (concept 0.29). It is not a thread pool and it does not make CPU work faster.

## 2. Java version

```java
public class CacheDemo {
    public static String cached(String key) {
        return "hit:" + key;
    }
    public static void main(String[] args) {
        System.out.println(cached("auth"));
        System.out.println(cached("auth"));
    }
}
```

You would annotate a Spring method `@Cacheable` and size the pool with Caffeine. Timeouts live on the `RestClient`/`WebClient` builder.

## 3. Python version

```python
cache = TtlCache(clock=now)
value, hit = cache.cache_get("auth", compute, ttl=30.0)
# hit True on the second call until clock() passes expires_at

assert is_timeout(elapsed=5.0, limit=5.0) is True
results = asyncio.run(gather_in_order([one(), two()]))  # order preserved
```

| Java | Python |
| --- | --- |
| `@Cacheable` + Caffeine TTL | `TtlCache` (in-process dict + `expires_at`) |
| `ExecutorService.invokeAll` | `asyncio.gather` (cooperative I/O, not threads) |
| WebClient `responseTimeout` | `is_timeout` / httpx `timeout=` |
| Redis as the cache | Not in this lesson — keep it a dict |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `@Cacheable` forever | TTL is part of the contract | Stale answers after a prompt change |
| `parallelStream` / fork-join | `gather` still uses **one** thread until a await | Assuming gather speeds a cosine loop |
| Timeout only on connect | httpx default used to be "no timeout" | Hung CI if you skip `timeout=` (Module 1 already set 5s) |
| Cache the secret | Cache the **answer**, still redact logs | TTL cache becomes a secret store |

## 5. Exercise

Implement `cache_get` (clock + TTL), `is_timeout`, and `merge_in_order`.

```bash
uv run pytest concepts/6_03
```

- Hint 1: on miss, call `compute()`, store `now + ttl`.
- Hint 2: `elapsed >= limit` is a timeout, including equality.
- Solution: `solutions/perf.py`.

## 6. Check

1. After TTL expiry, is the next call a hit or a miss?
2. Does `asyncio.gather` make numpy cosine faster?
3. Predict: `is_timeout(5, 5)`.
4. Why does ProductionDesk cache by question string, not by request id?

## Setup / troubleshooting

- **Event loop already running** (Jupyter): `asyncio.run` fails. Concept tests are `.py` files; use `await` in a notebook cell instead.
- **Windows:** `asyncio` ProactorEventLoop is fine here; we do not open sockets.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** ProductionDesk's second identical question is a cache hit (`cost_usd` 0, `cached: true`). Timeouts on the docs HTTP client remain 5s (Module 1).

**What you learned:** TTL cache, timeouts as deadlines, gather as cooperative I/O.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
