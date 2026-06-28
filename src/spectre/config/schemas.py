"""Pydantic configuration schemas for Spectre.

Purpose:
    Validate Hydra-composed configuration before it reaches infrastructure,
    dataset validation, logging, or future research components.

Design:
    Pydantic is used only for configuration schemas. Immutable research domain
    objects live under `spectre.domain` as frozen dataclasses.

Input:
    Schemas accept dictionaries produced by Hydra/OmegaConf composition.

Output:
    Validated configuration objects with normalized paths, extensions, labels,
    logging levels, and runtime directories.

Failure modes:
    Invalid configuration raises Pydantic validation errors. Public loader
    functions translate those errors into Spectre-specific exceptions.

Complexity:
    Validation is O(s + l + e), where s is the number of splits, l is labels,
    and e is allowed extensions.

Examples:
    >>> config = SpectreConfig(project_name="spectre")
    >>> config.project_name
    'spectre'

"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from spectre.constants import (
    ARTIFACTS_DIR_NAME,
    DATASET_DIR_NAME,
    DATASET_SPLITS,
    DEFAULT_RANDOM_SEED,
    LABELS,
    LOGS_DIR_NAME,
    MLRUNS_DIR_NAME,
    OUTPUTS_DIR_NAME,
    PROJECT_NAME,
    REPORTS_DIR_NAME,
    SUPPORTED_CAPTURE_EXTENSIONS,
)

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class StrictBaseModel(BaseModel):
    """Base schema that rejects unknown configuration fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class DatasetChecksConfig(StrictBaseModel):
    """Configurable structural dataset validation checks."""

    compute_sha256: bool = False
    compute_md5: bool = False
    check_mime_type: bool = False
    check_permissions: bool = True
    allow_symlinks: bool = False
    detect_duplicate_hashes: bool = False
    fail_on_unknown_extensions: bool = True

    @model_validator(mode="after")
    def validate_duplicate_hash_configuration(self) -> DatasetChecksConfig:
        """Require an enabled hash algorithm for duplicate-hash detection."""
        if self.detect_duplicate_hashes and not (
            self.compute_md5 or self.compute_sha256
        ):
            msg = "detect_duplicate_hashes requires compute_md5 or compute_sha256."
            raise ValueError(msg)
        return self


class DatasetConfig(StrictBaseModel):
    """Dataset configuration schema."""

    root: Path = Path(DATASET_DIR_NAME)
    splits: tuple[str, ...] = DATASET_SPLITS
    labels: tuple[str, ...] = LABELS
    allowed_extensions: tuple[str, ...] = SUPPORTED_CAPTURE_EXTENSIONS
    require_non_empty: bool = True
    checks: DatasetChecksConfig = Field(default_factory=DatasetChecksConfig)

    @field_validator("splits")
    @classmethod
    def validate_splits(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Validate that configured dataset splits are known and unique."""
        return _validate_known_unique_values(
            value=value,
            allowed=DATASET_SPLITS,
            field_name="dataset.splits",
        )

    @field_validator("labels")
    @classmethod
    def validate_labels(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Validate that configured labels are known and unique."""
        return _validate_known_unique_values(
            value=value,
            allowed=LABELS,
            field_name="dataset.labels",
        )

    @field_validator("allowed_extensions")
    @classmethod
    def validate_extensions(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        """Validate supported capture extensions."""
        normalized = tuple(extension.lower() for extension in value)
        return _validate_known_unique_values(
            value=normalized,
            allowed=SUPPORTED_CAPTURE_EXTENSIONS,
            field_name="dataset.allowed_extensions",
        )


class LoggingConfig(StrictBaseModel):
    """Logging configuration schema."""

    level: LogLevel = "INFO"
    json_logs: bool = Field(default=False, alias="json")
    show_timestamp: bool = True
    show_level: bool = True


class RuntimeConfig(StrictBaseModel):
    """Runtime directory and reproducibility configuration schema."""

    seed: int = Field(default=DEFAULT_RANDOM_SEED, ge=0)
    output_dir: Path = Path(OUTPUTS_DIR_NAME)
    artifact_dir: Path = Path(ARTIFACTS_DIR_NAME)
    report_dir: Path = Path(REPORTS_DIR_NAME)
    log_dir: Path = Path(LOGS_DIR_NAME)
    mlruns_dir: Path = Path(MLRUNS_DIR_NAME)


class SpectreConfig(StrictBaseModel):
    """Top-level Spectre configuration schema."""

    project_name: str = PROJECT_NAME
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)

    @field_validator("project_name")
    @classmethod
    def validate_project_name(cls, value: str) -> str:
        """Validate the project name is non-empty."""
        if not value:
            msg = "project_name must be non-empty."
            raise ValueError(msg)
        return value


def _validate_known_unique_values(
    *,
    value: tuple[str, ...],
    allowed: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Validate that values are non-empty, unique, and known."""
    if not value:
        msg = f"{field_name} must contain at least one value."
        raise ValueError(msg)
    if len(set(value)) != len(value):
        msg = f"{field_name} contains duplicate values: {value!r}."
        raise ValueError(msg)
    unknown = tuple(item for item in value if item not in allowed)
    if unknown:
        msg = f"{field_name} contains unsupported values: {unknown!r}."
        raise ValueError(msg)
    return value
