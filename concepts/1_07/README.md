# 1.7 Config and secrets   [Analog: @ConfigurationProperties, application.yml] [cost: mock] [~25 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_07/tests/test_skip.py` passes.

Official docs: [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/), [python-dotenv](https://github.com/theskumar/python-dotenv). OpenAI env: [developer quickstart](https://platform.openai.com/docs/libraries).

## 1. Concept

Process configuration comes from **environment variables**, optionally loaded from a local `.env` file. `pydantic-settings` is `@ConfigurationProperties`: typed fields, defaults, validation. Secrets are `SecretStr`. The course default is `LLM_PROVIDER=fake` so nothing paid ever runs unless you opt in.

## 2. Java version

```java
public class ConfigDemo {
    public static void main(String[] args) {
        String profile = System.getenv().getOrDefault("APP_PROFILE", "test");
        System.out.println(profile);
    }
}
```

Spring would bind `application-test.yml` plus env overrides. Profiles ≈ `LLM_PROVIDER=fake|ollama|openai`.

## 3. Python version

```python
class Settings(BaseSettings):
    llm_provider: str = "fake"
    openai_api_key: SecretStr = SecretStr("")
```

`.env.example` lists **names** and is committed. `.env` lists **values** and is gitignored. Doctor prints `OPENAI_API_KEY set: true/false` and never the value.

If you opt into OpenAI later, the call is the **Responses API** (`client.responses.create`, body from `responses_create_kwargs`). The Assistants API was sunset on 2026-08-26 and is not used in this course. [Migrate to Responses](https://platform.openai.com/docs/guides/migrate-to-responses).

| Java | Python |
| --- | --- |
| `@ConfigurationProperties` | `BaseSettings` |
| `application.yml` + profile | `.env` + `LLM_PROVIDER` |
| `SPRING_DATASOURCE_PASSWORD` | `OPENAI_API_KEY` as `SecretStr` |
| never commit `application-prod.yml` with passwords | never commit `.env` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| YAML committed, secrets in a vault | `.env` on disk for local overrides | Copying `.env` into a gist or a PR |
| `@Value("${key}")` in logs via toString | `repr(settings)` can leak unless `SecretStr` | Keys in exception messages |
| Default profile `dev` hits a real DB | Default provider **must** be `fake` | Accidental billed calls in CI |
| `export` in `.bashrc` | Per-project `.env` | Sharing one key across every repo |

## 5. Exercise

Default provider `fake`, redact `KEY`/`SECRET`/`TOKEN` names, list files that must not be committed.

```bash
uv run pytest concepts/1_07
```

- Hint 1: `default_llm_provider()` returns `"fake"`.
- Hint 2: if `"KEY"` in `name.upper()`, return `"***"`. Never-commit list is `[".env"]`.
- Solution: `solutions/config.py`.

## 6. Check

1. What is the difference between `.env` and `.env.example`?
2. Why is `SecretStr` better than `str` for `openai_api_key`?
3. If `LLM_PROVIDER` is unset, which client does DocsDesk use?
4. Name one field that must **not** appear in a Responses request body (`assistant_id` is the trap).

## Setup / troubleshooting

- **Create `.env`:** `cp .env.example .env` and edit locally. Git already ignores `.env` and `.env.*` except `.env.example`.
- **Windows:** Notepad may save ANSI. Keep UTF-8. Git LF.
- **CI:** no `.env` file. Defaults + job env only. Never add `OPENAI_API_KEY` to GitHub Actions for this module.
- **Live OpenAI (optional, not graded):** set `LLM_PROVIDER=openai` and a key in `.env`. Use `responses.create`, not Assistants. Cost is yours; graded tests stay on `fake`.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** a learner commits `.env` "just this once". Secret scanning should reject it. The lesson's `files_never_commit()` is the habit; GitHub push protection is the backstop.

**What you learned:** env + pydantic-settings; `.env` never in git; default `fake`; Responses API if you ever opt into OpenAI.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
