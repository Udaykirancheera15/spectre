"""Filesystem helpers for Spectre infrastructure.

Purpose:
    Provide deterministic, small filesystem primitives shared by dataset
    validation, manifest generation, environment metadata, and future reports.

Design:
    Helpers are pure wrappers around `pathlib` and avoid hidden global state.
    Directory walks are sorted to make manifests reproducible.

Input:
    Paths supplied by callers or configuration.

Output:
    Deterministically ordered paths or ensured directories.

Failure modes:
    Filesystem failures raise project-specific dataset exceptions with context.

Complexity:
    Recursive file walking is O(n log n) due to deterministic sorting.

Examples:
    >>> from pathlib import Path
    >>> Path(".").exists()
    True

"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from spectre.exceptions.dataset import DatasetPermissionError


def iter_files_deterministic(root: Path) -> Iterator[Path]:
    """Yield files below `root` in deterministic path order.

    Args:
        root: Directory to traverse recursively.

    Yields:
        File paths sorted by POSIX-style path string.

    Raises:
        DatasetPermissionError: If traversal fails due to filesystem access.

    """
    try:
        paths = sorted(root.rglob("*"), key=lambda path: path.as_posix())
    except OSError as error:
        message = "Failed to traverse directory."
        raise DatasetPermissionError(
            message,
            context={"path": str(root), "cause": str(error)},
        ) from error

    for path in paths:
        if path.is_file() or path.is_symlink():
            yield path


def ensure_directory(path: Path) -> None:
    """Create a directory and parents if they do not already exist.

    Args:
        path: Directory path to create.

    Raises:
        DatasetPermissionError: If the directory cannot be created.

    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        message = "Failed to create directory."
        raise DatasetPermissionError(
            message,
            context={"path": str(path), "cause": str(error)},
        ) from error
