"""Synthetic git repo fixture, built via plain git CLI calls (no GitPython)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def run(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    """A repo where auth.py and session.py always change together, and
    unrelated.py changes on its own — a clean fixture for coupling scores.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    run(repo, "init", "-q", "-b", "main")
    run(repo, "config", "user.email", "test@example.com")
    run(repo, "config", "user.name", "Test")

    for i in range(4):
        (repo / "auth.py").write_text(f"def login_v{i}(): pass\n")
        (repo / "session.py").write_text(f"def refresh_v{i}(): pass\n")
        run(repo, "add", "-A")
        run(repo, "commit", "-q", "-m", f"auth+session round {i}")

    (repo / "unrelated.py").write_text("x = 1\n")
    run(repo, "add", "-A")
    run(repo, "commit", "-q", "-m", "unrelated change")

    return repo
