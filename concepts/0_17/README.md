# 0.17 Properties   [Analog: getters/setters, Lombok] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_17/tests/test_skip.py` passes.

Related explainer: [notebook 02](../../notebooks/02_typing_pydantic.ipynb).

## 1. Concept

`@property` turns a method into an attribute lookup. Callers write `budget.dollars`, not `budget.getDollars()`. You add a setter only when assignment needs logic (validation, conversion). Most fields stay as plain `self.x`.

## 2. Java version

```java
public class PropertiesDemo {
    static class Budget {
        private int cents;
        int getCents() { return cents; }
        void setCents(int cents) { this.cents = cents; }
    }
    public static void main(String[] args) {
        var b = new Budget();
        b.setCents(199);
        System.out.println(b.getCents());
    }
}
```

Lombok `@Getter @Setter` generates the same boilerplate. Java callers still look like method calls.

## 3. Python version

```python
class Budget:
    def __init__(self, cents: int) -> None:
        self._cents = cents

    @property
    def dollars(self) -> float:
        return self._cents / 100

    @dollars.setter
    def dollars(self, value: float) -> None:
        self._cents = int(round(value * 100))
```

`budget.dollars` calls the getter. `budget.dollars = 2.5` calls the setter.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `getX()` / `setX()` on every field | Public attribute, property only when needed | A Java-in-Python class that is all getters |
| Lombok generates methods | `@property` is a real decorator (see 0.26) | Forgetting `@property` → `budget.dollars` is a function |
| Setter always exists | Read-only property has no setter | `budget.dollars = 1` raises `AttributeError` |
| `int` cents stay `int` | Division `/` returns `float` | `cents / 100` is `1.99`, not integer division |

## 5. Exercise

Implement `cents` and `dollars` on `Budget` in `exercises/properties.py`. Do **not** add `getCents`.

```bash
uv run pytest concepts/0_17
```

- Hint 1: `return self._cents / 100`.
- Hint 2: setter stores `int(round(value * 100))`.
- Solution: `solutions/properties.py`.

## 6. Check

1. Should a Python class named `Ticket` have `get_id()`?
2. `budget.dollars` with a `@property` — function or number?
3. What exception does assigning to a read-only property raise?
4. When is a plain `self.cents` better than a property?

## Setup / troubleshooting

- If pytest cannot collect `concepts/0_17`, you are not at the repo root (`uv run pytest concepts/0_17`).
- Encoding is not the issue here; interpreter selection is. Use `.venv` via `uv run`.

**Real scenario:** delete the getters/setters from a Java-style DocsDesk `Budget` and expose `dollars` as a property.

**What you learned:** attributes first; `@property` only when lookup needs code.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
