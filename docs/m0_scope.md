# M0 Scope

## Included

- packaging
- dependency declaration
- environment metadata
- configuration validation
- structured logging
- dataset structural validation
- deterministic dataset manifests
- immutable domain dataclasses
- core protocols
- plugin/registry architecture
- hierarchical CLI
- documentation and ADRs
- CI-readiness placeholders

## Excluded

- M1 data pipeline
- packet parsing
- flow extraction
- feature extraction
- VQ tokenization
- LLM training
- classifier inference
- mutation engines
- evasion probes
- benchmark execution
- MLflow and DVC integration

## Rationale

M0 must make future research reproducible and maintainable without prematurely implementing scientific components before their design and tests are ready.
