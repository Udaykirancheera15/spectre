# ADR 0001: Use existing Conda environment `spectre`

## Status

Accepted

## Context

The project requires Fedora-compatible Python 3.11.15 execution in an existing Conda environment named `spectre`.

## Decision

Use only the existing `spectre` Conda environment. Do not create additional Conda environments or virtual environments.

## Consequences

- Commands assume `conda activate spectre` or `conda run -n spectre`.
- Environment metadata is captured under `environment/`.
- Hosted CI workflows remain placeholders in M0 because they cannot assume the local environment exists.
