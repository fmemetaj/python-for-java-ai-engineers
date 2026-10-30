"""2–3 minute skip check for 3.3. Still recommended — this concept is NEW."""


def the_model_decides_whether_to_call_a_tool() -> bool:
    """In the tool-call loop, does the model choose when to emit function_call items?"""
    raise NotImplementedError


def outputs_can_omit_call_id() -> bool:
    """Can you submit function_call_output without the matching call_id?"""
    raise NotImplementedError
