# `spectre.datasets`

## Purpose

M0-safe dataset validation, hashing, and manifest generation.

## Responsibilities

- Validate dataset directory structure.
- Check file extensions, permissions, symlink policy, emptiness, optional hashes, optional MIME guesses, and duplicate hashes.
- Generate deterministic dataset manifests.

## What belongs here

- Structural dataset validation.
- File-level reproducibility metadata.
- Dataset manifest construction.

## What does not belong here

- Packet parsing.
- Flow extraction.
- Feature extraction.
- Traffic tokenization.
- Dataset splitting logic.
- Model training data loaders.

## Dependencies

- `spectre.config`
- `spectre.domain`
- `spectre.io`
- Python standard library

## Extension points

M1 may add separate data processing packages for flow parsing and tokenization. Those should not be mixed into M0 structural validation.
