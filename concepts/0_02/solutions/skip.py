"""Solutions for the 0.2 skip check."""


def cells_share_one_kernel() -> bool:
    """Do code cells in one notebook share a single kernel namespace?"""
    return True


def restart_clears_names() -> bool:
    """Does Restart Kernel drop names bound in earlier cells?"""
    return True
