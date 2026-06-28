# Development Workflow

Run all commands inside the existing `spectre` Conda environment.

## Quality gate

```bash
conda activate spectre
python tools/qa.py
```

Equivalent:

```bash
conda run -n spectre python tools/qa.py
```

The quality gate runs:

- Ruff
- Black
- mypy
- pytest with coverage

M0 coverage target: at least 90% infrastructure code coverage.

## Individual checks

```bash
python -m ruff check .
python -m black --check .
python -m mypy src tests tools
python -m pytest
```

## Self-review checklist

Before considering work complete, review:

- architecture boundaries
- type safety
- exception clarity
- reproducibility
- test coverage
- documentation
- future extensibility
- publication readiness
