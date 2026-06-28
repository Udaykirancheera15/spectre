"""Spectre core architecture contracts.

Purpose:
    Expose stable protocol interfaces for future framework components.

Design:
    Core interfaces define contracts only. Implementations live in focused
    packages and later milestones.

Input:
    This module accepts no runtime input.

Output:
    Importing this package exposes protocol interfaces.

Failure modes:
    Import failures indicate packaging corruption.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.core import TargetClassifier
    >>> hasattr(TargetClassifier, "predict")
    True

"""

from spectre.core.interfaces import (
    DatasetValidator,
    Evaluator,
    Probe,
    Reporter,
    TargetClassifier,
)

__all__ = [
    "DatasetValidator",
    "Evaluator",
    "Probe",
    "Reporter",
    "TargetClassifier",
]
