# `spectre.config`

## Purpose

Validated configuration loading for Spectre.

## Responsibilities

- Compose Hydra YAML configuration.
- Validate composed config with Pydantic schemas.
- Convert Hydra/Pydantic failures into project-specific exceptions.

## What belongs here

- Configuration schemas.
- Configuration loading and validation helpers.
- Configuration-specific documentation.

## What does not belong here

- Research domain dataclasses.
- Dataset traversal.
- Model training parameters that are not yet implemented.
- Experiment execution logic.

## Dependencies

- `hydra-core`
- `omegaconf`
- `pydantic`
- Spectre constants and exceptions

## Extension points

Future milestones should add config groups for tokenizers, classifiers, probes, evaluators, reporting, and experiments while keeping validation explicit and typed.
