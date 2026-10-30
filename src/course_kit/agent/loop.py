"""The agent loop by hand: state, max steps, stop conditions.

Java analog: a state machine you wrote. Here the model proposes the next
tool; your code still executes it, caps steps, and enforces approval.
https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from course_kit.llm import FakeLLM, FunctionCall, LLMResponse, function_call_output

from .memory import AgentMemory
from .trace import AgentTrace

Status = Literal["start", "llm", "tool", "approval", "done", "capped", "denied"]
ApprovalGate = bool | Callable[[FunctionCall], bool]


@dataclass
class AgentState:
    status: Status = "start"
    step: int = 0
    pending_approval: FunctionCall | None = None


@dataclass
class AgentResult:
    status: Status
    steps: int
    output_text: str
    response: LLMResponse | None = None
    state: AgentState = field(default_factory=AgentState)
    trace: AgentTrace = field(default_factory=AgentTrace)
    memory: AgentMemory = field(default_factory=AgentMemory)
    tool_names: list[str] = field(default_factory=list)


def _approved(gate: ApprovalGate, call: FunctionCall) -> bool:
    if callable(gate):
        return bool(gate(call))
    return bool(gate)


def _needs_approval(name: str, write_tools: frozenset[str]) -> bool:
    return name in write_tools


def run_agent_loop(
    client: FakeLLM,
    prompt: str,
    *,
    execute: Callable[[str, str], str],
    tools: Sequence[dict[str, object]],
    instructions: str = "",
    max_steps: int = 8,
    approve: ApprovalGate = False,
    write_tools: frozenset[str] | None = None,
    memory: AgentMemory | None = None,
    trace: AgentTrace | None = None,
    text_format: dict[str, object] | None = None,
) -> AgentResult:
    """Repeat complete() until the model returns no function_call, or we stop.

    Stop conditions: no function_call items (done), ``max_steps`` (capped),
    or a write tool that is not approved (denied). Each ``complete()`` is one
    step. The fake cannot teach live latency; graded tests check *your* cap.
    """
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")
    writes = write_tools if write_tools is not None else frozenset()
    notes = memory if memory is not None else AgentMemory()
    tracer = trace if trace is not None else AgentTrace()
    notes.add("user", prompt, pinned=True)

    spec = list(tools)
    input_items: list[dict[str, object]] = []
    previous_id: str | None = None
    used_tools: list[str] = []
    response: LLMResponse | None = None
    state = AgentState()

    with tracer.span("agent.run", "agent", prompt=prompt[:80]):
        while state.step < max_steps:
            state.step += 1
            state.status = "llm"
            extra = notes.as_context()
            combined = instructions
            if extra:
                combined = f"{instructions}\n\nMemory:\n{extra}".strip()
            with tracer.span(f"llm.step_{state.step}", "llm", step=state.step):
                response = client.complete(
                    prompt,
                    instructions=combined,
                    tools=spec,
                    text_format=text_format,
                    input_items=input_items,
                    previous_response_id=previous_id,
                    store=True,
                )
            previous_id = response.id
            if not response.function_calls:
                state.status = "done"
                return AgentResult(
                    status="done",
                    steps=state.step,
                    output_text=response.output_text,
                    response=response,
                    state=state,
                    trace=tracer,
                    memory=notes,
                    tool_names=used_tools,
                )
            for call in response.function_calls:
                used_tools.append(call.name)
                if _needs_approval(call.name, writes):
                    state.status = "approval"
                    state.pending_approval = call
                    with tracer.span(
                        f"approval.{call.name}",
                        "approval",
                        tool=call.name,
                        call_id=call.call_id,
                    ):
                        allowed = _approved(approve, call)
                    if not allowed:
                        state.status = "denied"
                        return AgentResult(
                            status="denied",
                            steps=state.step,
                            output_text="",
                            response=response,
                            state=state,
                            trace=tracer,
                            memory=notes,
                            tool_names=used_tools,
                        )
                state.status = "tool"
                with tracer.span(
                    f"tool.{call.name}",
                    "tool",
                    tool=call.name,
                    call_id=call.call_id,
                ):
                    output = execute(call.name, call.arguments)
                input_items.append(function_call_output(call.call_id, output))
                notes.add("observation", f"{call.name}: {output[:200]}")

    state.status = "capped"
    text = response.output_text if response is not None else ""
    return AgentResult(
        status="capped",
        steps=state.step,
        output_text=text,
        response=response,
        state=state,
        trace=tracer,
        memory=notes,
        tool_names=used_tools,
    )


def stop_reason(result: AgentResult) -> str:
    """Human-readable stop condition — useful in evals and traces."""
    mapping: dict[Status, str] = {
        "done": "no_function_call",
        "capped": "max_steps",
        "denied": "approval_denied",
        "start": "not_started",
        "llm": "in_llm",
        "tool": "in_tool",
        "approval": "awaiting_approval",
    }
    return mapping[result.status]


def parse_json_object(text: str) -> dict[str, Any] | None:
    """Best-effort JSON object from a final message. None if not an object."""
    import json

    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, dict) else None
