"""Core protocol interfaces for Spectre.

Purpose:
    Define stable architectural contracts for future classifiers, probes,
    evaluators, reporters, and dataset validators without implementing M1/M2
    functionality.

Design:
    Interfaces are Python protocols with narrow methods and typed domain
    objects. They avoid dependencies on ML frameworks, Scapy, or packet parsing.

Input:
    Future implementations will accept samples, predictions, metrics, and paths
    defined by their specific milestones.

Output:
    Protocol methods return immutable Spectre domain objects where possible.

Failure modes:
    Implementations should raise project-specific exceptions. Protocols define
    contracts only and do not raise by themselves.

Complexity:
    Protocol checks are static/type-level; runtime complexity is implementation
    dependent.

Examples:
    >>> from spectre.core.interfaces import Reporter
    >>> hasattr(Reporter, "write")
    True

"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, runtime_checkable

from spectre.domain.dataset import DatasetSummary
from spectre.domain.metrics import MetricResult
from spectre.domain.prediction import Prediction
from spectre.plugins.base import SpectrePlugin


@runtime_checkable
class TargetClassifier(Protocol):
    """Protocol for future target malware traffic classifiers."""

    def predict(self, sample: object) -> Prediction:
        """Predict a label for one sample."""

    def predict_batch(self, samples: Sequence[object]) -> tuple[Prediction, ...]:
        """Predict labels for a deterministic sequence of samples."""


@runtime_checkable
class Probe(SpectrePlugin, Protocol):
    """Metadata-level protocol for future Spectre probes."""


@runtime_checkable
class Evaluator(Protocol):
    """Protocol for future metric evaluators."""

    def evaluate(self, predictions: Sequence[Prediction]) -> MetricResult:
        """Evaluate predictions and return one metric result."""


@runtime_checkable
class Reporter(Protocol):
    """Protocol for future report writers."""

    def write(self, result: object, output_path: Path) -> None:
        """Write a result object to an output path."""


@runtime_checkable
class DatasetValidator(Protocol):
    """Protocol for dataset validators."""

    def validate(self) -> DatasetSummary:
        """Validate a dataset and return a summary."""
