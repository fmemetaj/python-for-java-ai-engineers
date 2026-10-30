# 7.7 Portfolio README and five-minute demo   [Analog: product README / architecture.md] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/7_07/tests/test_skip.py` passes.

Official docs: [uv](https://docs.astral.sh/uv/). DocsDesk files: `modules/7-capstone/PORTFOLIO.md`, `docsdesk.portfolio.print_portfolio`.

## 1. Concept

The **portfolio README** is the first file a hiring manager opens. It has to say how to run offline, what the architecture is, what the evals scored, what 100 requests cost, what you fear, and what you will *not* claim. The **demo** is five minutes, simulated, on FakeLLM.

## 2. Java version

```java
public class ReadmeDemo {
    public static String[] sections() {
        return new String[] {"overview", "build", "run"};
    }
    public static void main(String[] args) {
        System.out.println(String.join(",", sections()));
    }
}
```

A Spring repo that only says "mvn spring-boot:run" is incomplete. You still want tests, limits, and how to build without a VPN.

## 3. Python version

```python
from docsdesk.portfolio import demo_minutes, print_portfolio, readme_sections

assert demo_minutes() == 5
assert "limitations" in readme_sections()
print_portfolio()
```

| Java | Python |
| --- | --- |
| `README.md` + `architecture.md` | the same files, plus eval/cost/threat sections |
| `mvn -q test` | `uv sync --locked && uv run pytest -q` |
| `application.yml` profiles | `LLM_PROVIDER=fake` |
| Demo day on a staging cluster | `uv run docsdesk v1` on a laptop, no deploy |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Hide known bugs until the onsite | List limitations next to the eval score | Interviewer finds FakeLLM and thinks you lied |
| Record a 25-minute walkthrough | Five minutes | Nobody watches |
| Paste `OPENAI_API_KEY` into README "for convenience" | `.env.example` only | Secret scan / leaked billing |
| Assistants playground as the demo | Responses + your loop | Sunset API on camera |

## 5. Exercise

Return README sections, `demo_minutes() == 5`, and a self-assessment list that mentions citations, approval, 30 cases, and secrets.

```bash
uv run pytest concepts/7_07
```

- Hint 1: sections include `limitations` and `demo`.
- Hint 2: join the checklist and look for `30`, `citation`, `approval`, `secret`.
- Solution: `solutions/readme.py`.

## 6. Check

1. Name two README sections a Spring README often skips that this capstone cannot.
2. How long is the demo?
3. Predict: you export a live key for the recording. What should the voice-over say?
4. Did `uv run docsdesk v1` send email?

## Setup / troubleshooting

- Clean clone check: `uv sync --locked --group dev` then `uv run docsdesk v1`.
- PATH / Store stub / WSL mixing: [troubleshooting](../../docs/setup/troubleshooting.md).
- Recording: say out loud "this is FakeLLM; writes are simulated."

**Real scenario:** `modules/7-capstone/PORTFOLIO.md` is the template you copy when you publish *your* brief.

**What you learned:** README as evidence; five-minute simulated demo; tick the self-assessment before you share the link.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
