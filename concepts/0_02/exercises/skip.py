"""2–3 minute skip check for 0.2."""


def cells_share_one_kernel() -> bool:
    """Do code cells in one notebook share a single kernel namespace?"""
    raise NotImplementedError


def restart_clears_names() -> bool:
    """Does Restart Kernel drop names bound in earlier cells?"""
    raise NotImplementedError
