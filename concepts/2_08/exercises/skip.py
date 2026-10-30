"""2–3 minute skip check for 2.8."""


def stored_state_still_bills_input() -> bool:
    """When using previous_response_id, are previous input tokens still billed as input?"""
    raise NotImplementedError


def http_session_means_free_tokens() -> bool:
    """Does a server-side session id make prior prompt tokens free?"""
    raise NotImplementedError
