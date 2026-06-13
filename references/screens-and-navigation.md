# JioGames Screens & Navigation Governance

> **Inherits `_core-rules.md`** — dark-only, JioType-only, token-first, no Lucide, no silent deviation rules are not repeated here.


> App shell, navigation, screen patterns, and cinematic techniques — all using design system tokens. Raw px and hex literals in screen CSS are violations; use `var(--token)` and reference approved layout constants (§12) only where no token exists.

**Structure**

1. Core Principles
2. Screen Inventory
3. App Shell & Safe Areas
4. Navigation System
5. Screen Decision Tree ← *most important*
6. Home Screen Patterns
7. Game Detail Page
8. Pass & Upgrade Screens
9. Cinematic Hero Techniques
10. Rail System
11. Platform Rules
12. Approved Layout Constants
13. Screen QA Checklist
14. Pre-Ship Release Gate

---

# 1. Core Principles

1. **Token-first.** All spacing, colour, sizing, radius, and motion use `var(--token)`. Raw px/hex in screen CSS = violation unless listed in §12 (Approved Layout Constants).
2. **JioType only.** No Rajdhani, Barlow, or any non-JioType font on any screen. Award/editorial rails that previously used non-JioType fonts require an approved RFC before use (see §12).
3. **Dark only.** No white or light surfaces on any screen, including game detail, sheets, and overlays.
4. **Screens compose contracted components.** Button, Card, Rail, Tab Bar, Pass Card, Genre Tile, Toast — use the contracts in component-contracts.md. Do not re-implement.
5. **Scroll performance.** Only `transform` and `opacity` in scroll-linked animations. No `top`/`left` parallax that triggers layout.
6. **`prefers-reduced-motion` required** on all ambient and entrance animations.

---

# 2. Screen Inventory

| Screen | Mobile | Web | TV | Notes |
|---|:---:|:---:|:---:|---|
| Login / OTP | ✓ | ✓ | — | Phone-number entry, OTP verification |
| Genre / Platform prefs | ✓ | ✓ | — | Post-login onboarding |
| Home | ✓ | ✓ | ✓ | Rail system, hero, tab bar |
| Game Detail | ✓ | ✓ | ✓ | Hero, play CTA, metadata, related content |
| Pass Found | ✓ | ✓ | — | Post-login pass discovery |
| Pass Upsell / Upgrade | ✓ | ✓ | — | Plan comparison, upgrade CTA |
| Continue / Jump Back In | ✓ | ✓ | ✓ | State 9 only — personalised returning user |
| Category / Browse | ✓ | ✓ | ✓ | Genre or platform filtered rail view |
| Search | ✓ | ✓ | ✓ | Full-screen search overlay |

---

# 3. App Shell & Safe Areas

**Canonical phone frame: `393×852px`** — use `var(--frame-mobile-w)` / `var(--frame-mobile-h)`.

```css
.phone {
  width: 100%; max-width: var(--frame-mobile-w);
  height: 100svh; max-height: var(--frame-mobile-h);
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  background: var(--bg);
}
.scroller {
  position: absolute; inset: 0;
  overflow-y: auto;
  scrollbar-width: none;
  overscroll-behavior: contain;
}
.scroller::-webkit-scrollbar { display: none; }
```

Safe area insets — already in `tokens.css` as `--safe-top` and `--safe-bot`. Use `var()`:

```css
padding-top: var(--safe-top);
padding-bottom: calc(var(--safe-bot) + var(--tab-bar-h) + var(--space-3));
```

### iOS status bar (faux)

44px is an approved layout constant (iOS physical constraint — see §12):

```css
.statusbar {
  position: sticky; top: 0; z-index: 50;
  height: 44px;                              /* approved layout constant — iOS safe area */
  padding: 0 var(--gutter);
  display: flex; align-items: center; justify-content: space-between;
}
```

---

# 4. Navigation System

## App Bar (auto-hiding home header)

```css
.appbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 40;
  display: flex; align-items: center;
  gap: var(--space-1-5);
  padding: var(--space-1-5) var(--gutter);
  transition: transform var(--dur-default) var(--spring),
              background var(--dur-default);
}
.appbar.header-hidden   { transform: translateY(-110%); }
.appbar.header-scrolled {
  background: rgba(0,0,0,.7);
  backdrop-filter: blur(14px);
}

.appbar .icon-btn {
  width: var(--ctrl-h-sm); height: var(--ctrl-h-sm);   /* 36px */
  min-width: var(--touch-min); min-height: var(--touch-min); /* 44px tap target */
  border-radius: 50%;
  background: rgba(255,255,255,.08);
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.appbar .icon-btn .dot {                     /* notification badge */
  position: absolute; top: 7px; right: 7px;
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--jio);
}
```

## Floating Pill Tab Bar

```css
.tabbar {
  position: absolute;
  bottom: var(--space-3);                    /* 24px — on-scale; 20px was banned */
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - var(--space-4));        /* 32px total inset = 2 × --space-2 */
  display: none;
  padding: var(--space-0-5) var(--space-2);  /* 4px 16px */
  background: rgba(14,17,25,.88);
  backdrop-filter: blur(28px) saturate(140%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--pill);
  box-shadow: 0 14px 40px -10px rgba(0,0,0,.7),
              inset 0 1px 0 rgba(255,255,255,.04);
  z-index: 45;
}
.tabbar.visible { display: flex; }

.tabbar .tab {
  flex: 1; height: var(--tab-bar-h);         /* 64px — from --tab-bar-h token */
  min-height: var(--touch-min);              /* 44px minimum target */
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: var(--space-0-5);                     /* 4px icon↔label gap */
  color: var(--icon-color-default);
  transition: color var(--dur-fast);
}
/* Solid glyph icons — fill only, no stroke rules */
.tabbar .tab svg { width: var(--icon-size-md); height: var(--icon-size-md); }
.tabbar .tab span { font-size: 10px; font-weight: 700; }
.tabbar .tab.active { color: var(--icon-color-active); }
```

### Sub-page tab bar variant

Circular back button + separate pill of tabs:

```css
.tabbar--sub .back-pill {
  width: var(--ctrl-h-sm);           /* 36px visual */
  height: var(--ctrl-h-sm);
  min-width: var(--touch-min);       /* 44px tap target */
  min-height: var(--touch-min);
  border-radius: 50%;
  /* Same glass treatment as main tab bar */
}
```

---

# 5. Screen Decision Tree

```
What are you building?
│
├── Post-login entry flow (new or returning user)
│     → Login → OTP → state-based branch (see FLOWS.md)
│     → Genre/prefs screen (state 1, 3, 7)
│     → Pass Found screen (state 2, 6)
│     → Home direct (state 4, 9)
│
├── Main browsable surface
│     → Home screen — hero + rail system + tab bar
│
├── Individual game
│     → Game Detail page (§7)
│
├── Pass management
│     → Pass Found screen (post-login discovery) — §8
│     → Upgrade sheet / upsell card (in-home) — §8
│
├── Personalised returning user
│     → Home with Continue rail (state 9) — §6
│
├── Content exploration
│     → Category / Browse screen — cinematic hero (§9) + rail grid
│
├── Deep-dive content list
│     → Full-screen search overlay
│     → Category detail with horizontal → grid switch (spacing-and-grid.md §6.2)
│
└── Cinematic / marquee hero moment
      → Cinematic Hero Techniques (§9)
```

---

# 6. Home Screen Patterns

### Hero structure

```css
.hero {
  position: relative;
  height: 70vw; min-height: 280px; max-height: 480px;
}
.hero .bg {
  position: absolute; inset: 0;
  background-size: cover; background-position: center top;
}
/* Gradient overlay — approved recipe from colour-governance.md §9 */
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom,
    rgba(6,8,15,.55) 0%,
    rgba(6,8,15,.1)  35%,
    rgba(6,8,15,.82) 68%,
    var(--bg) 100%);
}
.hero-content {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 0 var(--gutter) var(--hero-gap);
}
```

### Ken Burns push-in (approved ambient technique)

```css
.hero .bg {
  transform: scale(1.04);
  transition: transform 8s ease-out;
  filter: saturate(1.1) contrast(1.05);
}
/* Pause in reduced motion */
@media (prefers-reduced-motion: reduce) {
  .hero .bg { transition: none; transform: scale(1.04); }
}
```

### Continue rail ("Jump Back In") — State 9 only

```css
/* Screen-level layout constants — not DLS tokens (single-screen use) */
.continue-card {
  width: 210px;                              /* screen constant — see §12 */
  height: 128px;                             /* screen constant — see §12 */
  border-radius: var(--r4);
  scroll-snap-align: start;
  position: relative; overflow: hidden;
  transition: transform var(--dur-fast);
}
.continue-card:active { transform: scale(.96); }
.cc-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,.9), transparent);
}
```

---

# 7. Game Detail Page

### Top bar (transparent → frosted on scroll)

```css
.gd-topbar {
  position: fixed; top: 0; left: 0; right: 0; z-index: 40;
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--space-1-5) var(--gutter);
  transition: background var(--dur-default);
}
.gd-topbar.scrolled {
  background: rgba(6,8,15,.88);
  backdrop-filter: blur(16px);
}
.gd-icon-btn {
  width: var(--ctrl-h-sm); height: var(--ctrl-h-sm);  /* 36px visual */
  min-width: var(--touch-min); min-height: var(--touch-min); /* 44px target */
  border-radius: 50%;
  background: rgba(0,0,0,.45);
  backdrop-filter: blur(8px);
}
.gd-avatar {
  width: var(--ctrl-h-sm); height: var(--ctrl-h-sm);  /* 36px */
  border-radius: 50%;
  background: linear-gradient(135deg, var(--jio), var(--mint));
  border: 2px solid var(--border);
}
```

### Hero

```css
.gd-hero {
  height: 55vw; min-height: 220px; max-height: 340px;
  position: relative;
}
.gd-hero-grad {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 40%, var(--bg) 100%);
}
```

### Typography (use `.text-*` classes — no hardcoded sizes)

```css
/* Apply .text-display or h1 role to game title */
.gd-title   { font-weight: 900; color: var(--text); letter-spacing: -1px; }
/* Apply .text-section-title to section headings */
.gd-section-head { font-weight: 900; }
.gd-section-head em { font-style: italic; font-weight: 500; color: var(--jio); }
```

### Primary action row (Play + heart)

```css
.gd-play-btn {
  flex: 1; height: var(--ctrl-h);            /* 54px — primary control height */
  border-radius: var(--pill);
  background: var(--jio); color: var(--text-inv);
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  gap: var(--space-1);
}
.gd-play-btn svg { fill: var(--text-inv); }
.gd-heart-btn {
  width: var(--ctrl-h); height: var(--ctrl-h);  /* 54px — matches play btn */
  border-radius: 50%;
  background: rgba(255,255,255,.08);
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
}
.gd-heart-btn.liked {
  background: var(--jio-soft);
  border-color: var(--jio);
}
.gd-heart-btn.liked svg { fill: var(--jio); }
```

### Sub-components

| Component | Key tokens |
|---|---|
| Screenshot card `.gd-ss-card` | `width: 140px` (§12 constant) · `aspect-ratio: 16/9` · `border-radius: var(--r7)` · `scroll-snap-align: start` |
| Watch/play card `.gd-wlp-card` | `width: 220px` (§12 constant) · `border-radius: var(--r7)` · `background: var(--card-bg)` |
| Description `.gd-desc-text` | 3-line clamp · `.gd-read-more` `font-weight: 700` `color: var(--jio)` |
| Accordion `.gd-acc-btn` | `border-radius: var(--r3)` · `.open` top-only radius · `.gd-acc-plus` `rotate(45deg)` · body `max-height: 0→200px` |
| More-like-this `.gd-more-card` | 2-col grid · `aspect-ratio: 2/3` · `border-radius: var(--r7)` |

### Metadata patterns

```css
/* Gold star rating — --gold-laurel, not green */
.star { color: var(--gold-laurel); font-weight: 700; }
.star::before { content: "★ "; }

/* Dot separator */
.gd-meta-dot { width: 3px; height: 3px; border-radius: 50%; background: var(--text3); }

/* Age rating pill */
.gd-age-pill {
  font-size: 11px; font-weight: 700;
  border: 1.5px solid rgba(255,255,255,.6);
  border-radius: var(--r1); padding: 1px var(--space-0-5);
}

/* Genre line leading dash */
.genre-line::before {
  content: ''; display: inline-block;
  width: 18px; height: 1px; background: var(--jio-2);
  vertical-align: middle; margin-right: var(--space-1);
}

/* Key-value detail grid */
.gd-detail-key { font-size: 11px; font-weight: 500; color: var(--text2); }  /* 500 not 400 */
.gd-detail-val { font-size: 13px; font-weight: 700; color: var(--text); }
```

### Detail sheet (slide-up modal)

```css
.detail-sheet {
  position: absolute; bottom: 0; left: 0; right: 0;
  height: 78%;                               /* percentage layout — see §12 */
  background: var(--surface-1);
  border-radius: var(--r9) var(--r9) 0 0;   /* was 24px — now --r9 (28px) */
  transform: translateY(105%);
  transition: transform var(--dur-sheet) var(--spring);
  overscroll-behavior: contain;
}
.detail-sheet.open { transform: translateY(0); }
```

---

# 8. Pass & Upgrade Screens

## Pass-Found Screen

```css
.pass-hero { padding-top: 56px; position: relative; }  /* 56px: §12 constant */

.pass-hero-glow {
  position: absolute; filter: blur(40px);
  background: radial-gradient(circle, var(--jio-glow), transparent);
}
.pass-icon-wrap {
  width: var(--space-8); height: var(--space-8);   /* 64px = --space-8 */
  border-radius: 50%; position: relative;
}
.pass-icon-wrap::before,
.pass-icon-wrap::after {                             /* double pulse rings */
  content: ''; position: absolute; inset: 0;
  border-radius: 50%; border: 1px solid var(--jio);
  animation: pulse-ring 2s ease-out infinite;        /* keyframe in motion.md §6 */
}
.pass-icon-wrap::after { animation-delay: 1s; }

/* Pass card on found screen */
.pf-card {
  background: linear-gradient(145deg, #1a1a1f, #111115 55%, #080809);
  border: 1px solid rgba(0,168,89,.2);
  border-radius: var(--r5); padding: var(--space-3) var(--space-3);
  position: relative;
}
.pf-badge {
  border-radius: var(--pill);
  background: var(--jio-soft);
  border: 1px solid rgba(0,168,89,.22);
  color: var(--jio);
  font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: .5px;
}
```

## Pass Status Strip (home, when pass active)

```css
.pass-strip {
  background: linear-gradient(90deg, rgba(0,168,89,.12), transparent);
  border-radius: var(--r4);
  display: flex; align-items: center;
  gap: var(--space-1-5);
  padding: var(--space-1-5) var(--component-padding);
}
.ps-days-val { font-size: 20px; font-weight: 700; color: var(--jio); }
.ps-days-lbl { font-size: 11px; font-weight: 500; color: var(--text2); }
```

## Inline Upgrade Banner (dismissible)

```css
.pib-inner {
  background: linear-gradient(135deg, #060e08, #071008);
  border-radius: var(--r5);
  position: relative; overflow: hidden;
}
.pib-inner::before {                               /* green top-accent line */
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--jio), transparent);
}
.pib-icon {
  width: var(--space-5); height: var(--space-5);   /* 40px = --space-5 */
  border-radius: var(--r3);
}
```

### Banner enter/exit animations

Using `transform + opacity` — never `max-height` (triggers layout reflow):

```css
@keyframes banner-slide-down {
  from { opacity: 0; transform: translateY(-8px) scaleY(.95); transform-origin: top; }
  to   { opacity: 1; transform: translateY(0) scaleY(1); }
}
@keyframes banner-slide-up {
  from { opacity: 1; transform: translateY(0) scaleY(1); transform-origin: top; }
  to   { opacity: 0; transform: translateY(-8px) scaleY(.95); }
}
.pib-inner.entering { animation: banner-slide-down var(--dur-enter) var(--spring) both; }
.pib-inner.exiting  { animation: banner-slide-up  var(--dur-default) var(--ease-out) both; }
```

## End-Sheet Upgrade Drawer

```css
.end-sheet {
  background: linear-gradient(180deg, #0b1309, #04080b);
  border-radius: var(--r9) var(--r9) 0 0;    /* was 24px — now --r9 (28px) */
  transform: translateY(100%);
  transition: transform var(--dur-sheet) var(--spring);
  overscroll-behavior: contain;
}
.end-sheet.open { transform: translateY(0); }

.es-cta-p {
  height: var(--ctrl-h);                     /* 54px — primary CTA */
  border-radius: var(--pill);
  background: var(--jio); color: var(--text-inv);
}
.es-cta-s {
  height: var(--ctrl-h-sm);                  /* 36px — secondary, pad to 44px target */
  padding-block: calc((var(--touch-min) - var(--ctrl-h-sm)) / 2);
  border-radius: var(--pill);
  background: none; border: 1px solid var(--border);
}
.btn-maybe {
  height: var(--ctrl-h-ghost);               /* 40px — ghost/skip */
  background: none; color: var(--text3);
  border: none; border-radius: var(--pill);
}
```

## Nested Upgrade Card (Mobile ↔ Ultimate tabs)

`.nup-outer` → `.nup-tabs` (2-col) → `.nup-tab.active` → perks rail → `.nup-cta`.

**Ultimate accent: `var(--ultimate)` (`#00cc65`)** — canonical bright green. Never blue, never purple. JioGames premium stays in the green family end-to-end.

---

# 9. Cinematic Hero Techniques

Use these on marquee/landing surfaces, category heroes, and editorial features. Never on utility screens (search, settings, account).

## Category Hero — Aurora + Sparkle + Floating Orbs

Self-contained 560px atmospheric fold: eyebrow + title 130px · visual 230px · rail 170px.

```css
.cathero { height: 560px; isolation: isolate; }         /* §12 constant */
.cathero-bg { top: -15%; height: 130%; will-change: transform; } /* parallax overscan */

.aurora {
  filter: blur(60px); opacity: .7; border-radius: 50%;
  animation: auroraDrift1 12s linear infinite;
}
@keyframes auroraDrift1 {
  50% { transform: translate(40px, -30px) scale(1.2); }
}

.spark {
  width: 4px; height: 4px; background: var(--text);
  box-shadow: 0 0 8px var(--text);
  animation: sparkleAnim 4s linear infinite;
}
@keyframes sparkleAnim {
  0%,100% { opacity: 0; transform: scale(.4); }
  50%     { opacity: 1; transform: scale(1); }
}

.cathero-orb {
  background: radial-gradient(circle at 32% 30%, #FFE49A, #FF7B3A 70%);
  box-shadow: 0 0 60px rgba(255,194,61,.45),
              inset 0 -8px 20px rgba(180,40,0,.4);
  animation: orbFloat 6s linear infinite;
}
@keyframes orbFloat {
  50% { transform: translate(8px, -12px) rotate(8deg); }
}

/* Reduced motion — all ambient stops */
@media (prefers-reduced-motion: reduce) {
  .aurora, .spark, .cathero-orb { animation: none; }
  .cathero-bg { will-change: auto; }
}
```

## Brand Card — Focus-Scale Rail

Per-brand glow uses raw `rgba` — approved partner-brand exception (see §12):

```css
.brand-card {
  width: 140px; height: 187px;               /* §12 layout constants */
  border-radius: var(--r7);
  opacity: .82;
  transition: transform var(--dur-default) var(--spring-bounce),
              opacity var(--dur-fast),
              box-shadow var(--dur-fast);
}
.brand-card.focused {
  transform: scale(1.07); opacity: 1;
  box-shadow: 0 20px 48px rgba(0,0,0,.75),
              0 0 0 1.5px rgba(255,255,255,.22),
              0 0 32px var(--bc-glow);        /* per-brand colour */
}
/* Per-brand glow: raw rgba allowed for partner artwork — see §12 */
.brand-card.bc-steam   { --bc-glow: rgba(102,192,244,.7); }
.brand-card.focused .bc-logo { filter: drop-shadow(0 0 14px var(--bc-glow)); }
```

## Top-10 Outline Numeral

```css
.trend-card .rank {
  font-size: 140px; font-weight: 900;         /* §12 constant — display numeral */
  color: transparent;
  -webkit-text-stroke: 2px rgba(255,255,255,.7);
  margin-right: -12px;                        /* optical — poster overlaps numeral */
}
.trend-card .art {
  aspect-ratio: 2/3;
  box-shadow: 0 0 0 3px var(--bg),            /* separation ring */
              0 18px 30px -6px rgba(0,0,0,.85);
}
```

## Shimmer Sweep (highlight "new" cards)

Shimmer keyframe defined in motion.md §6. Use here via reference:

```css
.shimmer::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(110deg,
    transparent 30%,
    rgba(255,255,255,.25) 50%,
    transparent 70%);
  mix-blend-mode: screen;
  /* 3s sweep + 5s rest = 8s total cycle */
  animation: shimmer 8s linear infinite;
}
@media (prefers-reduced-motion: reduce) {
  .shimmer::after { animation: none; display: none; }
}
```

## Additional Keyframes (screen-specific)

```css
@keyframes wb-breathe     { 50% { opacity: 1; transform: scale(1.08); } }
@keyframes wb-ring-expand { to { transform: scale(1.5); opacity: 0; } }
@keyframes nup-dot-pulse  { 50% { box-shadow: 0 0 0 6px rgba(0,168,89,0); } }
@keyframes rise           { to { transform: translateY(-700px) scaleX(.5); opacity: 0; } }
@keyframes draw-check     { to { stroke-dashoffset: 0; } }
@keyframes pulse          { 50% { opacity: .4; transform: scale(.7); } }
@keyframes sweep          { to { background-position: -200% 0; } }
@keyframes riseIn         { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
```

---

# 10. Rail System

Full rail governance (trailing gutter, scroll-snap, grid switch rules) lives in spacing-and-grid.md §7. Summary for screens:

```css
.rail-scroll {
  display: flex; gap: var(--card-gap);
  overflow-x: auto; scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding-left: var(--gutter);
}
.rail-scroll > :last-child { margin-right: var(--gutter); } /* trailing spacer */
```

**Rail heading pattern:**

```css
.rail-head {
  padding: 0 var(--gutter);
  margin-bottom: var(--space-1-5);
  display: flex; align-items: center; justify-content: space-between;
}
/* Apply .text-rail-title to heading element */
.rail-head em { font-style: italic; font-weight: 500; color: var(--jio); }

.view-all-btn {
  height: var(--ctrl-h-sm);                  /* 36px */
  padding: 0 var(--space-1-5);
  border-radius: var(--pill);
  background: var(--glass-1);
  border: 1px solid var(--border-subtle);
  font-size: 12px; font-weight: 700; color: var(--text2);
}
```

**Title-in-art rule:** when card artwork bakes in the game title (editorial/world/indie/vault rails), hide the text overlay. Don't double-label.

---

# 11. Platform Rules

### Web (≥768px)

```css
@media (min-width: 768px) {
  /* Full-width container, centred */
  .page-container {
    max-width: var(--container-web);
    margin-inline: auto;
    padding-inline: var(--gutter);
  }

  /* App bar becomes sticky site header */
  .site-header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(6,8,15,.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0 var(--gutter);
    height: var(--app-bar-h);               /* 64px */
    display: flex; align-items: center;
    gap: var(--space-3);
  }

  /* Tab bar → horizontal nav in header (not floating pill) */
  .tabbar { display: none; }

  /* Hero scales up — cap at 560px */
  .hero { max-height: 560px; }

  /* Rails may become grid for dense surfaces */
  /* See colour-governance.md §6.2 — editorial stays rail, browse/library → grid */
}
```

### TV (≥1280px, ≥720px tall)

```css
@media (min-width: 1280px) and (min-height: 720px) {
  /* Safe zone */
  .page-container { padding: var(--tv-safe); }

  /* No tab bar — D-pad navigation */
  .tabbar { display: none; }

  /* No bottom sheet or end-sheet — full-screen patterns only */
  .bottom-sheet, .end-sheet, .detail-sheet { display: none; }

  /* No backdrop-filter — performance */
  .appbar.header-scrolled { backdrop-filter: none; }
  .gd-topbar.scrolled { backdrop-filter: none; }

  /* No ambient cinematic loops */
  .aurora, .spark, .cathero-orb { animation: none; }

  /* Focus ring on all interactive elements — from component-contracts.md */
  .focusable:focus {
    outline: none;
    border-color: var(--jio);
    box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4);
    transform: scale(1.05);
    transition: transform var(--dur-fast) var(--spring), box-shadow var(--dur-fast);
    z-index: 1;
  }
}
```

---

# 12. Approved Layout Constants

These dimensions have no token equivalent — they are screen-level or physical constraints. Use exactly these values; they are not arbitrary.

| Constant | Value | Location | Reason |
|---|---:|---|---|
| Status bar height | `44px` | `.statusbar` | iOS physical safe-area height |
| Pass-found hero padding-top | `56px` | `.pass-hero` | Optical balance above pass icon |
| Category hero height | `560px` | `.cathero` | Editorial fold: 130+230+170+30 |
| Continue card width | `210px` | `.continue-card` | State-9 rail — single-screen constant |
| Continue card height | `128px` | `.continue-card` | State-9 rail — single-screen constant |
| Brand card width | `140px` | `.brand-card` | Partner logo card width |
| Brand card height | `187px` | `.brand-card` | 4:3 ish card proportion |
| Screenshot card width | `140px` | `.gd-ss-card` | Game detail screenshot rail |
| Watch/play card width | `220px` | `.gd-wlp-card` | Game detail video rail |
| Detail sheet height | `78%` | `.detail-sheet` | Fills most of screen, leaves hero peek |
| TV primary button min-width | `240px` | `.btn-primary` (TV) | Minimum readable CTA width on 1080p canvas |
| Top-10 rank font-size | `140px` | `.trend-card .rank` | Decorative outline numeral — display only |
| Partner brand glow | `rgba(per-brand)` | `.brand-card.bc-*` | Partner artwork colour — raw rgba approved for partner glow only |

### Non-JioType font exception

The Awards rail previously used Rajdhani and Barlow fonts ("Secondary Type System"). This is a **governance violation** under the JioType-only rule. It has been removed from this document. Reinstatement requires an RFC with DLS owner approval.

---

# 13. Screen QA Checklist

| Check | Required |
|---|---|
| All spacing uses `var(--space-*)` or layout alias tokens | Yes |
| All colours use tokens — raw hex only in approved gradient recipes or §12 partner glow | Yes |
| All button/CTA heights use `var(--ctrl-h)`, `var(--ctrl-h-sm)`, `var(--ctrl-h-ghost)` | Yes |
| Icon buttons have `min-width/min-height: var(--touch-min)` for tap area | Yes |
| All radius values use `var(--r*)` or `var(--pill)` — no raw `px` | Yes |
| `font-weight: 400`, `600`, `800` absent — only 300/500/700/900 | Yes |
| Non-JioType fonts absent — awards rail RFC required | Yes |
| Sheets and drawers use `var(--r9)` top-radius | Yes |
| Tab bar `bottom` uses `var(--space-3)` — not raw `20px` | Yes |
| `banner-slide-down/up` uses `transform + opacity` — not `max-height` | Yes |
| All ambient animations (`aurora`, `breathe`, marquee) pause in `prefers-reduced-motion` | Yes |
| TV: no backdrop-filter, no ambient loops, all elements focusable | If TV in scope |
| `tokens/validate.sh` passes with exit 0 | Yes |

---

# 14. Pre-Ship Release Gate

> A screen ships only if:

- [ ] Every token is sourced from `tokens.css` — no raw hex or px except §12 constants
- [ ] All contracted components composed from component-contracts.md — not re-implemented
- [ ] Touch targets meet `var(--touch-min)` — icon buttons padded, not inflated
- [ ] Non-JioType fonts absent
- [ ] Sheets and modals use `var(--r9)` top-radius, `overscroll-behavior: contain`
- [ ] All ambient/cinematic animations have `prefers-reduced-motion` fallback
- [ ] TV in scope: no backdrop-filter, no ambient loops, focus ring on all interactives
- [ ] Layout constants from §12 used for dimensions that have no token equivalent
- [ ] `tokens/validate.sh` passes with exit 0
