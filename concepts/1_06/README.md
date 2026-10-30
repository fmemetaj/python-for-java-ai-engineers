# 1.6 Logging   [Analog: SLF4J/Logback] [cost: mock] [~20 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/1_06/tests/test_skip.py` passes.

Official docs: [logging](https://docs.python.org/3/library/logging.html).

## 1. Concept

Use a **named logger** (`logging.getLogger(__name__)`) in library code, not `print`. Configure handlers once at the process edge (DocsDesk's `configure_logging`). A **redacting filter** strips secrets before anything hits a handler — the Logback "masking converter" analog.

## 2. Java version

```java
public class LoggingDemo {
    public static void main(String[] args) {
        System.out.println("Use a named logger, not System.out");
        System.out.println("Never log secrets");
    }
}
```

In a real service you would call `LoggerFactory.getLogger(DocsClient.class)` and never `System.out`.

## 3. Python version

```python
import logging

log = logging.getLogger(__name__)

log.info("provider=%s", settings.llm_provider)
# never: log.info("key=%s", settings.openai_api_key)
```

`docsdesk.logging_setup.RedactingFilter` replaces known secret values with `***` on the handler.

| Java | Python |
| --- | --- |
| SLF4J API | `logging.getLogger` |
| Logback.xml | dictConfig / programmatic handlers |
| MDC | `LoggerAdapter` / context vars (later modules) |
| `%logger` | `record.name` (`docsdesk.client`) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| `System.out.println` in a spike | `print` in a library module | pytest cannot assert on logs; secrets leak to stdout |
| DEBUG is "safe" | DEBUG is still stored/shipped | Keys in debug logs |
| One root logger | Child loggers propagate unless you stop them | Duplicate lines, or filters skipped |
| Parameterized `"{}", key` | `%s` lazy formatting | `f"key={secret}"` formats *before* the filter if you f-string the secret into `msg` — pass secrets as `args` **and** still redact |

## 5. Exercise

Return the logger name for a module, and redact secret substrings.

```bash
uv run pytest concepts/1_06
```

- Hint 1: `logger_name` is `__name__` (the string you were given).
- Hint 2: `str.replace(secret, "***")` for each non-empty secret.
- Solution: `solutions/logging_util.py`.

## 6. Check

1. Why is `logging.getLogger(__name__)` better than `print` in `docsdesk.client`?
2. If DEBUG is disabled in prod, is logging the API key still wrong?
3. Where should DocsDesk attach the redacting filter — logger or handler?
4. Predict: `log.info("key=%s", secret)` vs `log.info(f"key={secret}")` with a filter that only sees `record.msg`.

## Setup / troubleshooting

- **Windows consoles:** logging UTF-8 can garble in old `cmd.exe`. Use Windows Terminal; this repo sets `PYTHONUTF8=1` in CI.
- **pytest `caplog`:** it attaches its own handler. DocsDesk tests use a `StringIO` handler *with* the filter so assertions see the redacted text.
- More: [troubleshooting](../../docs/setup/troubleshooting.md).

**Real scenario:** a support engineer pastes DocsDesk logs into a ticket. If the OpenAI key was in a line, it is now in the ticket system. The redacting filter is the regression test in `tests/test_docsdesk.py`.

**What you learned:** module loggers, not print; redact secrets on the handler; never log keys even at DEBUG.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
