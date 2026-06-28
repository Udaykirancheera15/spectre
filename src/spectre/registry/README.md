# `spectre.registry`

## Purpose

Deterministic registration mechanisms for Spectre extension points.

## Responsibilities

- Register plugin instances by stable metadata name.
- Reject duplicate registrations.
- Provide reproducibly sorted plugin names and metadata.
- Raise project-specific registry exceptions.

## What belongs here

- Generic registry implementations.
- Future entry-point discovery helpers.
- Registry-specific validation policies.

## What does not belong here

- Plugin protocol definitions.
- Concrete plugin implementations.
- Attack, model, tokenizer, or reporting logic.

## Dependencies

- `spectre.plugins`
- `spectre.exceptions`
- Python standard library

## Extension points

Future milestones can add registries for probes, mutators, evaluators, tokenizers, classifiers, and reporters using the same deterministic registration pattern.
