"""Thin wrappers around the git CLI.

Everything PreMerge needs (log, diff, merge-base) is a subprocess call away,
so we shell out directly instead of taking on a GitPython dependency.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field


class GitError(RuntimeError):
    """Raised when a git subprocess invocation fails."""


def run_git(repo: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def list_local_branches(repo: str) -> list[str]:
    out = run_git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads/")
    return [line.strip() for line in out.splitlines() if line.strip()]


def current_branch(repo: str) -> str:
    return run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()


def rev_parse(repo: str, ref: str) -> str:
    return run_git(repo, "rev-parse", ref).strip()


def merge_base(repo: str, ref_a: str, ref_b: str) -> str:
    return run_git(repo, "merge-base", ref_a, ref_b).strip()


def commit_log_with_files(repo: str, rev: str = "HEAD") -> list[list[str]]:
    """Return, per commit (newest first), the list of files it touched.

    Merge commits are skipped (--no-merges): their diff is usually the union
    of both parents' work and would artificially inflate coupling scores.
    """
    out = run_git(
        repo, "log", "--no-merges", "--name-only", "--pretty=format:COMMIT:%H", rev
    )
    commits: list[list[str]] = []
    current_files: list[str] | None = None
    for line in out.splitlines():
        if line.startswith("COMMIT:"):
            if current_files is not None:
                commits.append(current_files)
            current_files = []
        elif line.strip():
            assert current_files is not None
            current_files.append(line.strip())
    if current_files is not None:
        commits.append(current_files)
    return commits


_DIFF_GIT_RE = re.compile(r"^diff --git a/.+ b/(.+)$")
_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass
class BranchDiff:
    """Changes on `ref` relative to `base` (typically their merge-base)."""

    files: set[str] = field(default_factory=set)
    # file -> list of (start_line, length) ranges touched, in the `ref` version
    hunks: dict[str, list[tuple[int, int]]] = field(default_factory=dict)
    binary_files: set[str] = field(default_factory=set)


def diff_name_only(repo: str, base: str, ref: str) -> list[str]:
    out = run_git(repo, "diff", "--name-only", base, ref)
    return [line.strip() for line in out.splitlines() if line.strip()]


def diff_hunks(repo: str, base: str, ref: str) -> BranchDiff:
    """Parse `git diff -U0 base ref` into per-file touched line ranges."""
    out = run_git(repo, "diff", "-U0", base, ref)
    result = BranchDiff()
    current_file: str | None = None
    for line in out.splitlines():
        match_file = _DIFF_GIT_RE.match(line)
        if match_file:
            current_file = match_file.group(1)
            result.files.add(current_file)
            result.hunks.setdefault(current_file, [])
        elif line.startswith("Binary files ") and current_file:
            result.binary_files.add(current_file)
        elif line.startswith("@@") and current_file:
            hunk_match = _HUNK_RE.match(line)
            if not hunk_match:
                continue
            start = int(hunk_match.group(3))
            # ponytail: a "+c,0" hunk (pure deletion) has no "+" length; treat
            # it as touching a single line so it can still collide with an
            # insertion at that point in the other branch.
            length = int(hunk_match.group(4)) if hunk_match.group(4) is not None else 1
            result.hunks[current_file].append((start, max(length, 1)))
    return result
