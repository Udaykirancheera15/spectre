import pytest
import structlog

from spectre.config.schemas import LoggingConfig
from spectre.logging.setup import setup_logging


def test_setup_logging_human_mode_emits_event(
    capsys: pytest.CaptureFixture[str],
) -> None:
    setup_logging(LoggingConfig(json=False))

    structlog.get_logger().info("human_event", key="value")

    captured = capsys.readouterr()
    assert "human_event" in captured.err
    assert "key" in captured.err


def test_setup_logging_json_mode_emits_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    setup_logging(LoggingConfig(json=True))

    structlog.get_logger().info("json_event", key="value")

    captured = capsys.readouterr()
    assert '"event": "json_event"' in captured.err
    assert '"key": "value"' in captured.err
