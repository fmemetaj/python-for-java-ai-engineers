"""2–3 minute skip check for 6.2."""


def every_log_line_should_carry_a_request_id() -> bool:
    """Should production log lines include a request id?"""
    raise NotImplementedError


def response_id_and_http_request_id_are_the_same_field() -> bool:
    """Is OpenAI response.id the same value as the HTTP request id?"""
    raise NotImplementedError
