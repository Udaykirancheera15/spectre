"""Dataset manifest generation for Spectre.

Purpose:
    Convert validated dataset records into deterministic JSON-compatible
    manifests for reproducible research.

Design:
    Manifest generation delegates structural checks to dataset validation and
    serializes records in deterministic order.

Input:
    A validated `DatasetConfig` and optional output path.

Output:
    JSON-compatible manifest dictionaries or written manifest files.

Failure modes:
    Dataset validation and JSON writing raise project-specific exceptions.

Complexity:
    Manifest generation is O(n log n) without hashing and O(total_bytes) with
    hashing enabled.

Examples:
    >>> from spectre.config.schemas import DatasetConfig
    >>> DatasetConfig().root.name
    'dataset'

"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from spectre.config.schemas import DatasetConfig
from spectre.datasets.validation import validate_dataset
from spectre.io.json import write_json
from spectre.version import collect_build_metadata


def build_dataset_manifest(config: DatasetConfig) -> dict[str, Any]:
    """Build a deterministic JSON-compatible dataset manifest.

    Args:
        config: Validated dataset configuration.

    Returns:
        Manifest dictionary suitable for JSON serialization.

    """
    summary = validate_dataset(config)
    build_metadata = collect_build_metadata(Path.cwd())
    return {
        "dataset_root": str(config.root),
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "spectre": {
            "version": build_metadata.version,
            "git_revision": build_metadata.git_revision,
            "python_version": build_metadata.python_version,
            "platform": build_metadata.platform,
        },
        "summary": {
            "total_files": summary.total_files,
            "total_bytes": summary.total_bytes,
            "is_valid": summary.is_valid,
            "counts_by_split_label": [
                {"split": split, "label": label, "count": count}
                for split, label, count in summary.counts_by_split_label
            ],
            "issue_count": len(summary.issues),
        },
        "records": [
            {
                "split": record.split,
                "label": record.label,
                "path": record.path.as_posix(),
                "size_bytes": record.size_bytes,
                "extension": record.extension,
                "md5": record.md5,
                "sha256": record.sha256,
                "mime_type": record.mime_type,
            }
            for record in sorted(summary.records, key=lambda item: item.path.as_posix())
        ],
        "issues": [
            {
                "path": issue.path.as_posix(),
                "code": issue.code,
                "message": issue.message,
                "fix_hint": issue.fix_hint,
            }
            for issue in sorted(summary.issues, key=lambda item: item.path.as_posix())
        ],
    }


def write_dataset_manifest(config: DatasetConfig, output_path: Path) -> None:
    """Build and write a dataset manifest JSON file.

    Args:
        config: Validated dataset configuration.
        output_path: Destination JSON path.

    """
    write_json(build_dataset_manifest(config), output_path)
