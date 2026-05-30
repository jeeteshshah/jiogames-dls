# JioGames Colour Governance

> **Token-first, not eye-first.** Designers and developers choose a **semantic token**, not a hex value. If no existing token covers the need, that is a governance request — not permission to add a raw value.

JioGames is dark-only. Green is the sole primary action accent. Blue and purple are banned everywhere except narrow category-coding decoration. This document tells you **which token to use**, **when not to add a new colour**, **what is forbidden**, and **how QA catches violations before release**.

**Structure**

1. Brand Palette vs Product Application
2. Core Principles
3. Full Token Index
4. Colour Decision Tree ← *most important*
5. Text Colour Rules
6. Surface & Background Rules
7. Border & Divider Rules
8. State Colour Mapping
9. Approved Gradient Recipes
10. Forbidden Combinations
11. Platform Rules
12. Accessibility & Contrast
13. Exception Process
14. Colour QA Checklist
15. Pre-Ship Release Gate

---

# 1. Brand Palette vs Product Application

The Jio master brand palette includes Green, Mint, Marigold, Green 900, Black, and White.

JioGames does not use every brand colour as a default product UI colour. JioGames applies the brand palette through a dark, cinematic gaming product system.

White and Black are official brand neutrals, but they are not default JioGames product surfaces. Product chrome, cards, sheets, modals, headers, navigation, and app surfaces must remain dark.

Core brand colours are not automatically product UI colours. A colour becomes usable in product UI only when it has a defined semantic token, role, and governance rule.

---

# 2. Core Principles

Permanent rules, all platforms:

1. **Dark only for JioGames product UI.** No light mode. No white or light product surfaces.
2. **White exists in the master brand palette**, but it is not a default JioGames app surface.
3. **Black exists in the master brand palette**, but the JioGames app canvas uses `--bg` for a cinematic product background, not flat pure black.
4. **One primary action accent: green.** `--jio` owns CTAs, active borders, check icons, eyebrow labels, selected states, and active navigation.
5. **Mint is a secondary brand colour**, not a primary product action colour.
6. **Marigold is for sparkle, rewards, offer badges, and celebration.** It must not replace green as the product action colour.
7. **Blue, indigo, and purple are banned** from brand, premium, CTA, selected, focus, navigation, and UI state roles.
8. **Category colours exist only as decorative metadata accents or artwork-led moments.** They are not product action colours.
9. **Ultimate Pass is green.** `--ultimate: #00cc65`. Never blue, never indigo, never purple.
10. **Product text uses the text token scale.** Use `--text` instead of pure white for normal product text.
11. **Glow over shadow.** Active and selected states use green glow. Soft grey drop-shadows are forbidden.
12. **Opacity over new colours.** Semi-transparent white (`rgba(255,255,255,…)`) builds borders, glass, and dividers. Do not invent new opaque greys.

---

# 3. Full Token Index

All values are sourced from `tokens/tokens.json` and generated into `tokens/tokens.css`. **Never hand-author these hex values in component CSS** — always reference the token name.

### Master Brand Palette

These are official Jio brand colours. Their product usage is controlled by the semantic tokens below.

| Brand colour | Value | Product usage |
|---|---:|---|
| Primary Green 1300 | `#00A859` | Main JioGames action and brand accent — maps to `--jio` |
| Secondary Mint 1600 | `#1CBABA` | Secondary brand accent, campaign support, decorative highlights — maps to `--mint` |
| Sparkle Marigold 1800 | `#F7AB20` | Rewards, offers, celebration, badges — maps to `--popular-gold` |
| Marketing Green 900 | `#00773D` | Marketing backgrounds and brand-led campaign surfaces — no default product token |
| Black | `#000000` | Brand neutral — inverse text on green CTAs, approved overlays — maps to `--text-inv` |
| White | `#FFFFFF` | Brand neutral — approved brand assets, logos, legal, artwork overlays only — no default product token |

### Brand Green

| Token | Value | Usage |
|---|---|---|
| `--jio` | `#00A859` | Primary brand green — CTAs, active borders, check icons, eyebrow labels, active tab |
| `--jio-2` | `#22C16C` | Genre leading dashes, mid-green accents |
| `--jio-3` | `#88E5AB` | Pale green tint, subtle decorative use only |
| `--jio-bright` | `#00E870` | Glow gradient tops, shimmer highlights, rail accent lines |
| `--jio-glow` | `rgba(0,200,100,.35)` | Box-shadow glow on selected/active elements |
| `--jio-soft` | `rgba(0,168,89,.12)` | Tinted fill on selected surfaces (OTP filled, chip selected) |

### Pass / Premium

| Token | Value | Usage |
|---|---|---|
| `--ultimate` | `#00cc65` | Ultimate Pass CTA and accent — bright green, **never blue** |
| `--ultimate-glow` | `rgba(0,200,100,.35)` | Ultimate Pass focus/active glow |
| `--popular-gold` | `#F7AB20` | "Most Popular" badge, reward badges, celebration markers |

### Backgrounds

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#06080F` | Page/screen canvas — never pure `#000` |
| `--card-bg` | `#111115` | Card surfaces — sits one level above `--bg` |
| `--sheet-bg` | `#0e1118` | Bottom sheet body (gradient end) |
| `--sheet-top` | `#131720` | Bottom sheet top (gradient start — slightly lighter/bluer) |

### Opaque Surface Ladder

| Token | Value | Usage |
|---|---|---|
| `--surface-1` | `#0E1119` | Lowest opaque elevation above `--bg` |
| `--surface-2` | `#161A24` | Mid elevation — drawers, secondary panels |
| `--surface-3` | `#1F2432` | Raised panels, popover backgrounds |
| `--surface-4` | `#2A3142` | Highest opaque elevation — rarely used |

### Glass Surfaces

| Token | Value | Usage |
|---|---|---|
| `--glass-1` | `rgba(255,255,255,.055)` | Input fields, OTP boxes, frosted headers |
| `--glass-2` | `rgba(255,255,255,.03)` | Subtle info panels, secondary cards |
| `--chip-bg` | `#0c0f14` | USP tiles, platform selection chips |

### Text

| Token | Value | Emphasis level | Usage |
|---|---|---|---|
| `--text` | `#F4F2EE` | Primary | Headings, input values, prices, critical info — not pure white |
| `--text2` | `#A8ADBA` | Secondary | Body copy, descriptions, sub-labels |
| `--text3` | `#6B7280` | Muted | Hints, timestamps, decorative labels |
| `--text4` | `#454A57` | Faint | Deep metadata, truly subordinate — non-compliant for readable text |
| `--text-inv` | `#000000` | Inverse | Text on primary green button only |

### Secondary Brand Accent

| Token | Value | Usage |
|---|---|---|
| `--mint` | `#1CBABA` | Secondary brand accent, campaign support, info accents, decorative highlights |

Mint may be used for secondary brand expression, campaign accents, info-led highlights, and decorative support. **Mint must not be used for primary CTAs, active navigation, selected states, focus rings, Ultimate Pass, payment success, or main brand ownership.** Green owns all primary UI behaviour.

### Functional Accents

| Token | Value | Usage |
|---|---|---|
| `--gold` | `#FFC23D` | Rating stars, premium markers |
| `--gold-laurel` | `#c9a84c` | Awards-rail divider/accent |
| `--amber` | `#F59E0B` | Warning states |
| `--amber-soft` | `rgba(245,158,11,.15)` | Warning tinted fill |
| `--red` / `--negative` | `#FF4757` | Errors, destructive states, negative trend |
| `--pink` | `#FF3D7F` | Rare — event/promo category art only |
| `--mint` | `#1CBABA` | Secondary brand accent and decorative support (see §3 Secondary Brand Accent) |
| `--cyan` | `#26D6C9` | Legacy decorative category token — prefer `--mint` for brand-approved secondary accent |
| `--violet` | `#8E5BFF` | Category art coding only — **never** brand, premium, CTA, active, or selected state |
| `--positive` | `#00A859` | Positive states (same value as `--jio`) |

### Borders & Dividers

| Token | Value | Usage |
|---|---|---|
| `--border` | `rgba(255,255,255,.1)` | Default component border |
| `--border-strong` | `rgba(255,255,255,.14)` | Emphasized border, input focus ring outline |
| `--border-subtle` | `rgba(255,255,255,.08)` | Light cards, inactive chips |
| `--border-ultimate` | `rgba(0,204,101,.3)` | Ultimate Pass card/focus border |
| `--divider` | `rgba(255,255,255,.07)` | Row/section separator lines |
| `--hairline` | `rgba(255,255,255,.08)` | Very faint horizontal rule |
| `--hairline-2` | `rgba(255,255,255,.16)` | Hairline in brighter context |

### Overlay

| Token | Value | Usage |
|---|---|---|
| `--overlay-scrim` | `rgba(0,0,0,.55)` | Backdrop behind sheets and modals (always pair with `blur(8px)`) |

---

# 4. Colour Decision Tree

> Start from your use case, not from a hex value you like.

```
What are you colouring?
│
├── A CTA button background
│     → --jio (primary) or --ultimate (Ultimate Pass CTA only)
│
├── An active border, check icon, or active tab indicator
│     → --jio
│
├── An eyebrow / uppercase label
│     → --jio (colour) + uppercase + letter-spacing 1.5px
│
├── A secondary brand accent or campaign support highlight
│     → --mint
│     → never for primary CTA, focus, selected, navigation, or Ultimate Pass
│
├── A reward, offer, sparkle, or celebration marker
│     → --popular-gold or --gold
│
├── Body copy / supporting text
│     → --text2 (never raw white, never --text3 for anything important)
│
├── Heading, price, card title, input value, critical info
│     → --text (not pure #fff — use the token)
│
├── Hint, timestamp, decorative label, low-stakes meta
│     → --text3 (never payment/error/subscription/gameplay-critical)
│
├── A product UI background (canvas, card, sheet, modal, header, nav)
│     → --bg, --card-bg, --surface-1..4, --sheet-bg, --glass-1 / --glass-2
│     → never brand white
│
├── A brand asset, logo, legal surface, or approved artwork overlay requiring white
│     → brand white may be used only as an approved exception (see §13)
│
├── A marketing-led green background
│     → Marketing Green 900 is for marketing/campaign surfaces only — not default product UI
│
├── An input or OTP box background
│     → --glass-1
│
├── A bottom sheet background
│     → linear-gradient(180deg, --sheet-top 0%, --sheet-bg 60%)
│
├── A border or edge line
│     → --border (default), --border-subtle (light), --border-strong (emphasis)
│     → --border-ultimate for Ultimate Pass elements only
│
├── A section/row separator
│     → --divider or --hairline
│
├── A glow on selected/active element
│     → --jio-glow (most elements), --ultimate-glow (Ultimate Pass only)
│
├── A selected surface tint
│     → --jio-soft
│
├── A modal/sheet backdrop
│     → --overlay-scrim + backdrop-filter: blur(8px)
│
├── An error message or destructive state
│     → --negative (border, label) — always pair with icon, never colour alone
│
├── A warning state
│     → --amber (border/icon) + --amber-soft (fill)
│
├── A rating star or premium marker
│     → --gold
│
├── A category decoration (not brand, not CTA)
│     → --mint / --violet / --pink — decoration only, never primary/action role
│
└── None of the above
      → Stop. This is a governance request. See §13.
```

---

# 5. Text Colour Rules

White exists in the master brand palette, but normal JioGames product text uses `--text`, not pure `#FFFFFF`. Use pure white only when required for approved brand assets, logos, legal layouts, or artwork overlays where token-based text does not provide enough contrast.

### Hierarchy

Use exactly one emphasis level per piece of text. Never skip levels arbitrarily.

| Level | Token | When to use |
|---|---|---|
| Primary | `--text` | Headings, prices, input values, game names, OTP digits, critical warnings |
| Secondary | `--text2` | Body copy, descriptions, plan summaries, perk lists |
| Muted | `--text3` | Timestamps, hints, terms, tab labels (inactive), placeholder text |
| Faint | `--text4` | Deep metadata, disabled states — very limited use |
| Inverse | `--text-inv` | Text on primary green CTA button only |
| Brand | `--jio` | Eyebrow labels, active state labels, links, amounts due in green |

### Hard Rules

- **Payment / subscription / error / OTP / gameplay-critical text: always `--text` (Primary).** Never `--text2` or below.
- `--text3` (muted) for muted hints only. If text matters to a user decision, step up to `--text2` or `--text`.
- Never use raw `#FFFFFF` or `#fff` for product text. Use `--text`.
- Product body copy uses `--text2`. Critical text uses `--text`. Muted text uses `--text3` only for low-stakes information.
- Links and inline interactive text: `--jio`, weight 700.
- Error messages: `--negative`, weight 700, always paired with an error icon.

### Contrast Targets

| Text token | Approx contrast on `--bg` | WCAG level |
|---|---|---|
| `--text` | ~14:1 | AAA |
| `--text2` | ~6.5:1 | AA |
| `--text3` | ~3.5:1 | AA large only (≥18px/700 or ≥24px) |
| `--text4` | ~2:1 | Decorative only — do not use for readable text |

`--text3` is **only WCAG AA-compliant at large text sizes**. Never use it for small body copy, captions, or anything below 18px at weight 500.

Contrast values are reference targets. Final checks must be validated in implementation using the actual background, font size, font weight, and surface treatment. Extra caution is required when text sits on artwork, gradients, glass, or overlays.

---

# 6. Surface & Background Rules

White and light surfaces are not part of the JioGames product UI surface system.

Game artwork, thumbnails, partner assets, and logos may contain white or light areas. Product chrome must not. This includes cards, sheets, modals, headers, navigation, inputs, tabs, panels, and system surfaces.

Pure black is banned for product surfaces. Use `--bg` for the app canvas. Black `rgba` is allowed only for approved overlays, scrims, artwork gradients, and inverse CTA text through `--text-inv`.

### Elevation Ladder

Surfaces sit on one of these levels, from lowest to highest:

```
--bg          #06080F   ← page canvas, always lowest
--card-bg     #111115   ← cards, rails, tiles
--surface-1   #0E1119   ← panels slightly above bg
--surface-2   #161A24   ← secondary drawers, sidebars
--surface-3   #1F2432   ← raised panels, tooltip bg
--surface-4   #2A3142   ← highest opaque surface (use sparingly)
--glass-1     rgba(255,255,255,.055)  ← inputs, frosted chrome
--glass-2     rgba(255,255,255,.03)   ← very subtle tint
```

Rules:
- **Never place a lower surface on top of a higher surface.** `--bg` never appears inside a `--card-bg` container as a background.
- **Don't skip rungs.** If you need a level between `--bg` and `--card-bg`, use `--surface-1`.
- Glass surfaces (`--glass-1`, `--glass-2`) require a sufficiently dark opaque surface underneath. Never use glass on `--bg` without a parent with at least `--card-bg` level background.
- `--chip-bg` (`#0c0f14`) is intentionally darker than `--bg` — it creates a sunken chip feel. Only for chips and USP tiles.

### Bottom Sheet

Always use the gradient recipe — never a flat `--sheet-bg`:
```css
background: linear-gradient(180deg, var(--sheet-top) 0%, var(--sheet-bg) 60%);
```
`--sheet-top` is lighter/bluer than `--sheet-bg`. Gradient direction is always top→bottom (180deg).

### Hero / Cinematic Surfaces

Hero images always sit behind a gradient overlay (see §9). Never display a hero image without an overlay — raw photography on dark UI creates uncontrolled contrast.

---

# 7. Border & Divider Rules

### Choosing a Border Token

| Situation | Token |
|---|---|
| Default component border (chips, inputs at rest) | `--border` |
| Lighter, lower-emphasis border (subtle cards, inactive tiles) | `--border-subtle` |
| Stronger border (selected chip outline, prominent container) | `--border-strong` |
| Active / focus border | `--jio` |
| Ultimate Pass card or focus | `--border-ultimate` |
| Section row separator | `--divider` |
| Very faint horizontal rule | `--hairline` |

### Hard Rules

- Never use solid white (`#fff`, `#ffffff`) borders.
- Never use `1px solid rgba(255,255,255,1)` — always semi-transparent.
- Active state adds `border-color: var(--jio)` — does not add a new border-width.
- Focus ring is a `box-shadow` glow, not a CSS `outline` replacement with a new border.
- Cards with no border at rest: `--border-subtle` appears on hover (web) or focus (TV), never at rest if the card is purely a surface.

---

# 8. State Colour Mapping

Every interactive state has a fixed colour recipe. Do not invent alternatives.

| State | Border | Fill | Glow / Shadow | Text |
|---|---|---|---|---|
| Default | `--border` or none | component bg | — | per hierarchy |
| Hover (web) | `--border-strong` | subtle bg shift | — | unchanged |
| Active / Pressed | unchanged | brief opacity dip | — | unchanged |
| Focus | `--jio` | unchanged | `0 0 0 3px rgba(0,168,89,.14)` | unchanged |
| Selected | `--jio` | `--jio-soft` | `--jio-glow` | label → `--jio` |
| Disabled | unchanged | unchanged | — | `opacity: .32` on whole component |
| Error | `--negative` | unchanged | `0 0 0 3px rgba(255,71,87,.2)` | `--negative` |
| Warning | `--amber` | `--amber-soft` | — | `--amber` |

TV focus state is more emphatic:
```css
box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4);
transform: scale(1.05);
```

Ultimate Pass elements replace `--jio` with `--ultimate` and `--jio-glow` with `--ultimate-glow` in all state recipes.

---

# 9. Approved Gradient Recipes

Raw `rgba` values inside gradients are permitted only for these approved recipes. Using them outside of these patterns is a violation.

### Hero Overlay

Applied over every cinematic/hero background image:
```css
background: linear-gradient(to bottom,
  rgba(6,8,15,.55) 0%,
  rgba(6,8,15,.1) 35%,
  rgba(6,8,15,.82) 68%,
  var(--bg) 100%);
```

### Bottom Sheet Surface

```css
background: linear-gradient(180deg, var(--sheet-top) 0%, var(--sheet-bg) 60%);
```

### Mobile Pass Card

```css
background: #0e1a14;
/* corner glow */
background: radial-gradient(circle, rgba(0,168,89,.18) 0%, transparent 70%);
```

### Ultimate Pass Card

```css
background: linear-gradient(135deg, #0a1f14 0%, #0d2a1a 60%, #08160e 100%);
/* corner glow */
background: radial-gradient(circle, rgba(0,232,112,.2) 0%, transparent 65%);
```

### Frosted Header (Web)

```css
background: rgba(6,8,15,.92);
backdrop-filter: blur(12px);
```

### Wide Card Artwork Label Overlay

```css
background: linear-gradient(to top, rgba(0,0,0,.85) 0%, transparent 100%);
```

### Most Popular Badge

```css
background: linear-gradient(90deg, var(--popular-gold), #ffcf5c);
```

### Shimmer / Skeleton Loading

```css
background: linear-gradient(90deg,
  var(--card-bg) 0%,
  rgba(255,255,255,.06) 40%,
  var(--card-bg) 80%);
background-size: 200% 100%;
animation: shimmer 1.6s linear infinite;
```

### Aurora / Radial Background Glow (Cinematic)

```css
background: radial-gradient(ellipse at 20% 50%, rgba(0,168,89,.12) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 20%, rgba(0,232,112,.07) 0%, transparent 60%);
```

---

# 10. Forbidden Combinations

These are hard DLS violations. `validate.sh` catches many — the rest are reviewer responsibility.

| Forbidden | Reason |
|---|---|
| White or light product UI surfaces | JioGames product UI is dark only |
| `background: #000` or `background: black` for app canvas or product surface | Use `--bg` for cinematic depth |
| `color: #fff` or `color: white` for normal product text | Use `--text` |
| Brand white used as card, sheet, modal, header, or navigation surface | White is not a JioGames product surface |
| Brand black used as the app canvas | Use `--bg` instead |
| Mint used as primary CTA, selected state, focus ring, active nav, or Ultimate Pass colour | Mint is secondary support only |
| Any blue (`hsl(200–280,…)`) in brand, premium, CTA, selected, focus, or navigation role | JioGames primary UI behaviour is green |
| Any indigo or purple in brand, premium, or UI state role | Same — `--violet` is category art only |
| Ultimate Pass rendered in any colour other than green (`--ultimate`) | Critical brand violation |
| Grey drop-shadow (`box-shadow: … rgba(0,0,0,.2)` soft diffuse) | Use glow instead |
| `transition: all` | Always list explicit properties |
| Non-JioType `font-family` | JioType only |
| `--text3` on payment, error, subscription, or OTP text | Contrast too low for critical info |
| Raw hex/rgba in component fills, borders, or text (outside approved gradient recipes in §9) | Bypasses token pipeline |
| `opacity: 0` as a disabled state without `pointer-events: none` | Ghost interaction zone — accessibility hazard |
| `--violet` as CTA, active indicator, or premium colour | Category coding only |
| Marketing Green 900 as default product surface or UI background | Campaign surfaces only |

---

# 11. Platform Rules

### Mobile

No platform-specific colour differences. All tokens apply at base value.

### Web (≥768px)

- Sticky header uses frosted recipe (§9) — not `--bg` or `--card-bg` flat fill.
- Hover state adds `--border-strong` border and subtle bg shift — 1 step lighter on surface ladder or `rgba(255,255,255,.04)` bg bump.
- Focus ring uses web recipe: `0 0 0 3px rgba(0,168,89,.14)`.

### TV (≥1280px, ≥720px tall)

- No hover states — only focus states.
- Focus ring is more emphatic than mobile/web: `0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4)` + `scale(1.05)`.
- No frosted glass on TV — performance cost, not supported. Use opaque `--surface-1`/`--surface-2` instead of `--glass-1`.
- `backdrop-filter` banned on TV.
- TV safe zone (`--tv-safe: 80px`) must never reveal `--bg` — the app shell fill must extend edge-to-edge.

---

# 12. Accessibility & Contrast

### Contrast Requirements

| Token | Background | Ratio | Compliant for |
|---|---|---|---|
| `--text` on `--bg` | — | ~14:1 | All text sizes — AAA |
| `--text2` on `--bg` | — | ~6.5:1 | All text sizes — AA |
| `--text3` on `--bg` | — | ~3.5:1 | Large text only (≥18px/500 or ≥24px/any) |
| `--jio` on `--bg` | — | ~4.6:1 | Large text (≥18px/700) — AA |
| `--text-inv` on `--jio` | — | ~5.4:1 | AA — CTA label |
| `--negative` on `--bg` | — | ~5.1:1 | AA — error text |

### Hard Rules

- Never rely on colour alone to communicate state — pair with icon, label, or weight change.
- Error states: icon + `--negative` text, not `--negative` border alone.
- Selected states: border + fill change, not colour shift alone.
- `--text4` (`#454A57`) is **non-compliant for readable text** at any size. Decorative/structural use only.
- Disabled components use `opacity: .32` — this reduces all colours proportionally, keep that in mind for contrast checks on disabled text.
- Contrast values are reference targets. Final checks must be validated in implementation using the actual background, font size, font weight, and surface treatment. Extra caution is required when text sits on artwork, gradients, glass, or overlays.

---

# 13. Exception Process

A new colour or raw value is needed only when:
- Approved gradient recipes (§9) do not cover the visual need
- A new functional accent is required for a new product surface (new pass tier, new category)

Use of Brand White, Brand Black, Marketing Green 900, or Mint outside the defined semantic roles requires approval. White product surfaces require explicit approval and should be treated as a brand, legal, partner, or asset-led exception — not a product UI pattern.

**Process:**
1. Identify which token from §3 comes closest — document why it fails
2. Propose the new value with name, usage scope, and contrast check
3. Requires approval from 2 DLS owners
4. Add to `tokens.json` first — never add a raw value to a component before it is in tokens
5. Regenerate `tokens.css` via `python3 tokens/build.py`
6. Update this document's §3 index and the relevant decision tree branch in §4

---

# 14. Colour QA Checklist

Run before any component or screen ships:

| Check | Required |
|---|---|
| No `background: #000`, `black`, or white/light product surfaces | Yes |
| No blue/indigo/purple in brand, premium, or UI state role | Yes |
| Ultimate Pass uses `--ultimate` (green) only — never blue | Yes |
| Green owns all primary product actions and active states | Yes |
| Mint is not used for CTA, selected, focus, active navigation, or Ultimate Pass | Yes |
| Marketing Green 900 is not used as a default app surface | Yes |
| White exists only in approved brand, logo, legal, or artwork overlay contexts | Yes |
| Brand black is not used as the app canvas or default product surface | Yes |
| All text uses token names — no raw hex in `color` properties | Yes |
| `--text3` only on decorative/low-stakes text — never payment/error/subscription/OTP | Yes |
| Critical text (payment, error, subscription, OTP) at `--text` (Primary) | Yes |
| Active/selected states use `--jio` border + `--jio-soft` fill + `--jio-glow` shadow | Yes |
| No soft grey drop-shadows (`rgba(0,0,0,.1–.3)` diffuse) | Yes |
| Gradients use only approved recipes from §9 | Yes |
| Raw `rgba` values exist only inside gradient or approved glow recipes | Yes |
| TV: no `backdrop-filter` or `--glass-1`/`--glass-2` | If TV in scope |
| New colour value added to `tokens.json` before use | If new colour |
| `tokens/validate.sh` passes with exit 0 | Yes |

---

# 15. Pre-Ship Release Gate

> A screen or component ships only if all of these pass:

- [ ] Brand palette colours are mapped to product semantic roles before use — no raw brand hex in component CSS
- [ ] White and black are used only in approved product contexts
- [ ] Mint is used only as secondary support — not primary UI behaviour
- [ ] Decision tree in §4 resolved every colour choice — no guessing
- [ ] No token from §10 Forbidden list present
- [ ] All text meets contrast targets from §12 for its size and weight
- [ ] State colour mapping (§8) implemented fully — not just default state
- [ ] Gradients match an approved recipe from §9 or exception was approved via §13
- [ ] TV: no glass surfaces, no backdrop-filter, emphatic focus ring present
- [ ] Any new colour token added to `tokens.json`, build re-run, no stale `tokens.css`
- [ ] `tokens/validate.sh` passes with exit 0
