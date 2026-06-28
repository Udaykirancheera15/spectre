import json
from pathlib import Path

from spectre.io.filesystem import ensure_directory, iter_files_deterministic
from spectre.io.json import write_json


def test_iter_files_deterministic_returns_sorted_files(tmp_path: Path) -> None:
    (tmp_path / "b").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "b" / "two.pcap").write_bytes(b"2")
    (tmp_path / "a" / "one.pcap").write_bytes(b"1")

    paths = tuple(
        path.relative_to(tmp_path).as_posix()
        for path in iter_files_deterministic(tmp_path)
    )

    assert paths == ("a/one.pcap", "b/two.pcap")


def test_ensure_directory_creates_parent_directories(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b"

    ensure_directory(target)

    assert target.is_dir()


def test_write_json_writes_sorted_indented_json(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "manifest.json"

    write_json({"b": 2, "a": 1}, output)

    assert json.loads(output.read_text(encoding="utf-8")) == {"a": 1, "b": 2}
    assert output.read_text(encoding="utf-8").startswith('{\n  "a"')
