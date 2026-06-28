# `spectre.domain`

## Purpose

Immutable research domain objects for Spectre.

## Responsibilities

- Represent dataset records, prediction records, metric results, and runtime metadata.
- Preserve experiment state in immutable, typed structures.
- Avoid coupling research objects to configuration frameworks or I/O implementations.

## What belongs here

- Frozen dataclasses describing stable research concepts.
- Lightweight invariants that prevent invalid records.
- Serialization-friendly structures.

## What does not belong here

- Filesystem traversal.
- Packet parsing.
- Model inference.
- Hydra or Pydantic configuration models.
- Database, report, or artifact writing logic.

## Dependencies

This package should depend only on the Python standard library and stable Spectre constants/type aliases.

## Extension points

Future milestones may add domain objects for flows, packets, probes, attacks, fidelity checks, and benchmark results. Those additions should remain immutable unless there is a documented scientific reason for mutability.
