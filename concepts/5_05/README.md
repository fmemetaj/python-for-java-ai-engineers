# 5.5 Optional: one framework comparison   [Analog: Spring AI / LangChain4j] [cost: mock] [~60 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_05/tests/test_skip.py` passes. **Optional** (🟣). Still in `course check m5`.

Framework chosen at build time: **OpenAI Agents SDK** names (`Agent`, `Runner.run`) as the comparison, because it sits on the Responses API we already teach. We do **not** add that package. A 40-line facade in `course_kit.agent.facade` reuses `run_agent_loop`. Official SDK docs: [openai-agents-python](https://openai.github.io/openai-agents-python/). Java side: [Spring AI](https://docs.spring.io/spring-ai/reference/) / LangChain4j.

## 1. Concept

A **framework** bundles instructions + tools into an `Agent` object and hides the loop behind `Runner.run`. It does not replace max_steps, approval, or FakeLLM. Lesson 5.2 is still what runs.

## 2. Java version

```java
public class FrameworkDemo {
    public static String run(String agent, String input) {
        return agent + ":" + input;
    }
    public static void main(String[] args) {
        System.out.println(run("triage", "500 after capture"));
    }
}
```

Spring AI's `ChatClient` plus tool callbacks is the same idea: a fluent call site over a loop you no longer see. LangChain4j's `AiServices` is the other Java cousin.

## 3. Python version

```python
agent = Agent(name="triage", instructions=load_triage_instructions(), tools=list(TRIAGE_TOOL_SPECS))
result = Runner().run(
    agent,
    incident,
    client=fake,
    execute=runner.invoke_handled,
    max_steps=8,
    approve=True,
    write_tools=WRITE_TOOLS,
)
```

| Java / Spring AI | This course's facade | OpenAI Agents SDK (not installed) |
| --- | --- | --- |
| `@Bean ChatClient` | `Agent(...)` | `Agent(name=..., instructions=..., tools=...)` |
| `.prompt().call()` | `Runner().run(...)` | `Runner.run(agent, input)` |
| `@Tool` methods | Responses tool dicts | `@function_tool` |
| Your `@PreAuthorize` | `approve=` / `write_tools=` | You still need a gate |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Spring hides the dispatcher | The facade hides `while function_calls` | Forgetting the cap still exists |
| Swap implementations via `@Primary` | Same FakeLLM as 5.2 | Adding LangChain "to be production" without evals |
| BOM manages versions | We pin nothing extra | Framework churn (curriculum F6) — that is why this lesson is optional |
| Compile-time tool interfaces | JSON tool dicts | Assuming the SDK validates args (you still do, Module 3) |

**What did it buy us?** Call-site brevity and a named Agent object. **What did it not buy us?** A different loop, free memory, or a skipped approval gate.

## 5. Exercise

Implement `make_agent` and `run_named` that wrap a provided `run_loop` callable.

```bash
uv run pytest concepts/5_05
```

- Hint 1: `Agent` is a dataclass: name, instructions, tools.
- Hint 2: `run_named` must pass those three into `run_loop`.
- Solution: `solutions/facade.py`.

## 6. Check

1. Does `Runner.run` call a different API than `run_agent_loop`?
2. Why did this course not add `openai-agents` to `pyproject.toml`?
3. Predict: missing `max_steps` on the facade — whose bug?
4. Spring AI analog: ChatClient or RestTemplate?

## Setup / troubleshooting

- Optional lesson. Do not `uv add openai-agents` for graded work.
- If imports fail, `uv sync --locked --group dev` from the repo root.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk triage can be started as `Runner().run(agent, incident, ...)` — same 5-step fake.

**What you learned:** frameworks rename the loop; they do not replace the engineering.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
