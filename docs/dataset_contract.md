# Dataset Contract

The existing dataset is expected to follow:

```text
dataset/
  train/
    benign/
    malware/
  val/
    benign/
    malware/
  test/
    benign/
    malware/
```

## Supported capture extensions

- `.pcap`
- `.pcapng`
- `.cap`

## M0 validation checks

Configurable checks include:

- required split directories
- required label directories
- supported extensions
- non-empty files
- file readability
- symbolic link policy

The current local repository dataset is symlink-based, so `configs/dataset/local.yaml` sets `allow_symlinks: true`. Publication artifacts should document whether symlink targets are stable and accessible.
- optional MD5
- optional SHA-256
- optional MIME guess using Python standard library
- optional duplicate hash detection

## Explicit non-goals

M0 does not parse packets, validate protocol correctness, extract flows, tokenize traffic, or inspect payload semantics.
