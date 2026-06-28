# `spectre.core`

## Purpose

Stable architectural contracts for Spectre.

## Responsibilities

- Define protocol interfaces for future classifiers, probes, evaluators, reporters, and validators.
- Keep contracts independent of specific ML, packet, or reporting libraries.

## What belongs here

- Narrow protocol interfaces.
- Architecture-level contracts shared across packages.

## What does not belong here

- Concrete classifier implementations.
- Probe implementations.
- Mutation engines.
- Dataset parsing.
- Report rendering.

## Dependencies

- `spectre.domain`
- `spectre.plugins`
- Python standard library

## Extension points

Later milestones may refine or add protocols, but existing contracts should remain backward compatible unless an ADR justifies a breaking change.
