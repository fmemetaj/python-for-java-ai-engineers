"""2–3 minute skip check for 2.9."""


def responses_stream_uses_typed_events() -> bool:
    """Does Responses streaming use typed SSE events such as response.output_text.delta?"""
    raise NotImplementedError


def reuse_chat_chunk_handlers_unchanged() -> bool:
    """Can you reuse Chat Completions delta-chunk handlers unchanged on Responses streams?"""
    raise NotImplementedError
