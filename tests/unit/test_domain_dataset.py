from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from spectre.domain.dataset import DatasetRecord, DatasetSummary, DatasetValidationIssue


def test_dataset_record_normalizes_extension_and_is_frozen() -> None:
    record = DatasetRecord("train", "benign", Path("sample.PCAP"), 10, ".PCAP")

    assert record.extension == ".pcap"
    with pytest.raises(FrozenInstanceError):
        record.size_bytes = 1  # type: ignore[misc]


def test_dataset_record_rejects_invalid_split() -> None:
    with pytest.raises(ValueError, match="Unsupported dataset split"):
        DatasetRecord("dev", "benign", Path("sample.pcap"), 1, ".pcap")


def test_dataset_record_rejects_invalid_label() -> None:
    with pytest.raises(ValueError, match="Unsupported dataset label"):
        DatasetRecord("train", "unknown", Path("sample.pcap"), 1, ".pcap")


def test_dataset_record_rejects_negative_size() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        DatasetRecord("train", "benign", Path("sample.pcap"), -1, ".pcap")


def test_dataset_record_rejects_unsupported_extension() -> None:
    with pytest.raises(ValueError, match="Unsupported capture extension"):
        DatasetRecord("train", "benign", Path("sample.txt"), 1, ".txt")


def test_dataset_validation_issue_requires_code_and_message() -> None:
    with pytest.raises(ValueError, match="code"):
        DatasetValidationIssue(Path("x"), "", "message")
    with pytest.raises(ValueError, match="message"):
        DatasetValidationIssue(Path("x"), "code", "")


def test_dataset_summary_computes_totals_and_validity() -> None:
    records = (
        DatasetRecord("train", "benign", Path("a.pcap"), 10, ".pcap"),
        DatasetRecord("train", "malware", Path("b.pcapng"), 20, ".pcapng"),
    )
    summary = DatasetSummary(records=records)

    assert summary.total_files == 2
    assert summary.total_bytes == 30
    assert summary.is_valid


def test_dataset_summary_reports_invalid_when_issues_exist() -> None:
    issue = DatasetValidationIssue(Path("x"), "missing", "Missing path")
    summary = DatasetSummary(issues=(issue,))

    assert not summary.is_valid
