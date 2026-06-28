import json
from pathlib import Path

from spectre.config.schemas import DatasetChecksConfig, DatasetConfig
from spectre.datasets.manifest import build_dataset_manifest, write_dataset_manifest


def _make_dataset(root: Path) -> None:
    for split in ("train", "val", "test"):
        for label in ("benign", "malware"):
            directory = root / split / label
            directory.mkdir(parents=True)
            (directory / f"{split}_{label}.pcap").write_bytes(b"capture")


def test_build_dataset_manifest_contains_records_summary_and_metadata(
    tmp_path: Path,
) -> None:
    _make_dataset(tmp_path)
    config = DatasetConfig(
        root=tmp_path,
        checks=DatasetChecksConfig(compute_md5=True),
    )

    manifest = build_dataset_manifest(config)

    assert manifest["dataset_root"] == str(tmp_path)
    assert manifest["summary"]["total_files"] == 6
    assert manifest["summary"]["is_valid"] is True
    assert len(manifest["records"]) == 6
    assert manifest["records"] == sorted(
        manifest["records"], key=lambda item: item["path"]
    )
    assert manifest["spectre"]["version"] == "0.1.0.dev0"


def test_write_dataset_manifest_writes_json(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    _make_dataset(dataset_root)
    output_path = tmp_path / "reports" / "manifest.json"

    write_dataset_manifest(DatasetConfig(root=dataset_root), output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["total_files"] == 6
