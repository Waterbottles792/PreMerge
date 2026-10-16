# Part B — Live Demo Script (≈ 6–7 minutes)

**Setup (before the demo):** `pip install -e .` then `bash docs/review3/demo.sh /tmp/pm-demo && cd /tmp/pm-demo`

| Min | Say | Run / show |
|---|---|---|
| 0:00 | **Problem:** conflicts are found only at merge time; `git merge` can't see *logical* coupling. | Slide / README §3 |
| 0:45 | **Idea:** two signals — direct overlap + historical coupling → one risk score. | `docs/PreMergeArchitecture.drawio.png` |
| 1:30 | Built-in help. | `premerge --help` |
| 2:00 | Ranked view of every branch pair. | `premerge analyze` — point at red 0.80 rows, yellow 0.20 rows, green 0.00 rows |
| 2:45 | **Direct overlap:** same lines of `auth.py`. | `premerge analyze feature-a feature-b` |
| 3:15 | Proof it is real. | `git checkout feature-a && git merge --no-commit feature-b` → CONFLICT; then `git merge --abort && git checkout main` |
| 3:45 | **Hidden coupling (the differentiator):** different files, git merges cleanly, PreMerge still flags 0.20. | `premerge analyze feature-c feature-d` |
| 4:30 | Merge-queue view, JSON, config, cache. | `premerge analyze --base feature-a` · `premerge analyze feature-a feature-b --json` · `premerge analyze feature-c feature-d --json --config /tmp/w.json` |
| 5:15 | **Quality evidence:** 30 tests, 96 % coverage, 76 % mutation score. | `cd <repo> && pytest -q --cov=premerge` |
| 5:45 | **CI:** GitHub Action comment on a PR (open the PR page / `docs/screenshots`), updated in place. | Browser |
| 6:15 | Limitations & future work: validation study, rename tracking, ML scoring, dashboard (Figma). | README §16 |

Likely viva questions: why Jaccard? (symmetric, bounded 0–1, ignores commits touching neither file); why no ML? (no labelled dataset yet); what if history is rewritten? (`--no-cache`); what are the false-positive risks? (large "misc" commits inflate coupling).
