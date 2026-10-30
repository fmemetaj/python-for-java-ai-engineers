# 2.1 LLM client (SDK) configured from env   [Analog: RestTemplate/WebClient bean] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/2_01/tests/test_skip.py` passes.

Official docs: [Python SDK](https://platform.openai.com/docs/libraries), [Responses](https://platform.openai.com/docs/guides/migrate-to-responses).

## 1. Concept

An **LLM client** is an HTTP SDK object, not a magic runtime. Configure it from environment variables (`LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`) the way a Spring `RestClient` bean is configured from `application.yml`. The default provider is **`fake`**: no network, no bill.

## 2. Java version

```java
public class LlmClientDemo {
    public static void main(String[] args) {
        String profile = System.getenv().getOrDefault("LLM_PROVIDER", "fake");
        String key = System.getenv().getOrDefault("OPENAI_API_KEY", "");
        System.out.println(profile);
        System.out.println(key.length());
    }
}
```

You would expose a `RestClient` `@Bean` that reads the key from env and never logs it.

## 3. Python version

```python
from course_kit.llm import get_client, responses_create_kwargs

fake = get_client("fake")
body = responses_create_kwargs(model="gpt-4.1-mini", instructions="...", input="...")
```

`get_client()` is the Spring profile switch. CI always uses `fake`. If you opt into live OpenAI, call **`client.responses.create`** — never the Assistants API (sunset 2026-08-26).

| Java | Python |
| --- | --- |
| `@Bean RestClient` | `OpenAI()` / `get_client()` |
| `application-test.yml` | `LLM_PROVIDER=fake` |
| `@Value` secret | env + `SecretStr`; never print |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| One `RestClient` bean | Easy to construct a new client per call | Lost timeouts; keys in traces |
| Profiles compiled in | Env read at process start | Forgetting `.env.example` → `.env` |
| Access logs strip `Authorization` | `print(settings)` can leak | Keys in CI logs |
| SOAP/REST XML client | JSON SDK | Treating the SDK as a chatbot UI |

## 5. Exercise

Build the env-based provider string, the Responses request body (`input` + `instructions` + `store: false`), and a check that a key never appears in a log line.

```bash
uv run pytest concepts/2_01
```

- Hint 1: default provider is `fake` when the env value is missing or blank.
- Hint 2: Responses body uses `input`, not `messages`.
- Solution: `solutions/client.py`.

## 6. Check

1. Where does the official Python SDK read `OPENAI_API_KEY` from?
2. Why is the Assistants API not in this course?
3. What goes in a Responses request instead of `messages`?
4. Predict: `LLM_PROVIDER` unset → which client?

## Setup / troubleshooting

- Copy `.env.example` to `.env`. Never commit `.env`.
- Doctor prints `OPENAI_API_KEY set: true/false`, never the value.
- Windows: restart the editor after changing env vars.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk constructs the client once from `Settings` and answers a pasted auth page offline.

**What you learned:** the LLM SDK is a configured HTTP client. Default `fake`. Responses, not Assistants.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
