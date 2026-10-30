# 0.11 Collections   [Analog: ArrayList/HashMap/HashSet/record] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_11/tests/test_skip.py` passes.

Related explainer: [notebook 01](../../notebooks/01_pythonic_essentials.ipynb).

## 1. Concept

The four everyday collections: `list` (ordered, mutable), `dict` (key → value, insertion-ordered), `set` (unique, unordered for equality purposes), `tuple` (ordered, immutable). They replace `ArrayList`, `HashMap`, `HashSet`, and an immutable `List` / record-like row.

## 2. Java version

```java
import java.util.List;
import java.util.Map;
import java.util.Set;

public class CollectionsDemo {
    public static void main(String[] args) {
        var levels = List.of("INFO", "ERROR", "INFO");
        var unique = Set.copyOf(levels);
        var counts = Map.of("INFO", 2, "ERROR", 1);
        System.out.println(unique.size() + counts.get("INFO"));
    }
}
```

## 3. Python version

```python
levels = ["INFO", "ERROR", "INFO"]
unique = set(levels)  # {"INFO", "ERROR"}
counts = {"INFO": 2, "ERROR": 1}
row = ("ERROR", 1)  # tuple: immutable pair
```

| Java | Python |
| --- | --- |
| `ArrayList` | `list` — `[]` |
| `HashMap` (no order until later JDKs) | `dict` — insertion-ordered since 3.7 |
| `HashSet` | `set` |
| `List.of` / record | `tuple` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `map.get(k)` returns `null` | `d[k]` raises `KeyError`; `d.get(k)` returns `None` | Treating missing and `None` value as the same |
| `list.get(0)` | `items[0]`; negative index `items[-1]` is last | `items[len(items)]` is `IndexError` |
| `new HashSet<>(list)` uniqueness | `set(list)` loses order | Need unique-in-order → `list(dict.fromkeys(items))` |
| Mutable record fields | `tuple` cannot change; lists inside it still can | `t[0].append(1)` mutates the inner list |
| `Map` iteration = entries | `for k in d` yields **keys** | Forgot `.items()` |

## 5. Exercise

Port a Java `for` + `Map` aggregation: `count_levels`, plus `unique_in_order` and `pair_as_tuple`.

```bash
uv run pytest concepts/0_11
```

- Hint 1: `counts[level] = counts.get(level, 0) + 1` or `collections.Counter`.
- Hint 2: `dict.fromkeys(items)` keeps first-seen order; `tuple((level, count))`.
- Solution: `solutions/collections.py`.

## 6. Check

1. `{"a": 1, "b": 2}` iteration order?
2. `d["missing"]` vs `d.get("missing")`?
3. Is `("ERROR",)` a one-element tuple or a string in parentheses?
4. Why is `set(["INFO", "ERROR", "INFO"])` length 2?

**Real scenario:** DocsDesk counts log levels into a `dict` and freezes a `(level, count)` tuple for a report row.

**What you learned:** dicts remember insertion order; tuples are immutable rows; `[]` vs `{}` vs `set()` vs `()`.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
