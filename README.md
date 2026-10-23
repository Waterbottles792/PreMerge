# PreMerge

**Predict merge conflicts before they happen.**

PreMerge scores the collision risk between any two branches by combining two signals: direct line-level overlap from live diffs, and historical coupling learned from commit history. It runs as a local CLI and as a GitHub Action that posts a risk report comment on every pull request.

---

## How it works

```
risk(A, B) = 0.5 × line_overlap_score
           + 0.3 × file_overlap_score
           + 0.2 × historical_coupling_score
```

| Signal | What it catches | How |
|---|---|---|
| **Line overlap** | Both branches edit the same lines | `git diff -U0` hunk intersection against merge-base |
| **File overlap** | Both branches touch the same files (different lines) | `git diff --name-only` against merge-base |
| **Historical coupling** | Files that always change together in history — even with zero textual overlap | Jaccard similarity across commit log co-occurrence, cached in SQLite |

The third signal is the differentiator: it catches logical conflicts where `auth.py` and `session.py` have never conflicted textually but have co-changed in 9 of 10 commits.

---

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| CLI | [click](https://click.palletsprojects.com/) |
| Terminal output | [rich](https://github.com/Textualize/rich) |
| Git integration | `subprocess` → `git` binary (no GitPython) |
| Coupling cache | SQLite via stdlib `sqlite3` |
| GitHub API | stdlib `urllib` (no requests) |
| CI | GitHub Actions (2 workflows) |
| Container | Docker (`python:3.13-slim`) |
| Tests | pytest + pytest-cov |
| Config | `premerge.config.json` (JSON) |
| Packaging | pyproject.toml + setuptools |

No external database, no web server, no cloud services required.

---

## Installation

**Prerequisites:** Python 3.11+, `git` on your PATH.

```bash
git clone https://github.com/Waterbottles792/PreMerge.git
cd PreMerge
pip install -e .
premerge --help
```

**With Docker** (no local Python needed):

```bash
docker build -t premerge .
docker run --rm -v "$(pwd)":/repo premerge analyze --repo /repo
```

---

## Usage

```bash
# All local branch pairs, ranked by risk
premerge analyze

# One specific pair
premerge analyze feature-a feature-b

# All branches vs a base (CI-style)
premerge analyze --base main

# Machine-readable output
premerge analyze feature-a feature-b --json

# Skip the coupling cache (after a history rewrite)
premerge analyze --no-cache

# Limit history depth — faster on repos with thousands of commits
premerge analyze --depth 1000

# CI gate: exit 1 if any pair scores >= 0.6
premerge analyze --base main --fail-above 0.6
```

**Example output:**

```
                     PreMerge Conflict Risk Report
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Branch A  ┃ Branch B  ┃ Risk ┃ Why                                        ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ feature-a │ feature-b │ 0.80 │ auth.py: both branches edit overlapping    │
│           │           │      │ lines                                      │
│ feature-a │ feature-c │ 0.20 │ auth.py <-> session.py: historically       │
│           │           │      │ change together (coupling=1.00)            │
└───────────┴───────────┴──────┴────────────────────────────────────────────┘
```

Risk colour: 🔴 ≥ 0.50 · 🟡 ≥ 0.20 · 🟢 below that

**Tune the weights** — create `premerge.config.json` in your repo root:

```json
{
  "weights": {
    "line_overlap": 0.5,
    "file_overlap": 0.3,
    "coupling": 0.2
  }
}
```

---

## GitHub Action

Add `.github/workflows/premerge.yml` to any repository:

```yaml
name: PreMerge Conflict Risk Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  premerge:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: Waterbottles792/PreMerge/github_action@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: fail the check if any pair's risk score is >= this value
          # fail-above: "0.6"
```

The action posts a single comment on the PR and updates it in place on every push — no comment spam.

---

## Project structure

```
PreMerge/
├── premerge/
│   ├── cli.py          # click entrypoint, branch pair resolution
│   ├── git_utils.py    # subprocess wrappers: log, diff, merge-base, hunk parsing
│   ├── coupling.py     # Jaccard co-change engine + SQLite cache
│   ├── overlap.py      # file and line-range intersection
│   ├── scoring.py      # weighted risk score + plain-English explanations
│   ├── report.py       # rich table and JSON output
│   └── config.py       # weight loading from premerge.config.json
│
├── github_action/
│   ├── action.yml      # composite action definition
│   └── post_comment.py # posts/updates PR comment via stdlib urllib
│
├── tests/
│   ├── conftest.py         # synthetic git repo fixture (real git calls, tmp dirs)
│   ├── test_coupling.py    # Jaccard scores, symmetry, SQLite cache round-trip
│   ├── test_overlap.py     # file and line-level overlap detection
│   └── test_scoring.py     # combined score ordering
│
├── .github/workflows/
│   ├── tests.yml       # pytest on Python 3.11 and 3.12
│   └── premerge.yml    # dogfooding: PreMerge analyses its own PRs
│
├── Dockerfile
├── pyproject.toml
└── premerge.config.json
```

---

## Running tests

```bash
pip install pytest pytest-cov
pytest -v --cov=premerge
```

Tests build throwaway git repos with real `git` calls — no fixtures on disk, no network.

---

## Suggestions for improvement

**High value, low effort**

- **`--threshold` / non-zero exit code** — let teams fail CI when risk exceeds a configured value (e.g. `--fail-above 0.5`). Currently the action is informational only; making it a gate is one `sys.exit` away.
- **Publish to PyPI** — the action currently installs from GitHub (`pip install "premerge @ git+https://..."`). A PyPI release makes installs faster and version-pinnable.
- **Rename tracking** — add `git log -M --follow` support so a renamed file keeps its coupling history instead of starting fresh.

**Medium effort**

- **Base-coordinate hunk comparison** — both branches' hunk ranges are currently in their own post-diff line coordinates, not merge-base coordinates. Large diffs can produce false positive line-overlap hits. Normalising to base coordinates fixes this.
- **Configurable history depth** — a `--depth N` flag to limit how far back `git log` walks. Huge repos (100k+ commits) can make the cold coupling build slow; truncating at 1000–2000 commits is usually good enough.
- **GitLab CI / Bitbucket Pipelines support** — the core analysis is CI-agnostic; only `post_comment.py` is GitHub-specific. Abstracting the comment-posting step unlocks other platforms.

**Larger scope**

- **Validation study** — walk the merge history of real open-source repos, reconstruct pre-merge states, and measure precision/recall against actual conflict outcomes. This turns the scoring model from plausible into evidenced and drives weight calibration.
- **ML-based scoring** — once a labeled dataset exists from the validation study, replace fixed weights with a logistic regression or gradient boost model trained on actual conflict outcomes.
- **AST-level conflict detection** — text-clean merges that break at runtime (function renamed in one branch, called with old name in another) are invisible to PreMerge today. Parsing ASTs at diff time would catch these.
- **VS Code / JetBrains extension** — surface risk scores inline while the developer is still writing, before a PR exists.

---

## Contributors

| Name | GitHub | Role |
|---|---|---|
| Vikram | [@Waterbottles792](https://github.com/Waterbottles792) | Core engine, CLI, GitHub Action |
| Kanika Rathore | [@kanika10-hub](https://github.com/kanika10-hub) | Documentation and project planning |

*Semester 5 Software Engineering project.*
