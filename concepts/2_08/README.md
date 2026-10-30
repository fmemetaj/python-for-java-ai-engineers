# 2.8 Conversation state and context trimming   [Analog: HTTP session state] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_08/tests/test_skip.py` passes.

Official docs: [Conversation state](https://platform.openai.com/docs/guides/conversation-state), [Migrate](https://platform.openai.com/docs/guides/migrate-to-responses).

## 1. Concept

Three ways to keep a DocsDesk thread: **manual replay** of Items/messages, **`previous_response_id`** (with `store: true`), or the **Conversations API**. All prior input tokens remain billed. When the window fills, **trim** oldest turns (or summarize — a later skill).

## 2. Java version

```java
public class SessionDemo {
    public static void main(String[] args) {
        int turn1 = 400;
        int turn2 = 400 + turn1;
        System.out.println(turn1 + turn2);
    }
}
```

`HttpSession` stores server-side state. It does not make the next HTTP body free. Neither does `previous_response_id`.

## 3. Python version

```python
first = fake.complete(q1, store=True)
second = fake.complete(q2, previous_response_id=first.id, store=True)
# second.usage.input_tokens includes first's input
trim_oldest(messages, budget=200)
```

| Java | Python / API |
| --- | --- |
| `HttpSession` | `previous_response_id` + `store` |
| Resend POST body | manual Item replay |
| Filter a chat log | `trim_oldest` |

## 4. Differences & pitfalls

| Java habit | Reality | Pitfall |
| --- | --- | --- |
| Session id is cheap | billed input grows every turn | "why did my bill triple" |
| Filter list in place | slices copy; keep the latest question | dropping the current user turn |
| `store=true` default | ZDR orgs must `store: false` | compliance surprises |

## 5. Exercise

1. Trim oldest messages until the budget fits (keep the last turn).
2. Compute billed input for a chain: stored and replayed are the same sum.

```bash
uv run pytest concepts/2_08
```

- Hint 1: while len>1 and total tokens > budget, `pop(0)`.
- Hint 2: billed input on turn i is the running sum of prompt sizes.
- Solution: `solutions/trim.py`, `solutions/state.py`.

## 6. Check

1. Name the three state strategies.
2. Does stored state waive input fees?
3. What should a trimmer never drop?
4. Predict usage.input_tokens on turn 3 if each new question is 100 tokens and you replay.

## Setup / troubleshooting

- FakeLLM only honors `previous_response_id` when the earlier call used `store=True`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk `DeskSession` stores ids and still prints a larger `tokens in=` on the follow-up.

**What you learned:** session ≠ free tokens. Trim to fit the window.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
