from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from spectre.domain.runtime import RunMetadata


def test_run_metadata_is_frozen() -> None:
    metadata = RunMetadata(
        run_id="run-1",
        started_at_utc=datetime.now(UTC),
        python_version="3.11.15",
        platform="linux",
        spectre_version="0.1.0.dev0",
    )

    assert metadata.run_id == "run-1"
    with pytest.raises(FrozenInstanceError):
        metadata.run_id = "run-2"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        ("run_id", {"run_id": ""}),
        ("python_version", {"python_version": ""}),
        ("platform", {"platform": ""}),
        ("spectre_version", {"spectre_version": ""}),
    ],
)
def test_run_metadata_rejects_empty_required_fields(
    field_name: str,
    kwargs: dict[str, str],
) -> None:
    defaults = {
        "run_id": "run-1",
        "started_at_utc": datetime.now(UTC),
        "python_version": "3.11.15",
        "platform": "linux",
        "spectre_version": "0.1.0.dev0",
    }
    defaults.update(kwargs)

    with pytest.raises(ValueError, match=field_name):
        RunMetadata(**defaults)  # type: ignore[arg-type]
