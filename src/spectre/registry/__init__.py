"""Spectre registry package.

Purpose:
    Expose deterministic registries for Spectre extension points.

Design:
    Registries are separated from plugin contracts so discovery, storage, and
    listing mechanisms can evolve independently from plugin APIs.

Input:
    Plugin instances implementing `SpectrePlugin`.

Output:
    Registered plugin instances and metadata.

Failure modes:
    Public registry operations raise project-specific registry exceptions.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.registry import PluginRegistry
    >>> len(PluginRegistry())
    0

"""

from spectre.registry.registry import PluginRegistry

__all__ = ["PluginRegistry"]
