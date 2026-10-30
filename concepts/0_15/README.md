# 0.15 Streams vs comprehensions/generators/itertools   [Analog: Stream API] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_15/tests/test_skip.py` passes.

## 1. Concept

Java `Stream` is a lazy pipeline (`filter` / `map` / `collect`). Python's usual replacement is a **comprehension** (eager, 0.13) or a **generator** (lazy, 0.14). `itertools` covers the rest (`islice`, `chain`, `groupby`). There is no `parallel()` stream in the standard library — do not look for one here.

## 2. Java version

```java
import java.util.List;

public class StreamsDemo {
    static List<Integer> highIds(List<Ticket> tickets) {
        return tickets.stream()
            .filter(t -> "high".equals(t.priority()))
            .map(Ticket::id)
            .toList();
    }
    record Ticket(int id, String priority) {}
    public static void main(String[] args) {
        System.out.println(highIds(List.of(new Ticket(1, "high"))));
    }
}
```

## 3. Python version (three ways)

```python
# 1. comprehension — default for a small, finished list
high_ids = [t["id"] for t in tickets if t["priority"] == "high"]

# 2. loop — when the condition grows
# 3. generator — when you might stop early or the source is huge
high_ids_gen = (t["id"] for t in tickets if t["priority"] == "high")
```

Prefer the comprehension when it stays on one line of intent. Prefer a named loop when a reviewer would have to parse nested clauses. Prefer a generator when laziness matters.

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `stream().filter.map.collect` | comprehension or genexp | People write 6-line nested comps to mimic a pipeline |
| `parallel()` | not in stdlib | Assuming threads will speed a comprehension (they will not) |
| Reuse a `List` | Reuse a list; do **not** reuse a generator | Second pass empty (0.14) |
| `findFirst()` | `next((x for x in xs if …), None)` | `next(...)` without default raises `StopIteration` |

## 5. Exercise

Rewrite the Java pipeline three ways: `high_priority_ids` (comprehension), `high_priority_ids_loop`, `high_priority_ids_gen`.

```bash
uv run pytest concepts/0_15
```

- Hint 1: same filter `ticket["priority"] == "high"`, same map `ticket["id"]`.
- Hint 2: the generator version must return an iterator, not a list.
- Solution: `solutions/streams.py`.

## 6. Check

1. Which of the three ways is lazy?
2. Why is there no `tickets.stream().parallel()` equivalent in this lesson?
3. When is a 3-line `for` loop more professional than a comprehension?
4. Can you `len()` a generator expression?

**Real scenario:** DocsDesk picks high-priority ticket ids for a triage queue. The sample is tiny → comprehension. A 10 GB export → generator.

**What you learned:** Streams map to comprehensions first, generators when lazy, loops when messy. No parallel streams.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
