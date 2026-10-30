from course_kit.llm import FakeLLM
from course_kit.loader import load_concept_module
from docsdesk.tools import SEARCH_DOCS_TOOL

replay = load_concept_module("3_03", "replay")


def test_replay_two_step_script() -> None:
    client = FakeLLM(
        tool_calls={
            "q": [
                {
                    "call_id": "call_1",
                    "name": "search_docs",
                    "arguments": '{"query":"auth"}',
                }
            ]
        },
        after_tools={"q": "Auth uses a Bearer token (from search_docs)."},
    )

    def execute(name: str, arguments: str) -> str:
        assert name == "search_docs"
        return "found auth"

    response = replay.replay_tool_turn(client, "q", execute, tools=[SEARCH_DOCS_TOOL])
    assert response.function_calls == ()
    assert "Bearer" in response.output_text


def test_replay_message_only_skips_second_call() -> None:
    client = FakeLLM(script={"hello": "world"})
    response = replay.replay_tool_turn(client, "hello", lambda n, a: "nope")
    assert response.output_text == "world"
