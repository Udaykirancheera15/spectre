from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from spectre.core.interfaces import (
    DatasetValidator,
    Evaluator,
    Reporter,
    TargetClassifier,
)
from spectre.domain.dataset import DatasetSummary
from spectre.domain.metrics import MetricResult
from spectre.domain.prediction import Prediction


class ExampleClassifier:
    """Minimal classifier satisfying the TargetClassifier protocol."""

    def predict(self, sample: object) -> Prediction:
        """Return a deterministic benign prediction for tests."""
        return Prediction(
            label="benign",
            confidence=1.0,
            metadata=(("sample", str(sample)),),
        )

    def predict_batch(self, samples: Sequence[object]) -> tuple[Prediction, ...]:
        """Return deterministic predictions for all samples."""
        return tuple(self.predict(sample) for sample in samples)


class ExampleEvaluator:
    """Minimal evaluator satisfying the Evaluator protocol."""

    def evaluate(self, predictions: Sequence[Prediction]) -> MetricResult:
        """Return a count metric for supplied predictions."""
        return MetricResult("count", float(len(predictions)), len(predictions))


@dataclass(frozen=True, slots=True)
class ExampleReporter:
    """Minimal reporter satisfying the Reporter protocol."""

    writes: list[Path]

    def write(self, result: object, output_path: Path) -> None:
        """Record the output path that would be written."""
        del result
        self.writes.append(output_path)


class ExampleDatasetValidator:
    """Minimal dataset validator satisfying the DatasetValidator protocol."""

    def validate(self) -> DatasetSummary:
        """Return an empty valid summary."""
        return DatasetSummary()


def test_target_classifier_protocol() -> None:
    classifier = ExampleClassifier()

    assert isinstance(classifier, TargetClassifier)
    assert classifier.predict("sample").label == "benign"
    assert len(classifier.predict_batch(("a", "b"))) == 2


def test_evaluator_protocol() -> None:
    evaluator = ExampleEvaluator()

    assert isinstance(evaluator, Evaluator)
    assert evaluator.evaluate((Prediction("benign", 1.0),)).sample_count == 1


def test_reporter_protocol() -> None:
    reporter = ExampleReporter([])

    assert isinstance(reporter, Reporter)
    reporter.write({}, Path("out.json"))
    assert reporter.writes == [Path("out.json")]


def test_dataset_validator_protocol() -> None:
    validator = ExampleDatasetValidator()

    assert isinstance(validator, DatasetValidator)
    assert validator.validate().is_valid
