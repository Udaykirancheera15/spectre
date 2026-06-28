# ADR 0002: Use `src/` layout and clean architecture boundaries

## Status

Accepted

## Context

Spectre is expected to grow over 18–24 months across datasets, ML, attacks, evaluation, and reporting.

## Decision

Use a `src/` package layout with focused packages for domain, config, datasets, I/O, registry, plugins, exceptions, logging, CLI, and utilities.

## Consequences

- Packaging errors are caught early.
- Future M1/M2 components can be added without restructuring M0.
- Utilities are kept small to avoid a junk drawer.
