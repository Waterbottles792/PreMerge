# PreMerge — Dashboard Screen Specification

**Screen:** Dashboard (`Desktop / 02 Dashboard`)
**Canvas:** 1440 × 1024, desktop
**Fidelity:** Low-fidelity wireframe + exact Figma reconstruction values
**Foundations:** all tokens, type styles and components referenced here are
defined in [figma-spec.md](figma-spec.md) Parts 1–2. This document is the deep
specification for a single screen and supersedes §Screen 2 of that file.
**Status:** proposed component — **C1** in [MoSCoW.md](MoSCoW.md)

---

## 1. Purpose

The Dashboard answers one question on open: **"Is anything about to collide?"**

Everything is arranged in decreasing urgency — a scan-in-two-seconds summary,
then the ranked risk detail, then history. The **Analyze Repository** action is
placed top-right in the page header because it is the one thing a user comes to
*do* rather than *read*.

---

## 2. Layout Regions

| Region | X | Y | W | H | Behaviour |
|---|---|---|---|---|---|
| Frame | 0 | 0 | 1440 | 1024 | Fill `bg/canvas` |
| **Header** | 0 | 0 | 1440 | 64 | Fixed on scroll |
| **Sidebar** | 0 | 64 | 240 | 960 | Fixed on scroll |
| **Main content** | 240 | 64 | 1200 | 960 | 32px padding → content box X 272, W 1136 |

**Content origin X = 272 · content right edge X = 1408 · total content height 1008 — fits without scrolling.**

Vertical rhythm: page header → 32 → stat cards → 32 → risk overview → 32 → recent analyses.

---

## 3. Low-Fidelity Wireframe

```
+----------------------------------------------------------------------------+
| [PM] PreMerge     repo: acme/payments  v      [?]  [ user v ]              |
+--------------+-------------------------------------------------------------+
|              |                                                             |
| NAVIGATION   | Dashboard                       [ Analyze Repository ]      |
| ------------ | Conflict risk across 4 connected repositories               |
| > Dashboard  |                                                             |
|   Repos      | +---------+ +---------+ +---------+ +---------+             |
|   Risk       | |REPOS    | |BRANCHES | |HIGH RISK| |AVG RISK |             |
|   Coupling   | |   04    | |   17    | |   03    | |  0.34   |             |
|   Settings   | |connected| | active  | | pairs   | |all pairs|             |
| ------------ | +---------+ +---------+ +---------+ +---------+             |
| [+] Add repo |                                                             |
|              | +- RISK OVERVIEW --------------------[View all >]-+         |
|              | | 8 branch pairs    HIGH 3   MED 2   LOW 3        |         |
|              | | [######|####|##############]                    |         |
|              | | ----------------------------------------------- |         |
|              | | BRANCH A   BRANCH B   RISK          WHY         |         |
|              | | feature-a  feature-b  [####--] .80  same lines >|         |
|              | | feature-a  hotfix-x   [###---] .55  same file  >|         |
|              | | feature-c  feature-b  [#-----] .20  coupling   >|         |
|              | +-------------------------------------------------+         |
| ------------ |                                                             |
| Docs & Help  | +- RECENT ANALYSES ------------------[View log >]-+         |
| Sign out     | | WHEN    REPO / PAIR            RESULT           |         |
|              | | ----------------------------------------------- |         |
|              | | 2m ago  payments  a <> b       0.80  HIGH      >|         |
|              | | 1h ago  web-app   PR #42       0.15  LOW       >|         |
|              | | 3h ago  infra     main <> ops  0.55  HIGH      >|         |
|              | +-------------------------------------------------+         |
|              |                                                             |
+--------------+-------------------------------------------------------------+
```

**Notation:** `[ Label ]` button · `Label v` dropdown · `[####--]` magnitude bar
· `>` drill-down · `> Item` active nav.

---

## 4. Header — `Header / Global` (1440 × 64)

Fill `bg/surface`, 1px bottom border `border/default`.

| # | Element | X | Y | W | H | Content / Style |
|---|---|---|---|---|---|---|
| H1 | Logo mark | 24 | 20 | 24 | 24 | Product glyph, `brand/primary` |
| H2 | Wordmark | 56 | 18 | 92 | 28 | `PreMerge` — Inter 20/28, 600 |
| H3 | Repo switcher (Select) | 320 | 12 | 280 | 40 | `acme/payments` — `Mono/Default`, chevron 16×16 right |
| H4 | Help icon button | 1288 | 12 | 40 | 40 | Ghost, `?` icon 20×20 |
| H5 | Account menu | 1336 | 12 | 80 | 40 | Avatar 28×28 `radius/full` + chevron 16×16 |

Auto Layout: horizontal, `space-between`, padding `0 24`. Constraints Left+Right, Top.

---

## 5. Sidebar — `Sidebar / Global` (240 × 960 at Y 64)

Fill `bg/surface`, 1px right border `border/default`.

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| S1 | Group label | 24 | 88 | 192 | 16 | `NAVIGATION` — `Label/Overline`, `text/tertiary` |
| S2 | Nav item — **active** | 12 | 112 | 216 | 40 | `Dashboard` |
| S3 | Nav item | 12 | 156 | 216 | 40 | `Repositories` |
| S4 | Nav item | 12 | 200 | 216 | 40 | `Risk Report` |
| S5 | Nav item | 12 | 244 | 216 | 40 | `Coupling` |
| S6 | Nav item | 12 | 288 | 216 | 40 | `Settings` |
| S7 | Divider | 12 | 344 | 216 | 1 | `border/default` |
| S8 | Button / Secondary sm | 12 | 361 | 216 | 32 | `+ Add repository` |
| S9 | Divider | 12 | 908 | 216 | 1 | `border/default` |
| S10 | Nav item | 12 | 925 | 216 | 40 | `Docs & Help` |
| S11 | Nav item | 12 | 969 | 216 | 40 | `Sign out` |

**Nav item** — W 216, H 40, `radius/md`, padding `0 12`, gap 12, icon 20×20.
Active (S2): fill `brand/subtle`, text `brand/primary` `Body/Strong`.
Default: transparent, `text/secondary`. Hover: fill `bg/subtle`.

Auto Layout: vertical, gap 4, padding 12. Bottom cluster (S9–S11) in its own
frame pinned Bottom.

---

## 6. Section A — Page Header

| # | Element | X | Y | W | H | Content / Style |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 500 | 36 | `Dashboard` — `Display/Page`, `text/primary` |
| A2 | Subtitle | 272 | 136 | 600 | 20 | `Conflict risk across 4 connected repositories` — `Body/Default`, `text/secondary` |
| A3 | **Analyze Repository** | 1212 | 104 | 196 | 40 | **Button / Primary md** |

**A3 — the screen's primary call to action.**

| Property | Value |
|---|---|
| Component | `Button / Primary / md` |
| Fill | `brand/primary` · Hover `brand/hover` |
| Radius | `radius/md` |
| Padding | `0 16`, gap 8, centred |
| Icon | 20×20 scan/play glyph, `#FFFFFF`, leading |
| Label | `Analyze Repository` — `Body/Strong`, `#FFFFFF` |
| Right edge | X 1408 — flush with the content grid |

**States:** Default · Hover · Pressed · **Loading** (spinner 16×16 replaces icon,
label `Analyzing…`, button disabled) · Disabled (no repositories connected, 40% opacity)

**On click:** opens the *Analyze repository* modal (§10).

---

## 7. Section B — Statistics Cards

Four `Card / Stat` tiles, **272 × 120**, gap 16, at Y 184.
Each tile = 3 grid columns (80 × 3 + 16 × 2 = 272).

| # | X | Label | Value | Caption |
|---|---|---|---|---|
| B1 | 272 | `REPOSITORIES` | `4` | `connected` |
| B2 | 560 | `ACTIVE BRANCHES` | `17` | `across all repos` |
| B3 | 848 | `HIGH RISK PAIRS` | `3` | `risk ≥ 0.50` |
| B4 | 1136 | `AVERAGE RISK` | `0.34` | `across 8 pairs` |

**Tile internals** (offsets from tile origin; padding 20):

| Element | Offset Y | H | Style |
|---|---|---|---|
| Label | +20 | 16 | `Label/Overline`, `text/secondary` |
| Value | +44 | 40 | Inter 32/40, 700, `text/primary` |
| Caption | +92 | 16 | `Body/Small`, `text/tertiary` |

**Absolute Y for all four:** label 204 · value 228 · caption 276. Tiles end Y 304.

**Semantic treatment:**
- **B3** value in `risk/high`; a 8×8 `risk/high` dot sits 8px left of the label.
- **B4** value uses `Mono/ScoreLarge` — it is a score, and scores are always mono.
- B1, B2 values in `text/primary` — counts, not judgements.

**Card style:** fill `bg/surface`, 1px `border/default`, `radius/lg`, `shadow/sm`.
Auto Layout vertical, `Fill container` width within a 4-across horizontal frame, gap 16.

---

## 8. Section C — Risk Overview

`Card / Risk overview` — **X 272, Y 336, 1136 × 360**. Padding 0 (full-bleed table).

### C1 — Card header (Y 336, H 64)

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Title | 296 | 356 | 300 | 24 | `Risk overview` — `Heading/Card` |
| Link | 1284 | 358 | 100 | 20 | `View all →` — `Body/Strong`, `brand/primary`, right-aligned to 1384 |

### C2 — Distribution strip (Y 400, H 80)

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Caption | 296 | 408 | 400 | 16 | `8 branch pairs analysed against main` — `Body/Small`, `text/tertiary` |
| Count chip — high | 296 | 432 | 112 | 24 | dot 8×8 `risk/high` + `HIGH` (`Label/Overline`) + `3` (`Mono/Score`) |
| Count chip — med | 416 | 432 | 112 | 24 | dot `risk/med` + `MED` + `2` |
| Count chip — low | 536 | 432 | 112 | 24 | dot `risk/low` + `LOW` + `3` |
| **Distribution bar** | 296 | 468 | 1088 | 8 | Stacked, `radius/full` |

**Distribution bar segments** — widths proportional to counts, 2px gap between segments:

| Segment | Fill | Share | W |
|---|---|---|---|
| High | `risk/high` | 3 / 8 | 406 |
| Medium | `risk/med` | 2 / 8 | 270 |
| Low | `risk/low` | 3 / 8 | 406 |

(406 + 2 + 270 + 2 + 406 = 1086, plus rounding = 1088.)

> The bar carries no information the three count chips don't already state in
> text — it is a redundant encoding, deliberately. Colour alone never conveys a
> value on this screen.

### C3 — Table (header Y 480 H 40; rows Y 520 / 572 / 624, H 52 each)

**Columns** — inner width 1088 starting X 296:

| Col | X | W | Align | Header (`Label/Overline`) | Cell style |
|---|---|---|---|---|---|
| 1 | 296 | 220 | left | `BRANCH A` | `Mono/Default`, `text/primary` |
| 2 | 516 | 220 | left | `BRANCH B` | `Mono/Default`, `text/primary` |
| 3 | 736 | 180 | left | `RISK` | **Risk Badge** component |
| 4 | 916 | 428 | left | `WHY` | `Body/Default`, `text/secondary`, truncate to 1 line |
| 5 | 1344 | 40 | centre | — | Chevron `›` 16×16, `text/tertiary` |

Header row fill `bg/subtle`. Body rows: 1px bottom border `border/default`;
hover fill `bg/subtle`; cell padding `0 16`.

**Risk Badge** (from [figma-spec.md](figma-spec.md) §2.4) — always three parts:
bar 64×8 (fill = score × 64) + score `Mono/Score` 2dp + band label `Label/Overline`.

**Row data — use verbatim:**

| Branch A | Branch B | Risk | Why |
|---|---|---|---|
| `feature-a` | `feature-b` | `0.80` HIGH | auth.py — both branches edit overlapping lines |
| `feature-a` | `hotfix-x` | `0.55` HIGH | config.py — both branches touch this file |
| `feature-c` | `feature-b` | `0.20` MED | auth.py ↔ session.py — historically change together |

Only the top 3 of 8 appear; `View all →` reaches the rest. Card ends Y 696.

---

## 9. Section D — Recent Analyses

`Card / Recent analyses` — **X 272, Y 728, 1136 × 280**. Padding 0.

### D1 — Card header (Y 728, H 64)

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Title | 296 | 748 | 300 | 24 | `Recent analyses` — `Heading/Card` |
| Link | 1284 | 750 | 100 | 20 | `View log →` — `brand/primary`, right-aligned to 1384 |

### D2 — Table (header Y 792 H 40; rows Y 832 / 884 / 936, H 52 each)

**Columns** — inner width 1088 starting X 296:

| Col | X | W | Align | Header | Cell style |
|---|---|---|---|---|---|
| 1 | 296 | 140 | left | `WHEN` | `Body/Small`, `text/tertiary` |
| 2 | 436 | 220 | left | `REPOSITORY` | `Body/Default`, `text/primary` |
| 3 | 656 | 440 | left | `COMPARISON` | `Mono/Default`, `text/secondary` |
| 4 | 1096 | 248 | right | `RESULT` | **Risk Badge**, compact variant |
| 5 | 1344 | 40 | centre | — | Chevron `›` |

**Compact Risk Badge** for column 4: bar 48×6 + score + band label, right-aligned.

**Row data:**

| When | Repository | Comparison | Result |
|---|---|---|---|
| `2m ago` | acme/payments | `feature-a ↔ feature-b` | `0.80` HIGH |
| `1h ago` | acme/web-app | `PR #42 → main` | `0.15` LOW |
| `3h ago` | acme/infra | `main ↔ ops-refactor` | `0.55` HIGH |

Card ends Y 1008. **Total content height 1008 — no scroll at 1024.**

---

## 10. Analyze Repository Modal

Triggered by A3. Overlay `#101828` @ 40% across the full frame.

**Modal:** X 440, Y 312, **560 × 400**, fill `bg/surface`, `radius/lg`,
`shadow/md`, padding 24.

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| M1 | Title | 464 | 336 | 400 | 28 | `Analyze repository` — `Heading/Section` |
| M2 | Close icon button | 936 | 332 | 40 | 40 | Ghost, `×` 20×20 |
| M3 | Field label | 464 | 388 | 512 | 20 | `Repository` — `Body/Strong` |
| M4 | Select | 464 | 412 | 512 | 40 | `acme/payments` |
| M5 | Field label | 464 | 472 | 512 | 20 | `Compare` — `Body/Strong` |
| M6 | Radio group | 464 | 496 | 512 | 72 | `All branch pairs` (selected) · `All branches against a base` · `A specific pair` |
| M7 | Select | 464 | 584 | 512 | 40 | `Base: main` — shown only for options 2 and 3 |
| M8 | Checkbox + label | 464 | 640 | 512 | 20 | `Rebuild coupling cache` — unchecked |
| M9 | Helper | 488 | 664 | 488 | 16 | `Slower, but required after a history rewrite.` — `Body/Small`, `text/tertiary` |
| M10 | Button / Secondary md | 760 | 672 | 96 | 40 | `Cancel` |
| M11 | Button / Primary md | 868 | 672 | 108 | 40 | `Analyze` |

**On submit:** modal closes, A3 enters Loading state, and Section C shows the
loading variant (§11).

---

## 11. States & Variants

Draw each as a separate frame.

### `Desktop / 02 Dashboard` — Default
As specified above.

### `Desktop / 02 Dashboard — Loading`
- A3 in Loading state (`Analyzing…`, spinner, disabled)
- Section C table replaced by **3 skeleton rows**, H 52: grey bars `bg/subtle`,
  `radius/sm`, widths 180 / 180 / 140 / 380 at the column X positions
- Stat card values replaced by skeleton bars 80 × 32
- Section D unchanged — history is still valid during a new run

### `Desktop / 02 Dashboard — Empty`
For a user with no repositories connected.
- Stat cards show `—` in place of values, `text/tertiary`
- Sections C and D replaced by a single **empty-state card**, X 272, Y 336, 1136 × 320:

| Element | Y | Content |
|---|---|---|
| Illustration placeholder | 384 | 64 × 64, `bg/subtle`, `radius/lg`, centred |
| Heading | 472 | `No analyses yet` — `Heading/Section`, centred |
| Body | 504 | `Connect a repository to start predicting merge conflicts before they happen.` — `Body/Default`, `text/secondary`, centred, max-width 480 |
| Button / Primary md | 552 | 196 × 40 — `Analyze Repository`, centred |

### `Desktop / 02 Dashboard — All clear`
No pairs above 0.20.
- B3 value `0`, in `risk/low` rather than `risk/high`
- C2 distribution bar entirely `risk/low`
- C3 shows one row: `No branch pairs are at risk.` (`Body/Default`, `text/secondary`, centred across the full 1088 inner width, H 52)

---

## 12. Interactions

| Trigger | Action |
|---|---|
| **Analyze Repository** (A3) | Open modal §10 → on submit, Loading variant |
| Stat card B3 | → `Desktop / 04 Risk Report`, filtered to risk ≥ 0.50 |
| Section C row | → `Desktop / 04 Risk Report`, that pair pre-selected |
| Section C `View all →` | → `Desktop / 04 Risk Report`, unfiltered |
| Section D row | → `Desktop / 04 Risk Report`, that historical run restored |
| Section D `View log →` | → analysis log (out of scope) |
| Header repo switcher | Re-scopes all four sections; no navigation |
| Sidebar items | → corresponding screen |
| Row hover | Fill `bg/subtle`, chevron `text/secondary` |
| Keyboard | Tab order A3 → stat cards → C rows → D rows; ↑/↓ traverse rows; Enter opens |

---

## 13. Figma Build Order

1. **Foundations** — colour variables (Light + Dark), type styles, 12-col grid (16 gutter / 32 margin) on the Main frame
2. **Components** — Button, Select, Nav item, Card, Table row, **Risk Badge**
3. **Shell** — Header + Sidebar as one `Shell / Desktop` component with the Dashboard nav item active
4. **Section B** — build one stat tile, componentise with `label` / `value` / `caption` / `tone` properties, instance ×4 in a horizontal Auto Layout frame (gap 16)
5. **Section C** — header → distribution strip → table; rows are instances of `Table row / Risk`
6. **Section D** — reuse `Table row`, swap the column set
7. **Modal** §10
8. **Variants** — Loading, Empty, All clear
9. **Prototype** — wire §12

### Auto Layout summary

| Frame | Direction | Gap | Padding | Sizing |
|---|---|---|---|---|
| Main content | Vertical | 32 | 32 | Fill × Hug |
| Page header (A) | Horizontal | — | 0 | Fill, `space-between`, items top-aligned |
| Stat row (B) | Horizontal | 16 | 0 | Fill; children Fill equally |
| Card (C, D) | Vertical | 0 | 0 | Fill × Hug |
| Table row | Horizontal | 0 | `0 16` | Fill; only the `WHY` column set to Fill, all others fixed |

---

## 14. Acceptance Checklist

- [ ] Frame is exactly 1440 × 1024; content spans X 272–1408
- [ ] Header 64h and sidebar 240w are fixed on scroll
- [ ] All four stat cards are 272 × 120 with 16px gaps, ending at X 1408
- [ ] **Analyze Repository** is the only Primary button on the screen
- [ ] Every risk value shows number **and** bar **and** band label
- [ ] Section C and D tables share identical row height (52) and header height (40)
- [ ] Total content height 1008 — nothing clipped at 1024
- [ ] Loading, Empty and All-clear variants drawn
- [ ] Every colour is a variable; dark mode verified
- [ ] Risk vocabulary matches the CLI exactly: HIGH ≥ 0.50, MED ≥ 0.20, LOW below
