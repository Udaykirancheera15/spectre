"""Spectre research framework package.

Purpose:
    Provide the top-level package namespace for Spectre, a modular research
    framework for robustness evaluation of LLM-based malware traffic
    classifiers.

Design:
    The package is organized around clean architecture boundaries: domain
    objects, configuration, dataset validation, registries, logging,
    exceptions, and future plugin implementations.

Input:
    This module accepts no runtime input.

Output:
    Importing this module exposes package version metadata only.

Failure modes:
    Import failures indicate packaging or installation errors and should be
    treated as environment issues.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> import spectre
    >>> isinstance(spectre.__version__, str)
    True

"""

__version__ = "0.1.0.dev0"
