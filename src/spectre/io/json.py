"""JSON I/O helpers for Spectre infrastructure.

Purpose:
    Provide deterministic JSON serialization for manifests, environment
    metadata, and future reports.

Design:
    JSON is written with sorted keys and indentation for reproducibility and
    human review. Writes are atomic within the target filesystem directory.

Input:
    JSON-compatible Python objects and output paths.

Output:
    UTF-8 encoded JSON files.

Failure modes:
    Serialization and filesystem failures raise project-specific dataset
    manifest exceptions with context.

Complexity:
    Serialization is O(n), where n is the JSON payload size.

Examples:
    >>> import json
    >>> json.dumps({"a": 1}, sort_keys=True)
    '{"a": 1}'

"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from spectre.exceptions.dataset import DatasetManifestError
from spectre.io.filesystem import ensure_directory


def write_json(data: Any, output_path: Path) -> None:  # noqa: ANN401
    """Write JSON data atomically with deterministic formatting.

    Args:
        data: JSON-compatible payload.
        output_path: Destination file path.

    Raises:
        DatasetManifestError: If serialization or writing fails.

    """
    ensure_directory(output_path.parent)
    try:
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=output_path.parent,
            delete=False,
        ) as temporary_file:
            json.dump(data, temporary_file, indent=2, sort_keys=True)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)
        temporary_path.replace(output_path)
    except (OSError, TypeError, ValueError) as error:
        message = "Failed to write JSON file."
        raise DatasetManifestError(
            message,
            context={"path": str(output_path), "cause": str(error)},
        ) from error
