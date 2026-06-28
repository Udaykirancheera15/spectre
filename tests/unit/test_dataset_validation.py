import os
from pathlib import Path

import pytest

from spectre.config.schemas import DatasetChecksConfig, DatasetConfig
from spectre.datasets.validation import validate_dataset
from spectre.exceptions.dataset import DatasetNotFoundError


def _make_dataset(root: Path) -> None:
    for split in ("train", "val", "test"):
        for label in ("benign", "malware"):
            directory = root / split / label
            directory.mkdir(parents=True)
            (directory / f"{split}_{label}.pcap").write_bytes(b"capture")


def test_validate_dataset_accepts_valid_tree(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    config = DatasetConfig(root=tmp_path)

    summary = validate_dataset(config)

    assert summary.is_valid
    assert summary.total_files == 6
    assert summary.total_bytes == 42
    assert ("train", "benign", 1) in summary.counts_by_split_label


def test_validate_dataset_rejects_missing_root(tmp_path: Path) -> None:
    config = DatasetConfig(root=tmp_path / "missing")

    with pytest.raises(DatasetNotFoundError, match="root"):
        validate_dataset(config)


def test_validate_dataset_reports_missing_label_directory(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    target = tmp_path / "train" / "malware"
    for child in target.iterdir():
        child.unlink()
    target.rmdir()

    summary = validate_dataset(DatasetConfig(root=tmp_path))

    assert not summary.is_valid
    assert any(issue.code == "missing_label_directory" for issue in summary.issues)


def test_validate_dataset_reports_empty_file(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    empty_file = tmp_path / "train" / "benign" / "empty.pcap"
    empty_file.write_bytes(b"")

    summary = validate_dataset(DatasetConfig(root=tmp_path))

    assert any(issue.code == "empty_file" for issue in summary.issues)
    assert empty_file.relative_to(tmp_path) not in {
        record.path for record in summary.records
    }


def test_validate_dataset_reports_unsupported_extension(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    unsupported = tmp_path / "train" / "benign" / "notes.txt"
    unsupported.write_text("not a capture", encoding="utf-8")

    summary = validate_dataset(DatasetConfig(root=tmp_path))

    assert any(issue.code == "unsupported_extension" for issue in summary.issues)
    assert unsupported.relative_to(tmp_path) not in {
        record.path for record in summary.records
    }


def test_validate_dataset_can_ignore_unknown_extensions(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    unsupported = tmp_path / "train" / "benign" / "notes.txt"
    unsupported.write_text("not a capture", encoding="utf-8")
    config = DatasetConfig(
        root=tmp_path,
        checks=DatasetChecksConfig(fail_on_unknown_extensions=False),
    )

    summary = validate_dataset(config)

    assert summary.is_valid
    assert unsupported.relative_to(tmp_path) not in {
        record.path for record in summary.records
    }


def test_validate_dataset_reports_symlink_when_disallowed(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    target = tmp_path / "train" / "benign" / "train_benign.pcap"
    symlink = tmp_path / "train" / "benign" / "linked.pcap"
    symlink.symlink_to(target)

    summary = validate_dataset(DatasetConfig(root=tmp_path))

    assert any(issue.code == "symlink_not_allowed" for issue in summary.issues)


def test_validate_dataset_reports_unreadable_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _make_dataset(tmp_path)
    unreadable = tmp_path / "train" / "benign" / "train_benign.pcap"

    def fake_access(path: Path | str, mode: int) -> bool:
        return not (Path(path) == unreadable and mode == os.R_OK)

    monkeypatch.setattr(os, "access", fake_access)

    summary = validate_dataset(DatasetConfig(root=tmp_path))

    assert any(issue.code == "unreadable_file" for issue in summary.issues)


def test_validate_dataset_computes_hashes_and_detects_duplicates(
    tmp_path: Path,
) -> None:
    _make_dataset(tmp_path)
    duplicate = tmp_path / "train" / "benign" / "duplicate.pcap"
    duplicate.write_bytes(b"capture")
    config = DatasetConfig(
        root=tmp_path,
        checks=DatasetChecksConfig(
            compute_sha256=True,
            detect_duplicate_hashes=True,
        ),
    )

    summary = validate_dataset(config)

    assert any(record.sha256 is not None for record in summary.records)
    assert any(issue.code == "duplicate_hash" for issue in summary.issues)


def test_validate_dataset_adds_mime_guess_when_configured(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    config = DatasetConfig(
        root=tmp_path,
        checks=DatasetChecksConfig(check_mime_type=True),
    )

    summary = validate_dataset(config)

    assert all(hasattr(record, "mime_type") for record in summary.records)
