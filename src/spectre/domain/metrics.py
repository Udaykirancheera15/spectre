"""Metric domain objects for Spectre.

Purpose:
    Define immutable metric result records for future robustness evaluations,
    dataset checks, benchmarks, and reports.

Design:
    Metric results are frozen dataclasses with explicit validation of metric
    names, numeric values, and sample counts.

Input:
    Constructors accept metric names, values, sample counts, optional units, and
    metadata tuples.

Output:
    Instances provide stable metric records suitable for JSON serialization and
    publication artifacts.

Failure modes:
    Invalid metric names or negative sample counts raise `ValueError`.

Complexity:
    Construction is O(m), where m is the number of metadata pairs.

Examples:
    >>> result = MetricResult(name="coverage", value=0.95, sample_count=10)
    >>> result.sample_count
    10

"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite

from spectre.typing import ImmutableMetadata


@dataclass(frozen=True, slots=True)
class MetricResult:
    """Immutable metric result.

    Attributes:
        name: Stable metric identifier.
        value: Numeric metric value.
        sample_count: Number of samples contributing to the metric.
        unit: Optional metric unit.
        metadata: Optional immutable metadata pairs.

    """

    name: str
    value: float
    sample_count: int
    unit: str | None = None
    metadata: ImmutableMetadata = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate metric result invariants."""
        if not self.name:
            msg = "Metric name must be non-empty."
            raise ValueError(msg)
        if not isfinite(self.value):
            msg = f"Metric value must be finite, got {self.value!r}."
            raise ValueError(msg)
        if self.sample_count < 0:
            msg = "Metric sample_count must be non-negative."
            raise ValueError(msg)
