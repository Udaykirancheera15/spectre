"""Print Spectre environment metadata as JSON.

Purpose:
    Provide a simple engineering utility for inspecting the active runtime
    environment used by Spectre.

Design:
    The tool uses Spectre's standard reproducibility helper and prints sorted,
    indented JSON to stdout.

Input:
    No command-line arguments are required in M0.

Output:
    JSON environment metadata.

Failure modes:
    Import or serialization failures indicate installation problems.

Complexity:
    O(1), excluding Git metadata lookup.

Examples:
    ```bash
    conda activate spectre
    python tools/env_info.py
    ```

"""

from __future__ import annotations

import json
from pathlib import Path

from spectre.utils.reproducibility import collect_environment_info


def main() -> int:
    """Print environment metadata and return a process exit code."""
    print(json.dumps(collect_environment_info(Path.cwd()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
