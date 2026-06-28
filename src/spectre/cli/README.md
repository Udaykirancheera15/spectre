# `spectre.cli`

## Purpose

Command-line interface for Spectre.

## Responsibilities

- Expose M0 infrastructure commands.
- Preserve a hierarchical command structure for future milestones.
- Convert project-specific exceptions into actionable CLI messages.

## What belongs here

- Typer application wiring.
- CLI presentation of validation/config/environment results.

## What does not belong here

- Dataset validation logic.
- Model training logic.
- Attack execution.
- Report generation before reporting exists.

## Dependencies

- `typer`
- `rich`
- Spectre infrastructure modules

## Extension points

Future commands should be added as new groups or subcommands, such as `spectre train`, `spectre evaluate`, `spectre attack`, and `spectre report` when those subsystems exist.
