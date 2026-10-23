# PreMerge — Video Script

**Estimated runtime:** 8–10 minutes  
**Format:** screen recording with voiceover  
**Tone:** confident, technical, no filler

---

## SCENE 1 — The Hook (0:00–0:45)

**[SHOW: a terminal. Run this command:]**
```bash
git merge feature-b
```
**[SHOW: the conflict output — big red "CONFLICT" messages]**

---

**NARRATION:**

> "Every developer has seen this. You spend three days on a feature branch, you go to merge, and git hits you with a wall of conflicts. The work is done — but now you have to untangle it.
>
> What if you knew about this collision *before* you started? Before you wrote a single line on top of incompatible assumptions?
>
> That's PreMerge."

---

## SCENE 2 — One-Line Demo (0:45–1:45)

**[SHOW: a repo with two branches. Run:]**
```bash
premerge analyze feature-a feature-b
```

**[SHOW: the rich table output — colored risk scores]**
```
                     PreMerge Conflict Risk Report
┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Branch A  ┃ Branch B  ┃ Risk ┃ Why                                   ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ feature-a │ feature-b │ 0.82 │ auth.py: both branches edit           │
│           │           │      │ overlapping lines                     │
│ feature-a │ feature-c │ 0.23 │ auth.py <-> session.py: historically  │
│           │           │      │ change together (coupling=1.00)       │
└───────────┴───────────┴──────┴───────────────────────────────────────┘
```

---

**NARRATION:**

> "One command. PreMerge looks at your branches *right now*, before any merge is attempted, and tells you which pairs are on a collision course — and *why*.
>
> Red is high risk. Yellow is moderate. Green is safe.
>
> Notice that second row — `feature-a` and `feature-c`. They're not even touching the same files. But PreMerge is flagging them anyway, because `auth.py` and `session.py` have historically always changed together. That's a hidden logical conflict — and git has no idea it exists."

---

## SCENE 3 — What's Under the Hood (1:45–3:00)

**[SHOW: the architecture diagram — `docs/design/architecture_diagram/achitecture_diagram_updated_draw.io.png`]**

---

**NARRATION:**

> "Let me walk you through how this actually works.
>
> PreMerge runs two completely independent analyses on every branch pair, then combines them into one score.
>
> The first is **direct overlap** — are these branches editing the same files, the same lines? This is what git itself checks, so it's the obvious signal.
>
> The second is **historical coupling** — have the files these branches touch *always changed together* in the past? This is the signal git doesn't have. And it's the one that catches conflicts before they're conflicts."

**[SHOW: the scoring formula from `premerge/scoring.py`, lines 1–7 of the module docstring]**
```
risk(A, B) = w1 * line_overlap_score
           + w2 * file_overlap_score
           + w3 * avg_historical_coupling
```

---

**NARRATION:**

> "Three numbers, weighted and summed. The defaults are 0.5 for line overlap, 0.3 for file overlap, and 0.2 for historical coupling. You can tune all three in a config file. But here's the design insight: the formula is *transparent*. There's no black box. You can look at the score and immediately understand why it is what it is — because every score comes with a plain-English explanation."

---

## SCENE 4 — Code Deep Dive: The Coupling Engine (3:00–4:30)

**[SHOW: `premerge/coupling.py` — open the file in your editor]**

**[HIGHLIGHT: the module docstring at the top]**
```python
"""Historical logical-coupling analysis: files that tend to change together.

coupling(A, B) = |commits touching both A and B| / |commits touching A or B|
(Jaccard similarity of the two files' change-sets across commit history.)
"""
```

---

**NARRATION:**

> "This is the heart of PreMerge — the coupling engine. The algorithm is called Jaccard similarity. It's a measure from set theory.
>
> For any two files A and B, we look at every commit in history. How many commits touched *both* A and B? How many touched *either* A or B? Divide one by the other. That's your coupling score — zero means they never change together, one means they always do."

**[HIGHLIGHT: the `coupling()` method, lines 101–112]**
```python
def coupling(self, file_a: str, file_b: str) -> float:
    """Jaccard similarity of the two files' change-sets across history."""
    if self._file_counts is None:
        self.build()
    if file_a == file_b:
        return 1.0
    key = tuple(sorted((file_a, file_b)))
    together = self._pair_counts.get(key, 0)
    if together == 0:
        return 0.0
    either = self._file_counts[file_a] + self._file_counts[file_b] - together
    return together / either if either else 0.0
```

---

**NARRATION:**

> "Pure math, eight lines of Python. And it's fast — we build the co-occurrence matrix once from `git log`, then every query is just a dictionary lookup.
>
> But running `git log` on a repo with ten thousand commits is still slow. So we cache."

**[HIGHLIGHT: the `_cache_path()` method and the `CACHE_FILENAME` constant at the top]**
```python
CACHE_FILENAME = ".premerge_cache.sqlite"
```

---

**NARRATION:**

> "SQLite. The cache key is the current HEAD commit hash. History is append-only — if HEAD hasn't moved, the coupling scores are identical. So a warm run in CI — where nothing has changed — is essentially instant."

---

## SCENE 5 — Code Deep Dive: Overlap Detection (4:30–5:30)

**[SHOW: `premerge/overlap.py` — open the file]**

**[HIGHLIGHT: `compute_overlap()`, lines 26–50]**

---

**NARRATION:**

> "The overlap module handles the other signal — direct diff comparison.
>
> Both branches are diffed against their *common ancestor* using `git merge-base`. We're not comparing branch A to branch B directly — we're asking: what did each branch change *relative to where they both started from?* Then we intersect."

**[HIGHLIGHT: the `_ranges_intersect()` function]**
```python
def _ranges_intersect(a: tuple[int, int], b: tuple[int, int]) -> bool:
    a_start, a_len = a
    b_start, b_len = b
    return a_start < b_start + b_len and b_start < a_start + a_len
```

---

**NARRATION:**

> "Line-level detection. We parse every hunk header from `git diff -U0` — that gives us the exact line range each branch is modifying. If those ranges intersect, that's a line-level conflict. If the files overlap but the line ranges don't, that's a file-level conflict.
>
> Two different risk levels, distinguished automatically."

---

## SCENE 6 — No Dependencies on Purpose (5:30–6:00)

**[SHOW: `premerge/git_utils.py` — module docstring at the top]**
```python
"""Thin wrappers around the git CLI.

Everything PreMerge needs (log, diff, merge-base) is a subprocess call away,
so we shell out directly instead of taking on a GitPython dependency.
"""
```

**[SHOW: `pyproject.toml` — the dependencies section]**
```toml
dependencies = [
    "click>=8.1",
    "rich>=13.0",
]
```

---

**NARRATION:**

> "Two runtime dependencies. That's it. Click for the CLI, Rich for the terminal output. Git itself is driven through subprocess — we call the real git binary, which gives exact control over the output format without adding a library.
>
> And the GitHub Action posts comments using Python's stdlib `urllib`. No `requests`. No bloat. The whole thing installs in seconds."

---

## SCENE 7 — The GitHub Action + CI Gate (6:00–7:15)

**[SHOW: `.github/workflows/premerge.yml`]**
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
```

---

**NARRATION:**

> "This is the CI integration — three lines of config and it's live on every pull request. PreMerge runs, scores the branch against its base, and posts a formatted risk report directly as a PR comment. On every subsequent push, it *updates that same comment* instead of flooding the thread."

**[SHOW: a screenshot of a GitHub PR comment with the risk table — if you have one in `docs/screenshots/`; otherwise describe it]**

**[SHOW: `github_action/action.yml` — the new `fail-above` input and the gate step at the bottom]**
```yaml
  fail-above:
    description: "Fail the check if the highest risk score meets or exceeds this value (0.0–1.0)."
    required: false
    default: ""
```

```yaml
    - name: Enforce risk gate
      if: env.PREMERGE_GATE_PASSED == 'false'
      shell: bash
      run: |
        echo "::error::PreMerge risk threshold exceeded. See PR comment for details."
        exit 1
```

---

**NARRATION:**

> "And this is the engineering decision I'm most proud of — the risk gate.
>
> Set `fail-above: 0.6` and PreMerge becomes a hard CI gate, not just a report. Any branch pair scoring above the threshold fails the check and blocks the merge.
>
> But notice the order of steps: the analysis runs, the PR comment is *always posted first*, and only *then* does the gate fire. So the developer always sees the full report — including exactly which file or file pair triggered the failure — before the check turns red."

---

## SCENE 8 — Linting in CI (7:15–7:45)

**[SHOW: `.github/workflows/tests.yml` — the new `lint` job at the top]**
```yaml
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Lint
        run: pip install ruff && ruff check premerge/ tests/ github_action/
```

---

**NARRATION:**

> "Code quality gate. Ruff runs on every push and every PR — checking for import errors, unused variables, and import ordering. It runs as a separate job before pytest, so a lint failure fails fast without waiting for the full test suite.
>
> This is the CI pipeline: lint, then tests on Python 3.11 and 3.12 in parallel, then PreMerge scoring the PR against itself. The project eats its own dog food."

---

## SCENE 9 — Running It Locally (7:45–8:30)

**[SHOW: a terminal]**

**NARRATION:**

> "To run it yourself — clone the repo, install it, done."

**[TYPE and run, one at a time:]**
```bash
git clone https://github.com/Waterbottles792/PreMerge.git
cd PreMerge
pip install -e .
```

**[SHOW: the install completing]**

**NARRATION:**

> "Now analyze your own repo. `cd` into any git project and run:"

```bash
# Every branch pair, ranked by risk
premerge analyze

# All branches vs main — the CI view
premerge analyze --base main

# One specific pair
premerge analyze feature-a feature-b

# Fail if risk >= 0.5 — useful in a local pre-push hook
premerge analyze --base main --fail-above 0.5
```

**NARRATION:**

> "Or with Docker — no Python setup needed at all:"

```bash
docker build -t premerge .
docker run --rm -v "$(pwd)":/repo premerge analyze --repo /repo
```

---

## SCENE 10 — Closing (8:30–9:00)

**[SHOW: the rich table output from Scene 2 again — full screen]**

---

**NARRATION:**

> "PreMerge is a static analysis tool that turns git's own history into a prediction engine. Two signals — direct line overlap and historical coupling — combined into one transparent, tunable score. A CLI for local use, a GitHub Action for CI, and a hard risk gate when you need it.
>
> The whole thing is two runtime dependencies and a clean subprocess call to git.
>
> Thanks for watching."

---

## Appendix — Quick Reference for Recording

### Commands to have ready in your terminal

```bash
# Scene 2 — main demo
premerge analyze feature-a feature-b

# Scene 9 — installation
git clone https://github.com/Waterbottles792/PreMerge.git
cd PreMerge
pip install -e .
premerge analyze
premerge analyze --base main
premerge analyze --fail-above 0.5

# Docker run
docker build -t premerge .
docker run --rm -v "$(pwd)":/repo premerge analyze --repo /repo
```

### Files to open in editor (in order)

| Scene | File | Lines to highlight |
|---|---|---|
| 3 | `docs/design/architecture_diagram/achitecture_diagram_updated_draw.io.png` | — (image) |
| 3 | `premerge/scoring.py` | 1–7 (module docstring formula) |
| 4 | `premerge/coupling.py` | 1–7 (module docstring), 101–112 (`coupling()`), 17 (`CACHE_FILENAME`) |
| 5 | `premerge/overlap.py` | 20–23 (`_ranges_intersect()`), 26–50 (`compute_overlap()`) |
| 6 | `premerge/git_utils.py` | 1–6 (module docstring) |
| 6 | `pyproject.toml` | 6–9 (dependencies) |
| 7 | `.github/workflows/premerge.yml` | whole file |
| 7 | `github_action/action.yml` | `fail-above` input + "Enforce risk gate" step |
| 8 | `.github/workflows/tests.yml` | `lint` job (lines 10–18) |

### Talking points if you go off-script

- **Why not GitPython?** — Subprocess gives exact control over output format. GitPython abstracts it away, which makes hunk parsing harder, not easier.
- **Why SQLite for the cache?** — It's in stdlib, zero setup, and it survives process restarts unlike an in-memory dict. The whole cache is one file you can `rm` if it goes stale.
- **Why Jaccard and not something fancier?** — Jaccard is explainable. You can look at a coupling score of 0.9 and know it means "these files co-changed in 9 out of 10 commits." An ML model produces a number with no story behind it — and we don't have labeled training data yet anyway.
- **What's the difference between file overlap and line overlap?** — File overlap means both branches touched the same file. Line overlap means they touched *intersecting line ranges* in that file — which is much more likely to be an actual git conflict.
- **What does `--depth` do?** — Limits how far back `git log` walks when building the coupling matrix. On a repo with 50,000 commits, scanning all of history takes time. `--depth 2000` gives you recent coupling signal and completes in milliseconds.
