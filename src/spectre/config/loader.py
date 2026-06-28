"""Hydra configuration loading for Spectre.

Purpose:
    Compose Hydra configuration files and validate the result with Pydantic
    schemas before exposing configuration to the rest of the framework.

Design:
    The loader keeps Hydra/OmegaConf dependencies isolated in this module.
    Callers receive a validated `SpectreConfig` object or a project-specific
    exception with actionable context.

Input:
    A configuration directory and config name. By default these are
    `configs/` and `config` relative to the current working directory.

Output:
    A validated immutable `SpectreConfig` Pydantic model.

Failure modes:
    Missing config directories, Hydra composition failures, and schema
    validation failures raise `ConfigLoadError` or `ConfigValidationError`.

Complexity:
    Composition and validation are O(n), where n is the size of the composed
    configuration tree.

Examples:
    >>> from pathlib import Path
    >>> isinstance(Path("configs"), Path)
    True

"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf
from pydantic import ValidationError as PydanticValidationError

from spectre.config.schemas import SpectreConfig
from spectre.constants import CONFIG_DIR_NAME, DEFAULT_CONFIG_NAME
from spectre.exceptions.config import ConfigLoadError, ConfigValidationError


def load_config(
    config_path: Path = Path(CONFIG_DIR_NAME),
    config_name: str = DEFAULT_CONFIG_NAME,
) -> SpectreConfig:
    """Load and validate a Spectre configuration.

    Args:
        config_path: Directory containing Hydra configuration files.
        config_name: Hydra config name without `.yaml` suffix.

    Returns:
        A validated `SpectreConfig` instance.

    Raises:
        ConfigLoadError: If the configuration directory is missing or Hydra
            composition fails.
        ConfigValidationError: If the composed config violates the Pydantic
            schema.

    """
    resolved_config_path = config_path.resolve()
    if not resolved_config_path.is_dir():
        message = "Configuration directory does not exist."
        fix_hint = "Create the config directory or pass a valid config path."
        raise ConfigLoadError(
            message,
            context={"config_path": str(resolved_config_path)},
            fix_hint=fix_hint,
        )

    try:
        with initialize_config_dir(
            config_dir=str(resolved_config_path),
            version_base=None,
        ):
            composed = compose(config_name=config_name)
    except Exception as error:
        message = "Failed to compose Hydra configuration."
        fix_hint = "Check Hydra defaults and referenced config groups."
        raise ConfigLoadError(
            message,
            context={
                "config_path": str(resolved_config_path),
                "config_name": config_name,
                "cause": str(error),
            },
            fix_hint=fix_hint,
        ) from error

    raw_config = OmegaConf.to_container(composed, resolve=True)
    if not isinstance(raw_config, dict):
        message = "Composed configuration is not a mapping."
        raise ConfigValidationError(
            message,
            context={"config_name": config_name},
        )

    typed_config = cast(dict[str, Any], raw_config)
    return validate_config(typed_config)


def validate_config(raw_config: dict[str, Any]) -> SpectreConfig:
    """Validate a raw configuration dictionary.

    Args:
        raw_config: Mapping produced by Hydra/OmegaConf or tests.

    Returns:
        A validated `SpectreConfig` instance.

    Raises:
        ConfigValidationError: If validation fails.

    """
    try:
        return SpectreConfig.model_validate(raw_config)
    except PydanticValidationError as error:
        message = "Spectre configuration validation failed."
        fix_hint = "Update the relevant YAML config file to match the schema."
        raise ConfigValidationError(
            message,
            context={"errors": error.errors()},
            fix_hint=fix_hint,
        ) from error
