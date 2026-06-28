# `spectre.logging`

## Purpose

Centralized logging setup for Spectre.

## Responsibilities

- Configure human-readable console logs.
- Configure structured JSON logs.
- Keep logging setup out of library modules.

## What belongs here

- Logging setup functions.
- Future logging context helpers.

## What does not belong here

- Experiment tracking.
- MLflow integration.
- Report generation.
- Business logic.

## Dependencies

- `structlog`
- Python standard-library `logging`
- Spectre configuration schemas

## Extension points

Future milestones may add run IDs, MLflow integration, and artifact log sinks through explicit configuration.
