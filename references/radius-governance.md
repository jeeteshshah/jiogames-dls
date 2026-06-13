# JioGames Radius Governance

> **Inherits `_core-rules.md`** — dark-only, JioType-only, token-first, no Lucide, no silent deviation rules are not repeated here.


> Every component has one canonical radius token. If a screen uses a different value for the same component, that is drift — not a design decision.

Radius is not decoration. In JioGames' dark UI, radius communicates **layer depth**: smaller radius for artwork-led surfaces, larger radius for interactive chrome, maximum pill for CTAs and action chips. The scale runs from `--r1` (8px) to `--r9` (28px) plus `--pill` (100px).

**Structure**

1. Radius Scale
2. Component → Radius Canonical Map
3. Decision Tree
4. Inner Radius Rule (nesting)
5. Forbidden Patterns
6. Platform Rules
7. Radius QA Checklist
8. Pre-Ship Release Gate

---

# 1. Radius Scale

All tokens live in `tokens/tokens.json`, generated into `tokens/tokens.css`.

| Token | Value | Tier | Primary use |
|---|---:|---|---|
| `--r1` | `8px` | XS | Icon badges, progress pip, tiny indicators |
| `--r2` | `10px` | S | Marquee / feature hero cards (art-led, wide) |
| `--r3` | `12px` | S+ | GFF card, info panels, toast/snackbar |
| `--r4` | `14px` | M | Landscape game cards, square cards, OTP boxes, platform chips |
| `--r5` | `16px` | M+ | Input fields, genre tiles, cover-card image |
| `--r6` | `18px` | L | USP tiles |
| `--r7` | `20px` | L+ | Pass cards, upsell cards, large editorial cards |
| `--r8` | `22px` | XL | Reserved — oversized feature surfaces, approved case-by-case |
| `--r9` | `28px` | 2XL | Bottom sheet top corners only |
| `--pill` | `100px` | ∞ | Primary buttons, small CTAs, action chips, pill badges |

**Reading the tier:** higher tier = more interactive chrome, less raw artwork. Artwork-backed cards lean smaller (r2–r4). Interactive components lean larger (r5–r7). Sheets and modals use r9. Pills are full round.

---

# 2. Component → Radius Canonical Map

One component, one token. Deviations require a governance update.

| Component | Token | Notes |
|---|---|---|
| Primary button | `--pill` | Always full pill — never rectangular |
| Small CTA button | `--pill` | Same rule |
| Ghost / skip button | `--pill` | Same rule |
| Action chip | `--pill` | Horizontal filter/action chip |
| Platform chip (selectable) | `--r4` | Taller tile format — pill would look wrong |
| Number-confirmed pill | `--pill` | Inline phone number container |
| Popular badge | `--pill` | Small tag inline in pass card |
| Input field | `--r5` | Phone input, text fields |
| OTP box | `--r4` | Individual digit cell |
| Wide landscape card (16:9) | `--r4` | Artwork-led — smaller feels grounded |
| Square card (1:1) | `--r4` | Same family as landscape card |
| Cover portrait card image | `--r5` | Portrait artwork |
| Marquee / hero feature card | `--r2` | Larger canvas, smaller radius |
| Genre tile | `--r5` | Interactive overlay — larger than artwork card |
| Pass card (Mobile / Ultimate) | `--r7` | Premium surface — most rounded of all cards |
| Upsell card | `--r7` | Same tier as pass card |
| USP tile | `--r6` | Between card and pass |
| GFF (Did You Know) card | `--r3` | Compact info module |
| Info panel / secondary card | `--r3` | Low-elevation surface |
| Toast / snackbar | `--r3` | Small transient UI |
| Bottom sheet | `--r9` `--r9` `0` `0` | Top-left + top-right only; bottom is flush |
| Modal / dialog | `--r7` | All corners |
| Tab bar container | `--pill` | Floating pill tab bar |
| Avatar / profile image | `50%` | Circular — only case where 50% is allowed |
| Sheet handle nub | `2px` | Hard-coded optical exception (see §5) |

---

# 3. Decision Tree

```
What are you setting radius on?
│
├── A button or pill-shaped CTA
│     → --pill (always — no rectangular buttons)
│
├── An action chip or badge pill
│     → --pill
│
├── A platform/filter chip (tile format, not inline pill)
│     → --r4
│
├── An input field or OTP box
│     → Input → --r5
│     → OTP box → --r4
│
├── A card with artwork (landscape, square, marquee)
│     → Landscape / square game card → --r4
│     → Marquee / hero feature card → --r2
│     → Cover portrait card image → --r5
│
├── An interactive content tile (genre, category)
│     → --r5
│
├── A premium or upsell surface (pass card, upsell block)
│     → --r7
│
├── A secondary information surface (USP tile)
│     → --r6
│
├── A compact info module (GFF card, info panel, toast)
│     → --r3
│
├── A bottom sheet
│     → border-radius: var(--r9) var(--r9) 0 0
│
├── A modal / dialog
│     → --r7
│
├── An avatar or circular image
│     → 50% (only allowed case for 50% on a surface)
│
└── None of the above → governance request
```

---

# 4. Inner Radius Rule (Nesting)

When a child element sits inside a rounded parent with padding, the child's radius must be smaller than the parent's to maintain visual continuity. A flat-cornered child inside a rounded parent creates a pinched edge.

**Formula:**

```
inner-radius = outer-radius - padding
```

**Practical table:**

| Outer (parent) | Padding | Inner (child) max |
|---:|---:|---:|
| `--r7` (20px) | `--card-padding` (16px) | ~4px |
| `--r7` (20px) | `--card-padding` (24px web) | flush (0) |
| `--r5` (16px) | `--component-padding` (16px) | flush (0) |
| `--r9` (28px) | `--sheet-padding` (24px) | ~4px |
| `--pill` (100px) | any | child can be full pill too |

Rules:
- Child radius must never **exceed** the parent radius at its corner.
- A child touching the parent edge must have radius ≤ parent radius − distance from edge.
- When a child fills the full width of a rounded parent (no padding), set `border-radius: inherit` or use the same token.
- Inside a `--pill` container, child pill radius is safe because `100px` is always larger than any child dimension.

---

# 5. Forbidden Patterns

| Pattern | Reason | Correct |
|---|---|---|
| `border-radius: 50%` on a card, tile, or non-circular element | Oval distortion on non-square elements | Use correct `--r*` token |
| `border-radius: 50%` on anything other than avatars/circular icons | 50% is reserved for circular imagery only | Use `--pill` for pill shape |
| Raw `px` radius not in the scale (e.g. `6px`, `15px`, `24px`) | Off-scale, bypasses tokens | Snap to nearest token |
| Mixing radius tokens on a single component (e.g. `--r4` top, `--r7` bottom) | Creates visual inconsistency unless structurally required (e.g. sheet) | One token per component |
| `border-radius: 0` on an interactive component | Breaks visual language — everything interactive has a radius | Minimum `--r1` |
| Sheet handle nub with a radius token | The handle nub is 4px tall — `--r1` (8px) exceeds half its height and creates odd rendering | Hard-code `border-radius: 2px` (approved optical exception) |

---

# 6. Platform Rules

### Mobile

All canonical tokens apply. No platform-specific overrides.

### Web (≥768px)

No radius overrides. Tokens do not change at the web breakpoint — components use the same radius as mobile. Layout shifts (rail → grid) do not change card radius.

### TV (≥1280px, ≥720px tall)

No radius overrides. Cards, buttons, and sheets use the same tokens as mobile and web. The focus ring (`box-shadow`) adds visual size without changing the element's actual border-radius — do not compensate by enlarging the radius.

---

# 7. Radius QA Checklist

| Check | Required |
|---|---|
| Every radius uses a `--r*` or `--pill` token — no raw `px` values | Yes |
| No `border-radius: 50%` except avatars and circular icon wrappers | Yes |
| No `border-radius: 0` on interactive components | Yes |
| Buttons and action chips use `--pill` | Yes |
| Bottom sheet uses `var(--r9) var(--r9) 0 0` — not all-corners | Yes |
| Nested child radius ≤ outer radius − padding (§4 rule) | Yes |
| Component radius matches the canonical map in §2 | Yes |
| Sheet handle nub uses hard-coded `2px` — not a token | Yes |

---

# 8. Pre-Ship Release Gate

> A screen or component ships only if:

- [ ] All radius values use tokens from the scale — no custom `px` values
- [ ] Every component matches the canonical map (§2) — deviation logged as governance request
- [ ] Inner radius rule (§4) checked for any card or sheet with child surfaces
- [ ] `border-radius: 50%` exists only on circular imagery (avatars)
- [ ] Bottom sheet radius is top-only (`--r9 --r9 0 0`)
- [ ] TV pass: same radius tokens — no TV-specific overrides introduced
- [ ] `tokens/validate.sh` passes with exit 0
