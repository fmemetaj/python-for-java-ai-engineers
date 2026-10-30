"""Env-based settings. Default provider is fake; keys never go in git."""


def default_llm_provider() -> str:
    """The course default when LLM_PROVIDER is unset."""
    raise NotImplementedError


def redact_env(name: str, value: str) -> str:
    """Return `***` for KEY/SECRET/TOKEN names; otherwise the value."""
    raise NotImplementedError


def files_never_commit() -> list[str]:
    """Filenames that must stay gitignored because they may hold secrets."""
    raise NotImplementedError
