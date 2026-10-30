"""2–3 minute skip check for A.3."""


def low_detail_images_cost_a_flat_token_count() -> bool:
    """Is detail=low billed as a flat token count (85), not pixels-as-bytes?"""
    raise NotImplementedError


def images_are_billed_as_output_tokens() -> bool:
    """Are image tokens billed as output tokens?"""
    raise NotImplementedError
