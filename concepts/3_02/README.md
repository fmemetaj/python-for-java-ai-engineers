# 3.2 Function/tool calling   [Analog: Interface dispatch / command pattern] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/3_02/tests/test_skip.py` passes.

Official docs: [Function calling](https://platform.openai.com/docs/guides/function-calling).

## 1. Concept

**Function calling** (tool calling) lets the model request that *your* code run, with JSON arguments. You advertise tools as JSON Schema. The model may emit a `function_call` item (`name`, JSON-string `arguments`, `call_id`). You dispatch like a command map / strategy interface — the model does not execute Python.

## 2. Java version

```java
public class ToolDispatchDemo {
    interface Tool { String run(String args); }
    static final class SearchDocs implements Tool {
        public String run(String args) { return "auth page"; }
    }
    public static void main(String[] args) {
        Tool tool = new SearchDocs();
        System.out.println(tool.run("auth"));
    }
}
```

A servlet would look up `name` in a `Map<String, Tool>` and call `run`. The LLM is the caller that picks the name; it is not the `Tool` implementation.

## 3. Python version

```python
SEARCH_DOCS_TOOL = {
    "type": "function",
    "name": "search_docs",
    "description": "Search internal DocsDesk pages by keyword.",
    "parameters": {
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True,
}
# output item: {type: "function_call", call_id, name, arguments: '{"query":"auth"}'}
# next input:  {type: "function_call_output", call_id, output: "..."}
```

| Java | Python / Responses |
| --- | --- |
| `interface Tool` + `Map` dispatch | `name` → your function |
| DTO method args | JSON Schema `parameters` |
| Return value | `function_call_output.output` (a string, often JSON) |
| Command `id` for tracing | `call_id` (required to pair the result) |

## 4. Differences & pitfalls

| Java habit | Python reality | Pitfall / bug it causes |
| --- | --- | --- |
| Nested `{"type":"function","function":{name}}` (Chat Completions) | Responses is internally tagged: `name` on the tool itself | Model never sees `search_docs` |
| Assuming the SDK runs the function | You must execute it | Dead loop; no docs retrieved |
| `arguments` already a Map | `arguments` is a **JSON string** | `TypeError` on `item.arguments["query"]` |
| Forgetting correlation ids | `call_id` on the output must match | Model ignores the result |
| Assistants `submit_tool_outputs` | Sunset. Use `function_call_output` items | Dead endpoint |

## 5. Exercise

Define `search_docs`, detect the Responses vs Chat tool shape, parse a `function_call`, and build the matching `function_call_output`.

```bash
uv run pytest concepts/3_02
```

- Hint 1: no nested `"function"` key on Responses tools.
- Hint 2: `json.loads` the arguments string; echo `call_id` on the output item.
- Solution: `solutions/tools.py`.

## 6. Check

1. Who executes `search_docs` — the model, or your process?
2. What three fields does a `function_call` item carry?
3. Why is Chat Completions' nested `function` object a migration trap?
4. Predict: passing `item.arguments["query"]` without `json.loads`.

## Setup / troubleshooting

- FakeLLM is scripted: it emits the `function_call` you configured, not a live model choice.
- If a live call returns no tools, you forgot `tools=[...]` on `responses.create`.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk advertises `search_docs` and `get_endpoint_spec`. The fake is scripted so CI is deterministic.

**What you learned:** tools are schemas plus *your* dispatch; `call_id` pairs the result.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
