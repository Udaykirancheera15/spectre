"""Version and build metadata helpers for Spectre.

Purpose:
    Provide semantic version metadata and best-effort source revision discovery
    without depending on external commands. Reproducible research artifacts can
    embed this metadata to identify the exact software state used for a run.

Design:
    The module exposes a PEP 440-compatible version string and helper functions
    that inspect Git metadata directly from the filesystem. It avoids invoking
    the `git` executable so it remains deterministic in minimal environments.

Input:
    Optional repository root paths may be supplied to revision helpers. If no
    path is supplied, discovery starts from the current working directory.

Output:
    Functions return immutable build metadata or `None` when revision metadata
    cannot be discovered.

Failure modes:
    Malformed or missing Git metadata is treated as unavailable metadata and
    returns `None`; filesystem permission failures are also handled as unknown
    metadata because version discovery must not prevent package import.

Complexity:
    Revision lookup is O(d + r), where d is the directory depth searched for a
    `.git` entry and r is the size of the referenced Git metadata file.

Examples:
    >>> from spectre.version import __version__
    >>> __version__.startswith("0.1.0")
    True

"""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from pathlib import Path

from spectre.constants import VERSION

__version__: str = VERSION


@dataclass(frozen=True, slots=True)
class BuildMetadata:
    """Immutable build metadata for a Spectre runtime.

    Attributes:
        version: PEP 440-compatible Spectre package version.
        git_revision: Best-effort Git commit SHA, or `None` if unavailable.
        python_version: Full Python interpreter version string.
        platform: Platform descriptor from the Python standard library.

    """

    version: str
    git_revision: str | None
    python_version: str
    platform: str


def get_git_revision(repo_root: Path | None = None) -> str | None:
    """Return the current Git revision for a repository if discoverable.

    Args:
        repo_root: Optional path inside or at the repository root. If omitted,
            discovery starts from the current working directory.

    Returns:
        A Git commit SHA string when available; otherwise `None`.

    Failure modes:
        Returns `None` when `.git` metadata is absent, malformed, unreadable, or
        represented in a form not handled by M0 revision discovery.

    """
    start = (repo_root or Path.cwd()).resolve()
    git_entry = _find_git_entry(start)
    git_dir = _resolve_git_dir(git_entry) if git_entry is not None else None
    if git_dir is None:
        return None

    head = _read_text(git_dir / "HEAD")
    if not head:
        return None

    return _revision_from_head(git_dir, head)


def collect_build_metadata(repo_root: Path | None = None) -> BuildMetadata:
    """Collect immutable Spectre build metadata for logs and artifacts.

    Args:
        repo_root: Optional path used for Git revision discovery.

    Returns:
        A `BuildMetadata` instance containing package, interpreter, platform,
        and best-effort source revision information.

    """
    return BuildMetadata(
        version=__version__,
        git_revision=get_git_revision(repo_root),
        python_version=sys.version,
        platform=platform.platform(),
    )


def _find_git_entry(start: Path) -> Path | None:
    """Find the nearest `.git` file or directory from `start` upward."""
    current = start if start.is_dir() else start.parent
    for candidate in (current, *current.parents):
        git_entry = candidate / ".git"
        if git_entry.exists():
            return git_entry
    return None


def _resolve_git_dir(git_entry: Path) -> Path | None:
    """Resolve a Git metadata directory from a `.git` path."""
    if git_entry.is_dir():
        return git_entry

    content = _read_text(git_entry)
    if content is None or not content.startswith("gitdir:"):
        return None

    git_dir_text = content.removeprefix("gitdir:").strip()
    if not git_dir_text:
        return None

    git_dir = Path(git_dir_text)
    if not git_dir.is_absolute():
        git_dir = git_entry.parent / git_dir
    return git_dir.resolve()


def _revision_from_head(git_dir: Path, head: str) -> str | None:
    """Resolve a Git revision from HEAD file contents."""
    stripped_head = head.strip()
    if not stripped_head:
        return None
    if not stripped_head.startswith("ref:"):
        return stripped_head

    ref_name = stripped_head.removeprefix("ref:").strip()
    if not ref_name:
        return None

    revision = _read_text(git_dir / ref_name)
    return revision.strip() if revision else None


def _read_text(path: Path) -> str | None:
    """Read UTF-8 text from a path, returning `None` on I/O failure."""
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
