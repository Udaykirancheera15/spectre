"""Streaming file hash utilities for Spectre datasets.

Purpose:
    Compute reproducibility hashes for capture files without loading entire
    files into memory.

Design:
    Hashing uses Python's `hashlib` in fixed-size chunks. Supported algorithms
    are centralized in `spectre.constants`.

Input:
    File paths and a supported hash algorithm name.

Output:
    Lowercase hexadecimal digest strings.

Failure modes:
    Missing paths and unreadable files raise project-specific dataset
    exceptions.

Complexity:
    Runtime is O(b), where b is file size in bytes. Memory use is O(1).

Examples:
    >>> from spectre.constants import HASH_ALGORITHM_SHA256
    >>> HASH_ALGORITHM_SHA256
    'sha256'

"""

from __future__ import annotations

import hashlib
from pathlib import Path

from spectre.constants import HASH_ALGORITHM_MD5, HASH_ALGORITHM_SHA256, HASH_ALGORITHMS
from spectre.exceptions.dataset import DatasetNotFoundError, DatasetPermissionError
from spectre.exceptions.validation import UnsupportedValidationCheckError

_CHUNK_SIZE_BYTES: int = 1024 * 1024


def compute_hash(path: Path, algorithm: str) -> str:
    """Compute a streaming file hash.

    Args:
        path: File path to hash.
        algorithm: Supported algorithm name, currently `md5` or `sha256`.

    Returns:
        Hexadecimal digest string.

    Raises:
        DatasetNotFoundError: If the file does not exist.
        DatasetPermissionError: If the file cannot be read.
        UnsupportedValidationCheckError: If the algorithm is unsupported.

    """
    if algorithm not in HASH_ALGORITHMS:
        message = "Unsupported hash algorithm."
        raise UnsupportedValidationCheckError(
            message,
            context={"algorithm": algorithm, "supported": HASH_ALGORITHMS},
        )
    if not path.exists():
        message = "Cannot hash missing file."
        raise DatasetNotFoundError(message, context={"path": str(path)})
    if not path.is_file():
        message = "Cannot hash non-file path."
        raise DatasetNotFoundError(message, context={"path": str(path)})

    digest = hashlib.new(algorithm)
    try:
        with path.open("rb") as file_obj:
            for chunk in iter(lambda: file_obj.read(_CHUNK_SIZE_BYTES), b""):
                digest.update(chunk)
    except OSError as error:
        message = "Cannot read file for hashing."
        raise DatasetPermissionError(
            message,
            context={"path": str(path), "cause": str(error)},
        ) from error
    return digest.hexdigest()


def compute_optional_hashes(
    path: Path,
    *,
    compute_md5: bool,
    compute_sha256: bool,
) -> tuple[str | None, str | None]:
    """Compute optional MD5 and SHA-256 hashes for a file.

    Args:
        path: File path to hash.
        compute_md5: Whether to compute MD5.
        compute_sha256: Whether to compute SHA-256.

    Returns:
        Tuple `(md5, sha256)` where disabled hashes are `None`.

    """
    md5 = compute_hash(path, HASH_ALGORITHM_MD5) if compute_md5 else None
    sha256 = compute_hash(path, HASH_ALGORITHM_SHA256) if compute_sha256 else None
    return md5, sha256
