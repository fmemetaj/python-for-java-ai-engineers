# 0.3 Variables   [Analog: typed locals / var] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_03/tests/test_skip.py` passes.

## 1. Concept

A Python name is a **label bound to an object**, not a typed stack slot. Assignment (`=`) rebinds the name. Calling a mutating method (`list.append`) changes the object that other names may still point at. Types are optional hints; they are not declarations the interpreter enforces.

## 2. Java version

```java
public class VariablesDemo {
    public static void main(String[] args) {
        var numbers = new java.util.ArrayList<Integer>();
        numbers.add(1);
        var alias = numbers;
        alias.add(2);
        numbers = new java.util.ArrayList<Integer>();
        System.out.println(alias.size());
    }
}
```

`alias` still refers to the list that has two elements after `numbers` is reassigned.

## 3. Python version

```python
numbers = [1]
alias = numbers
alias.append(2)
numbers = []
print(len(alias))  # 2
```

| Java | Python |
| --- | --- |
| `List<Integer> numbers = …` | `numbers = [1]` (optional `numbers: list[int]`) |
| Reassignment vs `list.add` | Same split: `=` rebinds; methods mutate |
| `var` infers a static type | No static type unless a type checker reads a hint |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Declare before use | First assignment creates the name | `NameError` if a branch never assigned |
| `final` / `var` documents mutability | Name rebinding is always allowed | Accidental `items = items + [x]` builds a new list |
| Two variables of different types | A name can be rebound to another type | `count = 0` then `count = "n/a"` hides a bug |
| `=` copies primitives | `=` never copies; it binds | `backup = tickets` then `tickets.clear()` empties `backup` |

## 5. Exercise

Implement `after_rebind` and `after_mutate` in `exercises/binding.py`.

```bash
uv run pytest concepts/0_03
```

- Hint 1: `alias = original` shares the object; `original = [0]` does not copy `alias`.
- Hint 2: `original.append(99)` is visible through every name bound to that list.
- Solution: `solutions/binding.py`.

## 6. Check

1. After `a = [1]; b = a; a = [2]`, what is `b`?
2. After `a = [1]; b = a; a.append(2)`, what is `b`?
3. Does `count: int = 0` prevent `count = "x"` at runtime?
4. Why is `NameError` closer to "uninitialized local" than to a compile error?

**Real scenario:** a DocsDesk cache alias (`cached = index`) is cleared when someone rebinds `index` vs when they call `index.clear()`.

**What you learned:** `=` rebinds a name; mutation changes a shared object.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
