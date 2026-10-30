"""2–3 minute skip check for 2.6."""


def prices_come_from_dated_yaml() -> bool:
    """Should USD rates come from a dated pricing.yaml sourced at platform.openai.com/docs/pricing?"""
    raise NotImplementedError


def previous_response_id_waives_input_fees() -> bool:
    """Does previous_response_id stop billing previous input tokens?"""
    raise NotImplementedError
