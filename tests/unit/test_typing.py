from pathlib import Path

from spectre.typing import JsonValue, LabelType, PathLike


def test_typing_aliases_are_importable() -> None:
    path_value: PathLike = Path("dataset")
    label_value: LabelType = "benign"
    json_value: JsonValue = {"label": label_value, "count": 1}

    assert str(path_value) == "dataset"
    assert json_value == {"label": "benign", "count": 1}
