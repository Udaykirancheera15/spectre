"""Prediction domain objects for Spectre.

Purpose:
    Define immutable model prediction records shared by future classifiers,
    evaluators, reports, and benchmarks.

Design:
    Predictions are frozen dataclasses with small invariants for confidence and
    probability ranges. They do not implement model inference.

Input:
    Constructors accept labels, confidence values, optional class probability
    tuples, model identifiers, and metadata tuples.

Output:
    Instances provide reproducible immutable prediction records.

Failure modes:
    Invalid confidence or probability values raise `ValueError`.

Complexity:
    Construction is O(c + m), where c is the number of probabilities and m is
    the number of metadata pairs.

Examples:
    >>> prediction = Prediction(label="malware", confidence=0.9)
    >>> prediction.confidence
    0.9

"""

from __future__ import annotations

from dataclasses import dataclass, field

from spectre.constants import LABEL_UNKNOWN, LABELS
from spectre.typing import ImmutableMetadata


@dataclass(frozen=True, slots=True)
class Prediction:
    """Immutable classifier prediction record.

    Attributes:
        label: Predicted label.
        confidence: Confidence assigned to the predicted label in `[0, 1]`.
        probabilities: Optional class probabilities as `(label, probability)`
            pairs.
        model_name: Optional model identifier.
        metadata: Optional immutable metadata pairs.

    """

    label: str
    confidence: float
    probabilities: tuple[tuple[str, float], ...] = field(default_factory=tuple)
    model_name: str | None = None
    metadata: ImmutableMetadata = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate prediction invariants."""
        if self.label not in (*LABELS, LABEL_UNKNOWN):
            msg = f"Unsupported prediction label: {self.label!r}."
            raise ValueError(msg)
        _validate_unit_interval(self.confidence, "confidence")
        for label, probability in self.probabilities:
            if label not in (*LABELS, LABEL_UNKNOWN):
                msg = f"Unsupported probability label: {label!r}."
                raise ValueError(msg)
            _validate_unit_interval(probability, f"probability[{label}]")


def _validate_unit_interval(value: float, name: str) -> None:
    """Validate that a numeric value is within the closed unit interval."""
    if not 0.0 <= value <= 1.0:
        msg = f"{name} must be in [0, 1], got {value!r}."
        raise ValueError(msg)
