# ADR 0005: Defer MLflow, DVC, and ML dependencies in M0

## Status

Accepted

## Context

M0 does not train models, run experiments, track metrics, or version derived datasets.

## Decision

Defer MLflow, DVC, PyTorch, Transformers, DeepSpeed, PEFT, nfstream, Scapy, and vector-quantize-pytorch until milestones that exercise them.

## Consequences

- M0 has a smaller dependency surface.
- Future dependency additions require milestone-specific justification and tests.
