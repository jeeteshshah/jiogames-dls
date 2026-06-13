# JioGames Typography — Governance System

> **Inherits `references/_core-rules.md`.** Rules in that file (dark-only, JioType-only, token-first, no Lucide, no silent deviation) are not repeated here.

> **This guide is token-first, not screen-first.** Future screens must not introduce new typography unless an existing token cannot solve the communication need. Designers choose a **semantic role**, not a font size. The same role scales through platform tokens across Mobile, Web, and TV.

JioType is the sole typeface. This document is not just a spec — it tells you **how to choose**, **when not to create new styles**, **how to scale across platforms**, and **how QA catches violations before release**.

**Structure**

1. Typeface & Font Loading
2. Core Typography Principles
3. Type Role Decision Tree ← *most important*
4. Typography Tokens
5. Platform Scaling
6. UI Pattern Mapping
7. Component Usage Rules
8. Responsive & Localization Rules
9. Accessibility Rules
10. Exception Rules
11. Existing Screen Examples
12. Figma & Developer Implementation
13. Platform QA Checklist
14. Pre-Ship Release Gate

---

# 1. Typeface & Font Loading

```css
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-Light.ttf');        font-weight:300; font-display:swap; }
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-LightItalic.ttf');  font-weight:300; font-style:italic; font-display:swap; }
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-Medium.ttf');       font-weight:500; font-display:swap; }
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-MediumItalic.ttf'); font-weight:500; font-style:italic; font-display:swap; }
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-Bold.ttf');         font-weight:700; font-display:swap; }
@font-face { font-family:'JioType'; src:url('/Assets/font/JioType-Black.ttf');        font-weight:900; font-display:swap; }
```

| Weight | Variant | Usage |
|---|---|---|
| 300 | Light | Very large display only (never small/body) |
| 500 | Medium | Body, supporting text, captions |
| 700 | Bold | Labels, sub-headings, button text |
| 900 | Black | All display, headings, prices, card titles |

Only these four weights exist. **No other weight value is permitted** (no 400/600/800).

---

# 2. Core Typography Principles

Permanent rules, all platforms:

- All headings use weight **900**.
- Negative letter-spacing on text ≥18px (bigger = tighter).
- Eyebrow / uppercase labels: `+1.5px` tracking, `var(--jio)`.
- Body uses `--text2`, never raw white.
- Italic `em` accent in headings = weight 500, `var(--jio)`.
- Prices use `font-variant-numeric: tabular-nums`.

### Italic accent pattern
```html
<h1 class="text-hero">Play <em>Smarter</em></h1>
```
```css
em { font-style: italic; font-weight: 500; color: var(--jio); }
```

### Letter-spacing rules
| Text Size | Value |
|---|---|
| ≥ 32px | `-0.6px` to `-1.5px` |
| 22–31px | `-0.3px` to `-0.6px` |
| 16–21px | `-0.2px` to `0` |
| 12–15px | `0` to `0.4px` |
| Eyebrow (uppercase) | `+1.5px` |
| Tiny badge (uppercase) | `+0.5px` |
| Input value | `+0.9px` |

---

# 3. Type Role Decision Tree

**How to choose a type style.** Any element on any screen maps to exactly one role. Walk the questions top to bottom; stop at the first match.

| Ask… | If yes, use |
|---|---|
| Is this the **most important message** on the page? | `text.hero` *or* `text.screenTitle` |
| Is this the **title** of a page, modal, sheet, or state? | `text.screenTitle` *or* `text.sheetTitle` |
| Is this **introducing a section** or content group? | `text.railTitle` |
| Is this the **name** of a game, plan, offer, reward, tournament, or card? | `text.cardTitle` |
| Is this **explaining** something? | `text.body` |
| Is this **metadata, helper text, terms, timer, hint, or secondary detail**? | `text.caption` |
| Is this an **uppercase label, state, badge, plan tag, or category marker**? | `text.badge` |
| Is this a **price, score, count, days left, wallet balance, or stat**? | `text.price` |
| Is this a **primary action**? | `text.cta` |

Any new page (Profile, Store, Rewards, Subscriptions, Search, Wallet, Tournament, Settings…) maps to these roles without inventing a style.

### The "No New Type Style" Rule

> **New typography styles are not allowed by default.** Every new screen must first use an existing typography token. A new style may be created **only** when all existing tokens fail to serve the communication need — and it must be reviewed and approved by the **design-system owner, product-design lead, and development lead**.

This is the single rule that keeps the system from fragmenting as the product grows.

---

# 4. Typography Tokens

Three permanent levels — never confuse them:

- **Level 1 — Type roles (permanent):** the 10 tokens below.
- **Level 2 — UI patterns (reusable):** see §6.
- **Level 3 — Screen examples (temporary):** see §11. Screens follow patterns, not old screen examples.

### Level 1 — the 10 roles

| Token | Class | Used for |
|---|---|---|
| `text.hero` | `.text-hero` | Hero / promo headline, home hero title |
| `text.screenTitle` | `.text-screen-title` | Page / detail title, pass-found / upsell title |
| `text.sheetTitle` | `.text-sheet-title` | Login sheet, OTP, pref, empty/error title |
| `text.railTitle` | `.text-rail-title` | Section / rail headings (italic `em` accent) |
| `text.cardTitle` | `.text-card-title` | Card names, plan name |
| `text.body` | `.text-body` | Descriptions, sub-text, perks, benefits |
| `text.caption` | `.text-caption` | Meta, hints, timers, terms, settings descriptions |
| `text.badge` | `.text-badge` | Eyebrow labels, plan tags, "Most Popular", age pill, nav active |
| `text.price` | `.text-price` | Prices, day-counts, scores, wallet balance, stats |
| `text.cta` | `.text-cta` | Button / CTA label |

```css
/* ── Component typography tokens — mobile base ── */
.text-hero        { font-family: var(--jio-font); font-size: 36px; font-weight: 900; line-height: 1.08; letter-spacing: -.02em; color: var(--text); text-wrap: balance; }
.text-screen-title{ font-family: var(--jio-font); font-size: 28px; font-weight: 900; line-height: 1.15; letter-spacing: -.6px;  color: var(--text); text-wrap: balance; }
.text-sheet-title { font-family: var(--jio-font); font-size: 26px; font-weight: 900; line-height: 1.15; letter-spacing: -.3px;  color: var(--text); }
.text-rail-title  { font-family: var(--jio-font); font-size: 18px; font-weight: 900; line-height: 1.2;  letter-spacing: 0;      color: var(--text); }
.text-rail-title em { font-style: italic; font-weight: 500; color: var(--jio); }
.text-card-title  { font-family: var(--jio-font); font-size: 22px; font-weight: 900; line-height: 1.2;  letter-spacing: 0;      color: var(--text); }
.text-body        { font-family: var(--jio-font); font-size: 14px; font-weight: 500; line-height: 1.55; letter-spacing: 0;      color: var(--text2); }
.text-caption     { font-family: var(--jio-font); font-size: 12px; font-weight: 500; line-height: 1.4;  letter-spacing: 0;      color: var(--text2); }
/* --text2 default: 12px at weight 500 is below AA on --bg at --text3 (3.5:1). --text2 (~6.5:1) is safe.
   Override to --text3 only for decorative, non-essential metadata (timestamps, inactive icons, placeholders).
   Never --text3 for terms, timers, nav labels, helper text, error text, or anything users must read. */
.text-badge       { font-family: var(--jio-font); font-size: 11px; font-weight: 700; line-height: 1;    letter-spacing: 1.5px; text-transform: uppercase; color: var(--jio); }
.text-price       { font-family: var(--jio-font); font-size: 22px; font-weight: 900; line-height: 1;    letter-spacing: -.5px;  color: var(--text); font-variant-numeric: tabular-nums; }
.text-cta         { font-family: var(--jio-font); font-size: 16px; font-weight: 700; line-height: 1;    letter-spacing: .04em;  color: var(--text-inv); }
/* --text-inv (#000) on var(--jio) — never raw #000 in component CSS */

/* ── Strong variants (`.text-caption-strong` / `.text-body-strong` in pattern tables) ── */
/* Use these instead of ad hoc font-weight overrides */
.text-caption-strong { font-family: var(--jio-font); font-size: 12px; font-weight: 700; line-height: 1.4; letter-spacing: 0; color: var(--text2); }
.text-body-strong    { font-family: var(--jio-font); font-size: 14px; font-weight: 700; line-height: 1.55; letter-spacing: 0; color: var(--text); }

/* ── Web overrides (base 20px) ── */
@media (min-width: 768px) {
  .text-hero{font-size:64px;letter-spacing:-1.5px;line-height:1.05;} .text-screen-title{font-size:48px;letter-spacing:-1px;}
  .text-sheet-title{font-size:32px;letter-spacing:-.6px;} .text-rail-title{font-size:24px;letter-spacing:-.3px;}
  .text-card-title{font-size:26px;letter-spacing:-.3px;} .text-body{font-size:16px;} .text-caption{font-size:13px;}
  .text-badge{font-size:12px;} .text-price{font-size:30px;letter-spacing:-.6px;} .text-cta{font-size:18px;}
}
/* ── TV overrides (base 24px — min 22px, min weight 500) ── */
@media (min-width: 1280px) and (min-height: 720px) {
  .text-hero{font-size:80px;letter-spacing:-2px;line-height:1.05;} .text-screen-title{font-size:48px;letter-spacing:-1px;}
  .text-sheet-title{font-size:40px;letter-spacing:-.8px;} .text-rail-title{font-size:32px;letter-spacing:-.5px;}
  .text-card-title{font-size:22px;} .text-body{font-size:24px;line-height:1.5;} .text-caption{font-size:20px;}
  .text-badge{font-size:18px;} .text-price{font-size:36px;letter-spacing:-.6px;} .text-cta{font-size:22px;}
}
```

**Variants:** `.text-badge` → override `color` for gold/white. `.text-cta` → black on green; secondary/outline uses `color: var(--text)`; ghost uses `.text-caption` + `--text3`. Caption-bold links ("See all", "Change", "Read more") → `.text-caption` + `700` + `var(--jio)`. Error text → `.text-caption` + `700` + `var(--negative)`.

---

# 5. Platform Scaling

> **Designers choose only the type role. The platform decides the size.**

A designer never says "make this 21px on TV." They say "this is `railTitle`" and the platform token resolves the size. The `.text-*` classes in §4 already encode this via media queries.

| Token | Mobile | Web | TV |
|---|---|---|---|
| `text.hero` | 36px | 64px | 80px (72–96) |
| `text.screenTitle` | 28–32px | 48px | 48px |
| `text.sheetTitle` | 26–28px | 32px | 40px |
| `text.railTitle` | 18px | 24px | 32px |
| `text.cardTitle` | 22px | 26px | 22px |
| `text.body` | 14px | 16px | 24px |
| `text.caption` | 11–12px | 13px | 20px |
| `text.badge` | 11px | 12px | 18px |
| `text.price` | 22–24px | 30px | 36px |
| `text.cta` | 16px | 18px | 22px |

Breakpoints: Web `≥768px`, TV `≥1280px & ≥720px`. Mobile is the base.

---

# 6. UI Pattern Mapping

Level 2 — reusable patterns. Every screen is built by composing these; map each block to its pattern, then apply the pattern's roles.

### 6.1 Page Header / Hero
Landing, subscriptions, profile overview, store, tournament, campaign.
| Element | Role |
|---|---|
| Main headline | `hero` *or* `screenTitle` |
| Supporting text | `body` |
| Primary action | `cta` |
| Secondary action | `.text-caption-strong` *or* secondary `cta` |
| Status / category | `badge` |
| Price / key number | `price` |

### 6.2 Standard Page Header
Profile, settings, wallet, search results, rewards, help, history, library.
| Element | Role |
|---|---|
| Page title | `screenTitle` |
| Page description | `body` |
| Section title | `railTitle` |
| Metadata | `caption` |
| Empty-state title | `sheetTitle` *or* `screenTitle` |
| Empty-state description | `body` |

### 6.3 Section & Rail
Home rails, game lists, benefits, recommendations, recently played, watch content.
| Element | Role |
|---|---|
| Section heading | `railTitle` |
| Section subtitle | `caption` *or* `body` |
| Card title | `cardTitle` |
| Card meta | `caption` |
| Badge | `badge` |
| See all | `.text-caption-strong` |

### 6.4 Card
Game, plan, stat, wallet, tournament, offer, voucher cards.
| Element | Role |
|---|---|
| Card title | `cardTitle` |
| Card subtitle | `body` *or* `caption` |
| Card meta | `caption` |
| Primary number | `price` |
| Badge / label | `badge` |
| CTA inside card | `cta` *or* `.text-caption-strong` |

### 6.5 Form & Input
Login, OTP, profile edit, search, redeem, payment, settings.
| Element | Role |
|---|---|
| Form title | `sheetTitle` |
| Field label | `badge` (compact) *or* `.text-caption-strong` |
| Input value | input value |
| Helper text | `caption` |
| Error text | `.text-caption-strong`, `--negative` |
| Success text | `.text-caption-strong` + icon |
| CTA | `cta` |

### 6.6 Pricing Block
Plans, passes, add-ons, offers, bundles, upgrade pages.
| Element | Role |
|---|---|
| Plan name | `cardTitle` *or* `screenTitle` |
| Plan label | `badge` |
| Price | `price` |
| Duration | `body` |
| Benefits | `body` |
| Limitations | `caption` |
| Offer badge | `badge` |
| Legal copy | `caption` (muted) |
| CTA | `cta` |

### 6.7 Profile Block
Profile, edit profile, achievements, stats, account, linked accounts.
| Element | Role |
|---|---|
| User name | `screenTitle` *or* `cardTitle` |
| User ID / phone | `caption` |
| Stat number | `price` |
| Stat label | `caption` |
| Section title | `railTitle` |
| Setting label | `.text-body-strong` |
| Setting description | `caption` |
| Status label | `badge` |

### 6.8 Empty / Error State
Across all pages.
| Element | Role |
|---|---|
| Title | `sheetTitle` |
| Message | `body` |
| Recovery CTA | `cta` |
| Help link | `.text-caption-strong` |
| Status badge | `badge` |

**Rule:** errors, payment issues, subscription expiry, gameplay blockers **never** use muted text.

### 6.9 Navigation / Modal / Bottom Sheet / Detail / List
| Element | Role |
|---|---|
| Active nav label | `.text-caption-strong` *or* `badge` |
| Inactive nav label | `caption` |
| Filter chip | `badge` (compact) |
| Category tab | `.text-caption-strong` |
| Notification count | tiny `badge` |
| Modal / sheet title | `sheetTitle` |
| Detail page title | `screenTitle` |

**Rule:** navigation text is readable but never louder than page content.

---

# 7. Component Usage Rules

> Typography is embedded **inside master components**. Designers and developers do not manually style repeated UI elements.

| Component | Always uses |
|---|---|
| Button | `text.cta` |
| Plan card | `text.cardTitle`, `text.price`, `text.body`, `text.badge` |
| Game card | `text.cardTitle`, `text.caption` |
| Page header | `text.screenTitle`, `text.body` |
| Rail header | `text.railTitle` |
| Form field | field label (`badge`/`.text-caption-strong`) + input value + `text.caption` helper |
| Pricing block | `text.cardTitle`, `text.price`, `text.body`, `text.badge` |

A new screen assembles components; it does not re-apply type by hand. This makes the system followed **automatically**, not by discipline.

---

# 8. Responsive & Localization Rules

### Line count
| Role | Max lines |
|---|---|
| Hero headline | 2 |
| Screen title | 2 |
| Card title | 2 |
| Rail title | 1 preferred, 2 allowed |
| Body | 2–4 (per component) |
| Caption | 1–2 |

### Overflow
- Card titles truncate after 2 lines.
- Metadata truncates after 1 line.
- CTA labels **must not wrap**.
- Prices **never truncate**.
- Error messages wrap fully (never clipped).

### Wrapping
- `text-wrap: balance` on hero and screen titles.
- Do **not** balance-wrap body copy.
- Never allow orphan words in hero titles.

### Localization safety

> All typography tokens must survive text expansion up to **30%** (Hindi & regional strings run longer than English).

- Keep English CTA labels short; CTA must not wrap even after expansion.
- Card titles may wrap to 2 lines.
- Test hero titles in English **and** Hindi.
- Do **not** use fixed-height containers for text-heavy components.
- **Never bake translatable text into artwork** — only decorative/non-translated text may live in art.

---

# 9. Accessibility Rules

Emphasis level is a **readability contract**, not just visual weight.

| Level | Token | Value | Use for |
|---|---|---|---|
| Primary | `--text` | `#F4F2EE` | Critical/must-read: headings, prices, plan names, errors |
| Secondary | `--text2` | `#A8ADBA` | Supporting only — never sole carrier of meaning |
| Muted | `--text3` | `#6B7280` | Decorative/non-essential metadata only — timestamps, inactive icons, deep meta |
| Accent | `--jio` | `#00A859` | Labels, links, italic accents |
| On-CTA | `--text-inv` | `#000000` | Text on green button |

- **Muted (`--text3`) must NOT be used** for: payment info, subscription terms, OTP instructions, errors, timers, nav labels, helper text, or anything users need to read to complete a task. Use `--text2` instead.
- `--text3` is allowed only for: decorative timestamps, inactive icon labels (when also dimmed by opacity), placeholder text, and deep metadata the user would never need to act on.
- Body targets WCAG AA. `--text3` is ~3.5:1 on `--bg` — below AA for body copy. `.text-caption` (12px/500) defaults to `--text2`; override to `--text3` only with explicit justification.
- Accent green on dark must clear **3:1** for any must-read use.
- **Never encode meaning by colour alone** — pair status with icon/label/weight.
- Error/payment/subscription text: Primary emphasis, weight ≥500.

---

# 10. Exception Rules

Controlled flexibility. Bespoke typography is allowed **only** for:

- Campaign hero art
- Top-10 numerals
- Logo lockups
- Event branding
- Esports / broadcast visuals
- Decorative game artwork
- One-off promotional display type

Exceptions must **never** be used for:

- Navigation · Forms · Payment · Subscription terms · Errors · OTP · Settings · Profile information · Game metadata · CTA labels

Every exception needs the same three-owner approval as a new token (§3).

---

# 11. Existing Screen Examples

Level 3 — temporary worked examples. Each is tagged with the patterns it composes. Sizes are mobile; scale per §5.

### Login Sheet → *Form & Input*
| Element | Role | Spec |
|---|---|---|
| Sheet title | `sheetTitle` | 26px / 900 / -0.3px, `--text` |
| Sub text | `body` | 14px / 500 / 1.55, `--text2` |
| Field label | `badge` | 11px / 700 uppercase, `--text2` |
| Phone input value | input value | 18px / 500 / +0.9px, `--text` |
| SIM label | `badge` | 10px / 700 uppercase, `var(--jio)` |
| Primary CTA | `cta` | 16px / 700, `var(--text-inv)` on `var(--jio)` |
| Terms | `caption` | 12px / 500, `--text2` |

### OTP → *Form & Input*
| Element | Role | Spec |
|---|---|---|
| OTP title | `sheetTitle` | 26px / 900, `--text` |
| OTP sub | `body` | 14px / 500, `--text2`; number `strong` → `--text` |
| OTP digit | input value | 26px / 700, `--text` |
| Resend timer | `body` | 14px / 500, `--text2`; link `var(--jio)` |
| GFF label | bespoke | 8.5px / **700** / +2px uppercase, `var(--ultimate)` (approved exception — see §10) |

### Preferences → *Page Header + Card*
| Element | Role | Spec |
|---|---|---|
| Pref title | `sheetTitle` | 28px / 900, `--text` |
| Pref sub | `body` | 13px / 500, `--text2` |
| Genre tile name | `cardTitle` | 14px / 900, white-over-art |
| Platform chip text | `badge` | 11px / 700, `--text2` → `var(--jio)` selected |

### Home → *Page Hero + Section & Rail + Navigation*
| Element | Role | Spec |
|---|---|---|
| Hero game title | `hero` | 36px / 900, white |
| Hero eyebrow | `badge` | 11px / 700 uppercase, `var(--jio)` |
| Rail heading | `railTitle` | 18px / 900; italic `em` accent |
| Card title | `cardTitle`/wide | 13px / 900, white |
| Pass strip days | `price` | 20px / 700, `var(--jio)` |
| Tab bar label | `caption` | 10px / **700**, `--text3` → `var(--jio)` active |

### Game Detail → *Page Hero + Section & Rail*
| Element | Role | Spec |
|---|---|---|
| Game title | `screenTitle` | 28px / 900, `--text` |
| Section heading | `railTitle` | 18px / 900; italic `em` |
| Meta chip | `body` | 13px / 500, `--text2` |
| Age pill | `badge` | 11px / 700, white, bordered |
| Play button | `cta` | 16px / 700, `var(--text-inv)` on `var(--jio)` |
| Description | `body` | 14px / 500, `--text2` (3-line clamp) |
| Detail value | `.text-caption-strong` | 13px / 700, `--text` |

### Pass Upsell → *Pricing Block*
| Element | Role | Spec |
|---|---|---|
| Title | `screenTitle` | 32px / 900, `--text` |
| Plan label | `badge` | 11px / 700 uppercase, `var(--jio)` |
| Pass card name | `cardTitle` | 22px / 900, `--text` |
| Plan price | `price` | 22–24px / 900, tabular-nums |
| Perk text | `body` | 13–14px / 500, `var(--text2)` (use `--text` for primary perk) |
| "Most Popular" | `badge` (gold) | 9px / 900 uppercase, `#000` on gold |

---

# 12. Figma & Developer Implementation

### Figma library rules

> Every text style in Figma maps to one typography token. **No detached text styles. No local font-size overrides** unless marked as an approved exception.

Style naming (repeat for Web and TV):
```
Typography/Mobile/Hero
Typography/Mobile/Screen Title
Typography/Mobile/Sheet Title
Typography/Mobile/Rail Title
Typography/Mobile/Card Title
Typography/Mobile/Body
Typography/Mobile/Caption
Typography/Mobile/Badge
Typography/Mobile/Price
Typography/Mobile/CTA
```

### Developer enforcement

> Developers use `.text-*` classes or typography tokens. Hardcoded `font-size`, `font-weight`, `line-height`, `letter-spacing` are **not allowed** in product components unless approved as a bespoke display case.

Lint checks (enforced via `tokens/.stylelintrc.json` + `tokens/validate.sh`):

| Rule | Status |
|---|---|
| No font-weight outside 300 / 500 / 700 / 900 | automated |
| No raw white body text | automated |
| No font-family other than JioType | automated |
| No muted colour for critical information | manual review |
| No CTA text below 16px mobile / 18px web / 22px TV | manual review |
| No TV text below 22px | manual review |

Run before commit:
```bash
./tokens/validate.sh path/to/screen.html
```

---

# 13. Platform QA Checklist

### Mobile QA
- [ ] Text checked at 360px width
- [ ] 2-line titles render correctly
- [ ] CTA does not wrap
- [ ] Small captions readable
- [ ] Dark-mode contrast holds
- [ ] Hindi expansion checked (if applicable)

### Web QA
- [ ] Checked at 768 / 1024 / 1440px
- [ ] Hero not excessively long
- [ ] Body width not too wide (max ~65ch)
- [ ] Cards align when titles wrap to different line counts
- [ ] Browser zoom at 125% holds

### TV QA
- [ ] Readable from 3m distance
- [ ] No text below 22px
- [ ] CTA focus state readable
- [ ] Rail titles readable from sofa distance
- [ ] Card title does not fight with artwork
- [ ] No thin weight (300) anywhere
- [ ] No muted text for important information

---

# 14. Pre-Ship Release Gate

> **No screen moves to development** unless all text styles use approved Figma typography styles.
>
> **No screen goes live** unless design QA confirms all of the following.

- [ ] Typography tokens used correctly (roles, not ad-hoc sizes)
- [ ] No unauthorized font sizes
- [ ] No unauthorized font weights (only 300/500/700/900)
- [ ] No raw white body text
- [ ] No muted critical text (payment / subscription / error / OTP / gameplay)
- [ ] TV minimum size (22px) followed
- [ ] CTA text readable on all platforms, never wrapping
- [ ] Price and numeric values use tabular numbers
- [ ] Text wrapping & overflow checked (line counts §8)
- [ ] Localization checked where applicable (30% expansion)
- [ ] `tokens/validate.sh` passes with no ERRORs
- [ ] Any bespoke type is on the approved exception list (§10)
