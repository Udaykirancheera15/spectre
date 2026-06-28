"""Dataset domain objects for Spectre.

Purpose:
    Define immutable research objects that describe dataset records,
    validation issues, and validation summaries without coupling them to any
    filesystem traversal implementation.

Design:
    Objects are frozen dataclasses with explicit invariants in `__post_init__`.
    They use standard-library types only and remain independent of Pydantic,
    Hydra, Scapy, or ML dependencies.

Input:
    Constructors accept normalized dataset metadata produced by validation or
    manifest generation code.

Output:
    Instances provide immutable, hashable records suitable for tests, manifests,
    logs, and future experiment metadata.

Failure modes:
    Invalid constructor arguments raise `ValueError` with actionable messages.
    Public validation modules should wrap unrecoverable failures in
    project-specific exceptions.

Complexity:
    Object construction is O(1), excluding caller-provided path normalization.

Examples:
    >>> from pathlib import Path
    >>> record = DatasetRecord("train", "benign", Path("a.pcap"), 1, ".pcap")
    >>> record.split
    'train'

"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from spectre.constants import DATASET_SPLITS, LABELS, SUPPORTED_CAPTURE_EXTENSIONS


@dataclass(frozen=True, slots=True)
class DatasetRecord:
    """Immutable metadata for one dataset capture file.

    Attributes:
        split: Dataset split name, such as `train`, `val`, or `test`.
        label: Supervised label, currently `benign` or `malware`.
        path: Dataset-relative or repository-relative capture path.
        size_bytes: File size in bytes.
        extension: Lowercase file extension including the leading dot.
        md5: Optional MD5 digest for reproducibility and duplicate detection.
        sha256: Optional SHA-256 digest for stronger reproducibility checks.
        mime_type: Optional standard-library MIME guess.

    """

    split: str
    label: str
    path: Path
    size_bytes: int
    extension: str
    md5: str | None = None
    sha256: str | None = None
    mime_type: str | None = None

    def __post_init__(self) -> None:
        """Validate immutable dataset record invariants."""
        normalized_extension = self.extension.lower()
        object.__setattr__(self, "extension", normalized_extension)
        if self.split not in DATASET_SPLITS:
            msg = f"Unsupported dataset split: {self.split!r}."
            raise ValueError(msg)
        if self.label not in LABELS:
            msg = f"Unsupported dataset label: {self.label!r}."
            raise ValueError(msg)
        if self.size_bytes < 0:
            msg = "Dataset record size_bytes must be non-negative."
            raise ValueError(msg)
        if normalized_extension not in SUPPORTED_CAPTURE_EXTENSIONS:
            msg = f"Unsupported capture extension: {normalized_extension!r}."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class DatasetValidationIssue:
    """Structured dataset validation issue.

    Attributes:
        path: Path associated with the issue.
        code: Stable machine-readable issue code.
        message: Human-readable diagnostic message.
        fix_hint: Optional actionable remediation hint.

    """

    path: Path
    code: str
    message: str
    fix_hint: str | None = None

    def __post_init__(self) -> None:
        """Validate issue invariants."""
        if not self.code:
            msg = "Dataset validation issue code must be non-empty."
            raise ValueError(msg)
        if not self.message:
            msg = "Dataset validation issue message must be non-empty."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class DatasetSummary:
    """Immutable summary of dataset validation or manifest discovery.

    Attributes:
        records: Valid dataset records discovered by the caller.
        issues: Structured validation issues discovered by the caller.
        counts_by_split_label: Count tuples keyed as `(split, label, count)` to
            remain immutable and JSON-serializable without custom mapping keys.

    """

    records: tuple[DatasetRecord, ...] = field(default_factory=tuple)
    issues: tuple[DatasetValidationIssue, ...] = field(default_factory=tuple)
    counts_by_split_label: tuple[tuple[str, str, int], ...] = field(
        default_factory=tuple
    )

    @property
    def total_files(self) -> int:
        """Return the number of valid records in the summary."""
        return len(self.records)

    @property
    def total_bytes(self) -> int:
        """Return the total size in bytes across valid records."""
        return sum(record.size_bytes for record in self.records)

    @property
    def is_valid(self) -> bool:
        """Return whether the summary contains no validation issues."""
        return not self.issues
