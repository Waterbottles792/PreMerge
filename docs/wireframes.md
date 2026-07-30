# PreMerge — Low-Fidelity Wireframes

**Component:** PreMerge Web Dashboard
**Status:** Design artifact for a *proposed* component — the web dashboard is
**C1 (Could Have)** in [MoSCoW.md](MoSCoW.md) and is not part of the v1 release,
which ships as a CLI and a GitHub Action. These wireframes define the interface
should the dashboard be built.
**Fidelity:** Low — structure, hierarchy and flow only. No colour, typography,
spacing, iconography or final copy. All data shown is placeholder.

---

## Design Conventions

Read the sketches with these conventions:

| Notation | Meaning |
|---|---|
| `+---+` `\|` | Container / panel boundary |
| `[ Label ]` | Button |
| `[ text... ]` | Text input field |
| `Label v` | Dropdown / select |
| `[ ]` `[x]` | Checkbox (unchecked / checked) |
| `[==O----]` | Slider control |
| `[####----]` | Progress or magnitude bar |
| `>` | Navigation affordance — this row/item drills down |
| `> Item` (nav) | Currently active navigation item |
| `(!)` | Warning / high-severity marker |
| `( )` | Informational / low-severity marker |
| `#  +  .` | Density marks in the coupling matrix (high / medium / low) |

**Global application shell.** Screens 2–6 share one layout: a persistent top bar
(product mark, repository switcher, help, account menu) and a persistent left
navigation rail. Only the main content region changes between screens. Screen 1
(Login) is deliberately outside this shell — it is pre-authentication and has no
navigation.

**Responsive intent.** At narrow widths the left rail collapses to an icon strip,
and the two-column master–detail layouts on screens 4 and 5 stack vertically
(list first, detail below).

---

## Navigation Map

```
   [ Login ]
       |
       | first sign-in / no repos connected
       +------------------> [ Repository Selection ]
       |                              |
       | returning user               | select repo
       v                              v
   [ Dashboard ] <---------------------
       |    |    |
       |    |    +----------------> [ Settings ]
       |    |
       |    +-------------------> [ Historical Coupling Analysis ]
       |                                    ^
       | click a branch pair                | drill into a file pair
       v                                    |
   [ Conflict Risk Report ] -----------------
```

Left-rail items (Dashboard, Repos, Risk, Coupling, Settings) are reachable from
any authenticated screen, so the graph above shows *primary task flow*, not the
only permitted transitions.

---

## 1. Login Page

### Layout
Single-column, vertically and horizontally centred card on an otherwise empty
canvas. No navigation chrome — this screen has exactly one job. The card is
ordered by likelihood of use: the OAuth path is placed first and given the most
visual weight, with credential fields below a divider as the secondary path.

### Components
- Product wordmark and one-line value proposition (orientation for first-time visitors)
- **Sign in with GitHub** — primary action, full-width button
- "or" divider separating the two authentication paths
- Email field, Password field
- "Remember me" checkbox; "Forgot password?" link
- **Sign in** — secondary submit button
- Inline error region, reserved in the layout so its appearance does not shift the form
- "Create account" link below the card

### Navigation
- **Sign in with GitHub** → OAuth consent → returns to **Repository Selection** (first sign-in) or **Dashboard** (returning user)
- **Sign in** (credentials) → same destinations
- **Create account** → registration
- **Forgot password?** → password reset
- No exit to authenticated screens without a successful sign-in

**Design note:** GitHub OAuth is primary because PreMerge must read repository
history to function — a user who signs up with email alone still has to connect
GitHub before any screen has content. Leading with OAuth collapses two steps into
one.

```
+----------------------------------------------------------------------------+
|                                                                            |
|                                                                            |
|                    +----------------------------------+                    |
|                    |                                  |                    |
|                    |          [ PreMerge ]            |                    |
|                    |        logo / wordmark           |                    |
|                    |                                  |                    |
|                    |   Predict merge conflicts        |                    |
|                    |   before they happen.            |                    |
|                    |                                  |                    |
|                    |  +----------------------------+  |                    |
|                    |  |   Sign in with GitHub   >  |  |                    |
|                    |  +----------------------------+  |                    |
|                    |      (primary  -  OAuth)         |                    |
|                    |                                  |                    |
|                    |  ---------- or ----------        |                    |
|                    |                                  |                    |
|                    |   Email                          |                    |
|                    |  +----------------------------+  |                    |
|                    |  |                            |  |                    |
|                    |  +----------------------------+  |                    |
|                    |   Password                       |                    |
|                    |  +----------------------------+  |                    |
|                    |  |                            |  |                    |
|                    |  +----------------------------+  |                    |
|                    |                                  |                    |
|                    |  [ ] Remember me    Forgot?  >   |                    |
|                    |                                  |                    |
|                    |  +----------------------------+  |                    |
|                    |  |          Sign in           |  |                    |
|                    |  +----------------------------+  |                    |
|                    |                                  |                    |
|                    |  (!) error message region        |                    |
|                    |                                  |                    |
|                    +----------------------------------+                    |
|                         New here?  Create account  >                       |
|                                                                            |
+----------------------------------------------------------------------------+
```

---

## 2. Dashboard

### Layout
Three horizontal bands inside the main region, ordered by decreasing urgency:

1. **Summary tiles** — four at-a-glance counters
2. **Top risk branch pairs** — the primary work surface, a ranked table
3. **Secondary panels** — coupling hotspots and recent activity, side by side

This is the answer-first arrangement: the single question a developer opens
PreMerge to ask is *"is anything about to collide?"*, so the ranked risk table
sits above the fold and everything else is supporting context.

### Components
- Section header with last-sync timestamp and manual **Sync** action
- Four stat tiles: repositories connected, active branches, high-risk pairs, average risk
- Ranked risk table: branch A, branch B, magnitude bar + numeric score, short reason, drill-down affordance
- **View all** link into the full Conflict Risk Report
- Coupling hotspots panel — the top historically coupled file pairs
- Recent activity feed — analysis runs, syncs, configuration changes

### Navigation
- Any table row → **Conflict Risk Report**, pre-selected to that pair
- **View all** → **Conflict Risk Report** (unfiltered)
- **Analyse >** in hotspots → **Historical Coupling Analysis**
- Repository switcher in the top bar → re-scopes the whole dashboard
- **Sync** → re-runs analysis in place; table shows a loading state, no navigation

**Design note:** score is shown as both a bar and a number. The bar supports fast
visual scanning of a ranked list; the number is what a user quotes in a code
review. Neither alone does both jobs.

```
+----------------------------------------------------------------------------+
| [PreMerge]      repo: acme/payments  v      [?]   [ user v ]               |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAV          | OVERVIEW                 last sync 2m ago   [Sync]          |
| ------------ |                                                             |
| > Dashboard  | +---------+ +---------+ +---------+ +---------+             |
|   Repos      | | REPOS   | | BRANCH  | |HIGH RISK| |AVG RISK |             |
|   Risk       | |   04    | |   17    | |   03    | |  0.34   |             |
|   Coupling   | |connected| | active  | |  pairs  | |all pairs|             |
|   Settings   | +---------+ +---------+ +---------+ +---------+             |
| ------------ |                                                             |
| [+] Add repo | +- TOP RISK BRANCH PAIRS -------------------------+         |
|              | | BR A      BR B      RISK           WHY          |         |
| ------------ | | ----------------------------------------------- |         |
| Docs   ?     | | feature-a feature-b [####----] .80 same lines > |         |
| Logout       | | feature-a hotfix-x  [###-----] .55 same file  > |         |
|              | | feature-c feature-b [##------] .20 coupling   > |         |
|              | | main      docs-fix  [--------] .00 clear      > |         |
|              | |                                   [View all >]  |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
|              | +- COUPLING HOTSPOTS ------+ +- ACTIVITY --------+          |
|              | | auth.py <> session  1.00 | | PR #42 run    2m  |          |
|              | | api.py  <> routes   0.80 | | repo synced   1h  |          |
|              | | db.py   <> models   0.60 | | weights saved 1d  |          |
|              | |             [Analyse >]  | |         [More >]  |          |
|              | +--------------------------+ +-------------------+          |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

---

## 3. Repository Selection

### Layout
Filter bar above a single scrolling list. One row per repository, one connection
toggle per row — a flat structure with no nesting, because the task ("turn
analysis on for this repo") is a single binary decision repeated N times.

### Components
- Search field (filter by name) and organisation dropdown
- Filter chips: All / Connected / Not connected
- Repository rows: name, branch count, last-scan time, connection toggle, drill-down
- Inline scan progress bar for a repository currently being analysed
- Pagination control
- **Empty state** panel for users with nothing connected yet, containing the single
  action that resolves it

### Navigation
- Toggle **ON** → begins first scan; row switches to the in-progress state
- Row `>` → **Dashboard**, scoped to that repository
- **Connect GitHub account** (empty state) → GitHub App installation flow
- **[+] Add repo** in the left rail → this screen

**Design note:** the first scan of a large repository is genuinely slow — it walks
the entire commit log to build the co-change matrix. That latency is made visible
inline with a progress bar rather than hidden behind a spinner or a blocking
modal, so the user can connect other repositories while it runs.

```
+----------------------------------------------------------------------------+
| [PreMerge]      repo: acme/payments  v      [?]   [ user v ]               |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAV          | REPOSITORIES                                                |
| ------------ |                                                             |
|   Dashboard  | +---------------------------+ +---------------+             |
| > Repos      | | search repositories...    | | org: all    v |             |
|   Risk       | +---------------------------+ +---------------+             |
|   Coupling   |  [ All ] [ Connected ] [ Not connected ]                    |
|   Settings   |                                                             |
| ------------ | +-------------------------------------------------+         |
| [+] Add repo | | NAME          BRANCHES  LAST SCAN     STATUS    |         |
|              | | ----------------------------------------------- |         |
| ------------ | | acme/payments      07    2 min ago   [ ON  ] >  |         |
| Docs   ?     | | acme/web-app       05    1 hr ago    [ ON  ] >  |         |
| Logout       | | acme/infra         03    3 d ago     [ ON  ] >  |         |
|              | | acme/docs          02    --          [ off ] >  |         |
|              | | acme/legacy-api    -- (scanning...)  [ ON  ]    |         |
|              | |     [############--------] 62%                  |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
|              | showing 5 of 12          < prev   1  2  3   next >          |
|              |                                                             |
|              | +- EMPTY STATE (no repos) ------------------------+         |
|              | |   No repositories connected yet.                |         |
|              | |   [ Connect GitHub account ]                    |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

---

## 4. Conflict Risk Report

The core screen of the product — everything else exists to lead here.

### Layout
**Master–detail.** A narrow ranked list of branch pairs on the left keeps the
full comparison set in view; a wide detail panel on the right explains the
selected pair. Selecting a different pair updates only the right panel, so a user
comparing several pairs never loses their place in the list.

The detail panel is ordered as *verdict → arithmetic → evidence → action*: the
score first, then the weighted breakdown that produced it, then the specific
files and line ranges, then what to do about it.

### Components
- Base-branch selector, **Re-run** and **Export JSON** actions
- Left: ranked, sortable pair list with scores; **load more** for long lists
- Right, per selected pair:
  - Headline score with magnitude bar and a HIGH / MED / LOW band
  - **Score breakdown** — each signal's weight × sub-score, and the total.
    This mirrors the documented formula exactly, so the number is auditable
    rather than opaque
  - **Evidence list** — files driving the score, severity-marked: line-level
    overlap `(!)` above file-level-only overlap `( )`, each with a plain-English
    reason and a link to the diff
  - Merge-base commit reference
  - Actions: **Open PR**, **Dismiss** (mute this pair)

### Navigation
- Left list item → updates the detail panel (no page change)
- **view diff >** → diff view for that file
- File name → **Historical Coupling Analysis**, focused on that file
- **Open PR >** → the pull request on GitHub (external)
- **Export JSON** → downloads the same payload the CLI's `--json` mode produces
- **Dismiss** → removes the pair from active ranking, with undo

**Design note:** exposing the weighted breakdown is a deliberate trust decision. A
predictive tool that outputs an unexplained number gets ignored the first time it
is wrong. Showing that 0.80 = (0.5 × 1.00) + (0.3 × 1.00) + (0.2 × 0.00) lets a
sceptical user check the arithmetic — and points them at Settings if they
disagree with the weighting rather than abandoning the tool.

```
+----------------------------------------------------------------------------+
| [PreMerge]      repo: acme/payments  v      [?]   [ user v ]               |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAV          | RISK REPORT   base: main v   [Re-run]  [Export JSON]        |
| ------------ |                                                             |
|   Dashboard  | +- PAIRS (8) ------+ +- DETAIL --------------------+        |
|   Repos      | | sort: risk v     | | feature-a  <->  feature-b   |        |
| > Risk       | |                  | |                             |        |
|   Coupling   | | >feature-a       | | RISK  0.80  [########--] HI |        |
|   Settings   | |  feature-b  .80  | |                             |        |
| ------------ | |  ------------    | | breakdown        w    score |        |
| [+] Add repo | |  feature-a       | |  line overlap   .5 x 1.00   |        |
|              | |  hotfix-x   .55  | |  file overlap   .3 x 1.00   |        |
| ------------ | |  ------------    | |  coupling       .2 x 0.00   |        |
| Docs   ?     | |  feature-c       | |  ------------------------   |        |
| Logout       | |  feature-b  .20  | |  total                 .80  |        |
|              | |  ------------    | |                             |        |
|              | |  main            | | (!) auth.py                 |        |
|              | |  docs-fix   .00  | |     both edit lines 40-52   |        |
|              | |  ------------    | |     [ view diff > ]         |        |
|              | |                  | |                             |        |
|              | |                  | | ( ) config.py               |        |
|              | |                  | |     same file, diff lines   |        |
|              | |                  | |                             |        |
|              | | [ load more ]    | | merge-base  a1b2c3d         |        |
|              | |                  | | [Open PR >] [Dismiss]       |        |
|              | +------------------+ +-----------------------------+        |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

---

## 5. Historical Coupling Analysis

### Layout
Three stacked bands, moving from overview to specifics:

1. **Controls** — history range, minimum coupling threshold, path filter
2. **Co-change matrix** — a symmetric grid of files with density marks, plus a legend
3. **Top coupled pairs** table, and a **selected pair** detail strip below it

The matrix answers "where is coupling concentrated in this codebase?"; the table
answers "which specific pairs are worst?"; the detail strip answers "why does
this pair score what it scores?"

### Components
- History range selector, minimum-coupling filter, path-glob filter, **Rebuild** action
- Symmetric co-change matrix with abbreviated file labels and a density legend
- Top coupled pairs table: file A, file B, Jaccard coupling, and the raw
  `together / either` commit counts behind it
- Selected-pair strip: score, co-change count, most recent shared commit, and
  links out

### Navigation
- Matrix cell → selects that pair, populating the detail strip
- Table row → same selection
- **view commits >** → commit history filtered to commits touching both files
- **view in risk report >** → **Conflict Risk Report**, filtered to branch pairs
  affected by this file pair
- **Rebuild** → invalidates the cached matrix and recomputes

**Design note:** the raw counts (`12 / 12`) sit next to the derived score because
Jaccard similarity is scale-blind — two files that changed together once, and
never apart, also score 1.00. Showing the denominator is what separates a strong
signal from a statistically meaningless one, and prevents users acting on noise.

```
+----------------------------------------------------------------------------+
| [PreMerge]      repo: acme/payments  v      [?]   [ user v ]               |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAV          | COUPLING     range: all history v    min: 0.3 v             |
| ------------ | path filter: [ src/**            ]   [Rebuild]              |
|   Dashboard  |                                                             |
|   Repos      | +- CO-CHANGE MATRIX -----------+ +- LEGEND ------+          |
|   Risk       | |        au se ap ro db mo un  | |  #  0.8 - 1.0 |          |
| > Coupling   | |  auth   \  #  +  .  .  .  .  | |  +  0.5 - 0.8 |          |
|   Settings   | | sessn   #  \  +  .  .  .  .  | |  .  0.2 - 0.5 |          |
| ------------ | |   api   +  +  \  #  +  .  .  | |     < 0.2     |          |
| [+] Add repo | | routes  .  .  #  \  .  .  .  | |  \  self      |          |
|              | |    db   .  .  +  .  \  #  .  | +---------------+          |
| ------------ | | models  .  .  .  .  #  \  .  |  click a cell              |
| Docs   ?     | | unrel   .  .  .  .  .  .  \  |  for pair detail           |
| Logout       | +------------------------------+                            |
|              |                                                             |
|              | +- TOP COUPLED PAIRS -----------------------------+         |
|              | | FILE A      FILE B      COUPLING  TOGETHER/ANY  |         |
|              | | ----------------------------------------------- |         |
|              | |>auth.py     session.py    1.00      12 / 12     |         |
|              | | api.py      routes.py     0.80       8 / 10     |         |
|              | | db.py       models.py     0.60       6 / 10     |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
|              | +- SELECTED: auth.py <-> session.py --------------+         |
|              | | Jaccard 1.00  -  changed together in 12 commits |         |
|              | | last: 'fix token refresh'  2026-07-21           |         |
|              | | [ view commits > ]   [ view in risk report > ]  |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

---

## 6. Settings

### Layout
Horizontal tab strip over a single scrolling column of grouped panels. Tabs
separate unrelated concerns (scoring, alerts, integrations, cache); within the
active tab, related controls are grouped into bordered panels with a local save
action, so a user changing one weight is not forced to review every setting on
the page.

### Components

**Scoring tab** (shown)
- Three weight sliders — line overlap, file overlap, coupling — each with its
  numeric value
- Live sum indicator with an inline validation message; **Save** is disabled while
  the sum is invalid
- **Reset defaults** (restores 0.5 / 0.3 / 0.2) and **Save**
- Risk threshold panel: numeric cut-offs for the high and medium bands, and a
  checkbox to fail the CI check above the high threshold
- Cache panel: current cache size, a reuse toggle, and **Clear cache**

**Other tabs:** Alerts (notification channels and triggers), Integrations (GitHub
App connection, token status), and an overflow `[...]` for account and danger-zone
actions.

### Navigation
- Tabs switch the panel set without leaving the screen
- **Save** persists and returns the user to their prior context
- **Clear cache** → confirmation dialog before destructive action
- Settings are per-repository, scoped by the top-bar repository switcher

**Design note:** the sum-to-1.00 constraint is enforced with a live indicator and
a disabled save rather than by silently normalising the values behind the scenes.
Auto-normalising would mean a user who types three numbers gets back three
different numbers, which reads as a bug. This mirrors the same constraint in the
CLI's `premerge.config.json`, so the two interfaces cannot disagree.

```
+----------------------------------------------------------------------------+
| [PreMerge]      repo: acme/payments  v      [?]   [ user v ]               |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAV          | SETTINGS                                                    |
| ------------ | [ Scoring ] [ Alerts ] [ Integr. ] [ Cache ] [...]          |
|   Dashboard  | ==========                                                  |
|   Repos      |                                                             |
|   Risk       | +- SCORING WEIGHTS -------------------------------+         |
|   Coupling   | |                                                 |         |
| > Settings   | | line overlap   [====O---------]  0.50           |         |
| ------------ | | file overlap   [==O-----------]  0.30           |         |
| [+] Add repo | | coupling       [=O------------]  0.20           |         |
|              | |                                                 |         |
| ------------ | | sum = 1.00   (ok)                               |         |
| Docs   ?     | | (!) weights must sum to 1.00                    |         |
| Logout       | |                                                 |         |
|              | |            [ Reset defaults ]   [ Save ]        |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
|              | +- RISK THRESHOLDS -------------------------------+         |
|              | | high  >= [0.50]   med >= [0.20]   else low      |         |
|              | | [x] fail CI check when risk >= high             |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
|              | +- CACHE -----------------------------------------+         |
|              | | coupling cache   4 repos / 2.1 MB               |         |
|              | | [x] reuse cache when history unchanged          |         |
|              | |                          [ Clear cache ]        |         |
|              | +-------------------------------------------------+         |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

---

## Cross-Cutting Notes

**Consistency.** The risk vocabulary is identical across every surface — the CLI
table, the PR comment, and all six screens use the same three bands (high ≥ 0.50,
medium ≥ 0.20, low below) and the same explanation strings generated by the
scoring engine. A user who learns to read one output can read all of them.

**Accessibility.** Risk level is never encoded by colour alone: every score
appears as a number, a magnitude bar, and a text band. The coupling matrix uses
distinct density glyphs rather than a colour ramp for the same reason. All
interactive elements are keyboard reachable, and the master–detail screens
support arrow-key traversal of the list.

**Loading and empty states.** Every screen that depends on analysis has a defined
empty state (screen 3) or in-progress state (screens 3, and the Sync action on
screen 2). First-scan latency on a large repository is surfaced with determinate
progress, not an indeterminate spinner.

**Open questions for the next design iteration**
1. Does the co-change matrix stay legible beyond ~30 files, or does it need
   clustering / a top-N view by default?
2. Should **Dismiss** on a branch pair be permanent, or expire when either branch
   receives new commits?
3. Are per-repository settings sufficient, or is an organisation-level default
   needed once a team connects many repositories?
4. Should the dashboard show a trend line for risk over time — this depends on
   C2 (conflict trend analytics), also currently deferred.
