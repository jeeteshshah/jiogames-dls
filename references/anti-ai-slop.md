# JioGames Anti-AI-Slop Guide

**Your UI must not look like a generic dark-mode SaaS app.**

AI models default to "dark mode" by putting a white-card app on a dark grey background. That is not JioGames. JioGames is a gaming platform with depth, glow, atmosphere, and brand-specific design decisions.

---

## The Biggest JioGames AI Tells

### 1. Soft grey shadows for state

```css
/* ❌ Generic AI dark-mode soft shadow on everything */
.card { box-shadow: 0 4px 16px rgba(0,0,0,.6); }

/* ✅ JioGames — glow for state */
.card.selected {
  box-shadow: 0 0 0 2px var(--jio), 0 6px 28px rgba(0,168,89,.45);
}

/* ✅ JioGames — deep directional shadow ONLY for physical lift */
.poster.featured {
  box-shadow: 0 18px 30px -6px rgba(0,0,0,.85);
}
```

State changes glow with brand colour. Black shadows are reserved for lifting a physical object (poster, tab bar, focused card) off the canvas — deep and directional, never the soft 4px SaaS blur. Don't put a soft grey shadow on a resting card.

---

### 2. Using blue/purple as the accent

The #1 AI tell: `#6366f1`, `#8b5cf6`, `#3b82f6` as primary accent.

**JioGames is green end-to-end. No exceptions, no blue anywhere.**

Every accent comes from the green family: `--jio` (`#00A859`) for standard, the brighter `--ultimate` (`#00cc65`) for the Ultimate Pass tier. The Ultimate Pass is **not** blue — it is a deeper, richer green than the Mobile pass. Never introduce blue or purple for buttons, inputs, active states, links, or premium tiers.

---

### 3. White cards on dark backgrounds

```css
/* ❌ Generic "dark mode" — white cards on dark bg */
.card { background: #1a1a2e; border: 1px solid #333; }

/* ✅ JioGames — layered dark surfaces, coloured borders */
.card { background: #111115; border: 1px solid rgba(255,255,255,.08); }
.card.active { border-color: rgba(0,168,89,.25); }
```

Cards are not lifted white rectangles. They are slightly lighter dark surfaces with subtle transparent borders.

---

### 4. Flat buttons with `border-radius: 8px`

```css
/* ❌ Generic rounded-rect button */
.btn { border-radius: 8px; background: #00A859; }

/* ✅ JioGames — full pill */
.btn { border-radius: 100px; background: var(--jio); color: #000; }
```

Primary buttons are always pills (`border-radius: 100px`). Never rectangular.

---

### 5. Light/white backgrounds anywhere

JioGames is **dark-only**. No exceptions.

```css
/* ❌ NEVER */
body { background: #ffffff; }
.modal { background: #f9fafb; }
.header { background: white; }

/* ✅ Always dark */
body { background: var(--bg); } /* #06080F */
.modal { background: var(--sheet-bg); }
.header { background: rgba(6,8,15,.92); }
```

If you ever find yourself reaching for a light colour for a background — stop. Ask if the element truly needs contrast from the dark bg, then use a slightly-lighter-dark surface.

---

### 6. Missing letter-spacing on headings

```css
/* ❌ Flat, boring */
h1 { font-size: 32px; font-weight: 900; }

/* ✅ JioGames — tight, premium */
h1 { font-size: 32px; font-weight: 900; letter-spacing: -.6px; line-height: 1.15; }
```

Negative letter-spacing is the single biggest typography signal for "gaming / premium product." Without it everything looks like a blog post.

---

### 7. Using wrong font weight for headings

```css
/* ❌ Too light for gaming */
h2 { font-weight: 600; }

/* ✅ JioGames — always black weight for headings */
h2 { font-weight: 900; }
```

JioGames uses weight 900 (Black) for every heading, title, price, and card name. Weight 700 is for labels and buttons only. Weight 500 is for body copy. Never weight 600 for headings.

---

### 8. Generic card grid with equal whitespace

```css
/* ❌ SaaS grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 24px;
}

/* ✅ JioGames — horizontal scroll rails with snap */
.rail-scroll {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding: 0 var(--gutter);
}
```

JioGames content lives in **horizontal scroll rails**, not vertical card grids (on mobile/TV). Grids are acceptable on web desktop only, and even then should feel like rows.

---

### 9. Missing depth gradient on hero images

```css
/* ❌ Raw image with no treatment */
.hero { background-image: url(...); background-size: cover; }

/* ✅ JioGames — atmospheric gradient overlay */
.hero-overlay {
  background: linear-gradient(to bottom,
    rgba(6,8,15,.55) 0%,
    rgba(6,8,15,.10) 35%,
    rgba(6,8,15,.82) 68%,
    #06080f 100%);
}
```

Hero images always fade into the page background at the bottom. No hard edge.

---

### 10. Ignoring TV platform

Building for mobile and forgetting TV means:
- Font sizes too small to read from 3m
- No focus states (D-pad doesn't hover)
- Missing safe-zone margins (80px)
- Hover-only microinteractions that never trigger

Always add TV variants. At minimum: larger type, visible focus glow, safe-zone gutters.

---

## The JioGames Detector Checklist

Before shipping any JioGames UI, verify:

```
□ Background is #06080F or darker — not grey, not #1a1a2e, never white
□ Primary accent is #00A859 — no blue, no purple, no indigo
□ Ultimate Pass is green (#00cc65), NOT blue — deeper green than Mobile pass
□ All headings use font-weight: 900
□ Negative letter-spacing on all text ≥18px
□ Buttons are full pills (border-radius: 100px)
□ Active/selected states use green glow, not grey shadow
□ Hero images have the 4-stop gradient overlay
□ Content in horizontal rails with scroll-snap (mobile/TV)
□ TV: font sizes ≥22px, visible focus glow, 80px gutters
□ No white or light backgrounds anywhere
□ No generic indigo/violet/blue as primary colour
□ JioType is the only font — no Inter, no Outfit
```

---

## What Good JioGames UI Feels Like

- **Atmosphere** — dark, immersive, like the screen is a portal into the game world
- **Precision** — tight typography, controlled spacing, nothing accidental
- **Brand** — green accents that feel earned, not sprinkled everywhere
- **Depth** — layered surfaces, glowing borders, radial accents in pass cards
- **Speed** — spring animations, immediate feedback, snappy transitions

If your UI looks like it could be a generic streaming app or a SaaS dashboard — it's wrong. JioGames should feel like a gaming product.
