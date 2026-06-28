"""Small focused utility package for Spectre.

Purpose:
    Expose narrowly scoped utilities that do not belong to a more specific
    package.

Design:
    This package is intentionally kept small to avoid becoming a junk drawer.
    New utilities should be placed in focused packages whenever possible.

Input:
    Utility-specific inputs.

Output:
    Utility-specific outputs.

Failure modes:
    Utilities should raise project-specific exceptions when failures are public.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.utils.reproducibility import collect_environment_info
    >>> callable(collect_environment_info)
    True

"""
