"""Run Spectre's local M0 quality gate.

Purpose:
    Execute formatting, linting, type checking, and tests from the active
    `spectre` Conda environment.

Design:
    Commands are invoked through the current Python interpreter, avoiding shell
    interpolation and hidden environment activation. This tool does not create
    Conda environments or virtual environments.

Input:
    No command-line arguments are required in M0.

Output:
    Tool output is streamed to the terminal. The process exits with status 0
    only if all checks pass.

Failure modes:
    Any failed command is reported and the tool exits non-zero after attempting
    all checks.

Complexity:
    Runtime is dominated by pytest and static analysis.

Examples:
    ```bash
    conda activate spectre
    python tools/qa.py
    ```

"""

from __future__ import annotations

import subprocess
import sys

_COMMANDS: tuple[tuple[str, ...], ...] = (
    (sys.executable, "-m", "ruff", "check", "."),
    (sys.executable, "-m", "black", "--check", "."),
    (sys.executable, "-m", "mypy", "src", "tests", "tools"),
    (sys.executable, "-m", "pytest"),
)


def main() -> int:
    """Run the full M0 quality gate and return a process exit code."""
    failed_commands: list[tuple[str, ...]] = []
    for command in _COMMANDS:
        print(f"\n$ {' '.join(command)}")
        result = subprocess.run(command, check=False)  # noqa: S603
        if result.returncode != 0:
            failed_commands.append(command)

    if failed_commands:
        print("\nQuality gate failed for:")
        for command in failed_commands:
            print(f"  {' '.join(command)}")
        return 1
    print("\nQuality gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
