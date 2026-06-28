from pathlib import Path

from spectre.version import __version__, collect_build_metadata, get_git_revision


def test_version_matches_development_release() -> None:
    assert __version__ == "0.1.0.dev0"


def test_collect_build_metadata_contains_runtime_fields() -> None:
    metadata = collect_build_metadata(Path.cwd())

    assert metadata.version == __version__
    assert metadata.python_version
    assert metadata.platform


def test_get_git_revision_returns_none_without_git_metadata(tmp_path: Path) -> None:
    assert get_git_revision(tmp_path) is None


def test_get_git_revision_reads_direct_head_commit(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    revision = "a" * 40
    (git_dir / "HEAD").write_text(revision, encoding="utf-8")

    assert get_git_revision(tmp_path) == revision


def test_get_git_revision_reads_symbolic_ref(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    ref_dir = git_dir / "refs" / "heads"
    ref_dir.mkdir(parents=True)
    revision = "b" * 40
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    (ref_dir / "main").write_text(revision, encoding="utf-8")

    assert get_git_revision(tmp_path) == revision


def test_get_git_revision_discovers_git_metadata_from_child(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    child = tmp_path / "nested" / "child"
    git_dir.mkdir()
    child.mkdir(parents=True)
    revision = "c" * 40
    (git_dir / "HEAD").write_text(revision, encoding="utf-8")

    assert get_git_revision(child) == revision


def test_get_git_revision_handles_empty_head(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("\n", encoding="utf-8")

    assert get_git_revision(tmp_path) is None


def test_get_git_revision_handles_empty_symbolic_ref(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: \n", encoding="utf-8")

    assert get_git_revision(tmp_path) is None


def test_get_git_revision_handles_missing_ref_target(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")

    assert get_git_revision(tmp_path) is None


def test_get_git_revision_handles_gitdir_file(tmp_path: Path) -> None:
    metadata = tmp_path / "metadata"
    worktree = tmp_path / "worktree"
    metadata.mkdir()
    worktree.mkdir()
    revision = "d" * 40
    (worktree / ".git").write_text(f"gitdir: {metadata}\n", encoding="utf-8")
    (metadata / "HEAD").write_text(revision, encoding="utf-8")

    assert get_git_revision(worktree) == revision


def test_get_git_revision_handles_malformed_gitdir_file(tmp_path: Path) -> None:
    (tmp_path / ".git").write_text("not-a-gitdir-file\n", encoding="utf-8")

    assert get_git_revision(tmp_path) is None


def test_get_git_revision_handles_empty_gitdir_file(tmp_path: Path) -> None:
    (tmp_path / ".git").write_text("gitdir: \n", encoding="utf-8")

    assert get_git_revision(tmp_path) is None
