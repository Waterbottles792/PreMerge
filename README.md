# PreMerge

Predicts merge conflicts *before* they happen, by analyzing git history and
live branch diffs instead of waiting for `git merge` to fail.

It combines two signals into a risk score per branch pair:

- **Historical coupling** — files that have changed together often in the
  past (hidden/logical coupling), even with no explicit code dependency.
- **Direct overlap** — files (and line ranges) that active branches have
  actually both touched relative to their common ancestor.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Every pairwise combination of local branches, ranked by risk
premerge analyze

# One specific pair
premerge analyze feature-a feature-b

# Every branch against a base (e.g. in CI, comparing all branches to main)
premerge analyze --base main

# Machine-readable output
premerge analyze feature-a feature-b --json

# Run against a repo elsewhere on disk
premerge analyze --repo /path/to/repo
```

Example output:

```
                         PreMerge Conflict Risk Report
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Branch A  ┃ Branch B  ┃ Risk ┃ Why                                           ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ feature-a │ feature-b │ 0.80 │ auth.py: both branches edit overlapping lines │
│ feature-a │ feature-c │ 0.20 │ auth.py <-> session.py: historically change   │
│           │           │      │ together (coupling=1.00) — one branch touched│
│           │           │      │ auth.py, the other touched session.py        │
└───────────┴───────────┴──────┴───────────────────────────────────────────────┘
```

## Scoring

```
risk(A, B) = w1 * line_overlap_score      # do the two branches edit the same lines?
           + w2 * file_overlap_score      # do they touch the same files?
           + w3 * avg_historical_coupling # do they touch files that historically change together?
```

Defaults: `w1=0.5, w2=0.3, w3=0.2`. Override via a `premerge.config.json` in
the repo root (see the one at the root of this repo) or `--config <path>`:

```json
{
  "weights": { "line_overlap": 0.5, "file_overlap": 0.3, "coupling": 0.2 }
}
```

Historical coupling is the Jaccard similarity of two files' change-sets
across commit history:

```
coupling(A, B) = commits touching both A and B / commits touching A or B
```

It's cached in `.premerge_cache.sqlite` inside the repo, keyed by the current
HEAD commit — re-running on an unchanged history is instant. (This treats
history as append-only; a history-rewriting rebase without moving HEAD would
serve a stale cache — delete the cache file if that ever bites you.)

## GitHub Action

`github_action/action.yml` runs PreMerge on `pull_request` events and posts
(or updates) a single PR comment with the risk report. See
`.github/workflows/premerge.yml` in this repo for the reference setup:

```yaml
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

## Project layout

```
premerge/
├── git_utils.py   # git log/diff/merge-base, via subprocess (no GitPython needed)
├── coupling.py    # historical co-change analysis + sqlite cache
├── overlap.py     # branch diff + line-range intersection
├── scoring.py     # combines coupling + overlap into a risk score
├── report.py      # rich table / JSON output
├── config.py      # premerge.config.json loading
└── cli.py         # `premerge analyze`
github_action/     # action.yml + post_comment.py (posts PR comments)
tests/             # synthetic git repo fixture (built via plain `git` calls) + unit tests
```

## v1 scope

Implemented: CLI + GitHub Action, file/line-level overlap detection,
historical coupling scoring, configurable weights, sqlite caching, unit
tests.

Not yet built (see the original plan for the full roadmap): the
multi-repo validation study (precision/recall against real OSS merge
history), SRS/design/test-plan docs, and the ML-based scoring stretch goal.
Statistical/heuristic scoring was the deliberate v1 choice; ML is future
work once there's a labeled dataset from the validation study.

<!-- test-action-pr: trivial change to trigger the PreMerge GitHub Action -->
