from pathlib import Path

from spectre.utils.reproducibility import collect_environment_info


def test_collect_environment_info_returns_reproducibility_fields() -> None:
    info = collect_environment_info(Path.cwd())

    assert info["python_version"]
    assert info["python_executable"]
    assert info["platform"]
    assert info["spectre_version"] == "0.1.0.dev0"
    assert "conda_prefix" in info
