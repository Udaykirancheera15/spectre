"""Spectre logging package.

Purpose:
    Expose explicit logging setup for CLI and future experiment entrypoints.

Design:
    Logging configuration is centralized and controlled by validated config.

Input:
    `LoggingConfig` instances.

Output:
    Configured human-readable or JSON structured logs.

Failure modes:
    Invalid configuration should be rejected before setup.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.logging import setup_logging
    >>> callable(setup_logging)
    True

"""

from spectre.logging.setup import setup_logging

__all__ = ["setup_logging"]
