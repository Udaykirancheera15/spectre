from spectre import constants


def test_dataset_splits_are_stable() -> None:
    assert constants.DATASET_SPLITS == ("train", "val", "test")


def test_labels_exclude_unknown_from_supervised_dataset_labels() -> None:
    assert constants.LABELS == ("benign", "malware")
    assert constants.LABEL_UNKNOWN not in constants.LABELS


def test_supported_capture_extensions_are_lowercase_dot_prefixed() -> None:
    assert constants.SUPPORTED_CAPTURE_EXTENSIONS == (".pcap", ".pcapng", ".cap")
    for extension in constants.SUPPORTED_CAPTURE_EXTENSIONS:
        assert extension.startswith(".")
        assert extension == extension.lower()


def test_semantic_version_is_development_release() -> None:
    assert constants.VERSION == "0.1.0.dev0"
    assert constants.VERSION_PUBLIC_LABEL == "0.1.0-dev"
