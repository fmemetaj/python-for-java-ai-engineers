"""Solutions for the skip check for 5.3."""


def pinned_user_incident_survives_trim() -> bool:
    """Should the pinned user incident survive a memory trim?"""
    return True


def previous_response_id_is_free_context() -> bool:
    """Is previous_response_id free (not billed as input tokens)?"""
    return False
