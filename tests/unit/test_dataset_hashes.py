from pathlib import Path

import pytest

from spectre.constants import HASH_ALGORITHM_MD5, HASH_ALGORITHM_SHA256
from spectre.datasets.hashes import compute_hash, compute_optional_hashes
from spectre.exceptions.dataset import DatasetNotFoundError
from spectre.exceptions.validation import UnsupportedValidationCheckError


def test_compute_hash_returns_known_md5_and_sha256(tmp_path: Path) -> None:
    sample = tmp_path / "sample.pcap"
    sample.write_bytes(b"abc")

    assert (
        compute_hash(sample, HASH_ALGORITHM_MD5) == "900150983cd24fb0d6963f7d28e17f72"
    )
    assert (
        compute_hash(sample, HASH_ALGORITHM_SHA256)
        == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_compute_optional_hashes_respects_flags(tmp_path: Path) -> None:
    sample = tmp_path / "sample.pcap"
    sample.write_bytes(b"abc")

    md5, sha256 = compute_optional_hashes(
        sample,
        compute_md5=True,
        compute_sha256=False,
    )

    assert md5 == "900150983cd24fb0d6963f7d28e17f72"
    assert sha256 is None


def test_compute_hash_rejects_unsupported_algorithm(tmp_path: Path) -> None:
    sample = tmp_path / "sample.pcap"
    sample.write_bytes(b"abc")

    with pytest.raises(UnsupportedValidationCheckError, match="Unsupported"):
        compute_hash(sample, "sha1")


def test_compute_hash_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DatasetNotFoundError, match="missing"):
        compute_hash(tmp_path / "missing.pcap", HASH_ALGORITHM_SHA256)


def test_compute_hash_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(DatasetNotFoundError, match="non-file"):
        compute_hash(tmp_path, HASH_ALGORITHM_SHA256)
