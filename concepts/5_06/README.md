# 5.6 Optional: MCP tools   [NEW — no Java equivalent] [cost: mock] [~45 min] [last verified: 2026-10-30, Python 3.11–3.13]

Skip if: `uv run pytest concepts/5_06/tests/test_skip.py` passes. **Still recommended** (NEW), even though the concept is optional (🟣) in the module. Still in `course check m5`.

Official spec: [MCP 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18). JSON-RPC 2.0. OpenAI can host remote MCP as a Responses tool; that path is paid and is **not** graded. This lesson uses an in-process `FakeMcpServer`.

## 1. Concept

**MCP** (Model Context Protocol) is a JSON-RPC contract so a tool host can advertise `tools/list` and run `tools/call` for any client (Claude Desktop, an IDE, or your agent loop). Your Python functions stay in *your* process. The protocol is the USB-C of tools — not a new model.

## 2. Intuition

A remote control with a published button list.

```
Client                     FakeMcpServer (in-process)
  initialize      →        protocolVersion + capabilities
  tools/list      →        [{name, description, inputSchema}]
  tools/call      →        {content: [{type:"text", text:"..."}]}
```

Then you map those tools into Responses `{"type":"function",...}` and the 5.2 loop is unchanged.

## 3. Why it exists

Every vendor invented a different "tool plugin" JSON. MCP is a shared shape so DocsDesk's `search_docs` can be offered to more than one orchestrator without rewriting the handler. Java would publish a SOAP/gRPC service or a Java SPI. Those are app-to-app. MCP is *model-facing*: the caller is an LLM client, not another Spring service.

### The Java analogy that misleads you

JDBC drivers / `ServiceLoader` / a servlet `Filter` look like "pluggable tools". They are process-local APIs for *your* code. MCP is a **protocol** (JSON-RPC messages) that a foreign client speaks. Wrapping `ToolRunner` in an `@Service` does not make it MCP. Opening a socket in CI is also not required — the fake speaks the same JSON in-process.

## 4. Step-by-step examples

**Example 1 — JSON-RPC envelope.** `{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}`.

**Example 2 — initialize.** Result includes `protocolVersion` `2025-06-18`.

**Example 3 — tools/list.** Each tool has `name`, `description`, `inputSchema`.

**Example 4 — tools/call.** `params: {name, arguments}` → `content[].text`.

**Example 5 — map to Responses function tools.** `mcp_tools_to_openai` copies name + schema into `type: function`.

```bash
uv run python concepts/5_06/examples.py
```

The fake cannot teach a live remote MCP server, OAuth, or hosted OpenAI MCP billing. Graded tests check *your* JSON-RPC handling.

## 5. Common pitfalls

- Treating MCP as "a better LangChain".
- Forgetting `jsonrpc: "2.0"`.
- Calling Assistants instead of mapping into Responses function tools.
- Opening stdio/HTTP in graded tests.

## 6. Exercises

1. **Guided:** `parse_tools_list` and `initialize_ok`.
2. **Open:** `handle_call` + `method_not_found` error `-32601`.

```bash
uv run pytest concepts/5_06
```

- Hint 1: `result.tools` is a list of `{name, inputSchema}`.
- Hint 2: unknown methods return `error.code == -32601`.
- Solution: `solutions/mcp_list.py`, `solutions/mcp_call.py`.

## 7. Check

1. Which JSON-RPC methods does this lesson implement?
2. Does `tools/call` run in the model vendor's process or yours?
3. Predict: `method: "nope"` — error code?
4. Why is JDBC a misleading analog?

## Setup / troubleshooting

- Optional lesson. No `pip install mcp`. The fake is in `course_kit.agent.mcp`.
- If `initialize` fails, check `jsonrpc` is the string `"2.0"`, not `2`.
- Hosted remote MCP stays opt-in and off CI.
- More: [../../docs/setup/troubleshooting.md](../../docs/setup/troubleshooting.md).

**Real scenario:** DocsDesk could expose `search_docs` over FakeMcpServer for a second client; triage still uses the same handlers.

**What you learned:** MCP is a JSON-RPC tool contract; the agent loop still belongs to you.

Feedback: [lesson-feedback](https://github.com/fmemetaj/python-for-java-ai-engineers/issues/new?template=lesson-feedback.yml).
