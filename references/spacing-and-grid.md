# JioGames Spacing & Grid — Governance System

> This guide is **token-first, not screen-first**. Future screens must not introduce new spacing, gutters, grids, or layout behaviour unless an existing token or layout pattern cannot solve the need. Designers choose **spacing intent**, not random pixel values. The same layout role scales across Mobile, Web, and TV.

> **Spacing is semantic.** Small gaps show relationship. Large gaps show separation. Gutters protect content. Grids create structure. Rails create browsing momentum. Choose the spacing **intent**, not the pixel value.

**Structure**

1. Foundation Tokens
2. The Spacing Scale — *incl. root token block (source of truth)*
3. Platform Aliases
4. Spacing Decision Tree
5. Vertical Rhythm — *incl. stack utilities*
6. Grid Rules (Mobile / Web / TV)
7. The Rail System
8. Layout Pattern Mapping
9. New Screen Layout Checklist
10. Component Spacing Rules
11. Responsive Rules
12. Exception Rules
13. QA Checklist
14. Release Gate

---

# 1. Foundation Tokens

The original layout constants are kept — but reframed as **semantic aliases** sitting inside a larger system. They are not raw values; they are roles.

| Token | Role | Meaning |
|---|---|---|
| `--gutter` | Page inset | Distance from screen edge to content |
| `--section-gap` (= `--rail-gap`) | Section gap | Vertical gap between major content blocks |
| `--card-gap` | Item gap | Gap between cards in rails or grids |
| `--tv-safe` (80px) | Safe-area inset | Minimum distance from TV screen edge |
| `--container-web` (1280px) | Container | Max content width on web |

Below these sits the full spacing scale.

---

# 2. The Spacing Scale

8px base unit (token number ≈ value ÷ 8). These are the **only** approved spacing values. CSS names replace `.` with `-` (e.g. `space.1.5` → `--space-1-5`).

| Token | CSS var | Value | Use |
|---|---|---:|---|
| `space.0` | `--space-0` | 0 | No spacing |
| `space.025` | `--space-0-25` | 2px | Optical correction only |
| `space.05` | `--space-0-5` | 4px | Icon→text, tiny internal gaps |
| `space.1` | `--space-1` | 8px | Tight related items |
| `space.1.5` | `--space-1-5` | 12px | Card item gap, compact groups |
| `space.2` | `--space-2` | 16px | Default component padding |
| `space.3` | `--space-3` | 24px | Internal section padding, form groups |
| `space.4` | `--space-4` | 32px | Major section gap on mobile |
| `space.5` | `--space-5` | 40px | Page block spacing on web |
| `space.6` | `--space-6` | 48px | Major web section gap |
| `space.8` | `--space-8` | 64px | Hero spacing, large web gaps |
| `space.10` | `--space-10` | 80px | TV safe zone, large layout inset |
| `space.12` | `--space-12` | 96px | TV hero or major separation |

> **No spacing outside the token scale is allowed** unless approved as an exception (§12). This stops "let us keep it 27px because it looks nice."

### Root token block (source of truth)

The spacing + layout portion of `tokens/tokens.css`. Copy directly. Aliases resolve per platform via the media queries below.

```css
:root {
  --space-0: 0;
  --space-0-25: 2px;
  --space-0-5: 4px;
  --space-1: 8px;
  --space-1-5: 12px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-5: 40px;
  --space-6: 48px;
  --space-8: 64px;
  --space-10: 80px;
  --space-12: 96px;

  --gutter: 16px;
  --section-gap: 32px;
  --card-gap: 12px;
  --component-padding: 16px;
  --card-padding: 16px;
  --sheet-padding: 24px;
  --hero-gap: 32px;

  --container-web: 1280px;
  --web-grid-gap: 24px;
  --hero-text-max: 640px;
  --tv-safe: 80px;
}

@media (min-width: 768px) {
  :root {
    --gutter: 40px;
    --section-gap: 48px;
    --card-gap: 24px;
    --component-padding: 24px;
    --card-padding: 24px;
    --sheet-padding: 32px;
    --hero-gap: 64px;
  }
}

@media (min-width: 1280px) and (min-height: 720px) {
  :root {
    --gutter: 80px;
    --section-gap: 64px;
    --card-gap: 24px;
    --component-padding: 32px;
    --card-padding: 32px;
    --hero-gap: 96px;
  }
}
```

---

# 3. Platform Aliases

Designers and developers use **aliases**, not raw scale values, for layout. The alias resolves to the right value per platform automatically.

| Alias | Mobile | Web | TV |
|---|---:|---:|---:|
| `--gutter` | 16px | 40px | 80px |
| `--section-gap` | 32px | 48px | 64px |
| `--card-gap` | 12px | 24px | 24px |
| `--component-padding` | 16px | 24px | 32px |
| `--card-padding` | 16px | 24px | 32px |
| `--sheet-padding` | 24px | 32px | n/a |
| `--hero-gap` | 32px | 64px | 96px |

**20px is banned** — it is off the 8px scale. Mobile gutter is 16px, card/grid gaps are 24px. **Every spacing value now resolves to a scale step** — there are zero off-scale spacing exceptions.

---

# 4. Spacing Decision Tree

**The most important section.** Walk top to bottom; stop at first match.

| Ask… | Use |
|---|---|
| Is this the **outer edge of the page**? | `--gutter` |
| Is this spacing **between major sections or rails**? | `--section-gap` |
| Is this spacing **between cards** in a rail or grid? | `--card-gap` |
| Is this **inside a card or component**? | `--component-padding` |
| Is this between **title and subtitle**? | `--space-1` or `--space-1-5` |
| Is this between **heading and content**? | `--space-2` |
| Is this between **form fields**? | `--space-2` or `--space-3` |
| Is this between **icon and label**? | `--space-0-5` or `--space-1` |
| Is this a **hero or major visual break**? | `--space-6` to `--space-12` |
| Is this **TV edge protection**? | `--gutter` or `--tv-safe` |

> **The "No Raw Spacing" rule:** raw pixel spacing is not allowed by default. Every padding/margin/gap uses a token. A non-token value is allowed only when no scale step fits a genuine optical need, and must be approved by the design-system owner.

---

# 5. Vertical Rhythm

The gap between two stacked blocks **encodes their relationship**: tighter = more related, looser = more separate. Never use one uniform gap for everything — that flattens hierarchy. Increase the gap as the relationship loosens.

| Relationship | Gap | Token |
|---|---|---|
| Within a tight group (label + value, icon + text) | 4–8px | `--space-0-5` / `--space-1` |
| Between related elements (title + subtitle, title + body) | 8–12px | `--space-1` / `--space-1-5` |
| Heading → its content block | 16px | `--space-2` |
| Between components inside a section | 16–24px | `--space-2` / `--space-3` |
| Between rails / major sections | 32px (web 48 / TV 64) | `--section-gap` |
| Between top-level page regions / hero break | 48px+ | `--space-6` … `--space-12` |

**Rule:** if two blocks belong together, keep them within `--space-2`. If they are distinct, push to `--section-gap` or larger. The jump in gap size is what the eye reads as grouping.

### Rhythm comes from the parent, not the child

> Vertical rhythm is owned by the **parent stack container** via `gap` — never by `margin` on individual children.

Child margins are banned for vertical rhythm because they cause margin-collapse, double-gaps between siblings, and first/last-child reset hacks. A `gap` on the stack is one source of truth: change it once, the whole rhythm updates.

**Stack utilities** (in `tokens/tokens.css`) — wrap any vertical group in one of these; never hand-place margins:

```css
.page-stack      { display: flex; flex-direction: column; gap: var(--section-gap); }       /* major sections */
.hero-stack      { display: flex; flex-direction: column; gap: var(--hero-gap); }           /* hero / major break */
.component-stack { display: flex; flex-direction: column; gap: var(--component-padding); }  /* components in a section */
.content-stack   { display: flex; flex-direction: column; gap: var(--space-1-5); }          /* related elements (title+body) */
.tight-stack     { display: flex; flex-direction: column; gap: var(--space-1); }            /* tight group (label+value) */
```

```css
/* ❌ Child margins — collapse, double-gaps, first/last hacks */
.title  { margin-bottom: 12px; }
.card   { margin-bottom: 16px; }
.section{ margin-bottom: 32px; }
```

- Wrap any vertically-stacked group in a stack utility (or a grid with `row-gap`).
- Different gaps between subgroups → **nest stacks**, don't reach for child margins.
- The only sanctioned margins are the documented horizontal exceptions (rail last-child trailing gutter §7, Top-10 numeral overlap). No vertical layout margins on children.

---

# 6. Grid Rules

Three distinct layout systems. Do not treat them the same.

## 6.1 Mobile — single column + horizontal rails

| Area | Rule |
|---|---|
| Page content | Single column |
| Page gutter | 16px |
| Rails | Horizontal scroll |
| Rail scroll padding | `scroll-padding-left: var(--gutter)` |
| Card gap | 12px |
| Cards per view | Based on card type, not a grid |
| Full-width sections | Background may bleed; content stays aligned to gutter |

Mobile should **not** use a complex 12-column grid for most pages — it slows decisions and adds complexity. Where a true grid is needed (genre tiles, "more like this") use 2 columns with `--space-1` gap.

## 6.2 Web — real 12-column grid

| Area | Rule |
|---|---|
| Container max width | 1280px |
| Page gutter | 40px |
| Grid columns | 12 |
| Grid gap | 24px (`--web-grid-gap`) |
| Card grid | `repeat(auto-fill, minmax(220px, 1fr))` |
| Dense listing pages | Use grid |
| Editorial rails | May still use horizontal rail |
| Hero text width | 520–640px (`--hero-text-max`) |

```css
.layout-container {
  max-width: var(--container-web);
  margin-inline: auto;
  padding-inline: var(--gutter);
}
.layout-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  column-gap: var(--web-grid-gap);
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--card-gap);
}
```

Common spans: card = 3 cols, feature = 6 cols, hero = 12 cols.

## 6.3 TV — rail-first, focus-first

TV is **not** web. It is rail-first and focus-driven.

| Area | Rule |
|---|---|
| Safe zone | 80px (all sides) |
| Layout | Horizontal rails |
| Vertical rail gap | 64px |
| Card gap | 24px |
| Focus movement | Must not clip at edges |
| Text area | Keep inside safe zone |
| Rail overscroll | Must preserve trailing gutter |
| Focus scale | Reserve gap for enlarged focused card (`scale(1.05)`) |

```css
.tv-safe-area { padding: var(--tv-safe); }
```

TV grids are rare — only library, search, or full browse pages.

---

# 7. The Rail System

Formalised. Every horizontal rail follows these rules.

| Rule | Value |
|---|---|
| Rail starts at | `var(--gutter)` |
| Rail ends with | `:last-child { margin-right: var(--gutter) }` |
| Card gap | `var(--card-gap)` |
| Section gap | `var(--section-gap)` |
| Scroll behaviour | smooth horizontal scroll |
| Snap | card-aligned (`scroll-snap-align: start`) |
| Edge clipping | never clip a focused TV card |
| Last card | must be fully reachable |

```css
.rail-scroll {
  display: flex;
  gap: var(--card-gap);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  /* Left gutter via padding-left only — NOT symmetric padding.
     padding-right on an overflow flex container is dropped at
     scroll-end by some engines, so the trailing gutter lives on
     the last child instead. */
  padding-left: var(--gutter);
  scroll-padding-left: var(--gutter);
}
/* Trailing-gutter protection — robust: margin is never clamped
   negative and isn't double-counted by `gap` (no item follows the
   last card). Works regardless of gutter vs card-gap size. */
.rail-scroll > :last-child {
  margin-right: var(--gutter);
}
```

> **Every horizontal rail must have leading and trailing gutter protection. The last card must never touch the screen edge.**

> **Why not `::after { flex: 0 0 calc(var(--gutter) - var(--card-gap)) }`?** `flex-basis` cannot be negative — if `--gutter < --card-gap` the value clamps to `0` and the trailing gutter silently collapses. The subtraction also assumes left-only padding; with symmetric padding it double-counts. The `:last-child` margin avoids both traps.

---

# 8. Layout Pattern Mapping

Like typography, spacing maps to reusable patterns — so subscriptions, profile, wallet, search, rewards, settings, and store all inherit correct spacing.

| Pattern | Uses |
|---|---|
| Page header | gutter, title gap, body gap |
| Hero | gutter, hero gap, CTA group gap |
| Section & rail | section gap, heading→rail gap, card gap |
| Card | card padding, title→meta gap, CTA gap |
| Form | field gap, helper gap, CTA top gap |
| Pricing block | plan-card padding, benefit gap, price gap |
| Profile block | avatar gap, stat gap, section gap |
| Empty state | icon gap, title gap, message gap, CTA gap |
| Navigation | item gap, icon↔label gap, active-indicator gap |

---

# 9. New Screen Layout Checklist

Run this **before building any new screen** — it forces the token-first path and prevents ad-hoc layout. Each step maps to the section that answers it.

1. **Pick the page type** → Page Hero or Standard Page Header? (§8 Pattern Mapping)
2. **List the building blocks** the screen contains (header, hero, rails, cards, form, pricing, profile, nav). Each maps to a layout pattern in §8.
3. **Choose the platform** → Mobile / Web / TV. Aliases resolve sizes automatically (§3); don't hand-pick per-platform values.
4. **Set page inset** → `--gutter`. Never a literal.
5. **Build vertical structure with stacks** → wrap every vertical group in a stack utility (§5). No child `margin-bottom`.
6. **Choose gaps by relationship** → tight group `--space-1`, related `--space-1-5`, components `--component-padding`, sections `--section-gap`, hero `--hero-gap` (§4, §5).
7. **Pick the layout engine per platform** → Mobile rails + 2-col grids, Web 12-col grid, TV rails inside safe zone (§6).
8. **Wire rails correctly** → leading `--gutter`, trailing `:last-child` margin, `--card-gap` between cards (§7).
9. **Use spacing-safe components** → cards/buttons/forms carry their own internal spacing (§10). Don't re-space instances.
10. **Confirm no raw values** → every padding/margin/gap is a token; run `tokens/validate.sh`.
11. **Check responsive + localization** → gutter scales, containers grow vertically, focus scale reserved on TV (§11).
12. **Flag any exception** → on the approved list (§12) and owner-approved.

If every step resolves to a token or pattern, the screen is system-compliant. If a step needs a value the system doesn't have, that is a governance request — not a one-off.

---

# 10. Component Spacing Rules

Repeated components carry their own spacing. Designers do not manually space every instance.

| Component | Spacing rule |
|---|---|
| Button | Internal padding fixed by size (`0 --space-2` h) |
| Card | Padding (`--card-padding`) + internal gaps built in |
| Plan card | Price / benefits / badge / CTA gaps built in |
| Game card | Artwork / title / meta spacing built in |
| Rail header | Heading→rail gap (`--space-1-5`) built in |
| Form field | Label / input / helper spacing built in |
| Bottom sheet | Handle / title / content / CTA spacing built in; pad `--sheet-padding` |
| Nav bar | Icon / label / item spacing built in |

> **A new screen assembles spacing-safe components. It does not manually place every text block and card.**

---

# 11. Responsive Rules

Spacing changes with layout, not randomly.

| Situation | Rule |
|---|---|
| Small mobile width | Keep gutter 16px; reduce inner density only if needed |
| Web 768px | Move to web gutter; avoid dense 12-col if content is still rail-based |
| Web large screens | Max content width (1280px) prevents stretched layouts |
| TV | Use safe zone + larger vertical rhythm |
| Text expansion (i18n) | Containers grow vertically — never fixed-height text containers |
| Cards with longer titles | Card height stays consistent inside a rail |
| Focus scale on TV | Reserve gap so focused (`scale(1.05)`) card does not collide |

---

# 12. Exception Rules

Off-scale / bespoke spacing allowed **only** for:

- Campaign hero art
- Game artwork bleed
- Top-10 visual numerals
- Esports / broadcast-style visuals
- Decorative backgrounds
- Partner branding lockups
- One-off promo compositions

**Not allowed** for: Navigation · Forms · Payments · Subscription terms · Profile information · Settings · OTP · Errors · Game metadata · CTA placement · Rail alignment.

Every exception needs design-system-owner approval, same as a new token.

---

# 13. QA Checklist

### Mobile QA
- [ ] Checked at 360px width
- [ ] Gutter is 16px
- [ ] Cards align to gutter
- [ ] Rails have trailing gutter
- [ ] CTA does not touch edges
- [ ] Section gaps consistent
- [ ] No random margins
- [ ] Text expansion does not break card height

### Web QA
- [ ] Checked at 768 / 1024 / 1440px
- [ ] Container max width 1280px
- [ ] Gutter is 40px
- [ ] Grid gap consistent (24px)
- [ ] Cards align across rows
- [ ] No stretched content
- [ ] Hero text width controlled (520–640px)
- [ ] Listing pages use grid; editorial rails still scroll

### TV QA
- [ ] 3m readability with layout
- [ ] Safe zone 80px
- [ ] Focus cards do not clip
- [ ] Rail gap 64px
- [ ] Card gap allows focus scale
- [ ] Last card reachable
- [ ] Text + CTA inside safe zone
- [ ] No important content near screen edge

---

# 14. Release Gate

> **No screen moves to development** unless spacing tokens are used and the layout pattern is identified.
> **No screen goes live** unless QA confirms all of:

- [ ] Spacing tokens used (no raw literals)
- [ ] Grid or rail pattern identified
- [ ] Page gutter follows platform token
- [ ] Cards use component spacing
- [ ] No random margins
- [ ] Vertical rhythm reflects hierarchy (related = tight, distinct = `--section-gap`+), not uniform gaps
- [ ] Vertical rhythm comes from parent stack `gap`, not child `margin-bottom`
- [ ] Rail leading + trailing gutter works
- [ ] TV safe zone followed
- [ ] Focus scale accounted for
- [ ] Responsive behaviour checked
- [ ] `tokens/validate.sh` passes (no unreviewed off-scale warnings)
- [ ] Any exception is on the approved list (§12)
