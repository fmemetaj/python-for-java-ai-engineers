from pydantic import ValidationError

from course_kit.loader import load_tool_registry
from mini_agent.models import Ticket

reg = load_tool_registry()


def test_function_tool_adapts_callable() -> None:
    tool = reg.FunctionTool("echo", str.upper)
    assert tool.name == "echo"
    assert tool.run("hi") == "HI"
    assert isinstance(tool, reg.Tool)


def test_add_and_call() -> None:
    registry = reg.ToolRegistry()
    registry.add(reg.FunctionTool("echo", str.upper))
    assert registry.names() == ["echo"]
    assert registry.call("echo", "docs") == "DOCS"


def test_decorator_registers_and_returns_function() -> None:
    registry = reg.ToolRegistry()

    @registry.register("classify")
    def classify(payload: str) -> str:
        ticket = Ticket(id=1, subject=payload[:40], body=payload)
        content = f"{ticket.subject} {ticket.body}".lower()
        if "login" in content:
            return "access"
        return "general"

    assert classify("cannot login today") == "access"
    assert registry.call("classify", "cannot login today") == "access"
    assert "classify" in registry.names()


def test_unknown_tool_raises_keyerror() -> None:
    registry = reg.ToolRegistry()
    try:
        registry.get("missing")
    except KeyError as exc:
        assert "missing" in str(exc)
    else:
        raise AssertionError("expected KeyError")


def test_ticket_validation_still_rejects_bad_ids() -> None:
    try:
        Ticket(id=0, subject="Help", body="Please assist")
    except ValidationError:
        return
    raise AssertionError("expected ValidationError")
