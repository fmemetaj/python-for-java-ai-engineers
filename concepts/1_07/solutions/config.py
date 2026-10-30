"""Env-based settings. Default provider is fake; keys never go in git (solution)."""


def default_llm_provider() -> str:
    """The course default when LLM_PROVIDER is unset."""
    return "fake"


def redact_env(name: str, value: str) -> str:
    """Return `***` for KEY/SECRET/TOKEN names; otherwise the value."""
    upper = name.upper()
    if any(marker in upper for marker in ("KEY", "SECRET", "TOKEN")):
        return "***"
    return value


def files_never_commit() -> list[str]:
    """Filenames that must stay gitignored because they may hold secrets."""
    return [".env"]
