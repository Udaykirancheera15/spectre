from dataclasses import FrozenInstanceError
from math import inf, nan

import pytest

from spectre.domain.metrics import MetricResult


def test_metric_result_is_frozen() -> None:
    result = MetricResult(name="accuracy", value=1.0, sample_count=10)

    assert result.value == 1.0
    with pytest.raises(FrozenInstanceError):
        result.value = 0.0  # type: ignore[misc]


def test_metric_result_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="Metric name"):
        MetricResult(name="", value=1.0, sample_count=1)


@pytest.mark.parametrize("value", [inf, -inf, nan])
def test_metric_result_rejects_non_finite_value(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        MetricResult(name="metric", value=value, sample_count=1)


def test_metric_result_rejects_negative_sample_count() -> None:
    with pytest.raises(ValueError, match="sample_count"):
        MetricResult(name="metric", value=1.0, sample_count=-1)
