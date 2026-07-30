# Changelog

## 2026-07-27 — Vikram

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

## 2026-07-30 — Kanika

Added the project documentation and design artifacts (PR #28,
`feature/project-documentation` → `main`).

**Docs**
- `README.md` — restructured into 16 sections; documents the GitHub Flow
  branching strategy (§13) and the project's folder structure (§14)
- `docs/MoSCoW.md` — Must/Should/Could/Won't requirements prioritization,
  every item mapped to its implementation status
- `docs/wireframes.md` — low-fidelity wireframes for the six proposed web
  dashboard screens (Login, Dashboard, Repositories, Risk Report, Coupling,
  Settings)
- `docs/figma-spec.md` — high-fidelity Figma-ready spec derived from the
  wireframes (frames, tokens, coordinates)
- `docs/dashboard-spec.md`, `docs/screenshots/README.md` — supporting design
  and evidence-capture docs

**CI / process**
- `.github/workflows/tests.yml` — pytest on Python 3.11 and 3.12
- `.github/pull_request_template.md`, `CONTRIBUTING.md` — PR template and
  contributor guide documenting the GitHub Flow process end to end
- Expanded `.gitignore` for build, coverage, and editor artifacts

**Cleanup**
- Removed a stray leftover `ponytail:` comment prefix from `coupling.py` and
  `git_utils.py`

## 2026-07-30 — Vikram

Added Docker support and closed out the remaining design/documentation gaps
(PR #29, `feature/docker-and-docs` → `main`).

**Docker**
- `Dockerfile` + `.dockerignore` — containerizes the CLI (Python 3.13-slim +
  `git`); verified `docker build` / `docker run ... analyze` end-to-end
  against this repo
- Fixed a real git "dubious ownership" failure when the container (running
  as root) reads a host-owned bind-mounted repo, via
  `git config --system --add safe.directory '*'` baked into the image
- `README.md` §12 — Docker quick start instructions and a local
  development tools section

**Architecture diagram**
- `docs/PreMergeArchitecture.drawio` — added the missing Containerization
  and Deployment/Infra elements plus a legend; re-exported the stale PNG
- Removed the dead, empty `docs/architecture_diag.png` placeholder
- Linked the diagram from `README.md` §10

**Design**
- Built the six wireframe screens out as an actual Figma file (Conflict
  Risk Dashboard) from `docs/figma-spec.md`; linked it from
  `docs/wireframes.md`, `docs/figma-spec.md`, and `README.md` §6
- `docs/user-stories.md` — the 25 GitHub Issues backing the project board,
  with their MoSCoW labels
