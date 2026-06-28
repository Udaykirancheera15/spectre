"""Immutable Spectre research domain objects.

Purpose:
    Expose domain dataclasses used across datasets, predictions, metrics, and
    runtime metadata.

Design:
    Domain objects are frozen dataclasses and avoid framework dependencies.
    Pydantic is reserved for configuration schemas rather than research objects.

Input:
    This module accepts no runtime input.

Output:
    Importing this package exposes stable domain dataclass APIs.

Failure modes:
    Import failures indicate packaging corruption or invalid dependencies.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.domain import MetricResult
    >>> MetricResult("accuracy", 1.0, 1).value
    1.0

"""

from spectre.domain.dataset import DatasetRecord, DatasetSummary, DatasetValidationIssue
from spectre.domain.metrics import MetricResult
from spectre.domain.prediction import Prediction
from spectre.domain.runtime import RunMetadata

__all__ = [
    "DatasetRecord",
    "DatasetSummary",
    "DatasetValidationIssue",
    "MetricResult",
    "Prediction",
    "RunMetadata",
]
