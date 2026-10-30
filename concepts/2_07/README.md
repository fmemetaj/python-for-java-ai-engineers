# 2.7 Chat Completions vs Responses API   [Analog: Stateless REST vs server-side session] [cost: mock] [~75 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_07/tests/test_skip.py` passes.

Official docs: [Migrate to Responses](https://platform.openai.com/docs/guides/migrate-to-responses). Assistants API sunset **2026-08-26**.

## 1. Concept

**Chat Completions** (`POST /v1/chat/completions`) is the previous standard: `messages[]` in, `choices[i].message.content` out. **Responses** (`POST /v1/responses`) is recommended for new work: `input` + `instructions` in, typed `output[]` Items out, helper `output_text`. Same task, both shapes, in this lesson.

## 2. Java version

Items ≈ a Java 21 sealed hierarchy. Chat Completions ≈ a stateless REST DTO with a `List<Message>`.

```java
public class ResponsesDemo {
    sealed interface Item permits MessageItem, ReasoningItem {}
    record MessageItem(String text) implements Item {}
    record ReasoningItem(int tokens) implements Item {}
    public static void main(String[] args) {
        Item item = new MessageItem("hi");
        String out = switch (item) {
            case MessageItem m -> m.text();
            case ReasoningItem r -> "";
        };
        System.out.println(out);
    }
}
```

## 3. Python version

```python
client.chat.completions.create(model=..., messages=[{"role": "user", "content": q}])
client.responses.create(model=..., input=q, instructions=..., store=False)
```

| Aspect | Chat Completions | Responses |
| --- | --- | --- |
| Input | `messages[]` | `input` + `instructions` |
| Output | `choices[].message` | typed `output[]` Items |
| State | resend transcript | replay Items, `previous_response_id`, or Conversations API |
| Streaming | `delta` chunks | typed SSE events |
| Structured out | `response_format` | `text.format` |
| Storage | stored by default for new accounts | stored by default; `store: false` |

Cost implication: `previous_response_id` does **not** waive prior input tokens.

## 4. Differences & pitfalls

| Java habit | Python / API reality | Pitfall |
| --- | --- | --- |
| One JSON DTO | Items are a union (`message`, `reasoning`, …) | `output[0]` is not always a message |
| Session id = free context | billed input still includes the chain | surprise 3× bill (2.6 / 2.8) |
| Jackson `choices` | `output_text` helper | reading `choices` on a Response |
| Old Assistants SDK | sunset | `assistant_id` in new code |

Common migration errors (official checklist): `choices[0].message.content` instead of `output_text`; treating every output row as a message; dropping reasoning items; `response_format` instead of `text.format`; Chat Completions stream handlers on Responses events; assuming stored state is free.

## 5. Exercise

1. Migrate a Chat Completions body to Responses (`store: false`, system → `instructions`).
2. Extract text from either shape; flag migration-error snippets.

```bash
uv run pytest concepts/2_07
```

- Hint 1: system role becomes top-level `instructions`; a single user message can become string `input`.
- Hint 2: Responses text is `output_text` or message content parts; Chat Completions is `choices[0].message.content`.
- Solution: `solutions/migrate.py`, `solutions/errors.py`.

## 6. Check

1. Name three differences between the APIs.
2. Name one cost implication of `previous_response_id`.
3. Where did `n` (multiple choices) go in Responses?
4. Predict: `assistant_id` in a Responses call?

## Setup / troubleshooting

- The fake returns both shapes without a key.
- If a blog shows `openai.ChatCompletion.create`, that is SDK 0.x — ignore it.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk speaks Responses. A vendor SDK still on Chat Completions can be migrated with the checklist, not rewritten as Assistants.

**What you learned:** Responses is the current API; Chat Completions remains supported; Assistants is gone; stored state still bills input.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
