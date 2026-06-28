from pathlib import Path

from typer.testing import CliRunner

from spectre.cli.main import app

runner = CliRunner()


def _make_dataset(root: Path) -> None:
    for split in ("train", "val", "test"):
        for label in ("benign", "malware"):
            directory = root / split / label
            directory.mkdir(parents=True)
            (directory / f"{split}_{label}.pcap").write_bytes(b"capture")


def _write_config_tree(config_root: Path, dataset_root: Path) -> None:
    (config_root / "dataset").mkdir(parents=True)
    (config_root / "logging").mkdir()
    (config_root / "runtime").mkdir()
    (config_root / "config.yaml").write_text(
        "defaults:\n"
        "  - dataset: local\n"
        "  - logging: default\n"
        "  - runtime: local\n"
        "  - _self_\n"
        "project_name: spectre\n",
        encoding="utf-8",
    )
    (config_root / "dataset" / "local.yaml").write_text(
        f"root: {dataset_root.as_posix()}\n"
        "splits: [train, val, test]\n"
        "labels: [benign, malware]\n"
        "allowed_extensions: [.pcap, .pcapng, .cap]\n"
        "require_non_empty: true\n"
        "checks:\n"
        "  compute_sha256: false\n"
        "  compute_md5: false\n"
        "  check_mime_type: false\n"
        "  check_permissions: true\n"
        "  allow_symlinks: false\n"
        "  detect_duplicate_hashes: false\n"
        "  fail_on_unknown_extensions: true\n",
        encoding="utf-8",
    )
    (config_root / "logging" / "default.yaml").write_text(
        "level: INFO\njson: false\nshow_timestamp: true\nshow_level: true\n",
        encoding="utf-8",
    )
    (config_root / "runtime" / "local.yaml").write_text(
        "seed: 1337\n"
        "output_dir: outputs\n"
        "artifact_dir: artifacts\n"
        "report_dir: reports\n"
        "log_dir: logs\n"
        "mlruns_dir: mlruns\n",
        encoding="utf-8",
    )


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "0.1.0.dev0" in result.output


def test_cli_config_validate_with_temp_config(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    config_root = tmp_path / "configs"
    _make_dataset(dataset_root)
    _write_config_tree(config_root, dataset_root)

    result = runner.invoke(
        app,
        ["config", "validate", "--config-path", str(config_root)],
    )

    assert result.exit_code == 0
    assert "Configuration valid" in result.output


def test_cli_dataset_validate_and_manifest(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    config_root = tmp_path / "configs"
    output_path = tmp_path / "manifest.json"
    _make_dataset(dataset_root)
    _write_config_tree(config_root, dataset_root)

    validate_result = runner.invoke(
        app,
        ["dataset", "validate", "--config-path", str(config_root)],
    )
    manifest_result = runner.invoke(
        app,
        [
            "dataset",
            "manifest",
            "--output",
            str(output_path),
            "--config-path",
            str(config_root),
        ],
    )

    assert validate_result.exit_code == 0
    assert "Dataset files: 6" in validate_result.output
    assert manifest_result.exit_code == 0
    assert output_path.is_file()


def test_cli_env_info() -> None:
    result = runner.invoke(app, ["env", "info"])

    assert result.exit_code == 0
    assert "python_version" in result.output


def test_cli_plugins_list() -> None:
    result = runner.invoke(app, ["plugins", "list"])

    assert result.exit_code == 0
    assert "No plugins registered" in result.output


def test_cli_doctor_with_temp_config(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    config_root = tmp_path / "configs"
    _make_dataset(dataset_root)
    _write_config_tree(config_root, dataset_root)

    result = runner.invoke(app, ["doctor", "--config-path", str(config_root)])

    assert result.exit_code == 0
    assert "Spectre Doctor" in result.output
