"""Command-line interface for Spectre.

Purpose:
    Provide a hierarchical CLI for M0 infrastructure commands and future
    extension points.

Design:
    Commands are grouped by responsibility: dataset, config, env, plugins,
    version, and doctor. Placeholder report commands are intentionally omitted
    from M0.

Input:
    CLI arguments, Hydra configuration files, and dataset paths.

Output:
    Human-readable terminal summaries and optional JSON artifacts such as
    dataset manifests.

Failure modes:
    Project-specific exceptions are converted to actionable CLI errors with
    non-zero exit codes. Dataset validation issues also produce non-zero exits.

Complexity:
    Command complexity is delegated to underlying infrastructure modules.

Examples:
    Run from an activated environment:

    ```bash
    spectre version
    spectre config validate
    spectre dataset validate
    ```

"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, NoReturn

import typer
from rich.console import Console
from rich.table import Table

from spectre.config.loader import load_config
from spectre.config.schemas import SpectreConfig
from spectre.constants import CONFIG_DIR_NAME, DEFAULT_CONFIG_NAME
from spectre.datasets.manifest import write_dataset_manifest
from spectre.datasets.validation import validate_dataset
from spectre.exceptions.base import SpectreError
from spectre.logging.setup import setup_logging
from spectre.registry import PluginRegistry
from spectre.utils.reproducibility import collect_environment_info
from spectre.version import __version__

app = typer.Typer(help="Spectre research framework CLI.", no_args_is_help=True)
dataset_app = typer.Typer(help="Dataset validation and manifest commands.")
config_app = typer.Typer(help="Configuration commands.")
env_app = typer.Typer(help="Environment metadata commands.")
plugins_app = typer.Typer(help="Plugin registry commands.")

app.add_typer(dataset_app, name="dataset")
app.add_typer(config_app, name="config")
app.add_typer(env_app, name="env")
app.add_typer(plugins_app, name="plugins")

_CONSOLE = Console()
_DEFAULT_CONFIG_PATH = Path(CONFIG_DIR_NAME)
_DEFAULT_MANIFEST_OUTPUT = Path("reports/dataset_manifest.json")
_MAX_DISPLAYED_ISSUES = 10


def _load_config_for_cli(config_path: Path, config_name: str) -> SpectreConfig:
    """Load configuration and translate Spectre errors to CLI exits."""
    try:
        config = load_config(config_path, config_name)
        setup_logging(config.logging)
    except SpectreError as error:
        _exit_with_error(error)
    return config


def _exit_with_error(error: SpectreError) -> NoReturn:
    """Render a Spectre error and terminate with exit code 1."""
    _CONSOLE.print(f"[red]error:[/red] {error}")
    raise typer.Exit(code=1)


@app.command("version")
def version_command() -> None:
    """Print the Spectre package version."""
    _CONSOLE.print(__version__)


@app.command("doctor")
def doctor_command(
    config_path: Annotated[
        Path,
        typer.Option(help="Hydra config directory."),
    ] = _DEFAULT_CONFIG_PATH,
    config_name: Annotated[
        str,
        typer.Option(help="Hydra config name."),
    ] = DEFAULT_CONFIG_NAME,
) -> None:
    """Run M0 environment, configuration, and dataset health checks."""
    config = _load_config_for_cli(config_path, config_name)
    env_info = collect_environment_info(Path.cwd())
    summary = validate_dataset(config.dataset)

    table = Table(title="Spectre Doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    table.add_row("Python", "ok", str(env_info["python_version"]))
    table.add_row("Config", "ok", f"{config_path}/{config_name}.yaml")
    table.add_row(
        "Dataset",
        "ok" if summary.is_valid else "failed",
        f"files={summary.total_files}, issues={len(summary.issues)}",
    )
    _CONSOLE.print(table)
    if not summary.is_valid:
        raise typer.Exit(code=1)


@config_app.command("validate")
def config_validate_command(
    config_path: Annotated[
        Path,
        typer.Option(help="Hydra config directory."),
    ] = _DEFAULT_CONFIG_PATH,
    config_name: Annotated[
        str,
        typer.Option(help="Hydra config name."),
    ] = DEFAULT_CONFIG_NAME,
) -> None:
    """Validate Hydra and Pydantic configuration."""
    config = _load_config_for_cli(config_path, config_name)
    _CONSOLE.print(f"Configuration valid: {config.project_name}")


@dataset_app.command("validate")
def dataset_validate_command(
    config_path: Annotated[
        Path,
        typer.Option(help="Hydra config directory."),
    ] = _DEFAULT_CONFIG_PATH,
    config_name: Annotated[
        str,
        typer.Option(help="Hydra config name."),
    ] = DEFAULT_CONFIG_NAME,
) -> None:
    """Validate dataset structure and configured file checks."""
    config = _load_config_for_cli(config_path, config_name)
    try:
        summary = validate_dataset(config.dataset)
    except SpectreError as error:
        _exit_with_error(error)

    _CONSOLE.print(
        f"Dataset files: {summary.total_files}; bytes: {summary.total_bytes}; "
        f"issues: {len(summary.issues)}"
    )
    for issue in summary.issues[:_MAX_DISPLAYED_ISSUES]:
        _CONSOLE.print(f"[yellow]{issue.code}[/yellow] {issue.path}: {issue.message}")
    if len(summary.issues) > _MAX_DISPLAYED_ISSUES:
        omitted = len(summary.issues) - _MAX_DISPLAYED_ISSUES
        _CONSOLE.print(f"... {omitted} additional issues omitted")
    if not summary.is_valid:
        raise typer.Exit(code=1)


@dataset_app.command("manifest")
def dataset_manifest_command(
    output: Annotated[
        Path,
        typer.Option(help="Output manifest JSON path."),
    ] = _DEFAULT_MANIFEST_OUTPUT,
    config_path: Annotated[
        Path,
        typer.Option(help="Hydra config directory."),
    ] = _DEFAULT_CONFIG_PATH,
    config_name: Annotated[
        str,
        typer.Option(help="Hydra config name."),
    ] = DEFAULT_CONFIG_NAME,
) -> None:
    """Write a deterministic dataset manifest JSON file."""
    config = _load_config_for_cli(config_path, config_name)
    try:
        write_dataset_manifest(config.dataset, output)
    except SpectreError as error:
        _exit_with_error(error)
    _CONSOLE.print(f"Wrote dataset manifest: {output}")


@env_app.command("info")
def env_info_command() -> None:
    """Print environment metadata relevant to reproducibility."""
    env_info = collect_environment_info(Path.cwd())
    table = Table(title="Spectre Environment")
    table.add_column("Key")
    table.add_column("Value")
    for key, value in sorted(env_info.items()):
        table.add_row(key, str(value))
    _CONSOLE.print(table)


@plugins_app.command("list")
def plugins_list_command() -> None:
    """List currently registered built-in plugins.

    M0 defines the registry architecture but does not ship attack, model, or
    evaluator plugins yet.
    """
    registry: PluginRegistry = PluginRegistry()
    if len(registry) == 0:
        _CONSOLE.print("No plugins registered in M0.")
        return
    table = Table(title="Spectre Plugins")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Category")
    table.add_column("Description")
    for metadata in registry.metadata():
        table.add_row(
            metadata.name,
            metadata.version,
            metadata.category or "",
            metadata.description,
        )
    _CONSOLE.print(table)


if __name__ == "__main__":
    app()
