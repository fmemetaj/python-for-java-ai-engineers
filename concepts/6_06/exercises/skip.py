"""2–3 minute skip check for 6.6 (optional analog)."""


def health_endpoint_should_not_call_the_model() -> bool:
    """Should GET /health avoid calling the LLM?"""
    raise NotImplementedError


def ci_must_bind_port_8000() -> bool:
    """Must CI bind TCP port 8000 to grade this lesson?"""
    raise NotImplementedError
