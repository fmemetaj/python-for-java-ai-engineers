# 0.22 Protocol and ABCs   [Analog: interface, abstract class] [cost: mock] [~35 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_22/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

A `Protocol` describes a **structural** type: if your class has the methods, it matches, even if it never subclasses the Protocol. An **ABC** (`abc.ABC`) is **nominal**: you inherit it (or register). pyright uses Protocols to catch mismatches the interpreter will not.

## 2. Java version

```java
public class ProtocolDemo {
    interface Retriever {
        String search(String query);
    }
    static class Memory implements Retriever {
        public String search(String query) { return query; }
    }
    public static void main(String[] args) {
        Retriever r = new Memory();
        System.out.println(r.search("login"));
    }
}
```

`implements Retriever` is required for the variable type. Extra classes that happen to have `search` are not `Retriever`s.

## 3. Python version

```python
class Retriever(Protocol):
    def search(self, query: str) -> list[str]: ...


class MemoryRetriever:
    def search(self, query: str) -> list[str]:
        return [query]


def top_hit(retriever: Retriever, query: str) -> str | None:
    hits = retriever.search(query)
    return hits[0] if hits else None
```

`MemoryRetriever` does **not** subclass `Retriever`. pyright still type-checks `top_hit(MemoryRetriever(), "login")`.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `implements I` is required | Protocol is structural | A typo `searh` is only caught by pyright, not by `javac` |
| Abstract class forces override | ABC raises if you instantiate without implementing | Mixing ABC *and* Protocol without a reason |
| One interface file per type | Protocols live next to the function | Over-wide Protocol (`**kwargs: Any`) hides mistakes |
| Runtime `instanceof I` | `isinstance(x, Retriever)` needs `@runtime_checkable` | Bare Protocol fails `isinstance` |

## 5. Exercise

Implement `MemoryRetriever.search` and `top_hit` in `exercises/protocol.py`. A second class in the tests has `search` and must work **without** inheriting `Retriever`.

```bash
uv run pytest concepts/0_22
```

- Hint 1: `[doc for doc in self.docs if query in doc]`.
- Hint 2: `return hits[0] if hits else None`.
- Solution: `solutions/protocol.py`.

## 6. Check

1. Does `MemoryRetriever` have to inherit `Retriever` for pytest to pass?
2. Who complains if `search` returns `str` instead of `list[str]` — pytest, pyright, or both?
3. When would you use an ABC instead of a Protocol?
4. Why does DocsDesk's tool registry use a Protocol (see the 0B deliverable)?

## Setup / troubleshooting

- Run `uv run pyright` after the exercise. pytest can be green while pyright flags a structural mismatch — that is the point.
- Select `.venv` or pyright uses the wrong Python and reports missing `pydantic`.

Docs: [typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol), [abc](https://docs.python.org/3/library/abc.html).

**Real scenario:** replace a Java `interface Tool` with a Protocol so tests can pass a fake tool without a shared base class.

**What you learned:** Protocol = structural (pyright); ABC = nominal (inheritance).

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
