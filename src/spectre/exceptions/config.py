"""Configuration exception types for Spectre.

Purpose:
    Provide typed failures for configuration loading, composition, and schema
    validation.

Design:
    Configuration errors inherit from `SpectreError` through
    `SpectreConfigError`, allowing callers to catch either broad Spectre
    failures or config-specific failures.

Input:
    Exceptions accept messages, structured context, and optional fix hints.

Output:
    Raised exceptions provide actionable configuration diagnostics.

Failure modes:
    These classes do not perform I/O and should not fail during construction.

Complexity:
    Construction is O(k), where k is the number of context fields.

Examples:
    >>> issubclass(ConfigValidationError, SpectreConfigError)
    True

"""

from __future__ import annotations

from spectre.exceptions.base import SpectreError


class SpectreConfigError(SpectreError):
    """Base class for Spectre configuration failures."""


class ConfigLoadError(SpectreConfigError):
    """Raised when a configuration source cannot be loaded."""


class ConfigValidationError(SpectreConfigError):
    """Raised when a loaded configuration violates the schema."""
