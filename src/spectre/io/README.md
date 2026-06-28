# `spectre.io`

## Purpose

Low-level deterministic I/O utilities.

## Responsibilities

- Filesystem traversal.
- Directory creation.
- Deterministic JSON serialization.
- Future report, CSV, checkpoint, and artifact I/O helpers.

## What belongs here

- Format-specific I/O helpers.
- Atomic write helpers.
- Deterministic traversal and serialization utilities.

## What does not belong here

- Dataset validation policy.
- Research domain objects.
- Model checkpoints as domain concepts.
- Report rendering logic beyond low-level I/O.

## Dependencies

This package should remain lightweight and mostly standard-library based.

## Extension points

Future modules may include `yaml.py`, `csv.py`, `html.py`, `checkpoints.py`, and report artifact writers.
