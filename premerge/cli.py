"""premerge CLI entrypoint."""

from __future__ import annotations

import itertools

import click
from rich.console import Console

from . import git_utils
from .config import load_weights
from .coupling import CouplingEngine
from .report import print_table, to_json
from .scoring import compute_risk


@click.group()
def main() -> None:
    """PreMerge: predict merge conflicts before they happen."""


@main.command()
@click.argument("branches", nargs=-1)
@click.option("--repo", default=".", help="Path to the git repository.")
@click.option(
    "--base", default=None, help="Base branch to compare against (default: current branch)."
)
@click.option(
    "--json", "as_json", is_flag=True, help="Output machine-readable JSON instead of a table."
)
@click.option("--config", "config_path", default=None, help="Path to premerge.config.json.")
@click.option("--no-cache", is_flag=True, help="Skip the historical-coupling cache.")
def analyze(
    branches: tuple[str, ...],
    repo: str,
    base: str | None,
    as_json: bool,
    config_path: str | None,
    no_cache: bool,
) -> None:
    """Rank branch pairs by merge-conflict risk.

    With two BRANCHES given, analyzes just that pair. With one BRANCH given,
    analyzes it against --base. With none given and --base set, analyzes
    every other local branch against --base; with neither given, analyzes
    every pairwise combination of local branches (the useful default for
    "which of my branches are about to collide with each other").
    """
    console = Console()

    if len(branches) >= 2:
        pairs = [(branches[0], branches[1])]
    elif len(branches) == 1:
        base_branch = base or git_utils.current_branch(repo)
        pairs = [(base_branch, branches[0])]
    elif base is not None:
        other_branches = [b for b in git_utils.list_local_branches(repo) if b != base]
        pairs = [(base, b) for b in other_branches]
    else:
        pairs = list(itertools.combinations(git_utils.list_local_branches(repo), 2))

    if not pairs:
        console.print("[yellow]No other branches found to compare against.[/yellow]")
        return

    weights = load_weights(repo, config_path)
    coupling_engine = CouplingEngine(repo, rev="HEAD", use_cache=not no_cache)

    scores = [compute_risk(repo, a, b, weights, coupling_engine) for a, b in pairs]
    scores.sort(key=lambda s: s.score, reverse=True)

    if as_json:
        click.echo(to_json(scores))
    else:
        print_table(scores, console)


if __name__ == "__main__":
    main()
