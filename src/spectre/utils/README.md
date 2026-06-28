# `spectre.utils`

## Purpose

Small, focused utility modules that do not yet justify a dedicated package.

## Responsibilities

- Provide reproducibility metadata helpers.
- Remain intentionally small and well-scoped.

## What belongs here

- Cross-cutting helpers with no better architectural home.
- Utilities that have explicit tests and documentation.

## What does not belong here

- Dataset logic.
- I/O helpers.
- Model utilities.
- Attack utilities.
- Random miscellaneous functions.

## Dependencies

Prefer the Python standard library and stable Spectre metadata modules.

## Extension points

If utilities grow beyond a narrow scope, split them into dedicated packages such as `spectre.io`, `spectre.validation`, or future ML-specific packages.
