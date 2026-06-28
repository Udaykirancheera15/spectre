"""Project-specific exception hierarchy for Spectre.

Purpose:
    Re-export stable exception classes for callers that need typed error
    handling across configuration, dataset, and validation subsystems.

Design:
    Exception implementations live in focused modules. This package initializer
    exposes the public exception API while avoiding side effects.

Input:
    This module accepts no runtime input.

Output:
    Importing this package exposes project-specific exception classes.

Failure modes:
    Import failures indicate packaging or dependency corruption.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.exceptions import SpectreError
    >>> issubclass(SpectreError, Exception)
    True

"""

from spectre.exceptions.base import NotImplementedForMilestoneError, SpectreError
from spectre.exceptions.config import (
    ConfigLoadError,
    ConfigValidationError,
    SpectreConfigError,
)
from spectre.exceptions.dataset import (
    DatasetManifestError,
    DatasetNotFoundError,
    DatasetPermissionError,
    DatasetStructureError,
    SpectreDatasetError,
)
from spectre.exceptions.registry import (
    DuplicatePluginError,
    InvalidPluginError,
    PluginNotFoundError,
    SpectreRegistryError,
)
from spectre.exceptions.validation import (
    SpectreValidationError,
    UnsupportedValidationCheckError,
    ValidationFailedError,
)

__all__ = [
    "ConfigLoadError",
    "ConfigValidationError",
    "DatasetManifestError",
    "DatasetNotFoundError",
    "DatasetPermissionError",
    "DatasetStructureError",
    "DuplicatePluginError",
    "InvalidPluginError",
    "NotImplementedForMilestoneError",
    "PluginNotFoundError",
    "SpectreConfigError",
    "SpectreDatasetError",
    "SpectreError",
    "SpectreRegistryError",
    "SpectreValidationError",
    "UnsupportedValidationCheckError",
    "ValidationFailedError",
]
