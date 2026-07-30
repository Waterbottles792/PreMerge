# PreMerge — Figma-Ready UI Specification

**Component:** PreMerge Web Dashboard (proposed — **C1** in [MoSCoW.md](MoSCoW.md))
**Source:** derived from [wireframes.md](wireframes.md)
**Target:** Desktop **1440 × 1024**
**Fidelity:** High — exact frames, coordinates, sizes, tokens and labels. Every
value below is directly enterable in Figma.
**Built file:** [Conflict Risk Dashboard](https://www.figma.com/design/CeB8cRjy4jC3VaYn2FjIk2/Conflict-Risk-Dashboard?node-id=0-1&p=f&t=ZHQxA9wcZdzwtEkJ-0)

All coordinates are **absolute within the 1440 × 1024 frame**, matching what
Figma's X/Y inspector displays. Sizes are `width × height` in px.

---

# PART 1 — FOUNDATIONS

## 1.1 Frame & Layout Shell

Every authenticated screen uses one shell. Build it once as a component, then
place per-screen content into the Main region.

| Region | X | Y | W | H | Notes |
|---|---|---|---|---|---|
| **Frame** | 0 | 0 | 1440 | 1024 | Page background `bg/canvas` |
| **Header** | 0 | 0 | 1440 | 64 | Fixed on scroll |
| **Sidebar** | 0 | 64 | 240 | 960 | Fixed on scroll |
| **Main** | 240 | 64 | 1200 | 960 | Vertical scroll |
| **Main content box** | 272 | 96 | 1136 | — | Main inset by 32px padding |

**Content origin is X = 272.** Content right edge is X = 1408.

## 1.2 Layout Grid

Apply to the Main region in Figma (Layout Grid → Columns):

| Property | Value |
|---|---|
| Type | Columns, Stretch |
| Count | 12 |
| Gutter | 16 |
| Margin | 32 |
| Column width | 80 (computed: (1136 − 11×16) ÷ 12) |

**Useful column spans:** 3 cols = 272 · 4 cols = 368 · 6 cols = 560 · 8 cols = 752 · 12 cols = 1136

## 1.3 Spacing Scale

Base unit **4px**. Use only these values:

`4` `8` `12` `16` `24` `32` `48` `64`

| Token | Value | Used for |
|---|---|---|
| `space/xs` | 4 | Icon-to-label gap |
| `space/sm` | 8 | Inside chips, tight stacks |
| `space/md` | 12 | Form label to input |
| `space/lg` | 16 | Card grid gutter, button gaps |
| `space/xl` | 24 | Card internal padding |
| `space/2xl` | 32 | Section-to-section vertical rhythm |
| `space/3xl` | 48 | Page header to first section |

## 1.4 Type Scale

Primary typeface **Inter**. Monospace **JetBrains Mono** — used *only* for
branch names, file paths, commit SHAs and numeric scores, so git identifiers are
always visually distinct from UI chrome.

| Style name | Font | Size / Line | Weight | Letter-spacing | Used for |
|---|---|---|---|---|---|
| `Display/Page` | Inter | 28 / 36 | 600 | −0.2 | Page titles |
| `Heading/Section` | Inter | 20 / 28 | 600 | −0.1 | Section headings |
| `Heading/Card` | Inter | 16 / 24 | 600 | 0 | Card titles |
| `Label/Overline` | Inter | 12 / 16 | 600 | +0.6, UPPERCASE | Table headers, sidebar group label |
| `Body/Default` | Inter | 14 / 20 | 400 | 0 | Body copy, table cells |
| `Body/Strong` | Inter | 14 / 20 | 500 | 0 | Emphasised cells, button labels |
| `Body/Small` | Inter | 12 / 16 | 400 | 0 | Captions, helper text, timestamps |
| `Mono/Default` | JetBrains Mono | 13 / 20 | 400 | 0 | Branch names, file paths, SHAs |
| `Mono/Score` | JetBrains Mono | 16 / 24 | 600 | 0 | Risk scores in tables |
| `Mono/ScoreLarge` | JetBrains Mono | 32 / 40 | 700 | 0 | Headline score, screen 4 |

## 1.5 Colour Tokens

Define as Figma variables with **Light** and **Dark** modes so both themes are
one toggle apart.

**Neutrals**

| Token | Light | Dark |
|---|---|---|
| `bg/canvas` | `#F7F8FA` | `#0C111D` |
| `bg/surface` | `#FFFFFF` | `#161B26` |
| `bg/subtle` | `#F2F4F7` | `#1F242F` |
| `border/default` | `#E4E7EC` | `#333741` |
| `border/strong` | `#D0D5DD` | `#4A4F5A` |
| `text/primary` | `#101828` | `#F5F5F6` |
| `text/secondary` | `#475467` | `#94969C` |
| `text/tertiary` | `#98A2B3` | `#85888E` |

**Brand & semantic**

| Token | Light | Dark | Meaning |
|---|---|---|---|
| `brand/primary` | `#4F46E5` | `#7A75F0` | Primary actions |
| `brand/hover` | `#4338CA` | `#8F8BF3` | Primary hover |
| `brand/subtle` | `#EEF2FF` | `#2A2A5A` | Selected row background |
| `risk/high` | `#D92D20` | `#F97066` | Risk ≥ 0.50 |
| `risk/high-bg` | `#FEF3F2` | `#3B1614` | — |
| `risk/med` | `#DC6803` | `#FDB022` | Risk ≥ 0.20 |
| `risk/med-bg` | `#FFFAEB` | `#3B2411` | — |
| `risk/low` | `#079455` | `#47CD89` | Risk < 0.20 |
| `risk/low-bg` | `#ECFDF3` | `#0F2F1E` | — |

> **Accessibility rule — non-negotiable.** Risk level is *never* encoded by
> colour alone. Every risk value renders as **numeric score + magnitude bar +
> text band label** (HIGH / MED / LOW). This is specified in every component
> below and must survive design review.

## 1.6 Radius, Border, Elevation

| Token | Value |
|---|---|
| `radius/sm` | 4 — chips, badges, bars |
| `radius/md` | 6 — buttons, inputs, selects |
| `radius/lg` | 8 — cards, panels |
| `radius/full` | 999 — avatar, toggle |
| `border/width` | 1 |
| `shadow/sm` | Y 1, Blur 2, `#101828` @ 5% |
| `shadow/md` | Y 4, Blur 8, `#101828` @ 8% — dropdowns, modals |

---

# PART 2 — COMPONENT LIBRARY

Build these as Figma components with variants before laying out screens.

## 2.1 Button

Auto Layout: horizontal, padding `0 16`, gap 8, centre-aligned.

| Variant property | Values |
|---|---|
| `type` | Primary · Secondary · Ghost · Danger |
| `size` | md (H 40) · sm (H 32) |
| `state` | Default · Hover · Pressed · Disabled |

| Type | Fill | Border | Text |
|---|---|---|---|
| Primary | `brand/primary` | none | `#FFFFFF`, `Body/Strong` |
| Secondary | `bg/surface` | 1px `border/strong` | `text/primary` |
| Ghost | transparent | none | `text/secondary` |
| Danger | `bg/surface` | 1px `risk/high` | `risk/high` |

Radius `radius/md`. Disabled = 40% opacity, no pointer.

## 2.2 Input / Select

| Property | Value |
|---|---|
| Height | 40 |
| Padding | `0 12` |
| Border | 1px `border/default`; focus → 1px `brand/primary` + 3px `brand/subtle` ring |
| Radius | `radius/md` |
| Placeholder | `Body/Default`, `text/tertiary` |
| Select chevron | 16×16, `text/secondary`, right-aligned, 12px inset |

## 2.3 Toggle, Checkbox, Slider

| Component | Spec |
|---|---|
| **Toggle** | Track 36×20, `radius/full`. Off `border/strong` fill; On `brand/primary`. Knob 16×16 white, 2px inset. |
| **Checkbox** | 16×16, `radius/sm`, 1px `border/strong`. Checked → `brand/primary` fill + white tick. |
| **Slider** | Track 4h, `radius/full`, `bg/subtle`. Filled portion `brand/primary`. Handle 16×16 circle, white, 1px `border/strong`, `shadow/sm`. |

## 2.4 Risk Badge

The single most reused component. Auto Layout horizontal, gap 8, H 24.

Composed of three parts, always all three:

1. **Bar** — 64 × 8, `radius/full`, track `bg/subtle`, fill = score × 64px
2. **Score** — `Mono/Score`, 2dp, e.g. `0.80`
3. **Band label** — `Label/Overline`, e.g. `HIGH`

| Variant `level` | Bar fill | Text | Band label |
|---|---|---|---|
| high | `risk/high` | `risk/high` | `HIGH` |
| med | `risk/med` | `risk/med` | `MED` |
| low | `risk/low` | `risk/low` | `LOW` |

## 2.5 Card

| Property | Value |
|---|---|
| Fill | `bg/surface` |
| Border | 1px `border/default` |
| Radius | `radius/lg` |
| Shadow | `shadow/sm` |
| Padding | 24 (header/body), 0 for full-bleed tables |
| Header | H 64, title `Heading/Card`, optional right-aligned action |

## 2.6 Table

| Element | Spec |
|---|---|
| Header row | H 40, fill `bg/subtle`, text `Label/Overline` / `text/secondary` |
| Body row | H 52 (H 64 on screen 3), 1px bottom border `border/default` |
| Row hover | fill `bg/subtle` |
| Row selected | fill `brand/subtle`, 2px left bar `brand/primary` |
| Cell padding | `0 16` |
| Chevron column | fixed 40 wide, icon 16×16 `text/tertiary` |

## 2.7 Chip / Filter Tab

H 32, padding `0 12`, radius `radius/sm`, `Body/Default`.
Default: `bg/surface` + 1px `border/default`. Active: `brand/subtle` fill, `brand/primary` text + border.

## 2.8 Nav Item (Sidebar)

W 216, H 40, radius `radius/md`, padding `0 12`, gap 12, icon 20×20.

| State | Fill | Text |
|---|---|---|
| Default | transparent | `text/secondary` |
| Hover | `bg/subtle` | `text/primary` |
| Active | `brand/subtle` | `brand/primary`, `Body/Strong` |

---

# PART 3 — SHELL SPECIFICATION

## 3.1 Header — `Header / Global` (1440 × 64)

Fill `bg/surface`, 1px bottom border `border/default`.

| # | Element | X | Y | W | H | Content / Style |
|---|---|---|---|---|---|---|
| 1 | Logo mark | 24 | 20 | 24 | 24 | Product glyph |
| 2 | Wordmark | 56 | 18 | 92 | 28 | `PreMerge` — Inter 20/28, 600 |
| 3 | Repo switcher (Select) | 320 | 12 | 280 | 40 | Label `acme/payments`, `Mono/Default` |
| 4 | Help icon button | 1288 | 12 | 40 | 40 | Ghost, `?` icon 20×20 |
| 5 | Account menu | 1336 | 12 | 80 | 40 | Avatar 28×28 (`radius/full`) + chevron 16 |

## 3.2 Sidebar — `Sidebar / Global` (240 × 960, at Y 64)

Fill `bg/surface`, 1px right border `border/default`.

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| 1 | Group label | 24 | 88 | 192 | 16 | `NAVIGATION` — `Label/Overline`, `text/tertiary` |
| 2 | Nav item | 12 | 112 | 216 | 40 | Dashboard |
| 3 | Nav item | 12 | 156 | 216 | 40 | Repositories |
| 4 | Nav item | 12 | 200 | 216 | 40 | Risk Report |
| 5 | Nav item | 12 | 244 | 216 | 40 | Coupling |
| 6 | Nav item | 12 | 288 | 216 | 40 | Settings |
| 7 | Divider | 12 | 344 | 216 | 1 | `border/default` |
| 8 | Button / Secondary sm | 12 | 361 | 216 | 32 | `+ Add repository` |
| 9 | Divider | 12 | 908 | 216 | 1 | `border/default` |
| 10 | Nav item | 12 | 925 | 216 | 40 | Docs & Help |
| 11 | Nav item | 12 | 969 | 216 | 40 | Sign out |

Set the **active** nav item per screen: Dashboard (S2), Repositories (S3),
Risk Report (S4), Coupling (S5), Settings (S6).

---

# PART 4 — SCREEN SPECIFICATIONS

---

## SCREEN 1 — Login

**Frame:** `Desktop / 01 Login` — 1440 × 1024. **No header, no sidebar.**
Fill `bg/canvas`.

### Card — `Auth / Sign in card`

| Property | Value |
|---|---|
| X / Y | 500 / 176 |
| Size | 440 × 672 |
| Fill | `bg/surface`, 1px `border/default`, `radius/lg`, `shadow/md` |
| Auto Layout | Vertical, padding 40, gap 24, fill-width children |

### Card contents (top to bottom, Y absolute)

| # | Element | X | Y | W | H | Content / Style |
|---|---|---|---|---|---|---|
| 1 | Logo mark | 692 | 216 | 56 | 56 | Centred |
| 2 | Title | 540 | 288 | 360 | 36 | `PreMerge` — `Display/Page`, centred |
| 3 | Subtitle | 540 | 328 | 360 | 40 | `Predict merge conflicts before they happen.` — `Body/Default`, `text/secondary`, centred |
| 4 | **Button / Primary md** | 540 | 400 | 360 | 40 | `Sign in with GitHub` + GitHub icon 20×20 |
| 5 | Divider + label | 540 | 464 | 360 | 20 | Rule `border/default` either side of `or` — `Body/Small`, `text/tertiary` |
| 6 | Field label | 540 | 508 | 360 | 20 | `Email` — `Body/Strong` |
| 7 | Input | 540 | 532 | 360 | 40 | Placeholder `you@company.com` |
| 8 | Field label | 540 | 588 | 360 | 20 | `Password` — `Body/Strong` |
| 9 | Input | 540 | 612 | 360 | 40 | Type: password, trailing show/hide icon |
| 10 | Checkbox + label | 540 | 668 | 180 | 20 | `Remember me` |
| 11 | Link | 780 | 668 | 120 | 20 | `Forgot password?` — `brand/primary`, right-aligned |
| 12 | **Button / Secondary md** | 540 | 708 | 360 | 40 | `Sign in` |
| 13 | Error region | 540 | 764 | 360 | 40 | `risk/high-bg` fill, 1px `risk/high`, `radius/md`. Reserved space — hidden by default so the layout never shifts. Text `Body/Small` / `risk/high` |
| 14 | Footer text + link | 500 | 872 | 440 | 20 | `New here? ` + `Create an account` — centred, below card |

### Variants to draw

- `state=Default` · `state=Error` (row 13 visible, inputs bordered `risk/high`) · `state=Loading` (button 4 shows spinner, label `Signing in…`, all inputs disabled)

### Prototype links
`Sign in with GitHub` → Screen 3 (first-time) · `Sign in` → Screen 2 · `Create an account` → Sign-up (out of scope)

---

## SCREEN 2 — Dashboard

> **Superseded.** A deeper, self-contained specification for this screen —
> including the Analyze Repository CTA, the risk-distribution strip, the Recent
> Analyses table, the analyze modal, and Loading / Empty / All-clear variants —
> lives in **[dashboard-spec.md](dashboard-spec.md)**. Build from that document;
> the section below is retained as the summary view.

**Frame:** `Desktop / 02 Dashboard` — shell + Main content. Sidebar active: **Dashboard**.

### Section A — Page header

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 400 | 36 | `Overview` — `Display/Page` |
| A2 | Sync timestamp | 1064 | 104 | 240 | 20 | `Last synced 2 minutes ago` — `Body/Small`, `text/tertiary`, right-aligned |
| A3 | **Button / Secondary md** | 1320 | 94 | 88 | 40 | `Sync` + refresh icon |

### Section B — Stat tiles (4 × `Card / Stat`, 272 × 120, gap 16)

| # | X | Y | Label (`Label/Overline`, `text/secondary`) | Value (Inter 32/40, 600) | Caption (`Body/Small`, `text/tertiary`) |
|---|---|---|---|---|---|
| B1 | 272 | 160 | `REPOSITORIES` | `4` | `connected` |
| B2 | 560 | 160 | `ACTIVE BRANCHES` | `17` | `across all repos` |
| B3 | 848 | 160 | `HIGH RISK PAIRS` | `3` | `risk ≥ 0.50` — value in `risk/high` |
| B4 | 1136 | 160 | `AVERAGE RISK` | `0.34` | `all pairs` — `Mono/ScoreLarge` |

Tile internals: padding 20; label Y+20, value Y+48, caption Y+92.

### Section C — `Card / Top risk branch pairs` (272, 312 — 1136 × 360)

| Element | Y | H | Detail |
|---|---|---|---|
| Card header | 312 | 64 | Title `Top risk branch pairs` (`Heading/Card`) at X 296; right: `View all →` link, `brand/primary`, ending X 1384 |
| Table header | 376 | 40 | Columns below |
| Rows 1–4 | 416 / 468 / 520 / 572 | 52 each | — |
| Card footer | 624 | 48 | `Showing 4 of 8 pairs` — `Body/Small`, `text/tertiary`, X 296 |

**Table columns** (inner width 1088, starting X 296):

| Col | X | W | Header label | Cell content |
|---|---|---|---|---|
| 1 | 296 | 220 | `BRANCH A` | `Mono/Default`, `text/primary` |
| 2 | 516 | 220 | `BRANCH B` | `Mono/Default`, `text/primary` |
| 3 | 736 | 180 | `RISK` | **Risk Badge** component |
| 4 | 916 | 428 | `WHY` | `Body/Default`, `text/secondary`, truncate 1 line with ellipsis |
| 5 | 1344 | 40 | — | Chevron `›` |

**Row data (use verbatim):**

| Branch A | Branch B | Risk | Why |
|---|---|---|---|
| `feature-a` | `feature-b` | 0.80 HIGH | auth.py — both branches edit overlapping lines |
| `feature-a` | `hotfix-x` | 0.55 HIGH | config.py — both branches touch this file |
| `feature-c` | `feature-b` | 0.20 MED | auth.py ↔ session.py — historically change together |
| `main` | `docs-fix` | 0.00 LOW | No overlap or coupling detected |

### Section D — Two cards side by side (Y 704, H 280)

**D1 — `Card / Coupling hotspots`** (272, 704 — 560 × 280)
Header `Coupling hotspots` + `Analyse →` link. Three rows, H 52:

| File A | File B | Coupling |
|---|---|---|
| `auth.py` | `session.py` | `1.00` |
| `api.py` | `routes.py` | `0.80` |
| `db.py` | `models.py` | `0.60` |

Columns within 512 inner: File A 190 · `↔` 24 · File B 190 · Score 108 (right-aligned, `Mono/Score`).

**D2 — `Card / Recent activity`** (848, 704 — 560 × 280)
Header `Recent activity` + `View log →` link. Three rows, H 52: icon 20×20 · description `Body/Default` · relative time `Body/Small` `text/tertiary` right-aligned.

| Description | Time |
|---|---|
| `Analysis run on PR #42` | `2m ago` |
| `Repository acme/payments synced` | `1h ago` |
| `Scoring weights updated` | `1d ago` |

**Total content height:** 984. Fits without scroll.

### Prototype links
Any Section C row → Screen 4 (that pair selected) · `View all →` → Screen 4 · `Analyse →` → Screen 5 · Stat tile B3 → Screen 4 filtered to high risk

---

## SCREEN 3 — Repository Selection

**Frame:** `Desktop / 03 Repositories`. Sidebar active: **Repositories**.

### Section A — Page header

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 400 | 36 | `Repositories` |
| A2 | **Button / Primary md** | 1236 | 94 | 172 | 40 | `+ Connect repository` |

### Section B — Toolbar

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| B1 | Search input | 272 | 160 | 400 | 40 | Leading search icon 16×16; placeholder `Search repositories…` |
| B2 | Select | 688 | 160 | 200 | 40 | `Organisation: All` |
| B3 | Chip (active) | 272 | 216 | 60 | 32 | `All` |
| B4 | Chip | 340 | 216 | 108 | 32 | `Connected` |
| B5 | Chip | 456 | 216 | 140 | 32 | `Not connected` |

### Section C — `Card / Repository list` (272, 272 — 1136 × 416, padding 0)

| Element | Y | H |
|---|---|---|
| Table header | 272 | 40 |
| Rows 1–5 | 312 / 376 / 440 / 504 / 568 | 64 each |
| Footer / pagination | 632 | 56 |

**Table columns** (inner 1088, starting X 296):

| Col | X | W | Header | Cell |
|---|---|---|---|---|
| 1 | 296 | 400 | `REPOSITORY` | Name `Body/Strong`; owner `Body/Small` `text/tertiary` beneath |
| 2 | 696 | 120 | `BRANCHES` | `Mono/Default`, right-aligned |
| 3 | 816 | 200 | `LAST SCAN` | `Body/Default`, `text/secondary` |
| 4 | 1016 | 180 | `STATUS` | **Toggle** 36×20 + label `On`/`Off` |
| 5 | 1196 | 148 | — | `View →` link, `brand/primary` |
| 6 | 1344 | 40 | — | Chevron |

**Row data:**

| Repository | Branches | Last scan | Status |
|---|---|---|---|
| `acme/payments` | 7 | 2 minutes ago | On |
| `acme/web-app` | 5 | 1 hour ago | On |
| `acme/infra` | 3 | 3 days ago | On |
| `acme/docs` | 2 | — | Off |
| `acme/legacy-api` | — | Scanning… | On |

**Row 5 — scanning state.** Replaces the Last-scan cell with a stacked
progress block: label `Building co-change matrix…` (`Body/Small`) at Y+12, and a
**progress bar** 320 × 6, `radius/full`, track `bg/subtle`, fill `brand/primary`
at 62%, at Y+36, with `62%` (`Mono/Default`) to its right.

> **Why determinate:** the first scan walks the full commit log. Real latency is
> shown as real progress, not an indeterminate spinner, so the user can connect
> other repositories while it runs.

**Footer:** `Showing 5 of 12 repositories` at X 296 (`Body/Small`, `text/tertiary`);
pagination cluster right-aligned ending X 1384 — `‹ Prev` · `1` `2` `3` (32×32 each, active = `brand/subtle`) · `Next ›`.

### Section D — `Card / Empty state` — **separate variant frame**

Draw as `Desktop / 03 Repositories — Empty`. Card at 272, 272 — 1136 × 280,
contents centred:

| Element | Y | Content |
|---|---|---|
| Illustration placeholder | 312 | 64 × 64, `bg/subtle`, `radius/lg` |
| Heading | 392 | `No repositories connected yet` — `Heading/Section` |
| Body | 424 | `Connect your GitHub account to start predicting merge conflicts.` — `Body/Default`, `text/secondary` |
| **Button / Primary md** | 468 | 220 × 40 — `Connect GitHub account` |

### Prototype links
Row / `View →` → Screen 2 scoped to that repo · Toggle On → same frame, row 5 scanning state · `Connect GitHub account` → GitHub App install (external)

---

## SCREEN 4 — Conflict Risk Report

**Frame:** `Desktop / 04 Risk Report`. Sidebar active: **Risk Report**.
**The core screen.** Master–detail; selecting a pair updates only the right panel.

### Section A — Page header

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 300 | 36 | `Risk Report` |
| A2 | Select | 1000 | 94 | 180 | 40 | `Base: main` |
| A3 | **Button / Secondary md** | 1188 | 94 | 100 | 40 | `Re-run` |
| A4 | **Button / Secondary md** | 1296 | 94 | 112 | 40 | `Export JSON` |

### Section B — `Panel / Pair list` (272, 160 — 368 × 800)

Card, padding 0.

| Element | Y | H | Detail |
|---|---|---|---|
| Panel header | 160 | 56 | `8 pairs` (`Body/Strong`) at X 288; `Sort: Risk ▾` select-as-text right-aligned ending X 624 |
| List items 1–4 | 216 / 296 / 376 / 456 | 80 each | — |
| `Load more` button | 880 | 40 | Ghost, full width inset 16 |

**List item internals** (368 wide, padding `12 16`):

| Element | Offset | Content |
|---|---|---|
| Branch A | Y+12 | `Mono/Default`, `text/primary` |
| Branch B | Y+32 | `↔ ` + `Mono/Default`, `text/secondary` |
| Risk badge | Y+52 | Compact variant — bar 48×6 + score only |
| Divider | bottom | 1px `border/default` |

Item 1 = **selected**: `brand/subtle` fill, 2px `brand/primary` left bar.

| # | Branch A | Branch B | Score |
|---|---|---|---|
| 1 | `feature-a` | `feature-b` | 0.80 |
| 2 | `feature-a` | `hotfix-x` | 0.55 |
| 3 | `feature-c` | `feature-b` | 0.20 |
| 4 | `main` | `docs-fix` | 0.00 |

### Section C — `Panel / Pair detail` (656, 160 — 752 × 800)

Card, padding 24. Content X starts 680, inner width 704.

**C1 — Pair heading** (Y 184, H 32)
`feature-a` `↔` `feature-b` — `Mono/Default` at 16px, `text/primary`.

**C2 — Headline score block** (Y 232, H 96)
Fill `risk/high-bg`, `radius/lg`, padding 20, full inner width 704.

| Element | X | Y | Content |
|---|---|---|---|
| Score | 700 | 252 | `0.80` — `Mono/ScoreLarge`, `risk/high` |
| Band pill | 800 | 262 | `HIGH RISK` — `Label/Overline`, `risk/high`, 1px border, H 24, padding `0 8` |
| Bar | 700 | 300 | 384 × 8, `radius/full`, track white, fill `risk/high` at 80% |
| Caption | 1100 | 296 | `Analysed 2 minutes ago` — `Body/Small`, `text/secondary`, right-aligned to 1384 |

**C3 — Score breakdown table** (Y 352, H 176)
Section label `SCORE BREAKDOWN` (`Label/Overline`) at Y 352.
Table starts Y 380 — header 32, rows 32, total row 40.

| Col | X | W | Align | Header |
|---|---|---|---|---|
| 1 | 680 | 320 | left | `SIGNAL` |
| 2 | 1000 | 128 | right | `WEIGHT` |
| 3 | 1128 | 128 | right | `SUB-SCORE` |
| 4 | 1256 | 128 | right | `CONTRIBUTION` |

| Signal | Weight | Sub-score | Contribution |
|---|---|---|---|
| Line overlap | 0.50 | 1.00 | 0.50 |
| File overlap | 0.30 | 1.00 | 0.30 |
| Historical coupling | 0.20 | 0.00 | 0.00 |
| **Total risk** | — | — | **0.80** |

Total row: top border 1px `border/strong`, `Body/Strong`, value `Mono/Score`.

> **Why this table exists.** A predictive tool that emits an unexplained number
> gets ignored the first time it is wrong. Showing the arithmetic makes the score
> auditable, and points a user who disagrees toward Settings rather than toward
> abandoning the tool. **Do not remove this in visual design.**

**C4 — Evidence list** (Y 560, H 216)
Section label `EVIDENCE` (`Label/Overline`) at Y 560. Two items, H 88, gap 12, starting Y 588.

Item layout: severity icon 20×20 at X 680 · content from X 712 · `View diff →` link right-aligned ending X 1384.

| # | Icon | File | Detail line |
|---|---|---|---|
| 1 | `risk/high` warning | `auth.py` (`Mono/Default`) | `Both branches edit overlapping lines (40–52 and 44–61)` |
| 2 | `text/tertiary` info | `config.py` (`Mono/Default`) | `Both branches touch this file, different lines` |

**C5 — Footer** (Y 800, H 96)
Top border 1px `border/default` at Y 800.

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Merge-base | 680 | 820 | 300 | 20 | `Merge base: a1b2c3d` — `Mono/Default`, `text/secondary` |
| **Button / Secondary md** | 1152 | 900 | 112 | 40 | `Dismiss` |
| **Button / Primary md** | 1276 | 900 | 132 | 40 | `Open PR →` |

### Variants to draw
`level=high` (above) · `level=low` — C2 uses `risk/low-bg` / `risk/low`, C4 replaced by an empty state: `No overlapping files or coupled pairs found.` (`Body/Default`, `text/secondary`, centred, H 88)

### Prototype links
List item → same frame, detail swapped · `View diff →` → diff view (out of scope) · File name → Screen 5 focused on that file · `Open PR →` → GitHub (external)

---

## SCREEN 5 — Historical Coupling Analysis

**Frame:** `Desktop / 05 Coupling`. Sidebar active: **Coupling**.
**Main content height 1140 — this screen scrolls.** Set Main to `Clip content`, vertical scroll.

### Section A — Page header + controls

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 400 | 36 | `Historical Coupling` |
| A2 | Select | 272 | 152 | 200 | 40 | `Range: All history` |
| A3 | Select | 488 | 152 | 180 | 40 | `Min coupling: 0.30` |
| A4 | Input | 684 | 152 | 280 | 40 | Placeholder `Path filter, e.g. src/**` |
| A5 | **Button / Secondary md** | 1288 | 152 | 120 | 40 | `Rebuild` |

### Section B — `Card / Co-change matrix` (272, 216 — 752 × 380)

Header H 56: title `Co-change matrix`. Grid area starts Y 288.

| Property | Value |
|---|---|
| Cell size | 40 × 40, gap 2 |
| Row label column | W 120, X 296, `Mono/Default` 12px, right-aligned, 8px right padding |
| Column labels | Rotated 0° (abbreviated to 2 chars), H 24, above grid at Y 264 |
| Grid origin | X 416, Y 288 |
| Grid | 7 × 7 cells → 7×40 + 6×2 = 292 × 292 |
| Cell radius | `radius/sm` |
| Diagonal (self) | `bg/subtle` fill, diagonal hatch |
| Cell hover | 2px `brand/primary` border |

**Cell fill by coupling value** — a single-hue sequential ramp, plus a glyph so
the value is never colour-only:

| Range | Fill | Glyph overlay |
|---|---|---|
| 0.80 – 1.00 | `brand/primary` @ 100% | `●` white |
| 0.50 – 0.79 | `brand/primary` @ 60% | `◐` white |
| 0.20 – 0.49 | `brand/primary` @ 30% | `○` `text/secondary` |
| < 0.20 | `bg/subtle` | none |

**Matrix rows/columns (7 files):** `auth.py` `session.py` `api.py` `routes.py` `db.py` `models.py` `unrelated.py`

**Values to draw** (symmetric): auth↔session 1.00 · api↔routes 1.00 · auth↔api 0.60 · session↔api 0.55 · db↔models 0.90 · api↔db 0.50 · all pairs involving `unrelated.py` 0.00.

### Section C — `Card / Legend` (1040, 216 — 368 × 380)

Header `Legend`. Four rows H 40 from Y 288: swatch 24×24 + glyph, then range label
(`Body/Default`) and meaning (`Body/Small`, `text/tertiary`).

Below at Y 460, a helper note (`Body/Small`, `text/secondary`):
`Click any cell to see the file pair's commit history.`

### Section D — `Card / Top coupled pairs` (272, 628 — 1136 × 300)

Header H 64: `Top coupled pairs`. Table header Y 692, H 40. Rows H 52 at Y 732 / 784 / 836.

| Col | X | W | Align | Header | Cell |
|---|---|---|---|---|---|
| 1 | 296 | 300 | left | `FILE A` | `Mono/Default` |
| 2 | 596 | 300 | left | `FILE B` | `Mono/Default` |
| 3 | 896 | 180 | right | `COUPLING` | `Mono/Score` |
| 4 | 1076 | 268 | right | `COMMITS TOGETHER / EITHER` | `Mono/Default`, `text/secondary` |
| 5 | 1344 | 40 | — | — | Chevron |

| File A | File B | Coupling | Together / Either |
|---|---|---|---|
| `auth.py` | `session.py` | 1.00 | 12 / 12 |
| `api.py` | `routes.py` | 0.80 | 8 / 10 |
| `db.py` | `models.py` | 0.60 | 6 / 10 |

Row 1 selected (`brand/subtle` + left bar).

> **Why column 4 is mandatory.** Jaccard similarity is scale-blind: two files
> that changed together once and never apart also score 1.00. The denominator is
> what separates a real signal from statistical noise. **Do not drop this column
> for visual balance.**

### Section E — `Card / Selected pair` (272, 960 — 1136 × 180)

| Element | X | Y | Content |
|---|---|---|---|
| Title | 296 | 984 | `auth.py ↔ session.py` — `Mono/Default` 16px |
| Stat 1 | 296 | 1024 | `Coupling 1.00` — label `Body/Small` above value `Mono/Score` |
| Stat 2 | 496 | 1024 | `Changed together 12 commits` |
| Stat 3 | 760 | 1024 | `Last together 2026-07-21` |
| **Button / Secondary sm** | 1080 | 1080 | 152 × 32 — `View commits →` |
| **Button / Secondary sm** | 1244 | 1080 | 164 × 32 — `View in risk report →` |

### Prototype links
Matrix cell → Section E updates · Table row → Section E updates · `View in risk report →` → Screen 4

---

## SCREEN 6 — Settings

**Frame:** `Desktop / 06 Settings`. Sidebar active: **Settings**.

### Section A — Page header + tabs

| # | Element | X | Y | W | H | Content |
|---|---|---|---|---|---|---|
| A1 | Page title | 272 | 96 | 400 | 36 | `Settings` |
| A2 | Tab bar | 272 | 152 | 1136 | 40 | 1px bottom border `border/default` |

**Tabs** — H 40, padding `0 16`, `Body/Strong`. Active: `brand/primary` text + 2px `brand/primary` bottom bar.

| Tab | X | W | State |
|---|---|---|---|
| `Scoring` | 272 | 88 | **Active** |
| `Alerts` | 360 | 80 | Default |
| `Integrations` | 440 | 120 | Default |
| `Cache` | 560 | 76 | Default |
| `Account` | 636 | 92 | Default |

### Section B — `Card / Scoring weights` (272, 216 — 1136 × 320)

Header H 64: title `Scoring weights`; subtitle `Body/Small` `text/tertiary`:
`Mirrors premerge.config.json — the CLI and dashboard share one configuration.`

**Three slider rows**, H 56, starting Y 296 (296 / 352 / 408):

| Element | X | W | Content |
|---|---|---|---|
| Label | 296 | 200 | `Line overlap` / `File overlap` / `Historical coupling` — `Body/Strong` |
| Slider | 512 | 560 | Values 0.50 / 0.30 / 0.20 |
| Value input | 1096 | 80 | H 40, `Mono/Default`, centred, 2dp |
| Helper | 1192 | 192 | `Body/Small`, `text/tertiary` — `same lines` / `same file` / `co-change history` |

**Sum indicator** (Y 472, H 32): pill at X 296, H 32, padding `0 12`, `radius/sm`.

| Variant | Fill | Text |
|---|---|---|
| `valid` | `risk/low-bg` | `Sum = 1.00 ✓` — `risk/low` |
| `invalid` | `risk/high-bg` | `Sum = 1.05 — weights must total 1.00` — `risk/high` |

**Card actions** (Y 472, right-aligned): `Reset to defaults` Secondary md 160×40 at X 1084 · `Save changes` Primary md 148×40 at X 1260.

> **Save is disabled while `sum ≠ 1.00`** (40% opacity). Do not auto-normalise
> silently — a user who types three numbers and gets three different ones back
> reads that as a bug.

### Section C — `Card / Risk thresholds` (272, 568 — 1136 × 180)

Header H 64: `Risk thresholds`.

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Label | 296 | 652 | 120 | 20 | `High risk ≥` |
| Input | 424 | 644 | 88 | 40 | `0.50` — `Mono/Default` |
| Swatch | 528 | 654 | 20 | 20 | `risk/high`, `radius/sm` |
| Label | 620 | 652 | 140 | 20 | `Medium risk ≥` |
| Input | 768 | 644 | 88 | 40 | `0.20` |
| Swatch | 872 | 654 | 20 | 20 | `risk/med` |
| Caption | 964 | 652 | 300 | 20 | `Anything below is Low` — `Body/Small`, `text/tertiary` |
| Checkbox + label | 296 | 700 | 500 | 20 | `Fail the CI check when risk ≥ High` — checked |

### Section D — `Card / Coupling cache` (272, 780 — 1136 × 200)

Header H 64: `Coupling cache`.

| Element | X | Y | W | H | Content |
|---|---|---|---|---|---|
| Stat | 296 | 864 | 300 | 40 | `4 repositories · 2.1 MB` — `Body/Strong`; caption `Cached co-change matrices` |
| Checkbox + label | 296 | 920 | 600 | 20 | `Reuse cache when commit history is unchanged` — checked |
| Helper | 320 | 944 | 700 | 16 | `Keyed by HEAD commit. Rebuild after a history rewrite.` — `Body/Small`, `text/tertiary` |
| **Button / Danger md** | 1252 | 864 | 156 | 40 | `Clear cache` |

`Clear cache` opens a confirmation dialog (480 × 200, centred, `shadow/md`):
title `Clear coupling cache?`, body `The next analysis will rebuild every matrix from scratch. This can take several minutes on large repositories.`, actions `Cancel` (Secondary) + `Clear cache` (Danger).

**Total content height:** 980. Fits without scroll.

---

# PART 5 — FIGMA FILE ORGANISATION

## 5.1 Pages

| Page | Contents |
|---|---|
| `📐 Foundations` | Colour variables (Light/Dark modes), type styles, grid, spacing, elevation |
| `🧩 Components` | All Part 2 components with every variant |
| `🖥 Screens — Desktop` | The 6 frames below |
| `🔀 Prototype` | Duplicated frames wired with the Part 4 links |
| `🗃 Archive` | Superseded explorations — never delete, move here |

## 5.2 Frame naming

```
Desktop / 01 Login
Desktop / 01 Login — Error
Desktop / 02 Dashboard
Desktop / 03 Repositories
Desktop / 03 Repositories — Empty
Desktop / 04 Risk Report
Desktop / 04 Risk Report — Low risk
Desktop / 05 Coupling
Desktop / 06 Settings
Desktop / 06 Settings — Invalid weights
```

## 5.3 Auto Layout & constraints — build rules

1. **Header** — horizontal Auto Layout, `space-between`. Logo cluster left, repo switcher centre, actions right. Constraint: Left+Right, Top. Fixed on scroll.
2. **Sidebar** — vertical Auto Layout, gap 4, padding 12. Bottom cluster in its own frame pinned Bottom. Constraint: Left, Top+Bottom. Fixed on scroll.
3. **Main** — vertical Auto Layout, gap 32, padding 32. Constraint: Left+Right, Top+Bottom. Every section is a fill-width child, so a section can be added or removed without manual repositioning.
4. **Cards** — vertical Auto Layout, `Fill container` width, `Hug contents` height.
5. **Table rows** — horizontal Auto Layout; each cell fixed-width per the column tables; only the free-text column set to `Fill`.
6. **All text** — `Auto width` for labels, `Auto height` + fixed width for anything that wraps or truncates.

## 5.4 Build order

1. Foundations: variables → type styles → grid
2. Components: Button → Input/Select → Toggle/Checkbox/Slider → **Risk Badge** → Card → Table row → Chip → Nav item
3. Shell: Header + Sidebar as one `Shell / Desktop` component
4. Screens in order 2 → 4 → 5 → 3 → 6 → 1 (build the data-dense screens first; they exercise every component, and Login needs almost none)
5. Variant frames (Error, Empty, Low risk, Invalid weights)
6. Prototype wiring

## 5.5 Handoff checklist

- [ ] Every colour is a **variable**, not a hex literal — dark mode must be one toggle
- [ ] Every text layer uses a **named style** from §1.4
- [ ] No off-scale spacing values (only 4/8/12/16/24/32/48/64)
- [ ] Risk shown as **number + bar + band label** everywhere — no colour-only encoding
- [ ] Every interactive component has Default / Hover / Pressed / Disabled variants
- [ ] Empty, loading and error states drawn for screens 1, 3, 4
- [ ] Contrast ≥ 4.5:1 for body text, ≥ 3:1 for UI borders, in **both** modes
- [ ] Focus ring visible on every focusable element (keyboard navigation)
- [ ] Labels match the CLI's vocabulary exactly — the same three risk bands and the
      same explanation strings the scoring engine emits

## 5.6 Traceability

| Screen | Wireframe | MoSCoW | Backing implementation |
|---|---|---|---|
| 1 Login | [wireframes.md](wireframes.md) §1 | C1 | — (new) |
| 2 Dashboard | §2 | C1 | `scoring.py`, `report.py` |
| 3 Repositories | §3 | C1 | `git_utils.py` |
| 4 Risk Report | §4 | M5, S4 | `scoring.py` — breakdown mirrors `compute_risk()` |
| 5 Coupling | §5 | M4 | `coupling.py` — Jaccard + raw counts |
| 6 Settings | §6 | S3, C6 | `config.py` — same weights as `premerge.config.json` |
