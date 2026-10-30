# 0.20 Inheritance and MRO   [Analog: extends / single inheritance] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_20/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

Python classes may list **multiple** bases. Method lookup follows the **MRO** (method resolution order), a linearization of the graph. `super()` does not mean "my parent class"; it means "the next class in the MRO of the original instance".

## 2. Java version

```java
public class InheritanceDemo {
    static class Tool {
        String tag() { return "tool"; }
    }
    static class Search extends Tool {
        @Override String tag() { return "search"; }
    }
    public static void main(String[] args) {
        System.out.println(new Search().tag());
    }
}
```

One superclass. `super.tag()` is that class.

## 3. Python version

```python
class Tool:
    def tag(self) -> str:
        return "tool"


class Search(Tool):
    def tag(self) -> str:
        return "search:" + super().tag()
```

`Search().tag()` → `"search:tool"`. With two bases, `class SearchWithMixin(Mixin, Search)`, `Mixin` is tried first.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Single `extends` | Multiple bases are legal | Diamond graphs; you must read `__mro__` |
| `super.method()` is the parent | `super()` is the next MRO entry | Cooperative mixins break if someone skips `super()` |
| `final` class | Anyone can subclass | Accidental override of `__init__` |
| Interface + class | Mixins are just classes | A mixin that stores state on `self` in a surprising order |

## 5. Exercise

Implement `Search.tag` with `super()`, and `mro_names(cls)`.

```bash
uv run pytest concepts/0_20
```

- Hint 1: `return "search:" + super().tag()`.
- Hint 2: `[item.__name__ for item in cls.__mro__]`.
- Solution: `solutions/inheritance.py`.

## 6. Check

1. `class C(A, B):` — which base is first in the MRO after `C`?
2. Does `super()` in `Search` always mean `Tool`?
3. Why does `SearchWithMixin().tag()` return `"mixin"` in the exercise?
4. When would you prefer composition over a mixin?

## Setup / troubleshooting

- Print `ClassName.__mro__` in the REPL (`uv run python`) when mixins surprise you.
- There is no extra install. If imports fail, you ran pytest from the wrong directory.

**Real scenario:** DocsDesk tools — prefer a `Protocol` (0.22) plus composition; use mixins only when `super()` cooperation is deliberate.

**What you learned:** multiple inheritance is real; `super()` follows the MRO.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
