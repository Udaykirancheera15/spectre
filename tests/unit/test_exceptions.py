from types import MappingProxyType

from spectre.exceptions import (
    ConfigLoadError,
    ConfigValidationError,
    DatasetManifestError,
    DatasetNotFoundError,
    DatasetPermissionError,
    DatasetStructureError,
    DuplicatePluginError,
    InvalidPluginError,
    NotImplementedForMilestoneError,
    PluginNotFoundError,
    SpectreConfigError,
    SpectreDatasetError,
    SpectreError,
    SpectreRegistryError,
    SpectreValidationError,
    UnsupportedValidationCheckError,
    ValidationFailedError,
)


def test_spectre_error_formats_message_context_and_fix_hint() -> None:
    error = SpectreError(
        "Dataset validation failed",
        context={"path": "dataset/train"},
        fix_hint="Check the dataset contract.",
    )

    rendered = str(error)

    assert "Dataset validation failed" in rendered
    assert "path=dataset/train" in rendered
    assert "Check the dataset contract" in rendered


def test_spectre_error_context_is_immutable() -> None:
    error = SpectreError("failure", context={"key": "value"})

    assert isinstance(error.context, MappingProxyType)


def test_config_exception_hierarchy() -> None:
    assert issubclass(ConfigLoadError, SpectreConfigError)
    assert issubclass(ConfigValidationError, SpectreConfigError)
    assert issubclass(SpectreConfigError, SpectreError)


def test_dataset_exception_hierarchy() -> None:
    dataset_errors = (
        DatasetManifestError,
        DatasetNotFoundError,
        DatasetPermissionError,
        DatasetStructureError,
    )

    for error_type in dataset_errors:
        assert issubclass(error_type, SpectreDatasetError)
    assert issubclass(SpectreDatasetError, SpectreError)


def test_validation_exception_hierarchy() -> None:
    assert issubclass(UnsupportedValidationCheckError, SpectreValidationError)
    assert issubclass(ValidationFailedError, SpectreValidationError)
    assert issubclass(SpectreValidationError, SpectreError)


def test_registry_exception_hierarchy() -> None:
    assert issubclass(DuplicatePluginError, SpectreRegistryError)
    assert issubclass(InvalidPluginError, SpectreRegistryError)
    assert issubclass(PluginNotFoundError, SpectreRegistryError)
    assert issubclass(SpectreRegistryError, SpectreError)


def test_milestone_exception_is_project_specific() -> None:
    assert issubclass(NotImplementedForMilestoneError, SpectreError)
