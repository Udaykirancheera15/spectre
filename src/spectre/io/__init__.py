"""Spectre I/O infrastructure package.

Purpose:
    Provide deterministic low-level I/O helpers shared by M0 infrastructure and
    future reporting/artifact modules.

Design:
    I/O helpers are separated from dataset validation so JSON, filesystem,
    reports, checkpoints, and other storage formats can evolve independently.

Input:
    Paths and serializable payloads supplied by callers.

Output:
    Deterministic filesystem traversal and serialized files.

Failure modes:
    Public functions raise project-specific exceptions with context.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.io.filesystem import ensure_directory
    >>> callable(ensure_directory)
    True

"""
