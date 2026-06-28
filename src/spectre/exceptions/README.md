# `spectre.exceptions`

## Purpose

Centralized project-specific exception hierarchy.

## Responsibilities

- Provide typed errors for configuration, dataset, validation, and milestone-boundary failures.
- Carry actionable diagnostic context and fix hints.
- Prevent public modules from raising ambiguous built-in exceptions directly.

## What belongs here

- Base Spectre exception classes.
- Domain-specific exception categories.
- Stable exception exports.

## What does not belong here

- Logging logic.
- CLI formatting logic.
- Recovery or retry policies.

## Dependencies

This package should depend only on the Python standard library and stable Spectre constants if needed.

## Extension points

Future subsystems such as probes, models, reports, and registry discovery should add focused exception modules when generic categories become insufficient.
