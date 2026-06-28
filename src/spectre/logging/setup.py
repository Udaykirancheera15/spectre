"""Structured logging setup for Spectre.

Purpose:
    Configure human-readable console logging or structured JSON logging through
    validated configuration.

Design:
    Logging setup is explicit and called by CLI entrypoints. Library modules
    should request loggers but not configure global logging themselves.

Input:
    A validated `LoggingConfig` object.

Output:
    Configured standard-library logging and structlog processors.

Failure modes:
    Invalid log levels should be rejected by configuration validation before
    this function is called.

Complexity:
    Configuration is O(1).

Examples:
    >>> from spectre.config.schemas import LoggingConfig
    >>> isinstance(LoggingConfig().level, str)
    True

"""

from __future__ import annotations

import logging
import sys

import structlog

from spectre.config.schemas import LoggingConfig


def setup_logging(config: LoggingConfig) -> None:
    """Configure Spectre logging.

    Args:
        config: Validated logging configuration.

    """
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
    ]
    if config.show_timestamp:
        shared_processors.append(timestamper)

    renderer: structlog.types.Processor
    if config.json_logs:
        renderer = structlog.processors.JSONRenderer(sort_keys=True)
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=False)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, config.level),
        force=True,
    )
    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, config.level)
        ),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=False,
    )
