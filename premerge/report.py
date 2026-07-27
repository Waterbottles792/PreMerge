"""CLI output formatting: rich table for humans, JSON for machines."""

from __future__ import annotations

import json as json_module

from rich.console import Console
from rich.table import Table

from .scoring import RiskScore


def print_table(scores: list[RiskScore], console: Console | None = None) -> None:
    console = console or Console()
    if not scores:
        console.print("[yellow]No branch pairs to analyze.[/yellow]")
        return

    table = Table(title="PreMerge Conflict Risk Report")
    table.add_column("Branch A")
    table.add_column("Branch B")
    table.add_column("Risk", justify="right")
    table.add_column("Why")

    for s in scores:
        why = s.explanations[0] if s.explanations else "no overlap or coupling detected"
        if len(s.explanations) > 1:
            why += f" (+{len(s.explanations) - 1} more)"
        risk_style = "red" if s.score >= 0.5 else "yellow" if s.score >= 0.2 else "green"
        table.add_row(
            s.branch_a, s.branch_b, f"[{risk_style}]{s.score:.2f}[/{risk_style}]", why
        )

    console.print(table)

    for s in scores:
        if len(s.explanations) > 1:
            console.print(f"\n[bold]{s.branch_a} vs {s.branch_b}[/bold] (risk={s.score:.2f}):")
            for line in s.explanations:
                console.print(f"  - {line}")


def to_json(scores: list[RiskScore]) -> str:
    payload = [
        {
            "branch_a": s.branch_a,
            "branch_b": s.branch_b,
            "score": s.score,
            "file_overlap": sorted(s.file_overlap),
            "line_overlap_files": sorted(s.line_overlap_files),
            "coupled_pairs": [
                {"file_a": a, "file_b": b, "coupling": c} for a, b, c in s.coupled_pairs
            ],
            "explanations": s.explanations,
        }
        for s in scores
    ]
    return json_module.dumps(payload, indent=2)
