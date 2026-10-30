# A.7 Pin, changelog, and compatibility   [Analog: Maven versions / Dependabot] [cost: mock] [~40 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/a_07/tests/test_skip.py` passes.

Official docs: [uv lock](https://docs.astral.sh/uv/concepts/projects/sync/), [Responses migration](https://platform.openai.com/docs/guides/migrate-to-responses). Fixture: `data/changelogs/sdk_fake.json`. Helper: `course_kit.upgrade`.

## 1. Concept

**Pinning** means the version you declared equals the version in the lockfile. **Changelogs** tell you which rows require `client.responses.create`. This course commits `uv.lock` and fails CI on drift (`uv sync --locked`).

## 2. Java version

```java
public class PinDemo {
    public static boolean pinOk(String declared, String locked) {
        return declared.equals(locked);
    }
    public static void main(String[] args) {
        System.out.println(pinOk("3.41.0", "3.41.0"));
        System.out.println(pinOk("3.41.0", "3.40.0"));
    }
}
```

Maven + a lock plugin / Dependabot PR: same idea. A version *range* in `pom.xml` without a lock is not reproducible.

## 3. Python version

```python
from course_kit.upgrade import load_changelog, pin_ok, requires_responses

pin_ok("3.41.0", "3.41.0")
requires_responses(load_changelog()[0])  # sunset → True
```

| Java | Python (this course) |
| --- | --- |
| `pom.xml` version | `pyproject.toml` range |
| `mvn versions:lock` / gradle lock | `uv.lock` |
| Dependabot PR | changelog fixture + this drill |
| `mvn -U` surprise | `uv sync` without `--locked` |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| SNAPSHOT of "latest SDK" | Latest OpenAI SDK can change request shapes | Lessons that silently use Assistants examples |
| Range `[,)` is fine in a leaf app | CI must `--locked` | "Works on my machine" after a PyPI publish |
| Changelog is optional reading | Sunset rows are **gates** | Shipping `beta.assistants` after 2026-08-26 |
| One BOM for the org | This repo pins in `uv.lock` | Editing pyproject and forgetting the lock |

## 5. Exercise

`pin_matches` and `needs_responses`.

```bash
uv run pytest concepts/a_07
```

- Hint 1: empty strings raise `ValueError`.
- Hint 2: `kind == "sunset"` or `"responses"` in `action`.
- Solution: `solutions/pin.py`.

## 6. Check

1. What does `uv sync --locked` refuse?
2. Why is a Maven range a partial analog?
3. Predict: changelog kind `sunset` → needs Responses?
4. Where does this repo store the fake changelog?
5. Did we publish a GitHub Release for this lesson?

## Setup / troubleshooting

- Stale lock: `uv lock` then commit both files. CI fails if they disagree.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** A.8 scans source; A.7 decides whether a changelog row is a migration.

**What you learned:** lockfile equality; sunset changelog rows point at Responses.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
