"""2–3 minute skip check for 4.3."""


def chunking_is_more_than_substring() -> bool:
    """Should a production chunker avoid splitting Markdown code fences?"""
    raise NotImplementedError


def one_file_must_be_one_chunk() -> bool:
    """Must each source file be exactly one embedding?"""
    raise NotImplementedError
