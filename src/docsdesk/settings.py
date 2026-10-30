"""Typed process settings. Java analogy: `@ConfigurationProperties` + profiles."""

from __future__ import annotations

from typing import Any, Self, cast

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load config from environment / optional `.env`. Never commit `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    llm_provider: str = "fake"
    openai_api_key: SecretStr = SecretStr("")
    openai_model: str = "gpt-4.1-mini"
    docs_base_url: str = "https://docs.internal.test"
    http_timeout_seconds: float = Field(default=5.0, gt=0)
    http_retries: int = Field(default=3, ge=1, le=8)

    @field_validator("llm_provider")
    @classmethod
    def provider_is_known(cls, value: str) -> str:
        name = value.strip().lower() or "fake"
        if name not in {"fake", "ollama", "openai"}:
            raise ValueError("LLM_PROVIDER must be fake, ollama, or openai")
        return name

    def secret_values(self) -> list[str]:
        """Values that must never appear in logs."""
        key = self.openai_api_key.get_secret_value()
        return [key] if key else []

    @classmethod
    def offline(cls, **data: Any) -> Self:
        """Build settings without reading `.env` (tests and CI isolation)."""
        factory = cast(Any, cls)
        return factory(_env_file=None, **data)
