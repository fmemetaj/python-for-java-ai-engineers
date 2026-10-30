"""2–3 minute skip check for 6.1. Still recommended — this concept is NEW."""


def llm_judge_needs_calibration_before_it_is_a_gate() -> bool:
    """Should an LLM-as-judge be calibrated against labels before it is a CI gate?"""
    raise NotImplementedError


def live_model_text_is_an_honest_junit_assert_equals() -> bool:
    """Is assertEquals on live model prose an honest CI gate?"""
    raise NotImplementedError
