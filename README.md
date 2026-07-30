# PreMerge

> A Git History-Based Predictive System for Early Merge Conflict Detection in
> Collaborative Software Development

---

## 1. Project Name

**PreMerge** — `premerge` on the command line, and "PreMerge Conflict Risk
Check" as a GitHub Action.

---

## 2. Project Overview

PreMerge predicts merge conflicts *before* they happen, instead of waiting for
`git merge` to fail.

It reads a repository's commit history and its live branch diffs, and produces a
**conflict-risk score for every pair of active branches**, along with a
plain-English explanation of *why* each pair is risky. It runs as a standalone
CLI for local use and as a GitHub Action that posts (and keeps updating) a
single risk-report comment on every pull request.

Two independent signals feed the score:

| Signal | What it answers | How it's measured |
|---|---|---|
| **Direct overlap** | Are these branches editing the same files and the same lines? | `git diff` against the branches' merge-base, down to hunk-level line ranges |
| **Historical coupling** | Are they editing files that have *always* changed together in the past? | Jaccard similarity of two files' change-sets across commit history |

The second signal is what makes PreMerge more than a dry-run merge: it surfaces
**hidden (logical) coupling** — the case where branch A touched `auth.py`, branch
B touched `session.py`, no text conflicts at all, but those two files have
co-changed in 9 of the last 10 commits and the two branches are almost certainly
building on incompatible assumptions.

---

## 3. Problem Statement

In collaborative development, merge conflicts are discovered at the *worst*
possible moment — at merge time, after both sides have already finished their
work and built on incompatible assumptions. The cost of resolving a conflict
scales with how long the two branches have been diverging, but developers get no
signal at all until the divergence is complete.

Existing tooling is reactive:

- `git merge` / `git rebase` report conflicts only when you attempt the merge.
- CI merge checks (e.g. GitHub's "this branch has conflicts") also fire only at
  merge time, and only against the base branch — never branch-to-branch.
- Nothing in the standard toolchain detects *semantic* or *logical* coupling.
  Two branches can merge cleanly and still break, because the files they touched
  are historically interdependent.

**PreMerge addresses the gap:** give teams a continuously available, ranked view
of which in-flight branches are on a collision course, early enough that the
cheap fix (a conversation, a rebase, a resequencing of work) is still available.

---

## 4. Target Users (Personas)

**Priya — Developer on a 6-person feature team**
Works on a long-lived feature branch alongside four teammates. Wants to know,
before she's three days deep, whether anyone else is editing the same modules.
*Uses:* `premerge analyze` locally, on demand.
*Needs:* fast, zero-config, readable output that names files, not just scores.

**Arjun — Tech Lead / Reviewer**
Owns the merge queue and decides what lands in what order. Wants a ranked list of
all open branch pairs so he can sequence merges to minimise conflict pain.
*Uses:* `premerge analyze --base main` and the PR comment.
*Needs:* explanations he can quote in a review, and no false-positive fatigue.

**Meera — DevOps / Platform Engineer**
Maintains CI. Wants conflict risk surfaced automatically on every PR without
adding a slow step to the pipeline.
*Uses:* the GitHub Action.
*Needs:* fast repeat runs (hence the SQLite cache), a machine-readable `--json`
mode, and no heavy dependencies.

**Dr. Rao — Engineering Manager / Researcher**
Interested in the empirical question: does historical coupling actually predict
conflicts? Wants the scoring model documented and tunable.
*Uses:* `premerge.config.json` weight tuning and JSON output for analysis.
*Needs:* a transparent, published formula rather than a black box.

---

## 5. Vision Statement

> **For** software teams working in parallel on a shared codebase,
> **who** currently discover merge conflicts only when it's already expensive to
> fix them,
> **PreMerge is** a git-history analysis tool
> **that** predicts and ranks conflict risk between branches days before a merge
> is attempted.
> **Unlike** `git merge` dry-runs and CI merge checks, which are purely reactive
> and text-level,
> **PreMerge** combines live branch divergence with learned historical coupling to
> catch both textual *and* hidden logical conflicts, and explains its reasoning in
> plain English.

Long-term: make "is anyone about to collide with me?" a question with an instant,
always-available answer — in the terminal, in CI, and eventually in the editor.

---

## 6. Key Features

- **Pairwise branch risk ranking** — analyze every combination of local branches,
  one specific pair, or all branches against a base, ranked highest-risk first.
- **Line-level overlap detection** — parses `git diff -U0` hunk headers to find
  branches editing *intersecting line ranges*, not just the same file.
- **Historical coupling engine** — builds a file co-occurrence matrix from commit
  history and scores every file pair by Jaccard similarity, catching hidden
  coupling with no textual overlap at all.
- **Human-readable explanations** — every score comes with lines like
  `auth.py <-> session.py: historically change together (coupling=1.00)`.
- **Configurable scoring weights** — tune the three signal weights in
  `premerge.config.json` with no code changes.
- **SQLite caching** — coupling analysis is cached keyed by HEAD commit, so
  repeat runs on unchanged history are effectively instant (designed for CI).
- **Dual output modes** — a `rich` colour-coded table for humans, `--json` for
  machines.
- **GitHub Action** — posts a single risk-report comment on `pull_request` events
  and *updates it in place* on every push, rather than spamming the thread.
- **Minimal dependency footprint** — `click` and `rich` only; git is driven via
  `subprocess`, and the Action's GitHub API calls use stdlib `urllib`.

Feature scope and priority are documented in
[docs/MoSCoW.md](docs/MoSCoW.md) — all Must Have requirements are implemented in
v1. The proposed web dashboard (C1) is wireframed in
[docs/wireframes.md](docs/wireframes.md) and built out in Figma:
[Conflict Risk Dashboard](https://www.figma.com/design/CeB8cRjy4jC3VaYn2FjIk2/Conflict-Risk-Dashboard?node-id=0-1&p=f&t=ZHQxA9wcZdzwtEkJ-0).

---

## 7. Success Metrics

**Product metrics** — is the prediction any good?

| Metric | Definition | Target |
|---|---|---|
| Precision | Of branch pairs flagged high-risk, the fraction that genuinely conflict | ≥ 0.70 |
| Recall | Of pairs that genuinely conflict, the fraction PreMerge flagged | ≥ 0.75 |
| F1 | Harmonic mean of the above | ≥ 0.72 |
| Hidden-conflict catch rate | Conflicts flagged *only* by the coupling signal, with zero direct overlap | > 0 (this is the differentiator) |

**Engineering metrics** — is it usable?

| Metric | Target |
|---|---|
| Cold-run analysis time, ~5k-commit repo | < 10 s |
| Warm (cached) re-run | < 1 s |
| Unit test coverage on core logic (`coupling`, `overlap`, `scoring`) | > 80 % |
| Added CI wall-clock time per PR | < 30 s |
| Runtime dependencies | ≤ 3 |

Precision/recall are to be established by the validation study described in
§15 — reconstructing historical merges from real open-source repositories and
comparing PreMerge's pre-merge prediction against the actual outcome. They are
**targets, not yet measured results.**

---

## 8. Assumptions

1. **The repository is a standard git repo** with accessible local history —
   not a shallow clone. (CI must use `fetch-depth: 0`.)
2. **History is append-only.** The coupling cache is keyed by HEAD commit hash;
   a history-rewriting rebase that doesn't move HEAD would serve a stale cache.
3. **Commit history is meaningful.** Coupling analysis assumes commits are
   reasonably scoped. A repo of 50-file "misc fixes" commits will produce noisy
   coupling scores.
4. **Merge commits are noise for coupling purposes** and are excluded
   (`--no-merges`), since their diffs are the union of both parents' work and
   would inflate co-change counts.
5. **Textual and historical proximity correlate with conflict risk.** This is the
   core hypothesis the validation study exists to test.
6. **Branches share a common ancestor** reachable by `git merge-base`.
7. **Users can interpret a relative risk score.** Scores are comparative rankings,
   not calibrated probabilities of conflict.

---

## 9. Constraints

**Technical**

- Python **3.11+** (uses modern typing syntax throughout).
- Requires the **`git` binary on PATH** — PreMerge shells out rather than
  embedding a git implementation.
- Analysis is **file- and line-level, not semantic.** PreMerge does not parse
  ASTs, so it cannot detect a conflict where branch A renames a function and
  branch B calls it — unless history shows those files are coupled.
- **Local branches only** for the default CLI mode; remote branches must be
  named explicitly (`origin/feature-x`).
- **Renames are not followed** in coupling analysis, so a renamed file starts a
  fresh co-change history.
- Line-range intersection is a **heuristic**, not a merge simulation — git's own
  three-way merge can still resolve overlaps PreMerge flags.

**Project**

- Single-semester scope; v1 deliberately targets **statistical/heuristic scoring
  over machine learning**, since ML requires the labeled dataset that the
  validation study has yet to produce.
- CI integration targets **GitHub Actions only**.
- No external service, database, or account required — everything runs locally or
  in the runner.

---

## 10. Project Architecture

Full diagram (with containerization and deployment): [`docs/PreMergeArchitecture.drawio`](docs/PreMergeArchitecture.drawio) / [rendered PNG](docs/PreMergeArchitecture.drawio.png).

```
                     ┌──────────────────────────────┐
   premerge analyze  │            cli.py            │  GitHub Action
   ─────────────────▶│   argument parsing, pairing  │◀───────────────
                     └───────────────┬──────────────┘
                                     │
                     ┌───────────────▼──────────────┐
                     │          scoring.py          │
                     │  weighted combination of the │
                     │   two signals + explanations │
                     └───┬────────────┬─────────┬───┘
                         │            │         │
          ┌──────────────▼──┐  ┌──────▼──────┐  │  ┌──────────────┐
          │   overlap.py    │  │ coupling.py │  └─▶│  config.py   │
          │ file + line     │  │ co-change   │     │ weights from │
          │ range overlap   │  │ matrix,     │     │ JSON config  │
          └────────┬────────┘  │ Jaccard,    │     └──────────────┘
                   │           │ SQLite cache│
                   │           └──────┬──────┘
                   │                  │
          ┌────────▼──────────────────▼───────┐     ┌──────────────┐
          │            git_utils.py           │     │  report.py   │
          │  subprocess wrappers: log, diff,  │     │ rich table / │
          │  merge-base, hunk-header parsing  │     │ JSON output  │
          └────────────────┬──────────────────┘     └──────────────┘
                           │
                    ┌──────▼──────┐
                    │  git CLI    │
                    └─────────────┘
```

**Data flow for one branch pair:**

1. `cli.py` resolves which branch pairs to analyze.
2. `scoring.py` asks `overlap.py` for direct overlap — which calls
   `git merge-base`, then `git diff -U0` for each branch, and intersects the
   resulting hunk ranges.
3. `scoring.py` asks `coupling.py` for historical coupling between files that
   *only one* branch touched — the hidden-risk signal. `coupling.py` builds (or
   loads from SQLite) the co-occurrence matrix from `git log --name-only`.
4. The three sub-scores are combined using weights from `config.py`.
5. `report.py` renders the ranked result as a table or JSON.

**Scoring model**

```
risk(A, B) = w1 · line_overlap_score      # do the branches edit the same lines?
           + w2 · file_overlap_score      # do they touch the same files?
           + w3 · historical_coupling     # do they touch files that co-change?
```

Defaults: `w1 = 0.5, w2 = 0.3, w3 = 0.2`. Historical coupling is the Jaccard
similarity of two files' change-sets:

```
coupling(A, B) = commits touching both A and B / commits touching A or B
```

**Design decisions**

- *No GitPython.* Everything needed is a `subprocess` call, which gives exact
  control over diff output format for hunk parsing and removes a dependency.
- *SQLite cache keyed by HEAD.* Treats history as append-only in exchange for
  near-zero-cost repeat runs in CI.
- *Merge commits excluded* from coupling analysis to avoid inflating co-change
  counts.
- *Layered, acyclic module graph* — `git_utils` knows nothing about scoring;
  `scoring` knows nothing about output formatting.

---

## 11. Installation

**Prerequisites:** Python 3.11+, and `git` available on your PATH.

```bash
git clone https://github.com/Waterbottles792/PreMerge.git
cd PreMerge

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e .
```

Verify:

```bash
premerge --help
```

**As a GitHub Action** — add `.github/workflows/premerge.yml` to your repository:

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
      - uses: Waterbottles792/PreMerge/github_action@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## 12. Quick Start – Local Development

**Run with Docker** (no local Python setup needed)

```bash
docker build -t premerge .

# Analyze the repo you're standing in
docker run --rm -v "$(pwd)":/repo premerge analyze --repo /repo

# Any other repo on disk
docker run --rm -v /path/to/other/repo:/repo premerge analyze --repo /repo
```

The image bundles Python, `git`, and the CLI. `-v "$(pwd)":/repo` mounts your
repo into the container read/write at `/repo`; PreMerge never needs network
access, so no other flags are required.

**Local development tools**

- **Python 3.11+** — the only runtime dependency; `pyproject.toml` pins `click`
  and `rich`.
- **git** — PreMerge shells out to the real `git` binary rather than a
  library, so any recent git works.
- **pytest** — the test suite (see below); no other dev tooling (linters,
  formatters) is currently enforced.
- **Docker** — optional, for the containerized path above.

**Run the analyzer**

```bash
# Every pairwise combination of local branches, ranked by risk
premerge analyze

# One specific pair
premerge analyze feature-a feature-b

# Every branch against a base — the CI-style view
premerge analyze --base main

# Machine-readable output
premerge analyze feature-a feature-b --json

# Analyze a repo elsewhere on disk
premerge analyze --repo /path/to/other/repo

# Bypass the coupling cache (after a history rewrite)
premerge analyze --no-cache
```

**Example output**

```
                         PreMerge Conflict Risk Report
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Branch A  ┃ Branch B  ┃ Risk ┃ Why                                           ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ feature-a │ feature-b │ 0.80 │ auth.py: both branches edit overlapping lines │
│ feature-a │ feature-c │ 0.20 │ auth.py <-> session.py: historically change   │
│           │           │      │ together (coupling=1.00) — one branch touched │
│           │           │      │ auth.py, the other touched session.py         │
└───────────┴───────────┴──────┴───────────────────────────────────────────────┘
```

Risk is colour-coded: 🔴 ≥ 0.50, 🟡 ≥ 0.20, 🟢 below that.

**Tune the weights** — create `premerge.config.json` in the repo root:

```json
{
  "weights": {
    "line_overlap": 0.5,
    "file_overlap": 0.3,
    "coupling": 0.2
  }
}
```

Or point at one explicitly with `--config <path>`.

**Run the tests**

```bash
pip install pytest
pytest              # builds synthetic git repos in tmp dirs — no fixtures on disk
pytest -v           # per-test detail
```

The test suite constructs throwaway git repositories via plain `git` calls, so
tests are hermetic and require no network or checked-in fixture repos.

**Try it on a demo conflict**

```bash
git checkout -b demo-a main && echo "change A" >> README.md && git commit -am "A"
git checkout -b demo-b main && echo "change B" >> README.md && git commit -am "B"
premerge analyze demo-a demo-b
```

---

## 13. Branching Strategy

PreMerge follows **GitHub Flow** — a single always-deployable `main`, short-lived
branches, and every change merged through a pull request. This is the model the
tool itself is designed to support: many small branches in flight at once is
exactly the situation where conflict prediction pays off.

### The flow

```
                         PR #12 review + checks
                                  |
                                  v
  main  ──●────●────────────────────●──────────────●──▶  always deployable
           \                       /                /
            ●────●────●───────────●                /     feature/dashboard-spec
                                                  /
                        ●────●────●──────────────●        fix/hunk-coordinates
                        ^                        ^
                   branch from main         squash & merge,
                                            delete branch
```

**The six steps**

| # | Step | Command |
|---|---|---|
| 1 | Create a branch off `main` | `git checkout -b feature/your-change` |
| 2 | Commit your work | `git commit -m "Add …"` |
| 3 | Open a pull request | `git push -u origin feature/your-change` |
| 4 | Automated checks run | Tests + PreMerge's own risk report |
| 5 | Review and discuss | At least one approval required |
| 6 | Merge and delete the branch | Squash & merge into `main` |

### Rules

| Rule | Detail |
|---|---|
| `main` is protected | Always deployable. No direct pushes — every change arrives via PR. |
| Branch naming | `feature/*` · `fix/*` · `docs/*` · `chore/*` |
| Branch lifetime | Target under 3 days. A long-lived branch is precisely the failure mode PreMerge exists to catch. |
| Staying current | Rebase onto `main` (`git rebase origin/main`); never merge `main` into your branch outside a PR. |
| Merging | Squash & merge, after one approving review and green checks. |
| Commit messages | Imperative mood, one logical change per commit — this directly improves PreMerge's own coupling signal. |
| Cleanup | Delete the branch after merge, so `premerge analyze` output stays focused on live work. |

### Required checks on every PR

| Workflow | What it does |
|---|---|
| [tests.yml](.github/workflows/tests.yml) | Runs `pytest` with coverage on Python 3.11 and 3.12 |
| [premerge.yml](.github/workflows/premerge.yml) | **Dogfooding** — runs PreMerge against itself and posts a conflict-risk comment on the PR |

The second one is the point: every pull request to this repository gets a comment
from the tool the repository builds, predicting how likely that PR is to conflict.

### Worked example

The `feature/project-documentation` branch was created to add the design and
planning documentation in [docs/](docs/):

```bash
git checkout main
git pull origin main
git checkout -b feature/project-documentation
# ... work, commit ...
git push -u origin feature/project-documentation
gh pr create --fill
```

See [docs/screenshots/](docs/screenshots/) for the branch, the pull request, and
the automated checks running against it.

---

## 14. Folder Structure

```
PreMerge/
├── premerge/                   # Core package
│   ├── __init__.py             # version
│   ├── cli.py                  # `premerge analyze` entrypoint (click)
│   ├── git_utils.py            # git log/diff/merge-base wrappers + hunk parsing
│   ├── coupling.py             # historical co-change engine + SQLite cache
│   ├── overlap.py              # branch diff + line-range intersection
│   ├── scoring.py              # weighted risk score + explanation generation
│   ├── report.py               # rich table and JSON output
│   └── config.py               # premerge.config.json loading, default weights
│
├── github_action/              # CI integration
│   ├── action.yml              # composite action definition
│   └── post_comment.py         # posts/updates the PR comment (stdlib urllib)
│
├── tests/                      # pytest suite
│   ├── conftest.py             # synthetic git repo fixture (plain git calls)
│   ├── test_coupling.py        # Jaccard scores, symmetry, cache round-trip
│   ├── test_overlap.py         # file- and line-level overlap detection
│   └── test_scoring.py         # combined score ordering
│
├── .github/                    # GitHub configuration
│   ├── workflows/
│   │   ├── tests.yml           # pytest + coverage on 3.11 / 3.12
│   │   └── premerge.yml        # dogfooding: PreMerge analyses its own PRs
│   └── pull_request_template.md
│
├── docs/                       # project documentation
│   ├── MoSCoW.md               # requirements prioritization
│   ├── wireframes.md           # low-fi wireframes (proposed web dashboard)
│   ├── figma-spec.md           # Figma-ready specs, all 6 screens @ 1440x1024
│   ├── dashboard-spec.md       # deep spec for the Dashboard screen
│   └── screenshots/            # GitHub Flow evidence (branch, PR, checks)
│
├── premerge.config.json        # scoring weights for this repo
├── pyproject.toml              # packaging, dependencies, pytest config
├── plan.md                     # original implementation plan + deviations
├── CHANGELOG.md                # dated, attributed build log
├── CONTRIBUTING.md             # GitHub Flow workflow, setup, testing, style
├── README.md                   # this file
└── .gitignore
```

---

## 15. Future Scope

**Near-term (next milestone)**

- **Validation study** — the highest-value missing piece. Walk the merge history
  of 3–5 real open-source repositories, reconstruct each merge's parent branches,
  run PreMerge against that reconstructed pre-merge state, and compare its
  prediction to the actual outcome (detected via `git merge --no-commit --no-ff`).
  Produces the precision/recall/F1 table in §7 and turns the scoring model from
  *plausible* into *evidenced*.
- **SE documentation set** — `docs/SRS.md`, `docs/design.md`, `docs/test-plan.md`.
- **Rename tracking** (`git log -M --follow`) so renamed files keep their coupling
  history.
- **Base-coordinate hunk comparison** — compare both branches' hunk ranges in
  merge-base line coordinates rather than each branch's own post-change numbering,
  improving line-overlap accuracy on large diffs.
- **CI test workflow** with coverage reporting, alongside the existing action.

**Medium-term**

- **ML-based scoring** — replace fixed weights with a model (logistic regression
  or gradient boosting) trained on the labeled dataset the validation study
  produces. This was deliberately deferred: fixed weights first, learned weights
  once there is data to learn from.
- **AST-level / semantic conflict prediction** — detect signature changes, renames
  and call-site edits that merge cleanly but break at runtime.
- **Slack / Discord notifications** in addition to PR comments.
- **Configurable risk thresholds** with an optional non-zero exit code, so teams
  can fail CI above a chosen risk level.

**Long-term**

- **VS Code extension** showing live conflict risk while you type.
- **Monorepo and cross-repo analysis** for coupled microservices.
- **Publish** to PyPI as `pip install premerge`, and list the action on the GitHub
  Actions Marketplace.

---

## 16. Contributors

| Name | GitHub | Role |
|---|---|---|
| Vikram | [@Waterbottles792](https://github.com/Waterbottles792) | Core engine — git plumbing, coupling analysis, overlap detection, scoring, CLI, GitHub Action |
| Kanika Rathore | — | Documentation and project planning |

See [CHANGELOG.md](CHANGELOG.md) for a dated, attributed record of what landed
when.

**Contributing:** branch from `main` following the conventions in §13, keep
commits scoped, add tests for anything touching `coupling`, `overlap` or
`scoring`, and open a pull request. PreMerge will comment on your PR with its own
assessment of how likely it is to conflict.

---

*Built as a Semester 5 Software Engineering project.*
