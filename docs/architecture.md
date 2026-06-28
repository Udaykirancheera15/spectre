# Spectre M0 Architecture

M0 establishes infrastructure only. It does not implement packet parsing, flow extraction, tokenization, model training, mutation engines, probes, or attack evaluation.

## Layers

```text
CLI
  -> config/logging/datasets/registry/utils
     -> domain/exceptions/constants/version/io
```

## Key design decisions

- `src/` package layout prevents accidental local imports.
- Pydantic validates configuration only.
- Frozen dataclasses represent immutable research/domain objects.
- Dataset validation is structural and configurable.
- Plugin contracts and registries are created in M0 to avoid future restructuring.
- I/O helpers are separated from dataset policy.
- Engineering utilities live in `tools/`; future experiment scripts live in `scripts/`.

## Extension points

Future milestones can add:

- `spectre.probes`
- `spectre.mutators`
- `spectre.classifiers`
- `spectre.tokenization`
- `spectre.evaluation`
- `spectre.reporting`

without changing the M0 core contracts.
