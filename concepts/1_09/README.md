# 1.9 Mocking   [Analog: Mockito, WireMock] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_09/tests/test_skip.py` passes.

Official docs: [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html), [unittest.mock](https://docs.python.org/3/library/unittest.mock.html), [respx](https://lundberg.github.io/respx/), [httpx mock transport](https://www.python-httpx.org/advanced/transports/).

## 1. Concept

Patch the name **where it is looked up**, not where it was defined. Mockito's `when(svc.get()).thenReturn(...)` still needs the mock injected. Python's `monkeypatch.setattr("docsdesk.client.httpx", ...)` is the lookup-site rule. For HTTP, prefer a **fake transport** (`httpx.MockTransport` or respx) over patching `httpx.get` globally — that is WireMock for a single process.

## 2. Java version

```java
public class MockingDemo {
    interface HttpGet { String get(String url); }
    static String title(HttpGet http, String url) {
        return http.get(url);
    }
    public static void main(String[] args) {
        System.out.println(title(u -> "{\"title\":\"Auth\"}", "/pages/auth"));
    }
}
```

The lambda is a hand-rolled mock. Mockito would generate `HttpGet`. WireMock would bind a port.

## 3. Python version

```python
def fetch_title(get, url: str) -> str:
    return get(url)["title"]


def test_title():
    def fake_get(url: str) -> dict[str, str]:
        return {"title": "Authentication"}

    assert fetch_title(fake_get, "/pages/auth") == "Authentication"
```

DocsDesk's client takes an optional `httpx.Client` (constructor injection). Tests pass `MockTransport`. respx is available in the `dev` group when you want WireMock-style route stubs.

| Java | Python |
| --- | --- |
| Mockito `@Mock` + `@InjectMocks` | `monkeypatch` / `unittest.mock.patch` |
| Patch *the dependency of the class under test* | Patch `module_under_test.dependency` |
| WireMock | `httpx.MockTransport` or respx |
| `verify(mock, times(1))` | `call_count` on a `Mock` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Mock the interface, inject it | If the SUT did `from httpx import get`, patch `sot.get` not `httpx.get` | Tests pass, production still hits the network |
| WireMock on a port | In-process transport | Flaky ports on Windows CI |
| `anyString()` | `unittest.mock.ANY` | Over-loose assertions |
| Final classes hard to mock | Everything is patchable | Patching stdlib and hiding real bugs |

## 5. Exercise

Build the dotted lookup path, and `fetch_title` against an injected getter (the Mockito-style seam).

```bash
uv run pytest concepts/1_09
```

- Hint 1: `lookup_path("docsdesk.client", "httpx")` → `"docsdesk.client.httpx"`.
- Hint 2: `payload = get(url); return payload["title"]`.
- Solution: `solutions/mocking.py`.

## 6. Check

1. `client.py` has `import httpx`. Where do you patch `Client`?
2. Why is constructor injection of `httpx.Client` easier to test than a module-level `httpx.get`?
3. When would you choose respx over `MockTransport`?
4. Predict: patching `httpx.get` while the SUT used `from httpx import get`.

## Setup / troubleshooting

- **Network in tests:** graded tests must not call the internet. If they hang, you missed the mock transport.
- **Windows:** no extra privileges needed for `MockTransport` (it is in-process).
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk's `get_page` is tested with `MockTransport` returning fixture JSON. A 500 on the first two calls (1.12) still never leaves the process.

**What you learned:** patch the lookup site; prefer an injected client or MockTransport to a global monkeypatch.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
