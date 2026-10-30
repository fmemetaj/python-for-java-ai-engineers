# 1.8 pytest   [Analog: JUnit 5, @BeforeEach, @ParameterizedTest] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_08/tests/test_skip.py` passes.

Official docs: [pytest](https://docs.pytest.org/).

## 1. Concept

pytest collects functions named `test_*` in files named `test_*.py`. Assertions are a plain `assert`. Fixtures are injected **by parameter name**. `@pytest.mark.parametrize` is `@ParameterizedTest`. There is no `Assertions.assertEquals`.

## 2. Java version

```java
public class TestingDemo {
    static void assertEquals(int expected, int actual) {
        if (expected != actual) {
            throw new IllegalStateException("not equal");
        }
    }
    public static void main(String[] args) {
        assertEquals(2, "ab".length());
    }
}
```

JUnit 5 would use `@Test`, `@BeforeEach`, `@ParameterizedTest`, and `Assertions.assertEquals`. This snippet stays on the JDK so CI can compile it.

## 3. Python version

```python
import pytest


@pytest.fixture
def client():
    with DocsClient(Settings(_env_file=None)) as c:
        yield c


@pytest.mark.parametrize("slug", ["auth", "tickets"])
def test_pages(client, slug):
    assert client.get_page(slug).slug == slug
```

| Java | Python |
| --- | --- |
| `@Test` | `def test_...` |
| `@BeforeEach` | `@pytest.fixture` (function scope) |
| `@ParameterizedTest` + `@CsvSource` | `@pytest.mark.parametrize` |
| `Assertions.assertEquals(a, b)` | `assert a == b` |
| `@ExtendWith(MockitoExtension.class)` | `monkeypatch` fixture (next concept) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `assertEquals(expected, actual)` order | `assert actual == expected` | Reading pytest diffs backwards |
| Injection by **type** (`@Autowired`) | Injection by **name** | Fixture `client` vs parameter `docs_client` → `FixtureLookupError` |
| Surefire method names any | collection is name-based | `def check_auth` is silently skipped |
| One class per fixture set | fixtures compose across modules | Unexpected shared state in `scope="module"` |
| `assertEquals` on doubles | `assert a == b` for ints/strings; use `pytest.approx` for floats | Flaky timeout tests |

## 5. Exercise

Translate JUnit annotations into pytest forms, and build parametrize case tuples.

```bash
uv run pytest concepts/1_08
```

- Hint 1: `@BeforeEach` → `@pytest.fixture`; `assertEquals` → `assert`.
- Hint 2: parametrize wants `[(slug,), ...]` so each row is a 1-tuple.
- Solution: `solutions/testing.py`.

## 6. Check

1. Why did pytest skip your `def should_load_auth` helper?
2. How does a test request the `tmp_path` fixture?
3. What JUnit feature is `@pytest.mark.parametrize`?
4. Predict: two tests both named `test_get_page` in different files — do they collide?

## Setup / troubleshooting

- **Collection errors:** a syntax error in `concepts/` is not collected unless you pass that path. Default `uv run pytest -q` uses `testpaths = ["tests"]`.
- **Windows:** `tmp_path` is a pathlib Path; open with `encoding="utf-8"`.
- **Slow tests:** this module is offline. If a test hangs, you omitted an httpx timeout (1.10).
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** translating a JUnit test class for DocsDesk. The `@BeforeEach` client becomes a fixture; the `@CsvSource` slugs become `parametrize`; Mockito waits until 1.9.

**What you learned:** pytest is JUnit with name-based fixtures and plain `assert`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
