# ADR 0006: Introduce plugin registry architecture in M0

## Status

Accepted

## Context

Spectre will eventually register probes, evaluators, mutators, tokenizers, classifiers, and reporters.

## Decision

Create metadata-level plugin contracts and deterministic registries in M0 without implementing concrete plugins.

## Consequences

- Future extension points are stable.
- No attack or ML logic is prematurely implemented.
- Entry-point discovery can be added later without changing registry basics.
