"""Project-wide constants for Spectre.

Purpose:
    Centralize stable strings, defaults, and filesystem names used across the
    M0 infrastructure layer to avoid duplicated magic values.

Design:
    Constants are represented as immutable tuples and strings. This module has
    no side effects and does not read environment variables or filesystem
    state.

Input:
    This module accepts no runtime input.

Output:
    Importing this module exposes constants for labels, dataset splits,
    capture extensions, directory names, and package metadata.

Failure modes:
    This module should not raise exceptions during normal import. Import
    failures indicate packaging corruption or interpreter issues.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> "train" in DATASET_SPLITS
    True

"""

from __future__ import annotations

PROJECT_NAME: str = "spectre"
PACKAGE_DISTRIBUTION_NAME: str = "spectre-research"

VERSION: str = "0.1.0.dev0"
VERSION_PUBLIC_LABEL: str = "0.1.0-dev"

LABEL_BENIGN: str = "benign"
LABEL_MALWARE: str = "malware"
LABEL_UNKNOWN: str = "unknown"
LABELS: tuple[str, ...] = (LABEL_BENIGN, LABEL_MALWARE)

SPLIT_TRAIN: str = "train"
SPLIT_VAL: str = "val"
SPLIT_TEST: str = "test"
DATASET_SPLITS: tuple[str, ...] = (SPLIT_TRAIN, SPLIT_VAL, SPLIT_TEST)

CAPTURE_EXTENSION_PCAP: str = ".pcap"
CAPTURE_EXTENSION_PCAPNG: str = ".pcapng"
CAPTURE_EXTENSION_CAP: str = ".cap"
SUPPORTED_CAPTURE_EXTENSIONS: tuple[str, ...] = (
    CAPTURE_EXTENSION_PCAP,
    CAPTURE_EXTENSION_PCAPNG,
    CAPTURE_EXTENSION_CAP,
)

CONFIG_DIR_NAME: str = "configs"
DATASET_DIR_NAME: str = "dataset"
ENVIRONMENT_DIR_NAME: str = "environment"
EXPERIMENTS_DIR_NAME: str = "experiments"
OUTPUTS_DIR_NAME: str = "outputs"
ARTIFACTS_DIR_NAME: str = "artifacts"
REPORTS_DIR_NAME: str = "reports"
LOGS_DIR_NAME: str = "logs"
MLRUNS_DIR_NAME: str = "mlruns"

DEFAULT_CONFIG_NAME: str = "config"
DEFAULT_RANDOM_SEED: int = 1337

ENVIRONMENT_YAML_NAME: str = "environment.yml"
PIP_FREEZE_NAME: str = "pip-freeze.txt"
SYSTEM_INFO_NAME: str = "system_info.json"

HASH_ALGORITHM_MD5: str = "md5"
HASH_ALGORITHM_SHA256: str = "sha256"
HASH_ALGORITHMS: tuple[str, ...] = (HASH_ALGORITHM_MD5, HASH_ALGORITHM_SHA256)
