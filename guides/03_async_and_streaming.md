# 03 — Async and generators without mystery

Python's `asyncio` is well suited to **I/O-bound** work, such as calling remote LLMs, databases and APIs. Scheduling multiple coroutines does **not** automatically make CPU-heavy Python code execute on multiple cores.

```python
import asyncio

async def fetch(name):
    await asyncio.sleep(0.1)  # simulate network waiting
    return name

# Sequential (waits for the first result before starting the second):
a = await fetch("a")
b = await fetch("b")

# Concurrent I/O; gather returns results in argument order:
a, b = await asyncio.gather(fetch("a"), fetch("b"))
```

**Notebook vs ordinary script:** notebooks typically allow top-level `await`. In `.py` modules use `asyncio.run(main())` under `if __name__ == "__main__":`.

`asyncio.gather` propagates exceptions (unless `return_exceptions=True`) and does not enforce a timeout. Use explicit timeouts for external calls.

**Streaming:** A generator yields chunks lazily:

```python
def tokens():
    yield "Hello"
    yield " world"

for part in tokens():
    print(part, end="")
```

A real async API may return an **async iterator** using `async for`. Do not confuse a synchronous generator, an async generator, and a coroutine.

**Your test:** make three tasks sleep 0.3, 0.1 and 0.2 seconds. What is the result order from `gather`? Why?

[Return to guide index](README.md)
