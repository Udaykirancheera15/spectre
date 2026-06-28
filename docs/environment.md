# Spectre Environment Policy

## Authoritative environment

Spectre uses the existing Conda environment named `spectre` as the authoritative development and experiment environment.

Do not create:

- another Conda environment
- `venv`
- `.venv`
- any project-local virtual environment

## Installation

Activate the existing environment:

```bash
conda activate spectre
python --version
python -m pip install -e ".[dev]"
```

Expected Python version:

```text
Python 3.11.15
```

For non-persistent shells, use:

```bash
conda run -n spectre python -m pip install -e ".[dev]"
```

## Environment metadata

M0 records environment metadata in:

```text
environment/
  environment.yml
  pip-freeze.txt
  system_info.json
```

Generate metadata with:

```bash
conda activate spectre
conda env export --no-builds > environment/environment.yml
python -m pip freeze > environment/pip-freeze.txt
python tools/write_environment_metadata.py
```

Equivalent non-persistent commands:

```bash
conda run -n spectre python -m pip freeze > environment/pip-freeze.txt
conda run -n spectre python tools/write_environment_metadata.py
```

`environment/environment.yml` is the primary Conda-first environment specification. `environment/pip-freeze.txt` records the realized Python package stack.

## Deferred environment tooling

`conda-lock` is deferred until heavier M1/M2 scientific and GPU dependencies are introduced.
