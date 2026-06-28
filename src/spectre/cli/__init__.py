"""Spectre CLI package.

Purpose:
    Provide command-line entrypoints for infrastructure and future experiment
    workflows.

Design:
    The CLI is hierarchical and M0-safe. It omits placeholder report commands
    until reporting is implemented.

Input:
    Command-line arguments and configuration files.

Output:
    Terminal output and optional files such as dataset manifests.

Failure modes:
    Commands convert project-specific exceptions to non-zero exits.

Complexity:
    Import-time complexity is O(1).

Examples:
    >>> from spectre.cli.main import app
    >>> app.info.name is None
    True

"""
