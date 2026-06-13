# JioGames DLS — Core Rules

Universal non-negotiables. **Read this file first for every task.**

All other `references/` files inherit these rules. They are not repeated there.

---

## Dark-only

No light mode. No white surfaces.

Backgrounds: `var(--bg)`, `var(--card-bg)`, `var(--surface-2)` — nothing lighter.
Never: `background: white`, `background: #fff`, `background: #F4F2EE`.

---

## JioType-only

```
font-family: 'JioType', sans-serif;
```

Never: Inter, Outfit, Roboto, Helvetica, or any system-font stack as primary.

Approved weights: **300, 500, 700, 900**. Banned: 100, 200, 400, 600, 800.

Load: `/Assets/font/JioType-{Light|Medium|Bold|Black}.ttf`

---

## Token-first — no raw values in component CSS

| I was about to write | Replace with |
|---|---|
| Any raw hex | `var(--jio)` or correct token |
| `#00A859` | `var(--jio)` |
| `#06080F` | `var(--bg)` |
| `#111115` | `var(--card-bg)` |
| `#F4F2EE`, `white`, `#fff` | `var(--text)` |
| `#A8ADBA` | `var(--text2)` |
| `54px` / `36px` (heights) | `var(--ctrl-h)` / `var(--ctrl-h-sm)` |
| `100px` / `50%` on buttons | `var(--pill)` |
| `14px` / `20px` border-radius | `var(--r4)` / `var(--r7)` |
| `400`, `600`, `800` font-weight | `300`, `500`, `700`, or `900` |
| `transition: all` | List explicit properties |
| `box-shadow` with grey | `var(--jio-glow)` |

Approved structural exceptions: see `references/tokens-and-components.md` → "Approved Structural Exceptions."

---

## Green-first — no blue, purple, or indigo

JioGames is green end-to-end. `var(--jio)` is the sole brand accent.

Never: `#6366f1`, `#8b5cf6`, `#7c3aed`, `#3b82f6`, or any blue/indigo/purple.

Pass tiers:
- **Mobile Pass** → `var(--jio)` (standard green)
- **All Screen Pass** → `var(--ultimate)` (brighter green — never blue)
- **Connect & Play Pass** → `var(--jio)`

---

## No generic AI UI

Do not use: soft grey drop-shadows, white cards on dark bg, over-padded centred layouts, flat blue primary buttons, gradient-mesh backgrounds, generic "grid of cards" layouts.

Run `references/anti-ai-slop.md` checklist before any generation.

---

## Icons — solid glyph only, DLS library only

- Use only `icons/svg/` or `icons/sprite.svg`
- Search `icons/index.json` for available icons — do not load all SVGs
- Never: Lucide, HeroIcons, Feather, Bootstrap Icons, or any third-party icon
- Never: `stroke-width` in CSS or `stroke=` attribute with a colour value
- Always: `fill: currentColor` on every icon path — colour is CSS-driven

```css
.icon-btn { color: var(--text); }
.icon-btn svg { fill: currentColor; }
```

---

## No silent deviation

Do not invent new colours, spacing, radii, typography, motion, icon styles, component variants, or layout patterns that are not in the DLS.

Do not silently "improve," "modernise," or "reinterpret" the system.

**If the DLS does not define what is needed → STOP. Use this exact format:**

> The current JioGames DLS does not define this clearly.
> I need your approval before changing or extending the system.
>
> Missing / conflicting area:
> * [state the gap]
>
> Recommended options:
> 1. Use the closest existing DLS rule: [option]
> 2. Add a new governed rule: [option]
> 3. Treat this as a one-off exception: [option]
>
> Which direction should I follow?

Do not generate the final UI until the user responds.

---

## Heading and type rules

- All headings, titles, prices, card names: **weight 900**
- Negative letter-spacing on all text ≥16px
- `var(--text3)` is decorative/non-essential only — ~3.5:1 contrast, below WCAG AA for small text
- Eyebrow labels: uppercase + `letter-spacing: 1.5px` + `color: var(--jio)`

---

## Glow over shadow

Active/selected states: `box-shadow: var(--jio-glow)`.
Never soft grey drop-shadows on active elements.

---

## Platform input models

| Platform | Input | Constraint |
|---|---|---|
| Mobile | Touch | No hover. Scroll-hide AppBar. |
| Web | Pointer + keyboard | Hover allowed. Always-visible AppBar. |
| TV | D-pad only | No hover. No sheets. No scroll snap on main nav. Focus ring mandatory. |

TV: all interactive elements need `:focus-visible` with `var(--jio-glow)` + `scale(1.05)`.
