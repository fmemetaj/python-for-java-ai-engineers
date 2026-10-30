"""Solutions for the skip check for A.1."""


def responses_image_items_use_input_image_type() -> bool:
    """Does Responses image input use type input_image (not a Chat Completions image_url message)?"""
    return True


def graded_work_may_fetch_https_image_urls() -> bool:
    """May graded tests download https image URLs?"""
    return False
