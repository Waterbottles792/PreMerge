# Changelog

## 2026-07-27 — Initial v1 build

Built the PreMerge MVP end to end: a CLI + GitHub Action that predicts merge
conflicts before they happen by combining historical file-coupling analysis
with live branch-diff overlap.

**Core engine (`premerge/`)**
- `git_utils.py` — git log/diff/merge-base wrappers via subprocess (no
  GitPython dependency; plain `git` CLI calls, incl. hunk-header parsing for
  line-level diffs)
- `coupling.py` — historical logical-coupling engine: builds a file
  co-occurrence matrix from commit history, scores pairs by Jaccard
  similarity, caches results in SQLite keyed by HEAD commit
- `overlap.py` — direct branch-overlap detection: file-level and
  line-range-level overlap between two branches relative to their
  merge-base
- `scoring.py` — combines line overlap, file overlap, and historical
  coupling into a single weighted risk score per branch pair, with
  human-readable explanations
- `config.py` — configurable scoring weights via `premerge.config.json`
- `report.py` / `cli.py` — `premerge analyze` command: rich table or JSON
  output, ranks all branch pairs (or a given pair) by risk

**Testing**
- `tests/` — synthetic git repo fixture (built via plain `git` calls, no
  external test repos needed) plus unit tests for coupling, overlap, and
  scoring

**CI integration**
- `github_action/action.yml` + `post_comment.py` — composite GitHub Action
  that runs PreMerge on `pull_request` events and posts/updates a single PR
  comment with the risk table (stdlib `urllib` against the GitHub REST API,
  no extra HTTP dependency)
- `.github/workflows/premerge.yml` — reference workflow wiring the action up
  on this repo

**Validation**
- Smoke-tested the CLI against a disposable demo repo (direct line overlap,
  hidden historical coupling, and a clean pair all score as expected)
- Opened and verified a real conflicting test PR (`conflict-pr` → `main`,
  since removed): PreMerge flagged it at risk 0.80 *before* any merge was
  attempted, and a `git merge --no-commit` dry-run confirmed a genuine,
  unresolvable content conflict — proving the risk score lines up with an
  actual Git conflict
- Fixed a bug in the reference workflow (local path actions need the repo
  checked out first) caught during that test

**Docs**
- `README.md` — usage, scoring formula, config, GitHub Action setup
- `plan.md` — original implementation plan, with a deviations note

**Not yet built** (see `plan.md` "Future Work" / Phase 6-7): the multi-repo
precision/recall validation study, `docs/SRS.md` / `design.md` /
`test-plan.md`, and the ML-based scoring stretch goal.
