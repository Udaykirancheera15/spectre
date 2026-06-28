"""Validation exception types for Spectre.

Purpose:
    Provide typed failures for validation routines that are not specific to one
    domain, such as unsupported checks or unrecoverable validation failures.

Design:
    Validation exceptions inherit from `SpectreValidationError`, separating
    validation policy failures from configuration and dataset access failures.

Input:
    Exceptions accept messages, structured context, and optional fix hints.

Output:
    Raised exceptions provide actionable validation diagnostics.

Failure modes:
    These classes do not perform I/O and should not fail during construction.

Complexity:
    Construction is O(k), where k is the number of context fields.

Examples:
    >>> issubclass(ValidationFailedError, SpectreValidationError)
    True

"""

from __future__ import annotations

from spectre.exceptions.base import SpectreError


class SpectreValidationError(SpectreError):
    """Base class for Spectre validation failures."""


class ValidationFailedError(SpectreValidationError):
    """Raised when a validation process fails unrecoverably."""


class UnsupportedValidationCheckError(SpectreValidationError):
    """Raised when a requested validation check is unsupported."""
