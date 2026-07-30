# Contributing to PreMerge

Thanks for contributing. This project follows **GitHub Flow** — one protected
`main`, short-lived branches, and every change merged through a pull request.

## Quick setup

```bash
git clone https://github.com/Waterbottles792/PreMerge.git
cd PreMerge
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
pip install pytest
pytest
```

## The workflow

### 1. Branch from `main`

```bash
git checkout main
git pull origin main
git checkout -b feature/your-change
```

Never commit directly to `main` — it is protected.

**Branch naming:**

| Prefix | Use for | Example |
|---|---|---|
| `feature/` | New capability | `feature/rename-tracking` |
| `fix/` | Bug fix | `fix/hunk-coordinate-space` |
| `docs/` | Documentation only | `docs/architecture-diagram` |
| `chore/` | Tooling, CI, dependencies | `chore/add-ruff` |

Keep branches short-lived — under three days. A branch that lives for two weeks
is precisely the failure mode PreMerge exists to detect.

### 2. Commit

One logical change per commit. Imperative mood, no trailing period:

```
Add rename tracking to the coupling engine
Fix hunk ranges being compared in the wrong coordinate space
```

Well-scoped commits directly improve PreMerge's own coupling signal — a repo of
50-file "misc fixes" commits produces noisy co-change scores.

### 3. Keep up to date with `main`

```bash
git fetch origin
git rebase origin/main
```

Rebase your branch onto `main`; never merge `main` into your branch outside a PR.

### 4. Open a pull request

```bash
git push -u origin feature/your-change
gh pr create --fill        # or open it in the GitHub UI
```

Fill in the PR template. Two checks run automatically:

| Check | What it does |
|---|---|
| **Tests** | Runs `pytest` on Python 3.11 and 3.12 |
| **PreMerge Conflict Risk Check** | Runs PreMerge on itself and comments the risk report |

Both must be green. Read PreMerge's own comment on your PR — if it flags high
risk against another open branch, coordinate before merging.

### 5. Review and merge

At least one approving review. **Squash and merge** into `main`, then delete the
branch — this keeps `premerge analyze` output focused on live work.

## Testing

```bash
pytest                                   # all tests
pytest tests/test_coupling.py -v         # one file
pytest --cov=premerge --cov-report=term  # with coverage
```

Tests build throwaway git repositories in temp directories via plain `git`
calls, so they are hermetic — no network, no checked-in fixture repos.

**Any change to `coupling.py`, `overlap.py` or `scoring.py` needs a test.**
These three modules are the prediction engine; a regression there is silent and
produces wrong scores rather than a crash.

## Code style

- Python 3.11+, type hints on all public functions
- Docstrings on modules and public functions — say *why*, not *what*
- No new runtime dependencies without discussion; the current footprint is
  `click` + `rich`, and keeping it small is a design goal
- Match the surrounding code's comment density and naming

## Reporting bugs

Open an issue with: what you ran, what you expected, what happened, and your
`git --version` and Python version. For wrong risk scores, include the
`premerge analyze --json` output.
