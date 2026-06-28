"""Generic in-memory plugin registry for Spectre.

Purpose:
    Provide a deterministic registration mechanism for future Spectre plugins,
    including probes, evaluators, mutators, tokenizers, classifiers, and
    reporters.

Design:
    The registry stores plugins by stable metadata name and rejects duplicates.
    It is intentionally small, explicit, and deterministic in M0. Entry-point
    discovery can be added later without changing the public registry contract.

Input:
    Objects implementing the `SpectrePlugin` protocol.

Output:
    Registered plugins, sorted plugin names, and sorted metadata tuples.

Failure modes:
    Invalid plugins, duplicate names, and missing lookups raise project-specific
    registry exceptions.

Complexity:
    Registration and lookup are O(1). Listing names or metadata is O(n log n)
    because results are sorted for reproducibility.

Examples:
    >>> registry = PluginRegistry()
    >>> registry.names()
    ()

"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, TypeVar

from spectre.exceptions.registry import (
    DuplicatePluginError,
    InvalidPluginError,
    PluginNotFoundError,
)
from spectre.plugins.base import PluginMetadata, SpectrePlugin

PluginT = TypeVar("PluginT", bound=SpectrePlugin)


class PluginRegistry(Generic[PluginT]):
    """Deterministic registry for Spectre plugin instances."""

    def __init__(self, plugins: Iterable[PluginT] = ()) -> None:
        """Initialize an empty registry and optionally register plugins."""
        self._plugins: dict[str, PluginT] = {}
        for plugin in plugins:
            self.register(plugin)

    def register(self, plugin: PluginT) -> None:
        """Register a plugin by metadata name.

        Args:
            plugin: Plugin instance implementing the `SpectrePlugin` protocol.

        Raises:
            InvalidPluginError: If plugin metadata is invalid.
            DuplicatePluginError: If a plugin with the same name exists.

        """
        metadata = _validate_plugin(plugin)
        if metadata.name in self._plugins:
            message = "Plugin name is already registered."
            raise DuplicatePluginError(
                message,
                context={"plugin_name": metadata.name},
                fix_hint="Use a unique plugin metadata name.",
            )
        self._plugins[metadata.name] = plugin

    def get(self, name: str) -> PluginT:
        """Return a registered plugin by name.

        Args:
            name: Stable plugin metadata name.

        Raises:
            PluginNotFoundError: If the plugin is not registered.

        """
        try:
            return self._plugins[name]
        except KeyError as error:
            message = "Plugin is not registered."
            raise PluginNotFoundError(
                message,
                context={"plugin_name": name},
                fix_hint="List plugins before requesting one by name.",
            ) from error

    def names(self) -> tuple[str, ...]:
        """Return registered plugin names sorted for reproducibility."""
        return tuple(sorted(self._plugins))

    def metadata(self) -> tuple[PluginMetadata, ...]:
        """Return registered plugin metadata sorted by plugin name."""
        return tuple(self._plugins[name].metadata for name in self.names())

    def __contains__(self, name: object) -> bool:
        """Return whether `name` is registered."""
        return isinstance(name, str) and name in self._plugins

    def __len__(self) -> int:
        """Return the number of registered plugins."""
        return len(self._plugins)


def _validate_plugin(plugin: SpectrePlugin) -> PluginMetadata:
    """Validate a plugin contract and return metadata."""
    try:
        metadata = plugin.metadata
    except AttributeError as error:
        message = "Plugin object does not expose metadata."
        raise InvalidPluginError(message) from error

    if not isinstance(metadata, PluginMetadata):
        message = "Plugin metadata must be a PluginMetadata instance."
        raise InvalidPluginError(message)
    return metadata
