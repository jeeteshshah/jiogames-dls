# Example: Create a TV Game Rail

## User prompt

> "Build a TV home screen with a featured hero and a game rail."

---

## Step 1 — Classify platform

| Decision | Value |
|---|---|
| Platform | TV (1920×1080px) |
| Screen type | Full screen — home |
| Primary action | Browse and select a game |
| Required states | Default, focused card (D-pad), selected |
| Input model | D-pad (no hover, no touch) |

---

## Step 2 — TV-specific rules (read before writing code)

From `references/motion.md §10`:
- No press/tap scale feedback — D-pad has no "press"
- No ambient loops (breathing, marquee, aurora)
- Focus `scale(1.05)` + glow **only** as focus state
- No `backdrop-filter` (performance)

From `references/sizing-scale.md §6`:
- `--ctrl-h-sm` (36px) and `--ctrl-h-ghost` (40px) are mobile/web only — below TV `--touch-min` (60px)
- Only `var(--ctrl-h)` (72px on TV via token) for interactive controls

From `references/screens-and-navigation.md §11`:
- No tab bar on TV — D-pad navigation
- No bottom sheets on TV — full-screen patterns
- Safe zone: `padding: var(--tv-safe)` (80px)

From `references/spacing-and-grid.md`:
- `--gutter` resolves to 80px on TV automatically
- `--section-gap` resolves to 64px on TV

---

## Step 3 — Key decisions

| Element | Token / pattern |
|---|---|
| Page wrapper | `padding: var(--tv-safe)` |
| Hero height | `55vh; min-height: 400px` |
| Card width | `var(--card-wide-w)` — resolves to 400px on TV |
| Card radius | `var(--r4)` |
| Card gap | `var(--card-gap)` — resolves to 24px on TV |
| Focus ring | `box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4); transform: scale(1.05)` |
| Rail title | `.text-rail-title` — TV media query handles font size |
| No hover states | `:hover` rules not written — TV has no hover |
| No `backdrop-filter` | Remove from all elements |
| Content entrance | `fade-up` 560ms, no stagger (TV collapses stagger) |
| Screen transition | Fade, not horizontal slide |

---

## Step 4 — What Claude must NOT do on TV

- `transition: background .3s` on hover → remove `:hover` block entirely
- `backdrop-filter: blur(…)` → remove
- `animation: breathe 18s …` on hero → remove
- `height: 36px` or `height: 40px` → these are mobile-only sizes
- Bottom sheet or end-sheet → not for TV
- Staggered entrance → collapse to single delay

---

## Step 5 — Rail trailing gutter (TV)

```css
/* TV gutter resolves to 80px via token — no code change needed */
.rail-scroll {
  padding-left: var(--gutter);              /* 80px on TV */
  gap: var(--card-gap);                     /* 24px on TV */
}
.rail-scroll > :last-child { margin-right: var(--gutter); }  /* trailing 80px */
```

---

## Step 6 — Final response

```
Files: index.html, styles.css, README.md, qa-report.md
Design: TV home screen — full-width cinematic hero with title + CTA,
        one featured game rail, D-pad navigation focus states.
Components: Button (primary, 72px on TV via --ctrl-h), Rail, Card (wide landscape, 400px)
Validation: Exit 0 — confirmed no backdrop-filter, no hover states, no ambient loops
Assumptions: TV only — no mobile/web responsive breakpoints included
Manual checks: Test focus order with D-pad; verify last card in rail is reachable; check safe-zone on different TV resolutions
```
