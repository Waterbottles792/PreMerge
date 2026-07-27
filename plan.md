# PreMerge — Implementation Plan

## Project Title
PreMerge: A Git History-Based Predictive System for Early Merge Conflict Detection in Collaborative Software Development

## One-Line Pitch
A CLI + GitHub Action that predicts merge conflicts *before* they happen by analyzing git commit history (logical coupling) and live branch diffs — instead of waiting for `git merge` to fail.

---

## 1. Problem Recap (for context, not to re-implement)
Developers only discover merge conflicts at merge time. By then, both sides have already built on incompatible assumptions. PreMerge analyzes:
1. **Historical co-change patterns** — files that have changed together frequently in the past (logical/hidden coupling), even if there's no explicit code dependency.
2. **Current branch divergence** — which files/lines each active branch has modified relative to their common ancestor.

It combines these into a **conflict-risk score per branch pair**, surfaced early via CLI or CI.

---

## 2. Goals for MVP (v1) — What "Done" Looks Like
By the end of the MVP, running one command should:
- Analyze a local git repo's history.
- Take two branch names (or auto-detect all active branches vs `main`).
- Output a ranked list of "risk" between branch pairs with a human-readable explanation (which files overlap, and why — historical coupling vs direct overlap).
- Work as a standalone CLI tool AND as a GitHub Action that comments on PRs.

Explicitly **out of scope for v1** (save for "Future Work" section of your report):
- Machine learning–based prediction (start with statistical/heuristic scoring, mention ML as future work — this is good for the "expand later" resume story).
- Multi-repo / monorepo cross-service analysis.
- Real-time file-lock / IDE plugin integration.
- Language-aware AST-level conflict prediction (v1 is file+line level, not semantic).

---

## 3. Core Concepts & Algorithms

### 3.1 Logical Coupling Score (historical)
For every pair of files (A, B) in the repo:
```
coupling(A, B) = (number of commits where A and B changed together) / (number of commits where A OR B changed)
```
This is the Jaccard similarity of their "change sets" across commit history. High coupling = these files tend to change together, so if branch X only touched A and branch Y only touched B, there's a hidden risk they're stepping on related logic even without a textual conflict.

Compute via:
```bash
git log --name-only --pretty=format:"COMMIT:%H"
```
Parse into `{commit_hash: [files_changed]}`, then build a co-occurrence matrix.

### 3.2 Direct Overlap Score (current branches)
For each pair of active branches:
1. Find merge-base: `git merge-base branchA branchB`
2. Get diffs of each branch from merge-base: `git diff <merge-base> branchA --name-only` and same for branchB
3. **File-level overlap**: files touched by both branches.
4. **Line-level overlap** (stronger signal): for files touched by both, check if the actual changed line ranges intersect using `git diff -U0` hunk headers (`@@ -a,b +c,d @@`).

### 3.3 Combined Risk Score
```
risk(branchA, branchB) = w1 * direct_line_overlap_score
                        + w2 * direct_file_overlap_score
                        + w3 * avg_historical_coupling(overlapping_and_related_files)
```
Start with simple fixed weights (e.g., w1=0.5, w2=0.3, w3=0.2), make them configurable via a `premerge.config.json`. Document this scoring formula clearly in the README — it's a key "SE metrics applied" talking point for your report.

### 3.4 Validation Methodology (for your evaluation section)
- Pick 3–5 real open-source repos with public history.
- For historical merge commits, reconstruct "what if we had run PreMerge right before this merge" using the parent branches.
- Compare: did PreMerge flag risk for merges that actually had conflicts (true positives) vs merges that were clean (true negatives)?
- Report precision/recall — this becomes your "Testing & Validation" chapter.

---

## 4. Tech Stack
- **Language:** Python 3.11+ (best git-plumbing libraries + fastest to prototype)
- **Git interaction:** `GitPython` library (wraps git CLI cleanly) — fallback to raw `subprocess` calls to `git` for anything GitPython doesn't expose well (hunk-level diff parsing)
- **CLI framework:** `click` or `typer`
- **Storage (for caching coupling analysis on large repos):** SQLite (via `sqlite3`, no ORM needed for this scope)
- **Output formatting:** `rich` (for pretty CLI tables)
- **CI Integration:** GitHub Actions (YAML workflow + a small Node or Python action wrapper that posts PR comments via GitHub REST API)
- **Testing:** `pytest`
- **Packaging:** `pyproject.toml`, publishable to PyPI eventually as `pip install premerge`

---

## 5. Project Structure
```
premerge/
├── pyproject.toml
├── README.md
├── plan.md                     # this file
├── premerge/
│   ├── __init__.py
│   ├── cli.py                  # entrypoint, argument parsing
│   ├── git_utils.py            # wraps git log/diff/merge-base calls
│   ├── coupling.py              # historical co-change analysis + caching
│   ├── overlap.py               # branch diff + line-range intersection logic
│   ├── scoring.py                # combines coupling + overlap into risk score
│   ├── report.py                 # formats CLI output (rich tables) and JSON output
│   └── config.py                 # loads premerge.config.json, default weights
├── github_action/
│   ├── action.yml
│   └── post_comment.py          # posts risk report as PR comment via GitHub API
├── tests/
│   ├── test_coupling.py
│   ├── test_overlap.py
│   ├── test_scoring.py
│   └── fixtures/                 # small synthetic git repos for testing (created in test setup)
├── evaluation/
│   ├── run_validation.py         # runs PreMerge against historical merges of sample repos
│   └── results/                  # precision/recall reports, CSVs, charts
└── docs/
    ├── SRS.md
    ├── design.md
    └── test-plan.md
```

---

## 6. Build Phases (map these to your sprints / SE report milestones)

### Phase 0 — Setup (Day 1)
- Init repo, pyproject.toml, CLI skeleton with `premerge --help` working.
- Set up pytest, a synthetic test git repo fixture (a fixture that programmatically creates commits via GitPython for reproducible tests).

### Phase 1 — Git Data Extraction (Days 2–4)
- `git_utils.py`: functions to get commit log with changed files, get merge-base, get diff between two refs (file-level and hunk-level).
- Unit tests using the synthetic repo fixture.

### Phase 2 — Historical Coupling Engine (Days 5–7)
- `coupling.py`: build the co-occurrence matrix from commit history.
- Cache results in SQLite keyed by commit hash range (so re-runs on unchanged history are instant — good talking point: "designed for CI performance").
- Handle large repos gracefully (batch commit parsing, progress bar).

### Phase 3 — Branch Overlap Detection (Days 8–10)
- `overlap.py`: file-level overlap, then line-range overlap using hunk header parsing.
- Edge cases: renamed files, deleted files, binary files (skip with a warning).

### Phase 4 — Risk Scoring & Reporting (Days 11–13)
- `scoring.py`: combine the two signals into a weighted score.
- `report.py`: CLI table output showing branch pairs ranked by risk, with a plain-English explanation line (e.g., "auth.py and session.py changed together in 8/10 past commits; branch A modified auth.py, branch B modified session.py").
- `config.py`: allow weight tuning via `premerge.config.json`.

### Phase 5 — GitHub Action Integration (Days 14–16)
- `action.yml` that runs on `pull_request` events.
- `post_comment.py`: calls PreMerge's own JSON output mode, formats it as a Markdown PR comment, posts via GitHub REST API using `GITHUB_TOKEN`.
- Test on a real (small) sample repo of your own with two branches you intentionally make conflict.

### Phase 6 — Validation Study (Days 17–20)
- Pick 3–5 public repos (medium size, active history — e.g., a mid-size Flask/Express open source project).
- `evaluation/run_validation.py`: walk merge commit history, reconstruct branch states pre-merge, run PreMerge, compare predicted risk vs actual conflict (you can detect actual conflicts by checking if the merge commit has conflict markers resolved, or by trying a dry-run `git merge --no-commit --no-ff`).
- Produce precision/recall/F1 table + a short write-up in `evaluation/results/`.

### Phase 7 — Polish & Docs (Days 21–23)
- README with install instructions, usage examples, architecture diagram.
- `docs/SRS.md`, `docs/design.md`, `docs/test-plan.md` — these map directly to your course deliverables (Modules 3, 4, 5).
- Record a short demo GIF/video for the README (great for resume/LinkedIn post).

---

## 7. SE Deliverables to Produce Alongside the Code
(These map to syllabus modules — write them as you build, not after)

| Deliverable | Maps to Module | Notes |
|---|---|---|
| SRS document | Module 3 (Requirements) | Functional + non-functional requirements, use cases for CLI and GitHub Action user |
| WBS + sprint plan | Module 2 | Use the phases above as sprints; track in GitHub Projects board |
| RMMM Plan | Module 2 | Risks: large repo performance, false positive fatigue, git edge cases (submodules, rebases) |
| Architecture/design doc | Module 4 | Component diagram of the modules above, coupling/cohesion discussion of your own codebase as a nice meta-touch |
| Test plan + test cases | Module 5 | Unit tests + the validation study counts as your "system testing" |
| Metrics report | Module 7 | Precision/recall from validation study, plus code quality metrics (run `radon`/`lizard` on your own codebase — nice meta-irony: measuring your own coupling) |

---

## 8. Definition of Done for MVP
- [ ] `premerge analyze` runs on any local git repo and outputs ranked branch-pair risk
- [ ] `premerge analyze --json` for machine-readable output
- [ ] GitHub Action posts a PR comment with risk report on `pull_request` events
- [ ] Test suite passes with >80% coverage on core logic (coupling, overlap, scoring)
- [ ] Validation study completed on ≥3 real repos with a precision/recall table
- [ ] README + SRS + design doc + test plan written
- [ ] Config file supports weight tuning without code changes

---

## 9. Stretch Goals (Future Work section of your report)
- ML model (e.g., logistic regression or gradient boosting on engineered features) trained on the validation dataset to replace fixed weights
- Slack/Discord webhook notifications instead of just PR comments
- VS Code extension showing live risk indicator while coding
- Support for monorepos / cross-repo microservice coupling
- Publish to PyPI + submit GitHub Action to the Marketplace

---

## 10. Instructions for Claude Code
Start with Phase 0 and Phase 1. For each phase:
1. Write the code with docstrings and type hints.
2. Write pytest tests alongside (use a synthetic git repo fixture created programmatically with GitPython, not a real repo, so tests are reproducible and fast).
3. Confirm each phase's CLI/output works before moving to the next phase.
4. Keep `docs/SRS.md`, `docs/design.md`, and `docs/test-plan.md` updated incrementally as features are added, rather than writing them all at the end.

---

## Implementation notes (deviations from the plan above)

- **No GitPython dependency**: everything needed (log, diff, merge-base) is a
  `subprocess` call to the `git` CLI. Fewer dependencies, and full control
  over the exact output format needed for hunk parsing. Test fixtures build
  synthetic repos the same way (plain `git` calls) rather than via GitPython.
- **v1 covers Phases 0–5** (CLI, coupling engine, overlap detection, scoring,
  GitHub Action). Phase 6 (multi-repo precision/recall validation study) and
  the `docs/SRS.md` / `design.md` / `test-plan.md` / `evaluation/` deliverables
  from Phase 7 are follow-up work, not yet built.
