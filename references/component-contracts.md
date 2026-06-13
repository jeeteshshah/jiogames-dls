# JioGames Component Contracts

> **Inherits `_core-rules.md`** — dark-only, JioType-only, token-first, no Lucide, no silent deviation rules are not repeated here.


> A component is **defined once** here — its tokens, every state, and its behavior on every platform. Screens **compose** contracted components; they do not re-implement CSS. If a screen needs a component variant that isn't contracted, that's a governance request, not a one-off.

This is the layer that stops screens from reinventing buttons and cards (the biggest drift source). Typography and spacing govern *values*; this governs *components*.

**Contents**

1. How to Read a Contract
2. The State Model
3. The Platform Interaction Model
4. Component Contracts
   - AppBar · Button · Card · Text Input · OTP · Chip · Bottom Sheet · Rail · Tab Bar · Pass Card · Genre Tile · Toast
5. Accessibility Contract (all components)
6. Release Gate

---

# 1. How to Read a Contract

Each component contract has eight fixed parts:

| Part | What it pins down |
|---|---|
| **Owner** | Named person accountable for this contract — approves all changes, reviews violations |
| **Anatomy** | The named sub-parts |
| **Tokens** | Every token the component consumes (no raw values allowed) |
| **Radius** | The canonical `--r*` or `--pill` token (cross-ref: radius-governance.md §2) |
| **Sizing** | Height/width token (`--ctrl-h`, `--card-wide-w`, etc.), whether platform-aware or fixed, and TV restriction if applicable |
| **States** | Visual spec for each applicable state (§2) |
| **Platform** | Mobile / Web / TV differences (§3) |
| **A11y** | Roles, labels, keyboard, target size |

Rules:
- A component may only use tokens listed in its contract. Adding a token = updating the contract.
- Radius is a contracted value. Different radius = drift. Change requires updating this contract and radius-governance.md §2.
- Sizing tokens are contracted values. Raw `px` for height/width = violation. New sizes require governance (sizing-scale.md §7).
- Touch/focus targets are separate from visual height. A compact visual element still needs transparent padding to meet `--touch-min` (sizing-scale.md §5).

---

# 2. The State Model

Every interactive component declares which of these it supports and how each looks. **No invented states.**

| State | Trigger | JioGames treatment |
|---|---|---|
| `default` | rest | base tokens |
| `hover` | pointer over (web only) | subtle bg/scale shift, `--dur-fast` |
| `active`/pressed | press | `transform: scale(.96–.98)`, `--dur-fast` |
| `focus` | keyboard / D-pad | green glow ring (never bare `outline:none`) |
| `selected` | chosen in a set | `--jio` border + `--jio-glow` |
| `disabled` | unavailable | `opacity:.32`, `cursor:not-allowed`, no animation |
| `loading` | async | spinner/skeleton, not just dimming |

Focus ring (shared): `box-shadow: 0 0 0 3px rgba(0,168,89,.15)` (mobile/web), TV uses the larger `0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4)` + `scale(1.05)`.

---

# 3. The Platform Interaction Model

| | Mobile | Web | TV |
|---|---|---|---|
| Primary input | touch | pointer + keyboard | D-pad (focus) |
| `hover` | none | yes | **none** |
| `focus` | on field entry | `:focus-visible` | **always visible**, drives navigation |
| Press feedback | `scale(.96)` | `scale(.97)` | avoid scale on press; use glow |
| Min target | 44×44px | 32×32px (pointer) | 60×60px focusable |
| Emphasis on select | border + glow | border + glow | glow ring + `scale(1.05)` |

Rule: TV has no hover. Any `:hover`-only affordance must also exist on `:focus`.

---

# 4. Component Contracts

## AppBar

**Owner:** Jeetesh Shah
**Source file:** `jiogames-header.html`

### Variants

| Variant | Class | Use case |
|---|---|---|
| Home — transparent | `.appbar` | Over hero image, page top |
| Home — scrolled | `.appbar.header-scrolled` | After scroll past 80px |
| Home — hidden | `.appbar.header-hidden` | Scrolling down past threshold |
| Game detail | `.appbar.appbar--detail` | Over game hero, back button only, no title |
| Inner page | `.appbar.appbar--inner` | Notifications, settings — solid bg + back + title |

**When to use which variant:**

| Surface | Variant |
|---|---|
| Home, Browse, Library (top-level) | `appbar` — logo + search + bell |
| Game detail, Pass upsell | `appbar--detail` — back only, overlays hero |
| Settings, Notifications, Search results | `appbar--inner` — back + title, solid bg |
| OTP, cinematic intro | No AppBar |

---

### Anatomy

**Home:**
```
[ JioGames logo ] [ PASS badge? ] ·····spacer····· [ Search ] [ Bell● ]
```

**Game detail (`appbar--detail`):**
```
[ ← Back ]
```
Container fully transparent — overlays hero image. Back button uses dark-glass modifier.

**Inner page (`appbar--inner`):**
```
[ ← Back ]  [ Page title ]  ·····flex-1·····  [ ⋮ Kebab? ]
```
Solid `var(--bg)` background + `1px solid var(--hairline)` bottom border.

---

### Sizing & Tokens

| Property | Token | Value |
|---|---|---|
| Container padding | — | `8px` top · `var(--gutter)` sides · `14px` bottom |
| Logo height | — | `26px`, `width: auto` — never distort |
| Icon button size | `--icon-wrapper-sm` | `40×40px` |
| Icon button radius | — | `50%` circular |
| Icon SVG size | `--icon-size-xs` | `14px` · `fill: currentColor` |
| Notification dot | `--jio` / `--bg` | `7×7px` · `top:8px right:8px` · ring `0 0 0 2px var(--bg)` |
| Scrolled bg | — | `rgba(0,0,0,.7)` + `blur(14px)` |
| Hide threshold | — | `scrollTop > 80px` + scrolling down |
| Jitter guard | — | `8px` delta filter |
| Transition | `--dur-default` `--spring` | `200ms cubic-bezier(.22,1,.36,1)` |
| Hide transform | — | `translateY(-110%)` |
| z-index | — | `40` |
| Active press | `--dur-fast` | `scale(.95)` · bg `rgba(255,255,255,.08)` |

---

### Icon button — shared spec

`.icon-btn` is **identical** across all AppBar variants as the base class. Only the `appbar--detail` back button adds `.icon-btn--dark` for legibility over hero imagery.

```css
/* Base — used on home search, bell; inner-page back, kebab */
.icon-btn {
  width: var(--icon-wrapper-sm);
  height: var(--icon-wrapper-sm);
  border-radius: 50%;
  background: rgba(255,255,255,.04);
  border: 1px solid var(--hairline);
  display: flex; align-items: center; justify-content: center;
  position: relative; cursor: pointer;
  transition: background var(--dur-fast), transform var(--dur-fast) var(--spring);
}
.icon-btn:active {
  background: rgba(255,255,255,.08);
  transform: scale(.95);   /* contracted value — never .92 or .96 */
}
.icon-btn svg {
  width: var(--icon-size-xs);
  height: var(--icon-size-xs);
  fill: currentColor;      /* solid glyph — no stroke, no stroke-width */
  color: var(--text);
}

/* Dark-glass modifier — appbar--detail back button only (over hero image) */
.icon-btn--dark {
  background: rgba(0,0,0,.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: none;
}
.icon-btn--dark:active {
  background: rgba(0,0,0,.65);
}
```

**Rule:** Do not create variant-specific icon button classes (e.g. `.gd-icon-btn`). Use `.icon-btn` + `.icon-btn--dark` only.

---

### Icons (DLS library)

All icons from `icons/svg/`. `24×24` viewBox, solid fill paths, no stroke.

| Icon | File | Used in |
|---|---|---|
| Search | `ic_search.svg` | Home |
| Notification | `ic_notification.svg` | Home |
| Back / chevron left | `ic_chevron_left.svg` | Game detail, Inner page |
| Kebab / more | `ic_more_vertical.svg` | Inner page (optional) |

```css
.icon-btn          { color: var(--text); }
.icon-btn svg      { fill: currentColor; }
/* Never use fill="<hex>" or stroke on DLS icons */
```

---

### States

**Home scroll states:**

| State | Class | Spec |
|---|---|---|
| transparent | `.appbar` | No background |
| scrolled | `.appbar.header-scrolled` | `rgba(0,0,0,.7)` + `blur(14px)` |
| hidden | `.appbar.header-hidden` | `translateY(-110%)` |

**Notification dot:**
Add `.has-notification` to bell button. Dot: `7×7px`, `background: var(--jio)`, `box-shadow: 0 0 0 2px var(--bg)`, `position: absolute; top:8px; right:8px`.

```html
<button class="icon-btn has-notification" aria-label="Notifications, new">
  <!-- bell svg -->
  <span class="dot" aria-hidden="true"></span>
</button>
```

**PASS badge** (home only, after logo):
```html
<span class="mp-badge">PASS</span>
```
Hide with `display:none` when user has no pass.

---

### Scroll JS contract

```javascript
(function(){
  var sc  = document.getElementById('scroller');
  var bar = document.querySelector('.appbar');
  var lastY = 0, threshold = 8;   /* 8px jitter guard */
  sc.addEventListener('scroll', function(){
    var y = sc.scrollTop;
    bar.classList.toggle('header-scrolled', y > 80);
    if (Math.abs(y - lastY) < threshold) return;
    bar.classList[y > lastY ? 'add' : 'remove']('header-hidden');
    lastY = y;
  }, {passive:true});
})();
```

`appbar--detail` and `appbar--inner`: no hide-on-scroll. Blur-on-scroll only:
```javascript
scroller.addEventListener('scroll', function(){
  bar.classList.toggle('header-scrolled', scroller.scrollTop > 20);
}, {passive:true});
```

---

### Platform

| Platform | Behaviour |
|---|---|
| Mobile | All 3 variants. Scroll hide/show active on home. |
| Web | Home bar always visible (no hide). `--gutter` → 40px via token. |
| TV | **Not used** — sidebar nav, D-pad back. No AppBar on TV. |

---

### A11y

- Container: `<header role="banner">`
- Logo: `<img alt="JioGames">`
- Search: `<button aria-label="Search">`
- Bell (no dot): `<button aria-label="Notifications">`
- Bell (with dot): `<button aria-label="Notifications, new">`
- Back: `<button aria-label="Back">`
- Kebab: `<button aria-label="More options">`
- Inner page title: `<h1>` (new page context)
- Focus ring: `box-shadow: 0 0 0 3px rgba(0,168,89,.4)`

---

### Forbidden (all variants)

- Avatar / profile button — dedicated profile surface only
- Heart / wishlist / like — page-level action, not nav
- `stroke-width` on any icon SVG — solid glyph only
- Raw `px` for icon button size — use `var(--icon-wrapper-sm)`
- Variant-specific icon button classes — use `.icon-btn` / `.icon-btn--dark` only
- Any icon beyond search / bell / back / kebab — governance approval required

---

## Button

**Owner:** Jeetesh Shah
**Anatomy:** container + label (+ optional leading icon).
**Tokens:** `--jio` (primary bg) · `--text-inv` (label) · `--component-padding` (h-pad) · `--space-1` (icon gap) · `--spring` · `--dur-fast` · type token `text.cta`.
**Radius:** `--pill` — all button variants. Never rectangular.
**Sizing:**
- Primary: `height: var(--ctrl-h)` — platform-aware (54px mobile/web → 72px TV automatically)
- Small CTA: `height: var(--ctrl-h-sm)` — **mobile/web only**; below TV `--touch-min`, do not use on TV
- Ghost: `height: var(--ctrl-h-ghost)` — **mobile/web only**; below TV `--touch-min`, do not use on TV
- Touch target: add transparent `padding-block` so total hit area ≥ `var(--touch-min)` on compact variants
**Variants:** primary (green/black) · secondary (`--glass-1` bg, `--text`) · cta-sm (36px, mobile/web only) · skip/ghost (`--text3`, no bg, mobile/web only).

| State | Spec |
|---|---|
| default | bg `--jio`, label `--text-inv`, radius `--pill`, height 54 (mobile) |
| active | `transform: scale(.97)` |
| focus | green glow ring |
| disabled | `opacity:.32`, `cursor:not-allowed` |
| loading | label → spinner, width held, still disabled |

**Platform:** Primary height `var(--ctrl-h)` — 54px mobile/web → 72px TV, automatic via token. TV adds focus glow + `scale(1.05)`, no hover. **cta-sm and ghost variants are mobile/web only** — do not render on TV (below 60px focus target minimum).
**A11y:** real `<button>`; icon-only needs `aria-label`; label never below 16/18/22px.

## Card

**Owner:** Jeetesh Shah
**Anatomy:** container + (media) + content stack.
**Tokens:** `--card-bg` · `--card-padding` · `--border-subtle` · `--jio-glow` (selected) · content via stack utilities.
**Radius:** `--r4` (landscape/square game card) · `--r7` (pass card, editorial feature) · `--r2` (marquee hero card). Choose by card type — see radius-governance.md §2.
| State | Spec |
|---|---|
| default | `--card-bg`, radius, optional `--border-subtle` |
| active | `scale(.98)` |
| selected | `--jio` border + `0 0 0 2px var(--jio), 0 6px 28px rgba(0,168,89,.45)` |
| focus (TV) | glow ring + `scale(1.05)` |

**Platform:** padding 16/24/32; TV focusable + glow.
**A11y:** if whole card is a link/button, wrap in one focusable element; don't nest interactives.
**Internal spacing:** use `.content-stack` / `.tight-stack` — never child margins.

## Text Input

**Owner:** Jeetesh Shah

**Tokens:** `--glass-1` bg · `--border` → `--jio` (focus) · `--component-padding` · `--text` (value) · `--text3` (placeholder) · focus glow.
**Radius:** `--r5` — all text input variants.
| State | Spec |
|---|---|
| default | `--glass-1`, `1.5px solid --border` |
| focus | border `--jio` + `0 0 0 3px rgba(0,168,89,.14)` |
| error | border `--negative`; message = caption-bold `--negative` |
| disabled | `opacity:.32` |

**A11y:** `<label>` always (not placeholder-as-label); correct `type`/`inputmode`/`autocomplete`; never block paste; value more readable than label.

## OTP

**Owner:** Jeetesh Shah

**Anatomy:** row of N boxes + hidden input.
**Tokens:** `--glass-1` · `--border`→`--jio` · `--jio-soft` (filled bg) · `--spring-bounce` · type 26px/700.
**Radius:** `--r4` — each OTP digit box.
| State | Spec |
|---|---|
| default | `--glass-1`, `--border` |
| active (cursor) | border `--jio` + glow + blinking caret |
| filled | border `--jio`, bg `--jio-soft`, `box-pop` animation |
| error | `shake` animation, border `--negative` |

**A11y:** single hidden input drives boxes; `inputmode="numeric"`, `autocomplete="one-time-code"`.

## Chip

**Owner:** Jeetesh Shah

**Tokens:** `--chip-bg` · `--border-subtle`→`--jio` · `--space-1`/`--space-3` padding · `text.badge`.
**Radius:** `--pill` (inline action chip) · `--r4` (platform/filter tile chip). Tile format uses `--r4` — pill would look over-rounded at that height.
| State | Spec |
|---|---|
| default | `--chip-bg`, `--border-subtle` |
| active | `scale(.95)` |
| selected | `--jio` border + (chip-specific) `--jio` text/glow |

**Platform:** TV focus ring; min target 44/32/60.
**A11y:** selectable chips = `role="button"` + `aria-pressed`; filter groups = `role="group"`.

## Bottom Sheet

**Owner:** Jeetesh Shah

**Tokens:** `--sheet-top`→`--sheet-bg` (gradient) · `--sheet-padding` · `--overlay-scrim` + blur · `--spring` · `--dur-sheet`.
**Radius:** `--r9 --r9 0 0` — top corners only. Bottom is flush to screen edge.
| State | Spec |
|---|---|
| closed | `translateY(100%)`, backdrop transparent |
| open | `translateY(0)`, backdrop `--overlay-scrim` + `blur(8px)` |

**Platform:** mobile/web only — **not used on TV** (TV uses full screens).
**A11y:** `role="dialog"`, focus trap, `Esc` closes, `overscroll-behavior: contain`, restore focus on close.

## Rail

**Owner:** Jeetesh Shah

**Tokens:** `--card-gap` (between cards) · `--gutter` (leading + last-child trailing) · `--section-gap` (below) · `text.railTitle` (head).
**Radius:** n/a — the rail container has no radius. Radius belongs to the child card components it contains.
**Behavior:** `scroll-snap-type: x mandatory`; leading `padding-left: var(--gutter)`; trailing `:last-child { margin-right: var(--gutter) }` (see spacing-and-grid.md §7); never `::after` calc spacer.
**Platform:** Mobile/TV rail-first; Web may become a grid. TV: focused card must not clip at edges; last card reachable.
**A11y:** keyboard/D-pad horizontal nav; `aria-label` on the rail; head is a real heading.

## Pass Card (Mobile / Ultimate)

**Owner:** Jeetesh Shah

**Tokens:** Mobile = `#0e1a14` bg + `--border` green; Ultimate = green gradient + `--border-ultimate` + `--ultimate` CTA (**never blue**) · `--card-padding` · `text.cardTitle` (name) · `text.price` · `text.body` (perks) · `text.badge` (tag/popular).
**Radius:** `--r7` — both Mobile and Ultimate tiers. Same radius, different backgrounds.
| State | Spec |
|---|---|
| default | tier bg + corner radial glow |
| active | `scale(.98)` |
**A11y:** price + plan name at Primary emphasis; CTA is a real button.

## Genre Tile

**Owner:** Jeetesh Shah

**Tokens:** image bg · `2px transparent`→`--jio` border · `--jio-glow` (selected) · `--spring`.
**Radius:** `--r5` — all genre/category tiles.
| State | Spec |
|---|---|
| default | image `brightness(.55)` |
| active | `scale(.96)` |
| selected | `--jio` border + glow + `scale(1.03)` + image `brightness(.95)` |

**A11y:** `role="checkbox"` + `aria-checked` (multi-select set).

## Tab Bar

**Owner:** Jeetesh Shah

**Anatomy:** container pill + N tab items (icon + label).
**Tokens:** `--card-bg` (container bg) · `--border-subtle` (container border) · `--jio` (active icon/label) · `--text3` (inactive) · `text.caption` (label) · `--dur-fast` · `--spring`.
**Radius:** `--pill` — the floating tab bar container is a full pill.
| State | Spec |
|---|---|
| default | icon + label `--text3` |
| active | icon + label `--jio`, no background change on tab item |
| pressed | `scale(.94)` on tab item |
| focus (TV) | not used — TV uses full-screen navigation patterns |

**Platform:** Mobile/Web — floating pill docked above safe-area bottom. **Not used on TV** (TV uses sidebar or full-screen nav).
**A11y:** `role="tablist"` on container; each tab `role="tab"` + `aria-selected`; active tab visually distinct by colour not position alone.

## Toast / Snackbar

**Owner:** Jeetesh Shah

**Tokens:** `--card-bg` · `--text` · `--component-padding` · `--dur-default`.
**Radius:** `--r3` — compact transient surface.
**Behavior:** enter fade+slide, auto-dismiss, `--dur-default`.
**A11y:** `role="status"` `aria-live="polite"`; never the sole signal for critical errors.

---

# 5. Accessibility Contract (all components)

Applies to every component above:

- Semantic element first (`<button>`/`<a>`/`<input>`), not `<div onclick>`.
- Never bare `outline: none` — always a visible focus replacement (green glow).
- Icon-only controls have `aria-label`; decorative icons `aria-hidden="true"`.
- Min target: 44 (mobile) / 32 (web pointer) / 60 (TV) px.
- Status never by colour alone — pair with icon/label/weight.
- Critical text (error/payment/subscription/OTP) at Primary emphasis, never `--text3`.
- `prefers-reduced-motion` honored (tokens already collapse durations).
- TV: every interactive element is focusable and shows the focus ring.

---

# 6. Release Gate

> A component instance ships only if:

- [ ] It uses a contracted component — not ad-hoc CSS
- [ ] Only tokens listed in the contract are used (no raw values)
- [ ] Radius matches the contracted `--r*` or `--pill` token — no raw px, no different token
- [ ] Inner radius rule checked if component contains nested rounded children (radius-governance.md §4)
- [ ] All applicable states implemented (focus + disabled not skipped)
- [ ] Focus ring present; no bare `outline: none`
- [ ] Per-platform behavior correct (TV focus, no hover-only affordances)
- [ ] Internal spacing via stack utilities, not child margins
- [ ] A11y contract met (semantics, labels, target size, contrast)
- [ ] Any new variant is added to this contract, owner-approved
- [ ] `tokens/validate.sh` passes
