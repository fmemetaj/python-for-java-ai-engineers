# 0.29 GIL and the asyncio event loop   [NEW — no Java equivalent] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/0_29/tests/test_skip.py` passes. **Still recommended.**

Related explainer: [notebook 03](../../notebooks/03_async_streaming.ipynb).

## 1. Concept

`asyncio` is **cooperative concurrent I/O on one thread**. `async def` creates a coroutine. `await` pauses it until something is ready. `asyncio.gather` runs many coroutines by interleaving their waits. It is **not** automatic multithreading and **not** CPU parallelism. The GIL still applies; `gather` does not make a tight Python loop faster.

## 2. Intuition

One event loop, one thread, many paused tasks. A task runs until it `await`s. While it waits (sleep, socket, HTTP), the loop starts another task. Nobody is preempted in the middle of a CPU loop — that is why a `for` over a million ints blocks **everyone**.

```
gather(lookup("kb"), lookup("user"))
   lookup kb  ----await sleep----  return
   lookup user ----await sleep---- return
   (the two waits overlap)
```

## 3. Why it exists

LLM calls, HTTP, and databases spend most of their time waiting. Java might use `CompletableFuture`, WebFlux, or a thread pool. Those are preemptive or thread-based. `asyncio` stays on one thread and asks you to `await` every wait. Fewer threads, no stack per request — but a forgotten `await` or a CPU-heavy function stalls the whole process.

### The Java analogy that misleads you

`CompletableFuture` / WebFlux look like `async`/`await`. They are **partial** analogs. A Java future can run on a thread pool and actually use extra cores for CPU work. `asyncio.gather` will not. WebFlux is reactive streams; asyncio is cooperative tasks on one loop. If you write `time.sleep(1)` inside a coroutine (blocking sleep), you freeze the loop — the equivalent of calling `Thread.sleep` on Netty's event thread.

## 4. Step-by-step examples

**Example 1 — `async def fake_lookup` + `await asyncio.sleep(0)`.** Sleep 0 yields, then returns. No real clock needed for tests.

**Example 2 — `asyncio.run(main())` in a `.py` file.** Notebooks may allow top-level `await`; scripts must not.

**Example 3 — `gather` keeps argument order.** `gather(a, b, c)` returns `[A, B, C]` even if `b` finishes first.

**Example 4 — overlap counter.** Ten tasks increment a shared `running` count, wait on an `Event`, and you observe `peak == 10`. That is concurrency, not parallelism.

**Example 5 — CPU does not get faster.** A pure-Python loop of `sum(range(n))` inside a coroutine holds the loop. Use processes or native code for CPU; use asyncio for I/O. Threads (0.28) also overlap I/O but with a GIL and a stack per thread.

```bash
uv run python concepts/0_29/examples.py
```

Docs: [asyncio](https://docs.python.org/3/library/asyncio.html).

## 5. Common pitfalls

- Forgetting `await` — you get a coroutine object, not a result.
- `time.sleep` instead of `asyncio.sleep`.
- Assuming `gather` uses extra cores.
- Nested `asyncio.run` (it is already running in pytest-asyncio style tests we avoid; here tests call `asyncio.run` once).
- Notebook vs script: copy-pasting `await gather(...)` into `examples.py` without `asyncio.run`.
- Windows: the default loop differs; `asyncio.run` still works. Set `PYTHONUTF8=1` if you print non-ASCII.

## 6. Exercises

1. **Guided:** `fake_lookup` and `gather_names` (order-preserving).
2. **Open:** `max_concurrent(count)` — return the peak number of overlapping tasks (should equal `count`).

```bash
uv run pytest concepts/0_29
```

- Hint 1: `await asyncio.sleep(0)` then `return name`. `gather(*[fake_lookup(n) for n in names])`.
- Hint 2: share `running` / `peak`; `await` an `asyncio.Event` that the last starter sets.
- Solution: `solutions/asyncio_loop.py`.

## 7. Check

1. Does `gather` of ten CPU-bound coroutines use ten cores?
2. Why is `CompletableFuture` a misleading analog?
3. Top-level `await` in a notebook vs `asyncio.run` in a module — which for `examples.py`?
4. When would you still pick `ThreadPoolExecutor` (0.28) over asyncio?

## Setup / troubleshooting

- **Notebook kernel:** select `.venv`. Top-level `await` works in Jupyter; this lesson's tests are `.py` files.
- **Windows / macOS / Linux:** `asyncio.run` is the portable entry point. Do not instantiate a loop by hand.
- **PATH:** `uv run pytest concepts/0_29` from the repo root.

**Real scenario:** DocsDesk runs ten fake I/O lookups with `asyncio.gather` (see `prepare_reply` in `mini_agent`). That overlap is I/O. Embedding a large numpy loop inside those coroutines would not go faster.

**What you learned:** asyncio is cooperative concurrent I/O on one thread; it does not make CPU code faster, and it is not Java's thread-pool future.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
