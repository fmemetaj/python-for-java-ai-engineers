from course_kit.loader import load_concept_module

facade = load_concept_module("5_05", "facade")


def test_make_agent() -> None:
    tools = [{"type": "function", "name": "search_docs"}]
    agent = facade.make_agent("triage", "Investigate.", tools)
    assert agent.name == "triage"
    assert agent.instructions == "Investigate."
    assert agent.tools == tools


def test_run_named_forwards() -> None:
    captured: dict[str, object] = {}

    def run_loop(prompt: str, *, tools: object, instructions: str, max_steps: int) -> str:
        captured["prompt"] = prompt
        captured["tools"] = tools
        captured["instructions"] = instructions
        captured["max_steps"] = max_steps
        return "ok"

    agent = facade.make_agent("triage", "Investigate.", [{"name": "search_docs"}])
    assert facade.run_named(agent, "incident", run_loop=run_loop, max_steps=8) == "ok"
    assert captured["prompt"] == "incident"
    assert captured["instructions"] == "Investigate."
    assert captured["max_steps"] == 8
    assert captured["tools"] == [{"name": "search_docs"}]


def test_what_it_bought() -> None:
    notes = facade.what_it_bought()
    blob = " ".join(notes).lower()
    assert "loop" in blob
    assert "max_steps" in blob or "cap" in blob
