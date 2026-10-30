from types import SimpleNamespace

from course_kit.loader import load_concept_module

loop = load_concept_module("5_02", "loop")


def test_next_status() -> None:
    assert loop.next_status(False, step=1, max_steps=3) == "done"
    assert loop.next_status(True, step=3, max_steps=3) == "capped"
    assert loop.next_status(True, step=1, max_steps=3) == "tool"


def test_should_stop() -> None:
    assert loop.should_stop("done") is True
    assert loop.should_stop("capped") is True
    assert loop.should_stop("denied") is True
    assert loop.should_stop("tool") is False


def test_run_capped_loop_done() -> None:
    turns = [
        SimpleNamespace(
            function_calls=(SimpleNamespace(name="search_docs", arguments="{}", call_id="c1"),),
            output_text="",
        ),
        SimpleNamespace(function_calls=(), output_text="ok"),
    ]

    def complete() -> SimpleNamespace:
        return turns.pop(0)

    ran: list[str] = []
    result = loop.run_capped_loop(
        complete,
        lambda name, _args: ran.append(name) or "{}",
        max_steps=4,
    )
    assert result["status"] == "done"
    assert result["steps"] == 2
    assert ran == ["search_docs"]
    assert result["output_text"] == "ok"


def test_run_capped_loop_cap() -> None:
    def complete() -> SimpleNamespace:
        return SimpleNamespace(
            function_calls=(SimpleNamespace(name="search_docs", arguments="{}", call_id="c"),),
            output_text="",
        )

    result = loop.run_capped_loop(complete, lambda n, a: "{}", max_steps=3)
    assert result["status"] == "capped"
    assert result["steps"] == 3
    assert result["tool_names"] == ["search_docs", "search_docs", "search_docs"]


def test_run_capped_loop_denied() -> None:
    def complete() -> SimpleNamespace:
        return SimpleNamespace(
            function_calls=(
                SimpleNamespace(
                    name="propose_page",
                    arguments='{"slug":"x"}',
                    call_id="w",
                ),
            ),
            output_text="",
        )

    ran: list[str] = []
    result = loop.run_capped_loop(
        complete,
        lambda name, _args: ran.append(name) or "{}",
        max_steps=4,
        write_tools=frozenset({"propose_page"}),
        approved=False,
    )
    assert result["status"] == "denied"
    assert ran == []
    assert result["tool_names"] == ["propose_page"]
