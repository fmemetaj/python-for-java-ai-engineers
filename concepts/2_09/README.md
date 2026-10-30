# 2.9 Streaming responses   [Analog: SSE / Flux — typed events] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_09/tests/test_skip.py` passes.

Official docs: [Migrate — streaming](https://platform.openai.com/docs/guides/migrate-to-responses) (`response.output_text.delta`, `response.completed`).

## 1. Concept

Streaming sends tokens as they are produced. Chat Completions uses chunk `delta`s. Responses uses **typed SSE events**. Reusing a Chat Completions chunk handler on Responses is a listed migration error.

## 2. Java version

```java
public class StreamDemo {
    public static void main(String[] args) {
        String[] events = {"response.output_text.delta", "response.completed"};
        for (String event : events) {
            System.out.println(event);
        }
    }
}
```

`Flux<ServerSentEvent<T>>` is the analog: branch on event name, assemble data.

## 3. Python version

```python
for event in fake.stream("summarize"):
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
```

`asyncio` here would be cooperative I/O, not a thread pool. FakeLLM just yields slices.

| Java | Python / API |
| --- | --- |
| `Flux<ServerSentEvent>` | iterator of `StreamEvent` |
| `event.name()` | `event.type` |
| `data` payload | `delta` / completed `response` |

## 4. Differences & pitfalls

| Java habit | Reality | Pitfall |
| --- | --- | --- |
| One `onNext(String)` | many event types | missing `response.completed` |
| Chat Completions `delta.content` | `response.output_text.delta` | empty UI |
| Blocking `readLine` | async iteration | stalling the event loop |

The fake cannot teach live time-to-first-token.

## 5. Exercise

Assemble deltas and recognize Responses event types.

```bash
uv run pytest concepts/2_09
```

- Hint 1: join `delta` for `response.output_text.delta` events.
- Hint 2: types starting with `response.` are Responses SSE names.
- Solution: `solutions/stream.py`.

## 6. Check

1. Name two Responses stream event types.
2. Why not reuse Chat Completions chunk handlers?
3. When is the FakeLLM stream finished?
4. Predict: last event type.

## Setup / troubleshooting

- Windows consoles may buffer `print(..., end="")`; tests join strings instead.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk can stream a fake answer into a terminal without a key.

**What you learned:** typed SSE events, not untyped chunks. Assemble deltas yourself.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
