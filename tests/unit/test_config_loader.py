from pathlib import Path

import pytest

from spectre.config.loader import load_config, validate_config
from spectre.exceptions.config import ConfigLoadError, ConfigValidationError


def test_validate_config_accepts_minimal_mapping() -> None:
    config = validate_config({"project_name": "spectre"})

    assert config.project_name == "spectre"


def test_validate_config_wraps_pydantic_errors() -> None:
    with pytest.raises(ConfigValidationError, match="validation failed"):
        validate_config({"project_name": ""})


def test_load_config_loads_repository_default_config() -> None:
    config = load_config(Path("configs"), "config")

    assert config.project_name == "spectre"
    assert config.dataset.root == Path("dataset")
    assert config.dataset.checks.check_permissions


def test_load_config_rejects_missing_config_directory(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(ConfigLoadError, match="does not exist"):
        load_config(missing, "config")


def test_load_config_wraps_hydra_composition_errors(tmp_path: Path) -> None:
    config_dir = tmp_path / "configs"
    config_dir.mkdir()

    with pytest.raises(ConfigLoadError, match="Failed to compose"):
        load_config(config_dir, "missing")


def test_load_config_wraps_schema_errors(tmp_path: Path) -> None:
    config_dir = tmp_path / "configs"
    config_dir.mkdir()
    (config_dir / "config.yaml").write_text("project_name: ''\n", encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="validation failed"):
        load_config(config_dir, "config")
