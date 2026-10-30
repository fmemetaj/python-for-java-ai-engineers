"""Solutions for the skip check for 4.3."""


def chunking_is_more_than_substring() -> bool:
    """Should a production chunker avoid splitting Markdown code fences?"""
    return True


def one_file_must_be_one_chunk() -> bool:
    """Must each source file be exactly one embedding?"""
    return False
