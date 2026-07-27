"""Combine branch overlap + historical coupling into a single risk score.

risk(A, B) = w1 * line_overlap_score
           + w2 * file_overlap_score
           + w3 * avg_historical_coupling(files only one branch touched)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import Weights
from .coupling import CouplingEngine
from .overlap import OverlapResult, compute_overlap


@dataclass
class RiskScore:
    branch_a: str
    branch_b: str
    score: float
    file_overlap: set[str]
    line_overlap_files: set[str]
    coupled_pairs: list[tuple[str, str, float]]
    explanations: list[str] = field(default_factory=list)


def _build_explanations(
    overlap: OverlapResult, coupled_pairs: list[tuple[str, str, float]]
) -> list[str]:
    lines = []
    for f in sorted(overlap.line_overlap_files):
        lines.append(f"{f}: both branches edit overlapping lines")
    for f in sorted(overlap.file_overlap - overlap.line_overlap_files):
        lines.append(f"{f}: both branches touch this file (different lines)")
    for a, b, score in coupled_pairs:
        lines.append(
            f"{a} <-> {b}: historically change together (coupling={score:.2f}) "
            f"— one branch touched {a}, the other touched {b}"
        )
    return lines


def compute_risk(
    repo: str,
    branch_a: str,
    branch_b: str,
    weights: Weights,
    coupling_engine: CouplingEngine,
) -> RiskScore:
    overlap = compute_overlap(repo, branch_a, branch_b)

    touched_files = overlap.diff_a.files | overlap.diff_b.files
    file_overlap_score = len(overlap.file_overlap) / len(touched_files) if touched_files else 0.0
    line_overlap_score = (
        len(overlap.line_overlap_files) / len(overlap.file_overlap)
        if overlap.file_overlap
        else 0.0
    )

    # Hidden-coupling signal: files each branch touched that it did *not*
    # directly share with the other branch, checked for historical coupling.
    only_a = overlap.diff_a.files - overlap.file_overlap
    only_b = overlap.diff_b.files - overlap.file_overlap
    coupled_pairs = coupling_engine.top_coupled_pairs(only_a, only_b)
    coupling_score = (
        sum(score for _, _, score in coupled_pairs) / len(coupled_pairs)
        if coupled_pairs
        else 0.0
    )

    total = (
        weights.line_overlap * line_overlap_score
        + weights.file_overlap * file_overlap_score
        + weights.coupling * coupling_score
    )

    return RiskScore(
        branch_a=branch_a,
        branch_b=branch_b,
        score=round(total, 4),
        file_overlap=overlap.file_overlap,
        line_overlap_files=overlap.line_overlap_files,
        coupled_pairs=coupled_pairs,
        explanations=_build_explanations(overlap, coupled_pairs),
    )
