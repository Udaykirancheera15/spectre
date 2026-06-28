from dataclasses import FrozenInstanceError, dataclass

import pytest

from spectre.exceptions.registry import (
    DuplicatePluginError,
    InvalidPluginError,
    PluginNotFoundError,
)
from spectre.plugins import PluginMetadata, SpectrePlugin
from spectre.registry import PluginRegistry


@dataclass(frozen=True, slots=True)
class ExamplePlugin:
    """Minimal test plugin implementing the SpectrePlugin protocol."""

    metadata: PluginMetadata


def test_plugin_metadata_is_frozen_and_validated() -> None:
    metadata = PluginMetadata("example", "0.1.0", "Example plugin")

    assert metadata.name == "example"
    with pytest.raises(FrozenInstanceError):
        metadata.name = "other"  # type: ignore[misc]


def test_plugin_metadata_rejects_empty_required_fields() -> None:
    with pytest.raises(ValueError, match="name"):
        PluginMetadata("", "0.1.0", "description")
    with pytest.raises(ValueError, match="version"):
        PluginMetadata("name", "", "description")
    with pytest.raises(ValueError, match="description"):
        PluginMetadata("name", "0.1.0", "")


def test_example_plugin_satisfies_protocol() -> None:
    plugin = ExamplePlugin(PluginMetadata("example", "0.1.0", "Example plugin"))

    assert isinstance(plugin, SpectrePlugin)


def test_registry_registers_and_gets_plugin() -> None:
    plugin = ExamplePlugin(PluginMetadata("example", "0.1.0", "Example plugin"))
    registry: PluginRegistry[ExamplePlugin] = PluginRegistry()

    registry.register(plugin)

    assert len(registry) == 1
    assert "example" in registry
    assert registry.get("example") is plugin


def test_registry_initializes_from_iterable() -> None:
    plugin = ExamplePlugin(PluginMetadata("example", "0.1.0", "Example plugin"))
    registry = PluginRegistry((plugin,))

    assert registry.names() == ("example",)


def test_registry_lists_names_and_metadata_deterministically() -> None:
    second = ExamplePlugin(PluginMetadata("second", "0.1.0", "Second plugin"))
    first = ExamplePlugin(PluginMetadata("first", "0.1.0", "First plugin"))
    registry = PluginRegistry((second, first))

    assert registry.names() == ("first", "second")
    assert tuple(metadata.name for metadata in registry.metadata()) == (
        "first",
        "second",
    )


def test_registry_rejects_duplicate_plugin_names() -> None:
    first = ExamplePlugin(PluginMetadata("example", "0.1.0", "First plugin"))
    second = ExamplePlugin(PluginMetadata("example", "0.1.0", "Second plugin"))
    registry = PluginRegistry((first,))

    with pytest.raises(DuplicatePluginError, match="already registered"):
        registry.register(second)


def test_registry_raises_for_missing_plugin() -> None:
    registry: PluginRegistry[ExamplePlugin] = PluginRegistry()

    with pytest.raises(PluginNotFoundError, match="not registered"):
        registry.get("missing")


def test_registry_rejects_plugin_without_metadata() -> None:
    registry: PluginRegistry[SpectrePlugin] = PluginRegistry()

    with pytest.raises(InvalidPluginError, match="metadata"):
        registry.register(object())  # type: ignore[arg-type]


def test_registry_rejects_invalid_metadata_type() -> None:
    class BadPlugin:
        @property
        def metadata(self) -> str:
            return "invalid"

    registry: PluginRegistry[SpectrePlugin] = PluginRegistry()

    with pytest.raises(InvalidPluginError, match="PluginMetadata"):
        registry.register(BadPlugin())  # type: ignore[arg-type]
