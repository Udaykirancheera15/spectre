"""Spectre configuration package.

Purpose:
    Provide validated configuration loading for Spectre infrastructure and
    future research components.

Design:
    Hydra composes YAML configuration; Pydantic validates schema correctness.
    Research domain objects remain separate frozen dataclasses.

Input:
    Configuration files under `configs/` or raw dictionaries in tests.

Output:
    Validated `SpectreConfig` instances.

Failure modes:
    Public loading functions raise project-specific configuration exceptions.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.config import SpectreConfig
    >>> SpectreConfig().project_name
    'spectre'

"""

from spectre.config.loader import load_config, validate_config
from spectre.config.schemas import (
    DatasetChecksConfig,
    DatasetConfig,
    LoggingConfig,
    RuntimeConfig,
    SpectreConfig,
)

__all__ = [
    "DatasetChecksConfig",
    "DatasetConfig",
    "LoggingConfig",
    "RuntimeConfig",
    "SpectreConfig",
    "load_config",
    "validate_config",
]
