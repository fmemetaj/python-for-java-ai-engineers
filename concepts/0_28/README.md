# 0.28 Threads and executors   [Analog: Thread, ExecutorService] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_28/tests/test_skip.py` passes.

Related explainer: [notebook 03](../../notebooks/03_async_streaming.ipynb).

## 1. Concept

`ThreadPoolExecutor` maps a function over items on worker threads, like Java's `ExecutorService`. Threads **overlap I/O waits**. They do **not** run Python bytecode in parallel on multiple cores: the **GIL** (global interpreter lock) allows only one thread to execute Python bytecode at a time. CPU-heavy loops need another process or a native extension, not more threads.

## 2. Java version

```java
import java.util.concurrent.Executors;

public class ThreadsDemo {
    public static void main(String[] args) throws Exception {
        try (var pool = Executors.newFixedThreadPool(2)) {
            var future = pool.submit(() -> "docs");
            System.out.println(future.get());
        }
    }
}
```

Java threads can run bytecode in parallel (no GIL). CPU-bound Java work *does* scale with cores.

## 3. Python version

```python
from concurrent.futures import ThreadPoolExecutor


def label(item: str) -> str:
    return item.upper()


with ThreadPoolExecutor(max_workers=2) as pool:
    out = list(pool.map(label, ["a", "b", "c"]))
```

`pool.map` preserves input order. Use `with` so the pool shuts down (0.25).

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Threads speed up CPU | GIL: CPU stays serial | A "parallel" JSON parser that is slower |
| `ExecutorService` for HTTP | Threads *do* help waiting on I/O | Mixing this with asyncio (0.29) without a plan |
| `synchronized` | `threading.Lock` | Mutating a shared list without a lock |
| Daemon threads | Interpreter exit kills them | Lost logs if you forget `with` / `join` |
| `Future.get()` | `f.result()` | Forgetting to handle the exception stored on the future |

## 5. Exercise

Implement `run_parallel(fn, items, max_workers=4)` with `ThreadPoolExecutor`, preserving order.

```bash
uv run pytest concepts/0_28
```

- Hint 1: `with ThreadPoolExecutor(...) as pool: return list(pool.map(fn, items))`.
- Hint 2: empty `items` → `[]` without creating a zero-worker pool.
- Solution: `solutions/threads.py`.

## 6. Check

1. Will ten threads hash a 2 GB file ten times faster in pure Python?
2. Will ten threads waiting on ten HTTP calls usually finish sooner?
3. Why is `pool.map` nicer than `submit` plus a list of futures for this exercise?
4. Next lesson: how is asyncio different from this pool?

## Setup / troubleshooting

- Tests must stay offline and fast; do not add real network calls.
- Windows: thread pools work the same; file locks in workers still need UTF-8 opens.
- macOS: no extra entitlements. If imports fail, it is PATH/venv, not threads.

Docs: [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html).

**Real scenario:** DocsDesk fan-out of fake I/O lookups — threads work; a CPU-bound embedding loop would not get faster.

**What you learned:** `ExecutorService` maps; the GIL breaks the CPU-parallelism part of the analogy.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
