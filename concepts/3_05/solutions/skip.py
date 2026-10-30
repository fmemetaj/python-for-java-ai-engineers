"""Solutions for the skip check for 3.5."""


def evals_can_run_offline_on_fixtures() -> bool:
    """Can a golden-set eval pass on FakeLLM without a paid API key?"""
    return True


def junit_of_a_pure_function_is_the_same_as_an_llm_eval() -> bool:
    """Is an LLM eval the same kind of test as JUnit of a deterministic function?"""
    return False
