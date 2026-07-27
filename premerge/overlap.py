"""Direct-overlap detection between two branches relative to their merge-base."""

from __future__ import annotations

from dataclasses import dataclass, field

from . import git_utils
from .git_utils import BranchDiff


@dataclass
class OverlapResult:
    base: str
    file_overlap: set[str] = field(default_factory=set)
    line_overlap_files: set[str] = field(default_factory=set)  # subset of file_overlap
    diff_a: BranchDiff = field(default_factory=BranchDiff)
    diff_b: BranchDiff = field(default_factory=BranchDiff)


def _ranges_intersect(a: tuple[int, int], b: tuple[int, int]) -> bool:
    a_start, a_len = a
    b_start, b_len = b
    return a_start < b_start + b_len and b_start < a_start + a_len


def compute_overlap(repo: str, branch_a: str, branch_b: str) -> OverlapResult:
    """Diff both branches against their common ancestor and find overlap."""
    base = git_utils.merge_base(repo, branch_a, branch_b)
    diff_a = git_utils.diff_hunks(repo, base, branch_a)
    diff_b = git_utils.diff_hunks(repo, base, branch_b)

    file_overlap = diff_a.files & diff_b.files
    line_overlap_files: set[str] = set()
    for f in file_overlap:
        if f in diff_a.binary_files or f in diff_b.binary_files:
            # Can't compare line ranges in binaries; a shared touched binary
            # file is still a file-level risk, just not a line-level one.
            continue
        hunks_a = diff_a.hunks.get(f, [])
        hunks_b = diff_b.hunks.get(f, [])
        if any(_ranges_intersect(ha, hb) for ha in hunks_a for hb in hunks_b):
            line_overlap_files.add(f)

    return OverlapResult(
        base=base,
        file_overlap=file_overlap,
        line_overlap_files=line_overlap_files,
        diff_a=diff_a,
        diff_b=diff_b,
    )
