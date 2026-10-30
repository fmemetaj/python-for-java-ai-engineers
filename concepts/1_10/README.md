# 1.10 HTTP with httpx   [Analog: RestTemplate/RestClient, WebClient] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_10/tests/test_skip.py` passes.

Official docs: [httpx](https://www.python-httpx.org/), [timeouts](https://www.python-httpx.org/advanced/timeouts/).

## 1. Concept

**httpx** is the HTTP client DocsDesk uses. Sync `httpx.Client` ≈ Spring `RestClient` / `RestTemplate`. `httpx.AsyncClient` ≈ `WebClient`. Always set a **timeout**. httpx's default is 5 seconds; the older `requests` library default is *no timeout* (hang forever). CI and learners use `MockTransport`, so this lesson is offline.

## 2. Java version

```java
public class HttpDemo {
    public static void main(String[] args) {
        System.out.println("RestClient timeout 5s");
        System.out.println("GET /pages/auth");
    }
}
```

You would configure `RestClient.Builder` with connect and read timeouts, then `GET /pages/auth`.

## 3. Python version

```python
timeout = httpx.Timeout(5.0)
with httpx.Client(base_url=url, timeout=timeout, transport=transport) as client:
    payload = client.get("/pages/auth").json()
```

Async:

```python
async with httpx.AsyncClient(timeout=timeout, transport=transport) as client:
    response = await client.get("/pages/auth")
```

`asyncio` here is cooperative concurrent I/O, not a thread pool and not CPU parallelism.

| Java | Python |
| --- | --- |
| `RestClient` | `httpx.Client` |
| `WebClient` + `Mono` | `httpx.AsyncClient` + `await` |
| `setConnectTimeout` / `setReadTimeout` | `httpx.Timeout(...)` |
| `ResponseEntity<T>` | `response.json()` then Pydantic (1.11) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Timeouts configured on the factory bean | Easy to construct `httpx.get(url)` with the 5s default — or `Timeout(None)` | Hanging tests; hanging production |
| `RestTemplate` is sync-only | Mixing `httpx.get` inside `async def` blocks the event loop | "Async" code that is still serial |
| Connection pool on the bean | Create **one** `Client` and reuse it | A new client per call leaks sockets on Windows |
| Jackson on the RestClient | `response.json()` is untyped until Pydantic | `KeyError` on missing fields |

## 5. Exercise

Read a timeout, GET JSON with `raise_for_status`. Tests use `MockTransport` (no network).

```bash
uv run pytest concepts/1_10
```

- Hint 1: `timeout.read` is the read timeout; refuse `None`.
- Hint 2: `response = client.get(path); response.raise_for_status(); return response.json()`.
- Solution: `solutions/http_client.py`.

## 6. Check

1. What is httpx's default timeout? What is requests' default?
2. Why does DocsDesk pass `timeout=` even on the mock transport?
3. When would you use `AsyncClient` instead of `Client`?
4. Predict: `await client.get` vs `client.get` inside `async def`.

## Setup / troubleshooting

- **SSL/proxy:** live calls (optional) honor `HTTPS_PROXY` and `SSL_CERT_FILE`. Graded tests never go live.
- **Windows:** close the client (`with` / `.close()`) or pytest may warn about unclosed transports.
- **macOS localhost vs `127.0.0.1`:** fixture hostname is `docs.internal.test` and never resolves — the transport intercepts.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk fetches `/pages/auth` through `MockTransport` in CI and through the same client class a learner might later point at a real Spring docs site (optional, not graded).

**What you learned:** httpx Client ≈ RestClient; always set timeouts; async is cooperative I/O.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
