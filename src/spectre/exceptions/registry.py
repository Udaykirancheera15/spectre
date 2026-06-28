"""Registry exception types for Spectre.

Purpose:
    Provide typed failures for plugin registration, lookup, and validation.

Design:
    Registry exceptions inherit from `SpectreRegistryError`, which itself
    inherits from the project-wide `SpectreError` base class.

Input:
    Exceptions accept messages, structured context, and optional fix hints.

Output:
    Raised exceptions provide actionable registry diagnostics.

Failure modes:
    These classes do not perform I/O and should not fail during construction.

Complexity:
    Construction is O(k), where k is the number of context fields.

Examples:
    >>> issubclass(DuplicatePluginError, SpectreRegistryError)
    True

"""

from __future__ import annotations

from spectre.exceptions.base import SpectreError


class SpectreRegistryError(SpectreError):
    """Base class for Spectre registry failures."""


class DuplicatePluginError(SpectreRegistryError):
    """Raised when a plugin name is registered more than once."""


class PluginNotFoundError(SpectreRegistryError):
    """Raised when a requested plugin name is absent from a registry."""


class InvalidPluginError(SpectreRegistryError):
    """Raised when an object does not satisfy the plugin contract."""
