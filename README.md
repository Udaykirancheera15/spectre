# Spectre

Spectre is a publication-oriented research framework for evaluating the robustness of LLM-based malware traffic classifiers under fidelity-aware adversarial perturbations.

The repository follows the supplied Spectre design document as the architectural specification. M0 establishes only infrastructure, configuration, reproducibility, validation, documentation, and stable extension points. It intentionally does **not** implement packet parsing, traffic tokenization, model training, mutation engines, evasion probes, or attack evaluation.

## Environment policy

The authoritative development environment is the existing Conda environment named `spectre`.

Do not create any additional Conda environments or Python virtual environments.

Use either:

```bash
conda activate spectre
python -m pip install -e ".[dev]"
```

or, for non-persistent shells:

```bash
conda run -n spectre python -m pip install -e ".[dev]"
```

Expected Python version:

```text
Python 3.11.15
```

## M0 quality gate

After installing development dependencies inside the existing `spectre` environment, run:

```bash
python tools/qa.py
```

Equivalent non-persistent form:

```bash
conda run -n spectre python tools/qa.py
```

The quality gate runs Ruff, Black, mypy, pytest, and coverage with a minimum M0 target of 90% infrastructure coverage.

## Initial command hierarchy

The M0 CLI is designed to grow without restructuring:

```text
spectre dataset validate
spectre dataset manifest
spectre env info
spectre config validate
spectre plugins list
spectre version
spectre doctor
```

Only M0-safe infrastructure behavior is implemented during M0.

## Repository organization

- `src/spectre/` — Python package.
- `configs/` — Hydra configuration.
- `dataset/` — existing train/validation/test capture dataset.
- `environment/` — exact environment metadata for experiments.
- `experiments/` — future published experiment definitions and outputs.
- `tools/` — engineering utilities such as QA and environment metadata capture.
- `scripts/` — reserved for future experiment scripts such as training, evaluation, and benchmarking.
- `docs/adr/` — architecture decision records.

## Deferred dependencies

M0 deliberately defers MLflow, DVC, PyTorch, Transformers, DeepSpeed, PEFT, nfstream, Scapy, and vector-quantize-pytorch until milestones that actually exercise them.
