"""Deterministic FakeLLM — recorded-style Responses and Chat Completions objects."""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping, Sequence

from .base import (
    ChatChoice,
    ChatCompletion,
    ChatMessage,
    ChatUsage,
    FunctionCall,
    LLMResponse,
    OutputItem,
    OutputMessage,
    OutputText,
    ReasoningItem,
    StreamEvent,
    Usage,
)
from .tokens import estimate_tokens

EFFORT_REASONING_TOKENS = {
    None: 0,
    "none": 0,
    "low": 16,
    "medium": 64,
    "high": 256,
}


class FakeLLM:
    """Scripted or default replies. Java analogy: a `@Primary` test stub bean.

    The fake cannot teach live latency, tokenizer drift, or temperature
    variance. Graded tests check *your* parsing, cost math, and loops.
    """

    def __init__(
        self,
        script: dict[str, str] | None = None,
        *,
        structured: Mapping[str, Mapping[str, object]] | None = None,
        tool_calls: Mapping[str, Sequence[Mapping[str, str]]] | None = None,
        after_tools: Mapping[str, str] | None = None,
        refusals: Sequence[str] | None = None,
        trajectories: Mapping[str, Sequence[Mapping[str, object]]] | None = None,
    ) -> None:
        self._script = dict(script or {})
        self._structured = {key: dict(value) for key, value in (structured or {}).items()}
        self._tool_calls = {key: list(value) for key, value in (tool_calls or {}).items()}
        self._after_tools = dict(after_tools or {})
        self._refusals = set(refusals or ())
        self._trajectories = {key: list(value) for key, value in (trajectories or {}).items()}
        self._agent_turns: dict[str, int] = {}
        self._store: dict[str, LLMResponse] = {}
        self._counter = 0

    def complete(
        self,
        prompt: str,
        *,
        instructions: str = "",
        previous_response_id: str | None = None,
        store: bool = False,
        temperature: float = 1.0,
        reasoning_effort: str | None = None,
        model: str = "gpt-4.1-mini",
        cached_tokens: int = 0,
        tools: Sequence[Mapping[str, object]] | None = None,
        text_format: dict[str, object] | None = None,
        input_items: Sequence[Mapping[str, object]] | None = None,
    ) -> LLMResponse:
        del temperature  # Fake is deterministic; live sampling is optional later.
        prior = self._lookup(previous_response_id)
        prior_input = prior.usage.input_tokens if prior is not None else 0
        input_tokens = estimate_tokens(instructions + prompt) + prior_input
        reasoning_tokens = EFFORT_REASONING_TOKENS.get(reasoning_effort, 0)
        if cached_tokens > input_tokens:
            cached_tokens = input_tokens

        if prompt in self._refusals:
            return self._finish(
                items=(),
                previous_response_id=previous_response_id,
                store=store,
                model=model,
                input_tokens=input_tokens,
                reasoning_tokens=reasoning_tokens,
                cached_tokens=cached_tokens,
                visible_text="",
                refusal="I'm sorry, I can't extract that.",
            )

        if prompt in self._trajectories:
            return self._from_trajectory(
                prompt,
                previous_response_id=previous_response_id,
                store=store,
                model=model,
                input_tokens=input_tokens,
                reasoning_tokens=reasoning_tokens,
                reasoning_effort=reasoning_effort,
                cached_tokens=cached_tokens,
                text_format=text_format,
            )

        tool_outputs = [
            item for item in (input_items or []) if item.get("type") == "function_call_output"
        ]
        if tool_outputs:
            text = self._after_tools.get(prompt) or self._default_after_tools(prompt)
            parsed = self._maybe_parsed(text, text_format)
            return self._message_response(
                text=text,
                previous_response_id=previous_response_id,
                store=store,
                model=model,
                input_tokens=input_tokens,
                reasoning_tokens=reasoning_tokens,
                reasoning_effort=reasoning_effort,
                cached_tokens=cached_tokens,
                output_parsed=parsed,
            )

        allowed = {str(tool.get("name")) for tool in (tools or []) if "name" in tool}
        planned = self._tool_calls.get(prompt)
        if planned:
            calls: list[FunctionCall] = []
            for spec in planned:
                name = spec.get("name", "")
                if allowed and name not in allowed:
                    continue
                calls.append(
                    FunctionCall(
                        call_id=spec.get("call_id", f"call_fake_{len(calls) + 1}"),
                        name=name,
                        arguments=spec.get("arguments", "{}"),
                    )
                )
            if calls:
                rendered = " ".join(call.arguments for call in calls)
                return self._finish(
                    items=tuple(calls),
                    previous_response_id=previous_response_id,
                    store=store,
                    model=model,
                    input_tokens=input_tokens,
                    reasoning_tokens=reasoning_tokens,
                    cached_tokens=cached_tokens,
                    visible_text=rendered,
                )

        if prompt in self._structured:
            payload = self._structured[prompt]
            text = json.dumps(payload, separators=(",", ":"), sort_keys=True)
            return self._message_response(
                text=text,
                previous_response_id=previous_response_id,
                store=store,
                model=model,
                input_tokens=input_tokens,
                reasoning_tokens=reasoning_tokens,
                reasoning_effort=reasoning_effort,
                cached_tokens=cached_tokens,
                output_parsed=dict(payload),
            )

        text = self._script.get(prompt) or self._default_text(prompt, instructions)
        parsed = self._maybe_parsed(text, text_format)
        return self._message_response(
            text=text,
            previous_response_id=previous_response_id,
            store=store,
            model=model,
            input_tokens=input_tokens,
            reasoning_tokens=reasoning_tokens,
            reasoning_effort=reasoning_effort,
            cached_tokens=cached_tokens,
            output_parsed=parsed,
        )

    def _from_trajectory(
        self,
        prompt: str,
        *,
        previous_response_id: str | None,
        store: bool,
        model: str,
        input_tokens: int,
        reasoning_tokens: int,
        reasoning_effort: str | None,
        cached_tokens: int,
        text_format: dict[str, object] | None,
    ) -> LLMResponse:
        """Replay one turn of a scripted multi-step agent trajectory.

        Each complete() for this prompt advances one turn. A turn is either
        ``{"tools": [{"call_id", "name", "arguments"}, ...]}`` or
        ``{"message": "..."}``. Past the last turn, the last message (or a
        default) is returned so a missing cap cannot spin forever.
        """
        script = self._trajectories[prompt]
        idx = self._agent_turns.get(prompt, 0)
        if idx < len(script):
            turn = script[idx]
            self._agent_turns[prompt] = idx + 1
        elif script:
            turn = script[-1]
        else:
            turn = {"message": "DocsDesk fake provider."}

        planned = turn.get("tools")
        if isinstance(planned, list) and planned and idx < len(script):
            calls = [
                FunctionCall(
                    call_id=str(spec.get("call_id", f"call_fake_{i + 1}")),
                    name=str(spec.get("name", "")),
                    arguments=str(spec.get("arguments", "{}")),
                )
                for i, spec in enumerate(planned)
                if isinstance(spec, Mapping)
            ]
            if calls:
                return self._finish(
                    items=tuple(calls),
                    previous_response_id=previous_response_id,
                    store=store,
                    model=model,
                    input_tokens=input_tokens,
                    reasoning_tokens=reasoning_tokens,
                    cached_tokens=cached_tokens,
                    visible_text="",
                )

        text = str(turn.get("message") or "DocsDesk fake provider.")
        parsed = self._maybe_parsed(text, text_format)
        return self._message_response(
            text=text,
            previous_response_id=previous_response_id,
            store=store,
            model=model,
            input_tokens=input_tokens,
            reasoning_tokens=reasoning_tokens,
            reasoning_effort=reasoning_effort,
            cached_tokens=cached_tokens,
            output_parsed=parsed,
        )

    def _message_response(
        self,
        *,
        text: str,
        previous_response_id: str | None,
        store: bool,
        model: str,
        input_tokens: int,
        reasoning_tokens: int,
        reasoning_effort: str | None,
        cached_tokens: int,
        output_parsed: dict[str, object] | None,
    ) -> LLMResponse:
        items: list[OutputItem] = []
        if reasoning_tokens:
            items.append(ReasoningItem(effort=reasoning_effort, summary=("fake reasoning",)))
        items.append(OutputMessage(content=(OutputText(text=text),)))
        return self._finish(
            items=tuple(items),
            previous_response_id=previous_response_id,
            store=store,
            model=model,
            input_tokens=input_tokens,
            reasoning_tokens=reasoning_tokens,
            cached_tokens=cached_tokens,
            visible_text=text,
            output_parsed=output_parsed,
        )

    def _finish(
        self,
        *,
        items: tuple[OutputItem, ...],
        previous_response_id: str | None,
        store: bool,
        model: str,
        input_tokens: int,
        reasoning_tokens: int,
        cached_tokens: int,
        visible_text: str,
        refusal: str | None = None,
        output_parsed: dict[str, object] | None = None,
    ) -> LLMResponse:
        visible_output = estimate_tokens(visible_text) if visible_text else 0
        output_tokens = visible_output + reasoning_tokens
        usage = Usage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cached_tokens=cached_tokens,
            reasoning_tokens=reasoning_tokens,
        )
        self._counter += 1
        response = LLMResponse(
            id=f"resp_fake_{self._counter:04d}",
            output=items,
            usage=usage,
            previous_response_id=previous_response_id,
            store=store,
            model=model,
            refusal=refusal,
            output_parsed=output_parsed,
            request_id=f"req_fake_{self._counter:04d}",
        )
        if store:
            self._store[response.id] = response
        return response

    def _maybe_parsed(
        self,
        text: str,
        text_format: dict[str, object] | None,
    ) -> dict[str, object] | None:
        if not text_format or text_format.get("type") != "json_schema":
            return None
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError:
            return None
        return loaded if isinstance(loaded, dict) else None

    def _default_after_tools(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "auth" in lowered:
            return "Auth uses a Bearer token (from search_docs)."
        if "ticket" in lowered or "endpoint" in lowered:
            return "GET /tickets/{id} returns a ticket. Timeouts are five seconds."
        return "Tool results applied. DocsDesk fake provider."

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "gpt-4.1-mini",
    ) -> ChatCompletion:
        prompt = "\n".join(item.get("content", "") for item in messages)
        instructions = next(
            (item.get("content", "") for item in messages if item.get("role") == "system"),
            "",
        )
        user = next(
            (item.get("content", "") for item in messages if item.get("role") == "user"),
            prompt,
        )
        text = self._script.get(user) or self._default_text(user, instructions)
        prompt_tokens = estimate_tokens(prompt)
        completion_tokens = estimate_tokens(text)
        self._counter += 1
        return ChatCompletion(
            id=f"chatcmpl_fake_{self._counter:04d}",
            model=model,
            choices=(ChatChoice(index=0, message=ChatMessage(role="assistant", content=text)),),
            usage=ChatUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    def stream(self, prompt: str, *, instructions: str = "") -> Iterator[StreamEvent]:
        response = self.complete(prompt, instructions=instructions)
        text = response.output_text
        step = max(1, len(text) // 4)
        if not text:
            yield StreamEvent(type="response.completed", response=response)
            return
        for index in range(0, len(text), step):
            yield StreamEvent(
                type="response.output_text.delta",
                delta=text[index : index + step],
            )
        yield StreamEvent(type="response.completed", response=response)

    def _lookup(self, response_id: str | None) -> LLMResponse | None:
        if not response_id:
            return None
        return self._store.get(response_id)

    def _default_text(self, prompt: str, instructions: str) -> str:
        lowered = f"{instructions}\n{prompt}".lower()
        if "auth" in lowered:
            return "Auth uses a Bearer token. DocsDesk never logs the token."
        if "ticket" in lowered:
            return "Tickets are fetched over HTTP with a timeout and retries."
        if "population" in lowered or "follow-up" in lowered:
            return "Follow-up: the previous turn is still billed as input tokens."
        return "DocsDesk fake provider: offline, deterministic, no paid API."
