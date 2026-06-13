# JioGames Component Patterns & Token Index

> **Inherits `references/_core-rules.md`.** Rules in that file (dark-only, JioType-only, token-first, no Lucide, no silent deviation) are not repeated here.

> This document is **not** the source of truth for typography, spacing, colour, radius, sizing, or motion.
> - Typography: [typography.md](typography.md) · Spacing: [spacing-and-grid.md](spacing-and-grid.md)
> - Colour: [colour-governance.md](colour-governance.md) · Radius: [radius-governance.md](radius-governance.md)
> - Sizing: [sizing-scale.md](sizing-scale.md) · Motion: [motion.md](motion.md)
> - Token values: [../tokens/tokens.json](../tokens/tokens.json) → generated into [../tokens/tokens.css](../tokens/tokens.css)
>
> **Literal values in this document are explanatory only.** Generated CSS must always use `var(--token)` names.
> This document shows how approved tokens combine into reusable JioGames components.

---

## Table of Contents

1. [Importing Tokens](#1-importing-tokens)
2. [Colour Tokens](#2-colour-tokens)
3. [Spacing & Radius Reference](#3-spacing--radius-reference)
4. [Elevation & Glow](#4-elevation--glow)
5. [Motion & State Tokens](#5-motion--state-tokens)
6. [Component Size Tokens](#6-component-size-tokens)
7. [Component Patterns](#7-component-patterns)
8. [Asset Paths](#8-asset-paths)
9. [Platform Component Behaviour](#9-platform-component-behaviour)
10. [Component QA Checklist](#10-component-qa-checklist)
11. [Approved Structural Exceptions](#11-approved-structural-exceptions)

---

## 1. Importing Tokens

`tokens.css` is generated — never hand-edit it.

```html
<!-- Every screen imports this. Use var(--token) only — no raw values. -->
<link rel="stylesheet" href="tokens/tokens.css">
```

To regenerate after editing `tokens.json`:
```bash
python3 tokens/build.py        # generate
python3 tokens/build.py --check  # CI: fails if tokens.css is stale
```

For the full `:root` block and `@media` overrides see `tokens/tokens.css` directly.

---

## 2. Colour Tokens

> **Quick reference only — explanatory, not copyable.** Literal values below are for human readability. Generated CSS must use `var(--token)` names, never raw hex. Full index lives in [colour-governance.md §3](colour-governance.md). Colour decisions, decision tree, forbidden combos: [colour-governance.md §4–§10](colour-governance.md).

### Most-used tokens

| Token | Value | Usage |
|---|---|---|
| `--jio` | `#00A859` | CTAs, active borders, check icons, eyebrow labels |
| `--jio-glow` | `rgba(0,200,100,.35)` | Box-shadow glow on selected/active |
| `--jio-soft` | `rgba(0,168,89,.12)` | Tinted fill on selected surfaces |
| `--ultimate` | `#00cc65` | Ultimate Pass CTA and accent (**never blue**) |
| `--popular-gold` | `#F7AB20` | "Most Popular" badge |
| `--bg` | `#06080F` | Page/screen background — never pure `#000` |
| `--card-bg` | `#111115` | Card surfaces |
| `--sheet-bg` / `--sheet-top` | `#0e1118` / `#131720` | Bottom sheet gradient |
| `--glass-1` | `rgba(255,255,255,.055)` | Input fields, OTP boxes |
| `--chip-bg` | `#0c0f14` | Platform chips, USP tiles |
| `--text` | `#F4F2EE` | Primary — headings, prices, critical info |
| `--text2` | `#A8ADBA` | Secondary — body, terms, timers, nav labels, helper text |
| `--text3` | `#6B7280` | **Decorative only** — inactive icons, timestamps, placeholders |
| `--text-inv` | `#000000` | Text on green CTA (`var(--text-inv)` on `var(--jio)`) |
| `--border` | `rgba(255,255,255,.1)` | Default component border |
| `--border-subtle` | `rgba(255,255,255,.08)` | Light cards, inactive chips |
| `--border-ultimate` | `rgba(0,204,101,.3)` | Ultimate Pass border |
| `--negative` | `#FF4757` | Errors, destructive states |
| `--overlay-scrim` | `rgba(0,0,0,.55)` | Sheet/modal backdrop |

---

## 3. Spacing & Radius Reference

Full scale, decision tree, and governance live in [spacing-and-grid.md](spacing-and-grid.md). Quick reference:

### Key Aliases (platform-aware)

| Alias | Mobile | Web | TV |
|---|---|---|---|
| `--gutter` | 16px | 40px | 80px |
| `--section-gap` | 32px | 48px | 64px |
| `--card-gap` | 12px | 24px | 24px |
| `--component-padding` | 16px | 24px | 32px |
| `--card-padding` | 16px | 24px | 32px |
| `--sheet-padding` | 24px | 32px | — |
| `--hero-gap` | 32px | 64px | 96px |

### Border Radius

| Token | Value | Usage |
|---|---|---|
| `--r1` | `8px` | Small icons, tiny badges |
| `--r2` | `10px` | Marquee cards |
| `--r3` | `12px` | GFF wrap, small containers |
| `--r4` | `14px` | Wide cards, square cards, platform chips, OTP boxes |
| `--r5` | `16px` | Input fields, genre tiles, cover-card image |
| `--r6` | `18px` | USP cards |
| `--r7` | `20px` | Pass / upsell cards, modals |
| `--r8` | `22px` | Reserved — oversized feature surfaces |
| `--r9` | `28px` | Bottom sheet top corners |
| `--pill` | `100px` | Primary buttons, action chips |

---

## 4. Elevation & Glow

JioGames uses **glow for state** and **deep directional shadow for physical lift**. No soft grey shadows.

### Glow Levels

| Level | CSS | Usage |
|---|---|---|
| Input focus | `box-shadow: 0 0 0 3px rgba(0,168,89,.14)` | Text input, phone field |
| OTP active | `box-shadow: 0 0 0 3px rgba(0,168,89,.15)` | Active OTP box |
| Card selected | `box-shadow: 0 0 0 2px var(--jio), 0 6px 28px rgba(0,168,89,.45)` | Genre tile selected |
| GFF rail glow | `box-shadow: 0 0 8px rgba(0,232,112,.5)` | Left accent rail |
| Ultimate active | `box-shadow: 0 0 0 3px rgba(0,204,101,.3)` | Ultimate pass focus |
| TV focus | `box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4)` | TV focused card |
| Physical lift | `box-shadow: 0 18px 30px -6px rgba(0,0,0,.85)` | Poster over numeral, floating tab bar |

### Background Depth Pattern

Layer backgrounds from darkest → lightest:
```
--bg       #06080F   page
--card-bg  #111115   card
--glass-1  rgba(255,255,255,.055)   input/surface
--border   rgba(255,255,255,.08)    edge
```

### Pass Card Backgrounds

```css
/* Mobile Pass */
.pass-mobile {
  background: #0e1a14;
  border: 1px solid rgba(0,168,89,.25);
  position: relative; overflow: hidden;
}
.pass-mobile::before {
  content: '';
  position: absolute; top: -40px; right: -40px;
  width: 160px; height: 160px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,168,89,.18) 0%, transparent 70%);
  pointer-events: none;
}

/* Ultimate Pass — richer green differentiates from Mobile */
.pass-ultimate {
  background: linear-gradient(135deg, #0a1f14 0%, #0d2a1a 60%, #08160e 100%);
  border: 1px solid var(--border-ultimate);
  position: relative; overflow: hidden;
}
.pass-ultimate::before {
  content: '';
  position: absolute; top: -60px; right: -30px;
  width: 200px; height: 200px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,232,112,.2) 0%, transparent 65%);
  pointer-events: none;
}
```

### Raw Colour in Gradients — Rule

Use tokens for all stable semantic colours. Raw `rgba` / hex values are allowed **only** inside:
- Approved gradient recipes (pass backgrounds, hero overlays, shimmer frames)
- Image treatments and artwork overlays (brightness, tint)
- Glow box-shadow recipes (already listed in Glow Levels above)

Raw values in normal component fills, borders, or text are violations. `validate.sh` will flag them.

---

## 5. Motion & State Tokens

These tokens appear throughout component state definitions. Listed here so developers are not surprised by undefined-looking variables.

### Motion

| Token | Value | Use |
|---|---|---|
| `--dur-fast` | `120ms` | Tap feedback, focus ring, small state changes |
| `--dur-default` | `200ms` | Standard component state transitions |
| `--dur-enter` | `420ms` | Screen enter animations |
| `--dur-sheet` | `400ms` | Bottom sheet open / close |
| `--spring` | `cubic-bezier(.22,1,.36,1)` | Default natural enter easing |
| `--spring-bounce` | `cubic-bezier(.34,1.56,.64,1)` | OTP fill pop, selection celebrate |
| `--ease-screen` | `cubic-bezier(.42,0,.18,1)` | Screen-to-screen slide |

### State

| Token | Use |
|---|---|
| `--overlay-scrim` | `rgba(0,0,0,.55)` — modal / sheet backdrop (pair with `blur(8px)`) |
| `--negative` | `#FF4757` — error borders, destructive state text, error messages |
| `--jio-glow` | `rgba(0,200,100,.35)` — box-shadow glow on selected / active |
| `--jio-soft` | `rgba(0,168,89,.12)` — tinted fill on selected surface |
| `--border-ultimate` | `rgba(0,204,101,.3)` — Ultimate Pass focus / active border |

`prefers-reduced-motion` collapses `--dur-fast`, `--dur-default`, and `--dur-enter` to `0ms` automatically via `tokens.css`. Components do not need to handle this separately.

---

## 6. Component Size Tokens

All dimensions are now live in `tokens.css` — use `var(--token)` in component CSS. Platform-aware tokens (`--ctrl-h`, `--touch-min`, `--card-wide-w`) resolve automatically via the TV `@media` block.

| Token | Mobile | TV | Component | Notes |
|---|---:|---:|---|---|
| `--ctrl-h` | 54px | 72px | `.btn-primary` | Platform-aware via token |
| `--ctrl-h-sm` | 36px | 36px | `.btn-cta-sm` | Fixed — not used on TV |
| `--ctrl-h-ghost` | 40px | 40px | `.btn-skip` | Fixed |
| `--touch-min` | 44px | 60px | all interactive | Min tap/focus target |
| `--otp-box-w` | 50px | — | `.otp-box` | Mobile/Web only |
| `--otp-box-h` | 64px | — | `.otp-box` | Mobile/Web only |
| `--card-wide-w` | 272px | 400px | `.wide-card` | Platform-aware via token |
| `--card-sq` | 96px | 96px | `.sq-card` | Fixed |
| `--genre-tile-h` | 156px | 156px | `.genre-tile` | Fixed |
| `--tab-bar-h` | 64px | — | tab bar | Mobile/Web only |
| `--app-bar-h` | 64px | — | site header | Web only |

Sheet handle (`40×4px`, `border-radius: 2px`) stays hard-coded — see approved structural exception in Bottom Sheet component.

---

## 7. Component Patterns

Typography roles are applied via `.text-*` classes from [typography.md §2](typography.md). Component CSS handles structure, states, and colour — not font sizes.

### Button (Primary)

Typography role: **`text.cta`** (`.text-cta`)

```css
.btn-primary {
  /* Layout */
  width: 100%;
  height: var(--ctrl-h);            /* 54px mobile/web → 72px TV via token */
  border-radius: var(--pill);
  padding: 0 var(--component-padding);
  /* Colour */
  background: var(--jio);
  color: var(--text-inv);           /* black on green */
  border: none;
  /* Typography — inherit from .text-cta */
  font-family: var(--jio-font);
  /* Interaction */
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform var(--dur-fast) var(--spring), opacity var(--dur-fast);
}
.btn-primary:active   { transform: scale(.97); }
.btn-primary:disabled { opacity: .32; cursor: not-allowed; }
```

### Button (Small CTA)

Typography role: **`text.cta`** (smaller size override in component)

```css
.btn-cta-sm {
  height: var(--ctrl-h-sm);         /* 36px */
  padding: 0 var(--space-3);        /* 0 24px */
  border-radius: var(--pill);
  border: none;
  cursor: pointer;
  font-family: var(--jio-font);
  font-size: 13px; font-weight: 700;  /* compact variant — approved exception */
  transition: transform var(--dur-fast), opacity var(--dur-fast);
}
.btn-cta-sm:active        { transform: scale(.96); }
.btn-cta-green            { background: var(--jio); color: var(--text-inv); }
.btn-cta-ultimate         { background: var(--ultimate); color: var(--text-inv); }
```

### Button (Ghost / Skip)

Typography role: **`text.caption`**

```css
.btn-skip {
  height: var(--ctrl-h-ghost);      /* 40px */
  background: none;
  border: none;
  font-family: var(--jio-font);
  color: var(--text3);
  cursor: pointer;
  transition: opacity var(--dur-fast);
}
.btn-skip:active { opacity: .6; }
```

### Text Input

Typography: input value uses **`text.body`** weight+size, placeholder muted.

```css
.input-field {
  background: var(--glass-1);
  border: 1.5px solid var(--border);
  border-radius: var(--r5);
  overflow: hidden;
  transition: border-color var(--dur-default), box-shadow var(--dur-default);
}
.input-field:focus-within {
  border-color: var(--jio);
  box-shadow: 0 0 0 3px rgba(0,168,89,.14);
}
.input-field input {
  flex: 1;
  background: none; border: none; outline: none;
  padding: var(--component-padding);
  font-family: var(--jio-font);
  font-size: 18px; font-weight: 500; /* input-value role */
  color: var(--text);
  letter-spacing: .9px;
}
.input-field input::placeholder {
  color: var(--text3);
  font-weight: 500;                 /* 300/500/700/900 only; 400 banned */
  letter-spacing: 0;
}
```

### OTP Boxes

```css
.otp-row {
  display: flex;
  gap: var(--space-1-5);            /* 12px — space.1.5 */
  justify-content: center;
}
.otp-box {
  width: var(--otp-box-w); height: var(--otp-box-h);  /* 50×64px */
  border-radius: var(--r4);
  background: var(--glass-1);
  border: 1.5px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--jio-font);
  font-size: 26px; font-weight: 700;
  color: var(--text);
  transition: border-color var(--dur-fast), background var(--dur-fast), box-shadow var(--dur-fast);
}
.otp-box.active {
  border-color: var(--jio);
  box-shadow: 0 0 0 3px rgba(0,168,89,.15);
}
.otp-box.filled {
  border-color: var(--jio);
  background: var(--jio-soft);                  /* rgba(0,168,89,.12) — closest approved token */
  animation: box-pop var(--dur-pop) var(--spring-bounce);
}
```

### Bottom Sheet

```css
.sheet-backdrop {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0); backdrop-filter: blur(0px);
  transition: background var(--dur-enter) var(--ease-out),
              backdrop-filter var(--dur-enter) var(--ease-out);
}
.sheet-backdrop.open {
  background: var(--overlay-scrim);
  backdrop-filter: blur(8px);
}
.bottom-sheet {
  position: absolute; bottom: 0; left: 0; right: 0;
  background: linear-gradient(180deg, var(--sheet-top) 0%, var(--sheet-bg) 60%);
  border-radius: var(--r9) var(--r9) 0 0;
  padding: 0 var(--gutter) var(--space-12);  /* 0 gutter 96px bottom */
  transform: translateY(100%);
  transition: transform var(--dur-sheet) var(--spring);
  z-index: 1;
}
.bottom-sheet.open { transform: translateY(0); }
/*
 * Approved structural exception: sheet handle uses vertical margin, not a parent stack.
 * Reason: it is centred independently (auto left/right) and does not belong to the
 * sheet content stack — wrapping it in a stack container would break horizontal centering.
 * All other sheet content uses .content-stack or .component-stack for vertical rhythm.
 */
.sheet-handle {
  width: 40px; height: 4px;
  border-radius: 2px;
  background: rgba(255,255,255,.15);
  margin: var(--space-2) auto var(--space-4);  /* 16px auto 32px */
}
```

### Horizontal Rail

Typography role for heading: **`text.railTitle`** (`.text-rail-title`)

```css
.rail-head {
  padding: 0 var(--gutter);
  margin-bottom: var(--space-1-5);  /* 12px — rail-head to cards */
}
/* Apply .text-rail-title to the heading element — do not hardcode size here */

.rail-scroll {
  display: flex;
  gap: var(--card-gap);
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding-left: var(--gutter);      /* leading gutter only */
  scroll-padding-left: var(--gutter);
  -webkit-overflow-scrolling: touch;
}
.rail-scroll::-webkit-scrollbar { display: none; }
/* Trailing gutter — :last-child margin, not calc() spacer (see spacing-and-grid.md §7) */
.rail-scroll > :last-child { margin-right: var(--gutter); }
```

### Wide Landscape Card (16:9)

Typography roles: title → **`text.cardTitle`** (wide variant), meta → **`text.caption`**

```css
.wide-card {
  flex-shrink: 0;
  width: var(--card-wide-w);        /* 272px mobile → 400px TV via token */
  border-radius: var(--r4);
  overflow: hidden;
  position: relative;
  scroll-snap-align: start;
  cursor: pointer;
}
.wide-card img {
  width: 100%; aspect-ratio: 16/9;
  object-fit: cover; display: block;
}
.wide-card-label {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: var(--space-3) var(--space-1-5) var(--space-1);  /* 24 12 8 */
  background: linear-gradient(to top, rgba(0,0,0,.85) 0%, transparent 100%);
}
/* Apply .text-card-title and .text-caption to children — not hardcoded here */
```

### Portrait Cover Card (2:3)

```css
.cover-card {
  flex-shrink: 0;
  scroll-snap-align: start;
  display: flex; align-items: flex-end;
  overflow: visible;
}
.cover-card-img {
  width: 84px;
  flex-shrink: 0;
  border-radius: var(--r2);
  overflow: hidden;
  box-shadow: -6px 6px 20px rgba(0,0,0,.8);  /* physical lift */
}
.cover-card-img img {
  width: 100%; aspect-ratio: 2/3;
  object-fit: cover; display: block;
}
```

### Square Card (1:1)

Typography roles: name → **`text.cardTitle`** (small), genre → **`text.caption`**

```css
.sq-card { flex-shrink: 0; width: var(--card-sq); scroll-snap-align: start; }
.sq-card-img {
  width: var(--card-sq); height: var(--card-sq);  /* 96×96px */
  border-radius: var(--r4);
  overflow: hidden;
}
.sq-card-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
/* Wrap .sq-card-img + name + genre in .tight-stack for vertical rhythm */
/* Apply .text-card-title and .text-caption to name/genre elements */
```

### Pass Upsell Card

Typography roles: name → **`text.cardTitle`**, price → **`text.price`**, perks → **`text.body`**, tag → **`text.badge`**

```css
.upsell-card {
  border-radius: var(--r7);
  padding: var(--card-padding);
  position: relative; overflow: hidden;
  cursor: pointer;
  transition: transform var(--dur-fast);
}
.upsell-card:active { transform: scale(.98); }

/* Internal layout: wrap in .content-stack — no child margins */

.upsell-card-tag {
  display: inline-flex; align-items: center;
  gap: var(--space-0-5);           /* 4px icon gap */
  font-family: var(--jio-font);
  font-size: 10px; font-weight: 700;
  letter-spacing: .5px; text-transform: uppercase;
  padding: 3px var(--space-1);     /* 3 8 */
  border-radius: var(--r7);
}
/* Apply .text-card-title to the plan name */

.upsell-perks {
  display: flex; flex-direction: column;
  gap: var(--space-1);             /* 8px — space.1 */
}
.upsell-perk {
  display: flex; align-items: flex-start;
  gap: var(--space-1);             /* 8px */
  font-family: var(--jio-font);
  font-size: 13px; font-weight: 500;
  color: rgba(244,242,238,.85);
  line-height: 1.4;
}
.upsell-check {
  width: 16px; height: 16px; flex-shrink: 0;
  fill: none; stroke: var(--jio);
  stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round;
}
.upsell-popular {
  background: linear-gradient(90deg, var(--popular-gold), #ffcf5c);  /* approved gradient recipe — colour-governance.md §9 */
  color: var(--text-inv);
  font-family: var(--jio-font);
  font-size: 9px; font-weight: 900;
  letter-spacing: .5px; text-transform: uppercase;
  padding: var(--space-0-5) var(--space-1);  /* 4 8 */
  border-radius: var(--pill);
  white-space: nowrap; flex-shrink: 0;
}
```

### Platform Chip (selectable)

Typography role: label → **`text.badge`**

```css
.platform-chip {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: var(--space-1);             /* 8px */
  border-radius: var(--r4);
  padding: var(--space-1-5) var(--space-1);  /* 12 8 */
  background: var(--chip-bg);
  border: 1.5px solid var(--border-subtle);
  cursor: pointer;
  font-family: var(--jio-font);
  transition: background var(--dur-fast), border-color var(--dur-fast), transform var(--dur-fast);
}
.platform-chip:active { transform: scale(.95); }
.platform-chip.selected {
  background: color-mix(in srgb, var(--jio) 8%, var(--chip-bg));  /* approved: dark green tint on chip bg */
  border-color: var(--jio);
  box-shadow: 0 0 0 1px var(--jio);
}
.platform-chip svg {
  width: 22px; height: 22px;
  fill: none; stroke: rgba(255,255,255,.45);
  stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;
  transition: stroke var(--dur-fast);
}
.platform-chip.selected svg { stroke: var(--jio); }
/* Apply .text-badge to label span; override color to --text2/--jio */
```

### Genre Tile (image-backed, selectable)

```css
.genre-tile {
  position: relative;
  border-radius: var(--r5);
  overflow: hidden; height: var(--genre-tile-h);  /* 156px */
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color var(--dur-default), transform var(--dur-fast), box-shadow var(--dur-default);
}
.genre-tile:active { transform: scale(.96); }
.genre-tile.selected {
  border-color: var(--jio);
  box-shadow: 0 0 0 2px var(--jio), 0 6px 28px rgba(0,168,89,.45);
  transform: scale(1.03);
}
.genre-tile img {
  width: 100%; height: 100%; object-fit: cover;
  filter: brightness(.55) saturate(.6);
  transition: filter var(--dur-enter);
}
.genre-tile.selected img { filter: brightness(.95) saturate(1.15); }
```

### Eyebrow Label

Typography role: **`text.badge`** (`.text-badge`)

```css
/* Use .text-badge class on the element.
   Parent stack controls vertical gap — do not add margin here. */
.eyebrow {
  font-family: var(--jio-font);
  font-size: 11px; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--jio);
}
```

### SIM / Action Chip

```css
.sim-chip {
  display: flex; align-items: center;
  gap: var(--space-1);             /* 8px */
  background: var(--jio-soft);
  border: 1px solid rgba(0,168,89,.28);
  border-radius: var(--r4);
  padding: var(--space-1-5) var(--space-1-5);  /* 12px */
  cursor: pointer;
  transition: background var(--dur-default), transform var(--dur-fast);
}
.sim-chip:active { background: rgba(0,168,89,.18); transform: scale(.98); }
```

### Number-Confirmed Pill

```css
.number-confirmed {
  display: inline-flex; align-items: center;
  gap: var(--space-1);             /* 8px */
  background: rgba(255,255,255,.06);
  border: 1px solid var(--border);
  border-radius: var(--pill);
  padding: var(--space-1) var(--space-1) var(--space-1) var(--space-2);  /* 8 8 8 16 */
  align-self: flex-start;
}
.nc-number { font-size: 14px; font-weight: 700; color: var(--text); }
.nc-change {
  font-size: 12px; font-weight: 700; color: var(--jio);
  background: var(--jio-soft);
  border: none; border-radius: var(--pill);
  padding: var(--space-0-5) var(--space-1);    /* 4 8 */
  cursor: pointer; font-family: var(--jio-font);
  transition: background var(--dur-fast);
}
.nc-change:active { background: rgba(0,168,89,.2); }
```

### OR Divider

```css
.or-divider { display: flex; align-items: center; gap: var(--space-1); }
.or-line    { flex: 1; height: 1px; background: var(--hairline); }
.or-text    { font-size: 11px; font-weight: 500; color: var(--text3); }
```

### Progress Dots (step indicator)

```css
/* Parent: .tight-stack or inline — not a vertical stack, use flex row */
.pref-progress { display: flex; gap: var(--space-0-5); }  /* 4px */
.pp-dot {
  height: 3px; border-radius: 2px; flex: 1;
  background: rgba(255,255,255,.1);
  transition: background var(--dur-default);
}
.pp-dot.done   { background: var(--jio); }
.pp-dot.active { background: rgba(0,168,89,.5); }
```

### Hero Overlay Gradient

```css
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom,
    rgba(6,8,15,.55) 0%,
    rgba(6,8,15,.1) 35%,
    rgba(6,8,15,.82) 68%,
    var(--bg) 100%);
}
```

---

## 8. Asset Paths

Case-sensitive. Capital `/Assets/`.

```
Hero (landscape):   /Assets/horizontal/[slug]-thumbnail--gamehero-1920x1080.jpeg
Cover (portrait):   /Assets/vertical/[slug]-thumbnail--cover-720x1080.jpeg
Background:         /Assets/hero/[slug]-thumbnail--background-1920x1080.jpeg
```

---

## 9. Platform Component Behaviour

Spacing and typography scale automatically via `tokens.css` media queries. This section covers **component structure differences** per platform only.

### Web (≥768px)

```css
@media (min-width: 768px) {
  .page-container {
    max-width: var(--container-web);
    margin-inline: auto;
    padding-inline: var(--gutter);
  }

  /* Sticky frosted header */
  .site-header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(6,8,15,.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0 var(--gutter);
    height: var(--app-bar-h);              /* 64px — from token */
    display: flex; align-items: center;
    gap: var(--space-3);             /* 24px */
  }

  /*
   * Rails vs grid — context-dependent (see spacing-and-grid.md §6.2):
   *   Editorial/discovery rails → keep as horizontal rail
   *   Dense listing / search / library / browse → switch to grid
   */
  .rail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: var(--card-gap);
    padding: 0;
    overflow: visible;
  }

  .wide-card { width: 100%; }
}
```

### TV (≥1280px, ≥720px tall)

Typography and spacing alias overrides are handled by `tokens.css`. Component-specific changes:

```css
@media (min-width: 1280px) and (min-height: 720px) {
  /* TV focusable — D-pad driven, no hover */
  .focusable:focus {
    outline: none;
    border-color: var(--jio);
    box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4);
    transform: scale(1.05);
    transition: transform var(--dur-fast) var(--spring), box-shadow var(--dur-fast);
    z-index: 1;
  }
  .focusable:hover:not(:focus) { transform: none; box-shadow: none; }

  /* Safe zone wrapper */
  .tv-safe { padding: var(--tv-safe); }

  /* Card width and button height resolve automatically via --card-wide-w and --ctrl-h tokens.
     No overrides needed here — tokens.css @media handles them. */

  /* Typography roles handle font sizes — do not override here.
     Apply .text-rail-title, .text-card-title etc. to elements. */

  /* TV min-width for primary button (layout only) */
  .btn-primary { min-width: 240px; }  /* 240px: approved TV layout constant — screens-and-navigation.md §12 */
}
```

---

## 10. Component QA Checklist

Before any component is added or updated, verify:

| Check | Required |
|---|---|
| Imports `tokens.css` — no inline `:root` redefinitions | Yes |
| All colours use tokens (raw hex/rgba only in approved gradients or glow recipes) | Yes |
| Typography role declared — `.text-*` class on correct element, no hardcoded `font-size` | Yes |
| Only allowed weights: 300 / 500 / 700 / 900 — 400 / 600 / 800 banned | Yes |
| Spacing uses `--space-*` tokens or semantic aliases — no raw px (except approved component dimensions in §6) | Yes |
| Vertical rhythm from parent stack utility — no child `margin-bottom` except approved structural exceptions | Yes |
| All applicable states implemented: default, active/pressed, focus, disabled | Yes |
| Focus ring present — never bare `outline: none` without a glow replacement | Yes |
| TV: focus ring defined; no hover-only affordance; min 60px focusable target | If TV in scope |
| Mobile: min 44×44px tap target on all interactive elements | Yes |
| Disabled state: `opacity: .32`, `cursor: not-allowed`, no animation | Yes |
| Loading state: spinner or skeleton — not just dimming | If async |
| New variant added to [component-contracts.md](component-contracts.md) with owner approval | If new variant |
| `tokens/validate.sh` passes with exit 0 | Yes |

---

## 11. Approved Structural Exceptions

Raw values allowed in component CSS **only** when listed here. Each exception has an owner, reason, allowed selector, and allowed value. Any unlisted raw value is a violation. To add a new exception: RFC + 2 DLS owner approvals.

| Exception | Allowed selector | Allowed value | Owner | Reason |
|---|---|---|---|---|
| Sheet handle vertical margin | `.sheet-handle` | `margin: var(--space-2) auto var(--space-4)` | DLS Owner | Centred independently with `auto`; belongs outside content stack — wrapping in stack breaks horizontal centring |
| Sheet handle dimensions | `.sheet-handle` | `width: 40px; height: 4px` | DLS Owner | Physical grab target; below `--space-1` granularity; proportions are optical |
| Sheet handle radius | `.sheet-handle` | `border-radius: 2px` | DLS Owner | 4px tall element — `--r1` (8px) exceeds half-height and causes rendering artefact |
| Physical lift shadow | `.cover-card-img`, `.trend-card .art`, `.tabbar` | `box-shadow: 0 18px 30px -6px rgba(0,0,0,.85)` | DLS Owner | Deep directional shadow for physical depth — not a state glow; one-shot structural |
| Popular badge gradient end | `.upsell-popular` | `#ffcf5c` | Pass Card Owner | Gradient pair for `--popular-gold`; no token for the lighter stop; approved in colour-governance.md §9 |
| Selected chip tint | `.platform-chip.selected` | `color-mix(in srgb, var(--jio) 8%, var(--chip-bg))` | Chip Owner | Bespoke dark-green selected surface; `color-mix` is token-safe (uses `--jio` and `--chip-bg`) |
| Genre tile glow | `.genre-tile.selected` | `0 6px 28px rgba(0,168,89,.45)` | Genre Tile Owner | Extended glow layered with `--jio` border; outer `rgba` layer has no token equivalent |
| OTP glow | `.otp-box.active` | `0 0 0 3px rgba(0,168,89,.15)` | OTP Owner | Slightly tighter than `--jio-glow` (0.35) for digit-box focus; optical tuning |
| Progress dot | `.pp-dot` | `height: 3px; border-radius: 2px` | DLS Owner | Sub-grid decorative element; 4px would be too heavy at this scale |
| Rail head to cards gap | `.rail-head` | `margin-bottom: var(--space-1-5)` | Rail Owner | Structural spacing between heading and scroll row; not part of a parent stack |
| TV primary button min-width | `.btn-primary` (TV) | `min-width: 240px` | Button Owner | Minimum readable CTA width on 1080p canvas; layout constant from screens-and-navigation.md §12 |
| GFF font size | `.gff-label` | `font-size: 8.5px` | DLS Owner | Sub-scale decorative label inside constrained GFF card; approved exception in typography.md §10 |
