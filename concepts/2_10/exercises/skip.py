"""2–3 minute skip check for 2.10."""


def prompts_belong_in_versioned_files() -> bool:
    """Should system instructions live in a versioned file that can be diffed?"""
    raise NotImplementedError


def evals_require_a_paid_key() -> bool:
    """Does a first eval set require OPENAI_API_KEY to run in CI?"""
    raise NotImplementedError
