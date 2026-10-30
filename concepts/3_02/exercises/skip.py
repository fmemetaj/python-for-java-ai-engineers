"""2–3 minute skip check for 3.2."""


def responses_tools_are_internally_tagged() -> bool:
    """Is a Responses function tool {type:function, name:...} (name at the top level)?"""
    raise NotImplementedError


def chat_tool_messages_use_call_id_items() -> bool:
    """Does Chat Completions submit tool results as function_call_output items?"""
    raise NotImplementedError
