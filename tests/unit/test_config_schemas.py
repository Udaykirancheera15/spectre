import pytest
from pydantic import ValidationError

from spectre.config.schemas import (
    DatasetChecksConfig,
    DatasetConfig,
    LoggingConfig,
    RuntimeConfig,
    SpectreConfig,
)


def test_default_spectre_config_matches_m0_defaults() -> None:
    config = SpectreConfig()

    assert config.project_name == "spectre"
    assert config.dataset.root.name == "dataset"
    assert config.dataset.splits == ("train", "val", "test")
    assert config.dataset.labels == ("benign", "malware")
    assert config.logging.level == "INFO"
    assert not config.logging.json_logs
    assert config.runtime.seed == 1337


def test_dataset_config_normalizes_extensions() -> None:
    config = DatasetConfig(allowed_extensions=(".PCAP", ".PCAPNG"))

    assert config.allowed_extensions == (".pcap", ".pcapng")


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("splits", ("train", "train")),
        ("labels", ("benign", "benign")),
        ("allowed_extensions", (".pcap", ".pcap")),
    ],
)
def test_dataset_config_rejects_duplicates(
    field_name: str,
    value: tuple[str, str],
) -> None:
    with pytest.raises(ValidationError, match="duplicate"):
        DatasetConfig.model_validate({field_name: value})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("splits", ("dev",)),
        ("labels", ("unknown",)),
        ("allowed_extensions", (".txt",)),
    ],
)
def test_dataset_config_rejects_unknown_values(
    field_name: str,
    value: tuple[str, ...],
) -> None:
    with pytest.raises(ValidationError, match="unsupported"):
        DatasetConfig.model_validate({field_name: value})


def test_dataset_config_rejects_empty_values() -> None:
    with pytest.raises(ValidationError, match="at least one"):
        DatasetConfig(splits=())


def test_dataset_checks_require_hash_algorithm_for_duplicate_detection() -> None:
    with pytest.raises(ValidationError, match="detect_duplicate_hashes"):
        DatasetChecksConfig(detect_duplicate_hashes=True)


def test_logging_config_rejects_invalid_level() -> None:
    with pytest.raises(ValidationError):
        LoggingConfig(level="TRACE")  # type: ignore[arg-type]


def test_runtime_config_rejects_negative_seed() -> None:
    with pytest.raises(ValidationError):
        RuntimeConfig(seed=-1)


def test_spectre_config_rejects_empty_project_name() -> None:
    with pytest.raises(ValidationError, match="project_name"):
        SpectreConfig(project_name="")


def test_spectre_config_rejects_unknown_top_level_fields() -> None:
    with pytest.raises(ValidationError):
        SpectreConfig(extra_field=True)  # type: ignore[call-arg]
