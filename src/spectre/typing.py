"""Shared typing aliases for Spectre.

Purpose:
    Centralize common type aliases used across package boundaries.

Design:
    This module contains type aliases only and intentionally avoids runtime
    validation, I/O, and dependency imports beyond the Python standard library.

Input:
    This module accepts no runtime input.

Output:
    Importing this module exposes stable aliases for paths, labels, metadata,
    and JSON-compatible values.

Failure modes:
    Import failures indicate Python packaging corruption.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.typing import LabelType
    >>> isinstance("benign", str)
    True

"""

from __future__ import annotations

from os import PathLike as OsPathLike
from pathlib import Path
from typing import TypeAlias

PathLike: TypeAlias = str | Path | OsPathLike[str]
LabelType: TypeAlias = str
JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
Metadata: TypeAlias = dict[str, JsonScalar]
ImmutableMetadata: TypeAlias = tuple[tuple[str, JsonScalar], ...]
