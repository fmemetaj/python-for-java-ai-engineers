"""Solutions for the skip check for 5.2."""


def max_steps_is_an_engineering_cap() -> bool:
    """Is max_steps a cap your loop enforces, not a model sampling parameter?"""
    return True


def the_model_executes_python_tools_itself() -> bool:
    """Does the model run your Python functions inside the API process?"""
    return False
