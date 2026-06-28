"""Spectre dataset infrastructure package.

Purpose:
    Provide M0-safe dataset validation, hashing, and manifest generation.

Design:
    This package validates filesystem structure and metadata only. It does not
    parse PCAP contents, extract flows, tokenize traffic, or mutate captures.

Input:
    Validated dataset configuration and capture file paths.

Output:
    Dataset summaries, hashes, and deterministic manifests.

Failure modes:
    Public functions raise project-specific dataset or validation exceptions for
    unrecoverable failures and return structured issues for expected data
    problems.

Complexity:
    Validation is O(n log n) without hashing and O(total_bytes) with hashing.

Examples:
    >>> from spectre.datasets import validate_dataset
    >>> callable(validate_dataset)
    True

"""

from spectre.datasets.hashes import compute_hash, compute_optional_hashes
from spectre.datasets.manifest import build_dataset_manifest, write_dataset_manifest
from spectre.datasets.validation import validate_dataset

__all__ = [
    "build_dataset_manifest",
    "compute_hash",
    "compute_optional_hashes",
    "validate_dataset",
    "write_dataset_manifest",
]
