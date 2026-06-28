"""Spectre plugin contracts.

Purpose:
    Expose metadata-level plugin contracts for future Spectre extension points.

Design:
    Plugins define what can be registered; registries live separately under
    `spectre.registry` so the registration mechanism can scale independently.

Input:
    This module accepts no runtime input.

Output:
    Importing this package exposes `PluginMetadata` and `SpectrePlugin`.

Failure modes:
    Import failures indicate packaging corruption.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.plugins import PluginMetadata
    >>> PluginMetadata("name", "0.1.0", "description").name
    'name'

"""

from spectre.plugins.base import PluginMetadata, SpectrePlugin

__all__ = ["PluginMetadata", "SpectrePlugin"]
