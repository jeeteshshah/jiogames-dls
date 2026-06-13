# JioGames Craft Details

> **Inherits `_core-rules.md`** — dark-only, JioType-only, token-first, no Lucide, no silent deviation rules are not repeated here.


Details that separate polished gaming UI from generic dark-mode apps.

---

## 1. The Glow + Shadow System

JioGames depth has **two distinct tools** — use the right one:

### Glow (coloured) — for state and brand

Active, selected, and focused states glow with brand colour spreading outward. Glow colours derive from the green accent (`--jio` or the brighter `--ultimate` green), never grey, never blue.

### Shadow (black) — for physical lift only

Real black shadows ARE used, but **only** to lift a physical object off the canvas: poster art over a Top-10 numeral, the floating tab bar, a focused brand card, hover lifts. These are deep and directional (`0 18px 30px -6px rgba(0,0,0,.85)`), not the soft 4px SaaS shadow.

### The distinction

| Use glow when… | Use black shadow when… |
|---|---|
| Element becomes active/selected/focused | A card/poster needs to float above siblings |
| Conveying "this is interactive / branded" | The tab bar / sheet hovers over content |
| Input focus, genre select, TV focus ring | Top-10 poster lifts off its rank numeral |

### Rules

- Never use a soft grey `0 4px 8px rgba(0,0,0,.1)` shadow — that's SaaS/light-mode thinking
- State changes (active/selected/focus) use **coloured glow**, not shadow
- Physical lift uses **deep directional black shadow** with negative spread
- Combine both on focused cards: `0 20px 48px rgba(0,0,0,.75), 0 0 32px var(--jio-glow)` (use `var(--ultimate-glow)` for Ultimate Pass surfaces)

### Glow Cheat Sheet

```css
/* Input focus */
.input:focus-within {
  border-color: var(--jio);
  box-shadow: 0 0 0 3px rgba(0,168,89,.14);
}

/* Selected card (genre tile) */
.card.selected {
  border-color: var(--jio);
  box-shadow: 0 0 0 2px var(--jio), 0 6px 28px rgba(0,168,89,.45);
}

/* GFF left rail glow */
.gff-rail {
  box-shadow: 0 0 8px rgba(0,232,112,.5);
}

/* TV focused element */
.focusable:focus {
  box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4);
}

/* Ultimate pass elements */
.ultimate:focus {
  box-shadow: 0 0 0 3px var(--ultimate), 0 0 24px var(--ultimate-glow);
}
```

---

## 2. Depth via Background Layering

Since dark UI has no light/shadow system, depth is communicated through background values:

```
Deepest:  #06080F   (page)
          #0e1118   (sheet)
          #111115   (card)
          #0c0f14   (chip)
Lightest: rgba(255,255,255,.055)  (input)
```

Never place a `#111115` element on a `#111115` background — increase contrast by at least 2 levels.

---

## 3. Hero Image Treatment

### Mobile hero overlay

```css
.hero-bg {
  position: absolute; inset: 0;
  background-size: cover;
  background-position: center;
}
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom,
    rgba(6,8,15,.55) 0%,
    rgba(6,8,15,.10) 35%,
    rgba(6,8,15,.82) 68%,
    #06080f 100%);
}
```

### Image filters on non-selected state

```css
/* Genre tile: desaturate until selected */
.genre-tile img {
  filter: brightness(.55) saturate(.6);
  transition: filter .35s;
}
.genre-tile.selected img {
  filter: brightness(.95) saturate(1.15);
}
```

### Image aspect ratios

| Card type | Ratio |
|---|---|
| Wide/landscape | `16/9` |
| Portrait/cover | `2/3` |
| Square | `1/1` |
| Hero (full screen) | `100vw × 58vh` (mobile), `100% × 100%` (TV) |

Always set explicit `aspect-ratio` — prevents layout shift.

---

## 4. Focus States

### Mobile (`:focus-visible`)

```css
/* Use focus-visible, never bare :focus */
.btn:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0,168,89,.4);
}

/* Never remove focus without replacement */
/* ❌ .btn:focus { outline: none; } */
```

### TV (D-pad / keyboard navigation)

TV **requires** visible focus — it's the only navigation method.

```css
.focusable {
  transition: transform .15s var(--spring),
              box-shadow .15s,
              border-color .15s;
}
.focusable:focus {
  outline: none;
  border-color: var(--jio);
  box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4);
  transform: scale(1.05);
  z-index: 1;
}
/* No hover on TV */
@media (hover: none) {
  .focusable:hover:not(:focus) {
    transform: none;
    box-shadow: none;
    border-color: var(--border);
  }
}
```

TV focus management rules:
- Every interactive element must be `tabindex="0"` or a native focusable
- Focus ring must always be visible — never hidden
- When a rail is focused, auto-focus the first card
- Maintain focus position when content updates

---

## 5. Touch & Mobile Craft

```css
/* Remove 300ms tap delay */
* { touch-action: manipulation; }

/* Intentional tap highlight (not disabled) */
button, a, [role="button"] {
  -webkit-tap-highlight-color: rgba(0,168,89,.1);
}

/* Sheet scroll lock */
.bottom-sheet, .modal {
  overscroll-behavior: contain;
}
```

---

## 6. Radial Glow Accents (Pass Cards)

Pass cards have a top-right radial glow. Recreate with `::before` pseudo-element:

```css
/* Mobile pass corner glow */
.pass-mobile::before {
  content: '';
  position: absolute; top: -40px; right: -40px;
  width: 160px; height: 160px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,168,89,.18) 0%, transparent 70%);
  pointer-events: none;
}

/* Ultimate pass corner glow (brighter green than Mobile pass) */
.pass-ultimate::before {
  content: '';
  position: absolute; top: -60px; right: -30px;
  width: 200px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,232,112,.2) 0%, transparent 65%);
  pointer-events: none;
}

/* Page-level glow (single-pass immersive screen) */
.page-glow-green::before {
  content: '';
  position: absolute; top: -120px; left: -80px;
  width: 420px; height: 420px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,200,100,.22) 0%, rgba(0,168,89,.08) 45%, transparent 70%);
  pointer-events: none; z-index: 0;
}
```

---

## 7. Scrollable Rails

```css
.rail-scroll {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding: 0 var(--gutter);
  scroll-padding-left: var(--gutter);
  -webkit-overflow-scrolling: touch;
}
.rail-scroll::-webkit-scrollbar { display: none; }
```

Cards must have `scroll-snap-align: start` for smooth snapping.

---

## 8. Performance

- Use `will-change: transform` on animated screens (`will-change: transform`)
- Prefer `transform` and `opacity` for animations — avoid animating layout properties
- Hero bg images: `fetchpriority="high"` on above-fold, `loading="lazy"` below
- Always set `width`/`height` on `<img>` to prevent layout shift
- Large game lists (50+ items): use `content-visibility: auto`

---

## 9. Content Copy Rules for Gaming Context

| Rule | Example |
|---|---|
| Active voice | "Play Now" not "Game Can Be Started" |
| Short, punchy | "Free with Jio" not "Available at no cost with your Jio subscription" |
| Numbers, not words | "500+ games" not "hundreds of games" |
| Platform labels always uppercase | "PC", "MOBILE", "CONSOLE" |
| Genre eyebrows in `var(--jio)` colour | "ACTION ADVENTURE" in green |
| CTA on green button: black text | "Start Playing" in `#000` |

---

## 10. Anti-Patterns Checklist

- [ ] No white or light backgrounds anywhere
- [ ] No `outline: none` without glow replacement
- [ ] No heavy grey `box-shadow` — use coloured glow
- [ ] Images have explicit dimensions
- [ ] Rails have `scroll-snap-type: x mandatory`
- [ ] No `transition: all`
- [ ] TV: every interactive element is keyboard-focusable
- [ ] TV: no hover-only states (use focus)
- [ ] `overscroll-behavior: contain` on sheets/modals
- [ ] `touch-action: manipulation` on root

---

## Pre-Ship Checklist

- [ ] Input focus: glow `box-shadow`, not outline
- [ ] Selected cards: green border + glow
- [ ] Pass cards: radial glow in `::before`
- [ ] Hero images: correct gradient overlay
- [ ] Genre tiles: desaturated default, saturated when selected
- [ ] TV: all interactives focusable with visible glow ring
- [ ] Scrollable rails: snap, no scrollbar, `touch-action`
- [ ] Performance: `will-change` on screens, lazy images below fold
