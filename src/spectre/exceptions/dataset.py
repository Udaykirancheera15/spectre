"""Dataset exception types for Spectre.

Purpose:
    Provide typed failures for dataset discovery, validation, manifesting, and
    filesystem access.

Design:
    Dataset exceptions inherit from `SpectreDatasetError`, enabling callers to
    handle dataset-specific failures without catching unrelated Spectre errors.

Input:
    Exceptions accept messages, structured context, and optional fix hints.

Output:
    Raised exceptions provide actionable diagnostics for dataset issues.

Failure modes:
    These classes do not perform I/O and should not fail during construction.

Complexity:
    Construction is O(k), where k is the number of context fields.

Examples:
    >>> issubclass(DatasetNotFoundError, SpectreDatasetError)
    True

"""

from __future__ import annotations

from spectre.exceptions.base import SpectreError


class SpectreDatasetError(SpectreError):
    """Base class for Spectre dataset failures."""


class DatasetNotFoundError(SpectreDatasetError):
    """Raised when a configured dataset root or path does not exist."""


class DatasetStructureError(SpectreDatasetError):
    """Raised when the dataset directory structure is invalid."""


class DatasetPermissionError(SpectreDatasetError):
    """Raised when a dataset path cannot be read as required."""


class DatasetManifestError(SpectreDatasetError):
    """Raised when dataset manifest generation or serialization fails."""
