# ADR 0003: Use frozen dataclasses for domain objects

## Status

Accepted

## Context

Research records such as dataset records, predictions, metrics, and runtime metadata should not mutate accidentally after creation.

## Decision

Represent immutable research/domain objects as frozen dataclasses. Reserve Pydantic for configuration schemas.

## Consequences

- Domain objects are lightweight and framework-independent.
- Configuration still receives runtime schema validation.
- Future mutable objects require explicit justification.
