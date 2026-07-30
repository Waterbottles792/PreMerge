# MoSCoW Prioritization — PreMerge v1

Requirements prioritization for **PreMerge**, the git history-based merge
conflict prediction system. Categories follow the MoSCoW method: **Must have**,
**Should have**, **Could have**, **Won't have (this release)**.

**Status legend:** ✅ Implemented · 🚧 Partial · ⬜ Not started

---

## Must Have — essential for v1

Without any one of these, PreMerge does not fulfil its core purpose: predicting
merge conflicts before a merge is attempted.

| # | Requirement | Rationale | Where | Status |
|---|---|---|---|---|
| M1 | **Branch comparison and analysis** — resolve a pair of branches to their common ancestor and diff both sides against it | The unit of analysis. Every other feature is downstream of a correct merge-base diff. | [`overlap.py`](../premerge/overlap.py), [`git_utils.py`](../premerge/git_utils.py) | ✅ |
| M2 | **File-level overlap detection** — identify files touched by both branches | The baseline conflict signal; cheap and always available. | [`overlap.py:32`](../premerge/overlap.py#L32) | ✅ |
| M3 | **Line-level overlap detection** — determine whether the branches' changed line ranges actually intersect | Distinguishes "both edited this file" from "both edited *the same part* of this file" — the difference between a warning and a real conflict. | [`git_utils.py:89`](../premerge/git_utils.py#L89), [`overlap.py:20`](../premerge/overlap.py#L20) | ✅ |
| M4 | **Historical coupling analysis** — score file pairs by how often they change together across commit history | The project's key differentiator. Catches *hidden* conflicts where branches share no files at all but touch historically interdependent ones. | [`coupling.py`](../premerge/coupling.py) | ✅ |
| M5 | **Merge conflict risk scoring** — combine the above into one ranked score per branch pair | Turns three raw signals into a single actionable number teams can sort by. | [`scoring.py`](../premerge/scoring.py) | ✅ |
| M6 | **Command Line Interface** — `premerge analyze`, covering all-pairs, single-pair and branch-vs-base modes | The primary interface for the developer persona; must work with zero configuration. | [`cli.py`](../premerge/cli.py) | ✅ |
| M7 | **GitHub Actions integration** — run automatically on `pull_request` events | Without CI integration the tool only helps developers who remember to run it. | [`github_action/action.yml`](../github_action/action.yml) | ✅ |
| M8 | **Pull Request risk reporting** — post the risk report as a PR comment, updating in place rather than re-posting | Puts the prediction where the merge decision is actually made. Update-in-place prevents comment spam on every push. | [`github_action/post_comment.py`](../github_action/post_comment.py) | ✅ |

**All Must Have requirements are implemented and covered by the test suite.**

---

## Should Have — important, but v1 ships without them if forced

Significant value, and all were achievable within v1 — but each has a viable
workaround, so none would have blocked release.

| # | Requirement | Rationale | Workaround if absent | Where | Status |
|---|---|---|---|---|---|
| S1 | **JSON output support** (`--json`) | Required for the GitHub Action to consume PreMerge's own output, and for any downstream analysis. | Parse the rendered table (brittle). | [`report.py:43`](../premerge/report.py#L43) | ✅ |
| S2 | **SQLite caching** of coupling analysis, keyed by HEAD commit | Coupling analysis is the expensive step. Caching makes repeat CI runs near-instant — the difference between a tolerable and an intolerable pipeline step. | Recompute every run; acceptable on small repos only. | [`coupling.py:33-73`](../premerge/coupling.py#L33-L73) | ✅ |
| S3 | **Configurable scoring weights** via `premerge.config.json` | Teams weight signals differently, and tunability is a prerequisite for the validation study that will calibrate them. | Edit source and reinstall. | [`config.py`](../premerge/config.py) | ✅ |
| S4 | **Detailed risk explanations** — plain-English reasons per pair | A bare score of `0.80` is not actionable. Naming the file and the reason is what makes the output usable in review. | Read the raw score and diff manually. | [`scoring.py:28-41`](../premerge/scoring.py#L28-L41) | ✅ |
| S5 | **Base branch comparison** (`--base main`) — all branches against one base | The tech-lead / merge-queue view; also the mode CI uses. | Run pairs individually. | [`cli.py:56-58`](../premerge/cli.py#L56-L58) | ✅ |
| S6 | **Binary file handling** — skip line-level comparison on binaries, retain file-level risk | Avoids nonsensical hunk analysis on non-text files without silently dropping a real signal. | — | [`overlap.py:35-38`](../premerge/overlap.py#L35-L38) | ✅ |
| S7 | **Cache bypass** (`--no-cache`) | Escape hatch for the known stale-cache case after a history rewrite. | Delete `.premerge_cache.sqlite` by hand. | [`cli.py:32`](../premerge/cli.py#L32) | ✅ |
| S8 | **Validation study** — precision/recall against real merge history | Converts the scoring model from *plausible* to *evidenced*, and produces the labeled dataset any future ML work depends on. | Report the model as an untested hypothesis. | — | ⬜ |
| S9 | **Rename tracking** in coupling analysis (`git log -M`) | A renamed file currently starts a fresh co-change history, silently degrading the coupling signal on refactor-heavy repos. | Accept reduced accuracy after renames. | — | ⬜ |
| S10 | **SE documentation set** — SRS, design doc, test plan | Course deliverables (Modules 3–5); also the artifacts a new contributor would need. | `plan.md` + this README. | [`docs/`](.) | 🚧 |

S1–S7 shipped in v1. **S8–S10 are the outstanding Should Haves** and are the
highest-priority items for the next milestone.

---

## Could Have — desirable, deferred

Real value, but none is on the critical path for a working conflict predictor.
Each was deferred on cost, dependency, or scope grounds.

| # | Requirement | Value | Why deferred |
|---|---|---|---|
| C1 | **Web dashboard** — browser view of risk across all branches | Better for teams than a terminal table; enables at-a-glance triage. | Requires a hosting story and a persistence layer PreMerge deliberately avoids in v1. |
| C2 | **Conflict trend analytics** — risk over time, hotspot files, chronically coupled modules | Turns a point-in-time check into a codebase-health metric; identifies modules worth refactoring. | Depends on storing historical runs (C1's persistence layer). |
| C3 | **Multi-repository support** — cross-service coupling in microservice estates | Extends hidden-coupling detection across repo boundaries, where it is arguably most valuable and least visible. | Coupling is currently computed from one repo's `git log`; cross-repo requires commit correlation by time/ticket. |
| C4 | **Interactive visualizations** — coupling graph, branch divergence view | Makes the coupling matrix legible; strong for demos and reports. | Presentation-layer work with no effect on prediction quality. |
| C5 | **Email / Slack / Discord notifications** | Pushes risk to developers who aren't looking at the PR yet — earlier warning. | PR comments already cover the primary workflow; each channel adds config and secrets surface. |
| C6 | **Configurable risk thresholds with non-zero exit code** | Lets teams *fail* CI above a chosen risk level rather than only reporting. | Needs calibrated thresholds — blocked on the S8 validation study. |
| C7 | **Graceful large-repo handling** — batched log parsing, progress bar | Keeps the tool usable on repos with 100k+ commits. | Current performance is acceptable at the target repo size; optimize when measured, not before. |

---

## Won't Have — explicitly out of scope for this release

Deliberately excluded. Listed so the boundary is documented rather than implied.

| # | Requirement | Why not in v1 |
|---|---|---|
| W1 | **Machine Learning–based prediction engine** | Requires a labeled dataset of (branch pair → did it actually conflict) that does not yet exist — it is the *output* of the S8 validation study. Fixed, documented, tunable weights first; learned weights once there is data to learn from. Sequencing, not rejection. |
| W2 | **Real-time monitoring service** | A persistent daemon watching branches implies hosting, auth, and state. v1 is intentionally a stateless tool you invoke, with CI providing the automation. |
| W3 | **IDE plugins (VS Code, IntelliJ)** | High value long-term — live risk while typing — but each is a separate codebase in a separate language. The JSON output mode (S1) is the deliberate integration seam that keeps this cheap to add later. |
| W4 | **Cloud-hosted SaaS platform** | Out of scope for an academic project: billing, tenancy, and granting a third party read access to private source. PreMerge runs on your machine or your runner, and never transmits code. |
| W5 | **Semantic / AST-level conflict prediction** | v1 is file- and line-level by design. Language-aware analysis means a parser per language and a large accuracy claim that would need its own validation. |
| W6 | **Automatic conflict resolution** | PreMerge predicts and explains; it does not modify code. Auto-resolution is a fundamentally different risk profile and a non-goal. |

---

## Summary

| Category | Total | Implemented | Outstanding |
|---|---|---|---|
| Must Have | 8 | 8 | 0 |
| Should Have | 10 | 7 | 3 (S8, S9, S10) |
| Could Have | 7 | 0 | 7 — post-v1 roadmap |
| Won't Have | 6 | — | Out of scope by decision |

**v1 is feature-complete against its Must Have set.** The critical path to a
complete deliverable now runs through **S8 (validation study)**, which unblocks
both C6 (risk thresholds need calibrated cut-offs) and W1 (ML scoring needs the
labeled dataset).

See [`plan.md`](../plan.md) for the original phase breakdown and
[`README.md`](../README.md) §15 for the roadmap narrative.
