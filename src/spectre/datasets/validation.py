"""Structural dataset validation for Spectre.

Purpose:
    Validate the existing dataset layout and file-level metadata required for
    reproducible M0 infrastructure without parsing packets or extracting flows.

Design:
    Validation is configurable through `DatasetConfig`. Expected dataset
    problems are returned as structured `DatasetValidationIssue` objects;
    unrecoverable root access failures raise project-specific exceptions.

Input:
    A validated `DatasetConfig` object.

Output:
    A `DatasetSummary` containing valid records, issues, counts, and optional
    hashes/MIME guesses.

Failure modes:
    Missing dataset roots raise `DatasetNotFoundError`. File-level validation
    problems are reported as issues so researchers can inspect all failures at
    once.

Complexity:
    Without hashing validation is O(n log n) due to deterministic traversal.
    With hashing it is O(total_bytes).

Examples:
    >>> from spectre.config.schemas import DatasetConfig
    >>> DatasetConfig().root.name
    'dataset'

"""

from __future__ import annotations

import mimetypes
import os
from collections import Counter, defaultdict
from pathlib import Path

from spectre.config.schemas import DatasetConfig
from spectre.datasets.hashes import compute_optional_hashes
from spectre.domain.dataset import DatasetRecord, DatasetSummary, DatasetValidationIssue
from spectre.exceptions.dataset import DatasetNotFoundError
from spectre.io.filesystem import iter_files_deterministic


def validate_dataset(config: DatasetConfig) -> DatasetSummary:
    """Validate a dataset according to M0 structural checks.

    Args:
        config: Validated dataset configuration.

    Returns:
        Dataset summary containing records and validation issues.

    Raises:
        DatasetNotFoundError: If the dataset root does not exist.

    """
    root = config.root
    if not root.exists():
        message = "Dataset root does not exist."
        raise DatasetNotFoundError(
            message,
            context={"dataset_root": str(root)},
            fix_hint="Create the dataset root or update configs/dataset/local.yaml.",
        )
    if not root.is_dir():
        message = "Dataset root is not a directory."
        raise DatasetNotFoundError(message, context={"dataset_root": str(root)})

    issues = list(_validate_required_structure(config))
    records: list[DatasetRecord] = []

    for split in config.splits:
        for label in config.labels:
            label_dir = root / split / label
            if not label_dir.is_dir():
                continue
            for path in iter_files_deterministic(label_dir):
                issue, include_file = _validate_file_path(path, config)
                if issue is not None:
                    issues.append(issue)
                if not include_file:
                    continue
                records.append(_record_from_path(path, root, split, label, config))

    issues.extend(_duplicate_hash_issues(records, config))
    counts = _counts_by_split_label(records)
    return DatasetSummary(
        records=tuple(records),
        issues=tuple(issues),
        counts_by_split_label=counts,
    )


def _validate_required_structure(
    config: DatasetConfig,
) -> tuple[DatasetValidationIssue, ...]:
    """Return issues for missing split or label directories."""
    issues: list[DatasetValidationIssue] = []
    for split in config.splits:
        split_dir = config.root / split
        if not split_dir.is_dir():
            issues.append(
                DatasetValidationIssue(
                    split_dir,
                    "missing_split_directory",
                    "Required dataset split directory is missing.",
                    "Create the split directory or update dataset.splits.",
                )
            )
            continue
        for label in config.labels:
            label_dir = split_dir / label
            if not label_dir.is_dir():
                issues.append(
                    DatasetValidationIssue(
                        label_dir,
                        "missing_label_directory",
                        "Required dataset label directory is missing.",
                        "Create the label directory or update dataset.labels.",
                    )
                )
    return tuple(issues)


def _validate_file_path(
    path: Path,
    config: DatasetConfig,
) -> tuple[DatasetValidationIssue | None, bool]:
    """Validate one candidate dataset file path.

    Returns:
        Tuple `(issue, include_file)`. Files with issues are excluded from
        records. Unsupported extensions can be ignored when configured.

    """
    if path.is_symlink() and not config.checks.allow_symlinks:
        return (
            DatasetValidationIssue(
                path,
                "symlink_not_allowed",
                "Dataset file is a symbolic link but symlinks are disabled.",
                "Set dataset.checks.allow_symlinks=true only if this is intentional.",
            ),
            False,
        )
    if config.checks.check_permissions and not os.access(path, os.R_OK):
        return (
            DatasetValidationIssue(
                path,
                "unreadable_file",
                "Dataset file is not readable by the current process.",
                "Fix file permissions or remove the file from the dataset.",
            ),
            False,
        )
    extension = path.suffix.lower()
    if extension not in config.allowed_extensions:
        if not config.checks.fail_on_unknown_extensions:
            return None, False
        return (
            DatasetValidationIssue(
                path,
                "unsupported_extension",
                "Dataset file has an unsupported capture extension.",
                "Remove the file or update dataset.allowed_extensions.",
            ),
            False,
        )
    if config.require_non_empty and path.stat().st_size == 0:
        return (
            DatasetValidationIssue(
                path,
                "empty_file",
                "Dataset capture file is empty.",
                "Replace the file with a valid capture or remove it.",
            ),
            False,
        )
    return None, True


def _record_from_path(
    path: Path,
    root: Path,
    split: str,
    label: str,
    config: DatasetConfig,
) -> DatasetRecord:
    """Create a dataset record from a validated path."""
    md5, sha256 = compute_optional_hashes(
        path,
        compute_md5=config.checks.compute_md5,
        compute_sha256=config.checks.compute_sha256,
    )
    mime_type = (
        mimetypes.guess_type(path.name)[0] if config.checks.check_mime_type else None
    )
    return DatasetRecord(
        split=split,
        label=label,
        path=path.relative_to(root),
        size_bytes=path.stat().st_size,
        extension=path.suffix.lower(),
        md5=md5,
        sha256=sha256,
        mime_type=mime_type,
    )


def _duplicate_hash_issues(
    records: list[DatasetRecord],
    config: DatasetConfig,
) -> tuple[DatasetValidationIssue, ...]:
    """Return duplicate hash issues when configured."""
    if not config.checks.detect_duplicate_hashes:
        return ()

    hash_to_paths: defaultdict[str, list[Path]] = defaultdict(list)
    for record in records:
        digest = record.sha256 or record.md5
        if digest is not None:
            hash_to_paths[digest].append(record.path)

    issues: list[DatasetValidationIssue] = []
    for digest, paths in sorted(hash_to_paths.items()):
        if len(paths) <= 1:
            continue
        issues.extend(
            DatasetValidationIssue(
                path,
                "duplicate_hash",
                "Dataset file has duplicate content hash.",
                f"Duplicate digest {digest}; inspect duplicate captures.",
            )
            for path in paths
        )
    return tuple(issues)


def _counts_by_split_label(
    records: list[DatasetRecord],
) -> tuple[tuple[str, str, int], ...]:
    """Return deterministic counts grouped by split and label."""
    counter: Counter[tuple[str, str]] = Counter(
        (record.split, record.label) for record in records
    )
    return tuple(
        (split, label, counter[(split, label)]) for split, label in sorted(counter)
    )
