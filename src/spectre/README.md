# `spectre` package

## Purpose

Top-level Python package for the Spectre research framework.

## Responsibilities

- Define stable package metadata.
- Contain cleanly separated subpackages for configuration, domain models, datasets, registries, logging, exceptions, and future research components.

## What belongs here

- Package-level exports.
- Cross-cutting package metadata.
- Public subpackages with documented responsibilities.

## What does not belong here

- Experiment scripts.
- Model training entrypoints.
- Dataset artifacts.
- Ad hoc helper functions that should live in a focused package.

## Dependencies

The top-level package should remain lightweight and avoid importing heavy optional dependencies.

## Extension points

New subsystems should be added as focused subpackages with their own `README.md`, tests, and architecture documentation.
