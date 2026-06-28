# ADR 0004: Use Hydra plus Pydantic for configuration

## Status

Accepted

## Context

Publication-quality experiments require reproducible, composable, and validated configuration.

## Decision

Use Hydra/OmegaConf for YAML composition and Pydantic for schema validation.

## Consequences

- Experiment configs can be composed cleanly.
- Invalid fields are rejected early.
- Pydantic remains isolated to configuration code.
