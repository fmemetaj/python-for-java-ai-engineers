"""2–3 minute skip check for 5.3."""


def pinned_user_incident_survives_trim() -> bool:
    """Should the pinned user incident survive a memory trim?"""
    raise NotImplementedError


def previous_response_id_is_free_context() -> bool:
    """Is previous_response_id free (not billed as input tokens)?"""
    raise NotImplementedError
