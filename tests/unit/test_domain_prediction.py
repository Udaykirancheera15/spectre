from dataclasses import FrozenInstanceError

import pytest

from spectre.domain.prediction import Prediction


def test_prediction_accepts_known_labels_and_is_frozen() -> None:
    prediction = Prediction(
        label="malware",
        confidence=0.9,
        probabilities=(("benign", 0.1), ("malware", 0.9)),
    )

    assert prediction.label == "malware"
    with pytest.raises(FrozenInstanceError):
        prediction.confidence = 0.1  # type: ignore[misc]


def test_prediction_accepts_unknown_label_for_abstention() -> None:
    prediction = Prediction(label="unknown", confidence=0.0)

    assert prediction.label == "unknown"


def test_prediction_rejects_invalid_label() -> None:
    with pytest.raises(ValueError, match="Unsupported prediction label"):
        Prediction(label="other", confidence=0.5)


def test_prediction_rejects_confidence_outside_unit_interval() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Prediction(label="benign", confidence=1.1)


def test_prediction_rejects_invalid_probability_label() -> None:
    with pytest.raises(ValueError, match="Unsupported probability label"):
        Prediction(label="benign", confidence=0.5, probabilities=(("other", 0.5),))


def test_prediction_rejects_probability_outside_unit_interval() -> None:
    with pytest.raises(ValueError, match="probability"):
        Prediction(label="benign", confidence=0.5, probabilities=(("benign", -0.1),))
