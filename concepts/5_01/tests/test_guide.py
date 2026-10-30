from course_kit.loader import load_concept_module

guide = load_concept_module("5_01", "guide")


def test_known_pipeline_lists_reasons() -> None:
    reasons = guide.reasons_not_to_use_agent(steps_known=True, model_picks_tools=False)
    assert "known_pipeline" in reasons
    assert "model_does_not_pick_tools" in reasons
    assert "extra_tool_rounds_cost_tokens" in reasons


def test_true_agent_has_no_blockers() -> None:
    reasons = guide.reasons_not_to_use_agent(steps_known=False, model_picks_tools=True)
    assert reasons == []
