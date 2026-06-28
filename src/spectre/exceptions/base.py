"""Base exception types for Spectre.

Purpose:
    Define the root exception hierarchy used by all public Spectre modules so
    failures are explicit, typed, and actionable.

Design:
    Exceptions carry a human-readable message, optional structured context, and
    an optional fix hint. This avoids silent failures and supports useful CLI
    diagnostics without coupling library code to a specific presentation layer.

Input:
    Exception constructors accept diagnostic messages and optional context.

Output:
    Raised exceptions provide stable project-specific error types.

Failure modes:
    Exception formatting itself is deterministic and should not raise.

Complexity:
    Construction and string formatting are O(k), where k is the number of
    context fields.

Examples:
    >>> error = SpectreError("failure", fix_hint="Check configuration")
    >>> "Check configuration" in str(error)
    True

"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType


class SpectreError(Exception):
    """Root exception for all project-specific Spectre failures.

    Args:
        message: Human-readable failure description.
        context: Optional structured context such as paths, config keys, or
            validation check names.
        fix_hint: Optional actionable remediation hint.

    """

    def __init__(
        self,
        message: str,
        *,
        context: Mapping[str, object] | None = None,
        fix_hint: str | None = None,
    ) -> None:
        """Initialize a project-specific exception with structured context."""
        super().__init__(message)
        self.message = message
        self.context = MappingProxyType(dict(context or {}))
        self.fix_hint = fix_hint

    def __str__(self) -> str:
        """Return a deterministic diagnostic string for logs and CLIs."""
        parts = [self.message]
        if self.context:
            context_text = ", ".join(
                f"{key}={value}" for key, value in sorted(self.context.items())
            )
            parts.append(f"context: {context_text}")
        if self.fix_hint:
            parts.append(f"fix: {self.fix_hint}")
        return " | ".join(parts)


class NotImplementedForMilestoneError(SpectreError):
    """Raised when a requested feature is intentionally deferred."""
