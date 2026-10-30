"""Solutions for the skip check for 6.6."""


def health_endpoint_should_not_call_the_model() -> bool:
    """Should GET /health avoid calling the LLM?"""
    return True


def ci_must_bind_port_8000() -> bool:
    """Must CI bind TCP port 8000 to grade this lesson?"""
    return False
