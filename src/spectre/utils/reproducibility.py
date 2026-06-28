"""Reproducibility helpers for Spectre.

Purpose:
    Collect runtime metadata needed to reproduce M0 infrastructure checks and
    future experiments.

Design:
    Helpers use only the Python standard library and Spectre version metadata.
    They do not mutate global random state in M0.

Input:
    Optional repository root paths for Git revision discovery.

Output:
    JSON-compatible dictionaries containing Python, platform, Conda, and Spectre
    metadata.

Failure modes:
    Missing environment variables are represented as `None`; metadata collection
    should not fail normal CLI operation.

Complexity:
    Metadata collection is O(1), excluding Git metadata lookup.

Examples:
    >>> info = collect_environment_info()
    >>> "python_version" in info
    True

"""

from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from spectre.version import collect_build_metadata


def collect_environment_info(repo_root: Path | None = None) -> dict[str, object]:
    """Collect JSON-compatible environment metadata.

    Args:
        repo_root: Optional path used for Git revision discovery.

    Returns:
        Dictionary containing interpreter, platform, Conda, and build metadata.

    """
    build_metadata = collect_build_metadata(repo_root)
    return {
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "conda_prefix": os.environ.get("CONDA_PREFIX"),
        "conda_default_env": os.environ.get("CONDA_DEFAULT_ENV"),
        "spectre_version": build_metadata.version,
        "git_revision": build_metadata.git_revision,
    }
