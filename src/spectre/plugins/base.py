"""Base plugin contracts for Spectre.

Purpose:
    Define the minimal plugin protocol shared by future probes, evaluators,
    mutators, tokenizers, classifiers, and reporters.

Design:
    M0 defines only metadata-level contracts. Concrete attack families and ML
    components are intentionally deferred to later milestones.

Input:
    Plugin implementations expose immutable metadata through properties.

Output:
    Registries can validate and list plugin identity without importing attack or
    model-specific APIs.

Failure modes:
    Invalid plugin metadata is rejected by registry validation with
    project-specific exceptions.

Complexity:
    Metadata access is O(1).

Examples:
    >>> from spectre.plugins.base import PluginMetadata
    >>> PluginMetadata("example", "0.1.0", "Example plugin").name
    'example'

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """Immutable metadata describing one Spectre plugin.

    Attributes:
        name: Stable unique plugin identifier.
        version: Plugin semantic version or package version.
        description: Human-readable description.
        category: Optional plugin category such as `probe` or `evaluator`.

    """

    name: str
    version: str
    description: str
    category: str | None = None

    def __post_init__(self) -> None:
        """Validate plugin metadata invariants."""
        for field_name, value in (
            ("name", self.name),
            ("version", self.version),
            ("description", self.description),
        ):
            if not value:
                msg = f"Plugin metadata field {field_name} must be non-empty."
                raise ValueError(msg)


@runtime_checkable
class SpectrePlugin(Protocol):
    """Minimal protocol implemented by all Spectre plugins."""

    @property
    def metadata(self) -> PluginMetadata:
        """Return immutable metadata for this plugin."""
