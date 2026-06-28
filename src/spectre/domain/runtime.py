"""Runtime domain objects for Spectre.

Purpose:
    Define immutable metadata records that identify a Spectre run, software
    version, interpreter, platform, and configuration context.

Design:
    Runtime metadata is represented as frozen dataclasses to make experiment
    records reproducible and resistant to accidental mutation.

Input:
    Constructors accept run identifiers, timestamps, version strings, platform
    descriptors, and optional config paths.

Output:
    Instances provide stable runtime metadata for logs, manifests, and future
    reports.

Failure modes:
    Empty required fields raise `ValueError`.

Complexity:
    Construction is O(m), where m is the number of metadata pairs.

Examples:
    >>> from datetime import UTC, datetime
    >>> metadata = RunMetadata(
    ...     "run", datetime.now(UTC), "3.11", "linux", "0.1"
    ... )
    >>> metadata.run_id
    'run'

"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from spectre.typing import ImmutableMetadata


@dataclass(frozen=True, slots=True)
class RunMetadata:
    """Immutable metadata describing one Spectre runtime invocation.

    Attributes:
        run_id: Stable run identifier.
        started_at_utc: Time the run started, expected to be timezone-aware UTC.
        python_version: Python interpreter version.
        platform: Platform descriptor.
        spectre_version: Spectre package version.
        git_revision: Optional source revision.
        config_path: Optional configuration path used for the run.
        metadata: Optional immutable metadata pairs.

    """

    run_id: str
    started_at_utc: datetime
    python_version: str
    platform: str
    spectre_version: str
    git_revision: str | None = None
    config_path: Path | None = None
    metadata: ImmutableMetadata = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate runtime metadata invariants."""
        for field_name, value in (
            ("run_id", self.run_id),
            ("python_version", self.python_version),
            ("platform", self.platform),
            ("spectre_version", self.spectre_version),
        ):
            if not value:
                msg = f"RunMetadata field {field_name} must be non-empty."
                raise ValueError(msg)
