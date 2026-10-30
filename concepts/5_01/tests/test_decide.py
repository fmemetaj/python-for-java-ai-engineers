from course_kit.loader import load_concept_module

decide = load_concept_module("5_01", "decide")


def test_rag_pipeline_is_workflow() -> None:
    assert decide.classify_orchestration(steps_known=True, model_picks_tools=False) == "workflow"
    assert (
        decide.should_use_agent(
            steps_known=True,
            model_picks_tools=False,
            branching=False,
        )
        is False
    )


def test_triage_is_agent() -> None:
    assert decide.classify_orchestration(steps_known=False, model_picks_tools=True) == "agent"
    assert (
        decide.should_use_agent(
            steps_known=False,
            model_picks_tools=True,
            branching=True,
        )
        is True
    )


def test_extract_json_is_single_call() -> None:
    assert (
        decide.classify_orchestration(steps_known=False, model_picks_tools=False) == "single_call"
    )


def test_no_model_is_not_an_agent() -> None:
    assert (
        decide.should_use_agent(
            steps_known=False,
            model_picks_tools=True,
            branching=True,
            needs_model=False,
        )
        is False
    )
