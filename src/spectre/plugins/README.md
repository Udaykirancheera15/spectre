# `spectre.plugins`

## Purpose

Metadata-level plugin contracts for Spectre extension points.

## Responsibilities

- Define the minimum protocol that future plugins must satisfy.
- Keep plugin identity independent from registration mechanics.
- Provide immutable plugin metadata.

## What belongs here

- Plugin protocols.
- Plugin metadata objects.
- Future plugin base protocols for probes, evaluators, mutators, tokenizers, classifiers, and reporters.

## What does not belong here

- Registry storage.
- Plugin discovery.
- Concrete evasion probes.
- Model or tokenizer implementations.

## Dependencies

This package should depend only on the Python standard library and stable Spectre domain types.

## Extension points

Later milestones should add specialized plugin protocols while keeping the base `SpectrePlugin` contract stable.
