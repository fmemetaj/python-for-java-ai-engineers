# 2.5 Provider abstraction (fake/ollama/openai)   [Analog: Interface + Spring profiles / @Primary test bean] [cost: mock] [~30 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_05/tests/test_skip.py` passes.

Official docs: [Responses](https://platform.openai.com/docs/guides/migrate-to-responses). Ollama stays loopback-only in this course.

## 1. Concept

`LLMClient` is a **Protocol** (Java `interface`). `get_client()` picks `fake`, `ollama`, or `openai` from env — Spring profiles / `@Primary` on a test stub. Graded work always uses **fake**.

## 2. Java version

```java
public class ProviderDemo {
    public static String client(String profile) {
        if ("test".equals(profile) || "fake".equals(profile)) {
            return "FakeLLM";
        }
        return "LiveClient";
    }
    public static void main(String[] args) {
        System.out.println(client("fake"));
    }
}
```

## 3. Python version

```python
def get_client(provider=None) -> LLMClient:
    name = (provider or os.environ.get("LLM_PROVIDER") or "fake").lower()
    if name == "fake":
        return FakeLLM()
```

| Java | Python |
| --- | --- |
| `interface LLMClient` | `Protocol` |
| `@Profile("test")` `@Primary` | `LLM_PROVIDER=fake` |
| WireMock | FakeLLM fixtures |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall |
| --- | --- | --- |
| Missing profile fails startup | A typo in env becomes a live call if you default wrong | Surprise bills |
| Assistants bean in old samples | Sunset 2026-08-26 | Copy-paste from old blogs |
| One prod profile | `openai` *and* `ollama` are both "not fake" | CI must refuse both |

## 5. Exercise

Resolve the provider, list valid names, and mark live providers as opt-in.

```bash
uv run pytest concepts/2_05
```

- Hint 1: valid = fake, ollama, openai. Default fake.
- Hint 2: live means not fake.
- Solution: `solutions/provider.py`.

## 6. Check

1. What does `@Primary` on a test bean correspond to?
2. Why does `get_client("openai")` raise in this repo?
3. Is Ollama a graded provider?
4. Predict: `LLM_PROVIDER=Assistants` → ?

## Setup / troubleshooting

- Keep `LLM_PROVIDER=fake` in `.env`.
- Ollama: loopback `127.0.0.1` only, never a cloud URL in course code.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk CI is the `fake` profile. A teammate's paid key stays on their laptop.

**What you learned:** Protocol + env profile. Fake is default. Live is explicit.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
