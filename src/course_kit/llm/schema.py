"""JSON Schema helpers for Structured Outputs.

Responses uses `text.format`; Chat Completions uses `response_format`.
Official guide: https://platform.openai.com/docs/guides/structured-outputs
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def _strict_object(schema: dict[str, Any]) -> None:
    """Mutate an object schema toward OpenAI strict JSON Schema rules."""
    if schema.get("type") == "object" or "properties" in schema:
        schema["additionalProperties"] = False
        properties = schema.get("properties")
        if isinstance(properties, dict):
            schema["required"] = list(properties.keys())


def json_schema_from_model(model: type[BaseModel]) -> dict[str, Any]:
    """JSON Schema for a Pydantic model, with additionalProperties=false."""
    schema = model.model_json_schema()
    _strict_object(schema)
    defs = schema.get("$defs")
    if isinstance(defs, dict):
        for definition in defs.values():
            if isinstance(definition, dict):
                _strict_object(definition)
    return schema


def responses_text_format(
    name: str,
    schema: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Inner `text.format` object for POST /v1/responses."""
    return {
        "type": "json_schema",
        "name": name,
        "strict": strict,
        "schema": schema,
    }


def chat_response_format(
    name: str,
    schema: dict[str, Any],
    *,
    strict: bool = True,
) -> dict[str, Any]:
    """Chat Completions `response_format` object (nested json_schema key)."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": name,
            "strict": strict,
            "schema": schema,
        },
    }


def function_call_output(call_id: str, output: str) -> dict[str, object]:
    """Input item that returns a tool result, keyed by the model's call_id."""
    return {"type": "function_call_output", "call_id": call_id, "output": output}
