# JioGames Motion Governance

> **Token-first.** Use `var(--dur-*)` and `var(--spring)` — never raw milliseconds or cubic-bezier strings in component CSS. Raw values are allowed only inside the approved named keyframe recipes in §6.

JioGames motion is **fast, game-native, spring-based, and purposeful**. Every animation earns its place. Motion communicates state — not decoration.

**Structure**

1. Core Principles
2. Token Reference
3. Motion Categories
4. Motion Decision Tree ← *most important*
5. Component Motion Map
6. Keyframe Library
7. Screen Transitions
8. Content Stagger
9. Performance Rules
10. TV Motion Rules
11. Reduced Motion Governance
12. Anti-Patterns
13. Motion QA Checklist
14. Pre-Ship Release Gate

---

# 1. Core Principles

1. **Token-first.** Duration and easing tokens are the source of truth. Component CSS uses `var(--dur-fast)`, not `120ms`.
2. **Raw durations only in keyframe recipes.** Keyframe percentages (e.g. `35% { transform: scale(1.14) }`) may use raw values. Everything else uses tokens.
3. **Compositor properties for layout movement and loops.** Use `transform` and `opacity` for all continuous animation and layout movement. One-shot UI state changes (`border-color`, `background`, `box-shadow`) are allowed when tokenised and not looped. Never animate `width`, `height`, `top`, `left`, `margin`, `padding`, or `box-shadow blur radius` in loops or scroll-linked contexts.
4. **Spring easing as default.** `--spring` for most enters. `--spring-bounce` only for playful one-shot feedback (OTP fill, selection).
5. **No `transition: all`.** Always list explicit properties.
6. **Reduced motion is mandatory.** Every animated component has a reduced-motion fallback. Focus glow is exempt — it is an affordance, not decoration.
7. **Purposeful, not decorative.** If removing an animation makes the UI clearer, remove it.
8. **Interactive UI stays under 500ms.** TV content enter may reach 600ms. Ambient loops are exempt.

---

# 2. Token Reference

All tokens live in `tokens/tokens.json`, generated into `tokens/tokens.css`.

### Easing

| Token | Value | Use |
|---|---|---|
| `--spring` | `cubic-bezier(.22,1,.36,1)` | Default enter — most UI elements |
| `--spring-bounce` | `cubic-bezier(.34,1.56,.64,1)` | Playful one-shot feedback — OTP fill, genre select |
| `--ease-screen` | `cubic-bezier(.42,0,.18,1)` | Screen-to-screen slide |
| `--ease-out` | `cubic-bezier(0,0,.2,1)` | Fades, overlay appear, tooltip enter |

`--ease-out` is for fades and overlays **only** — not for UI state transitions (use `--spring` instead).

### Duration

| Token | Value | Category | Use |
|---|---:|---|---|
| `--dur-instant` | 90ms | Micro | Tiny tap feedback, ripple |
| `--dur-fast` | 120ms | Micro | Press, focus ring, chip select |
| `--dur-default` | 200ms | State | Normal component state transitions |
| `--dur-pop` | 280ms | Feedback | OTP box fill, check icon appear |
| `--dur-error` | 380ms | Feedback | Shake animation |
| `--dur-sheet` | 400ms | Navigation | Bottom sheet open/close |
| `--dur-enter` | 420ms | Enter | Content enter — fade-up, tile-in, stagger |
| `--dur-screen` | 420ms | Navigation | Screen-to-screen slide transition |

`--dur-enter` and `--dur-screen` share the same value but are semantically independent. They may diverge in future releases.

**Ambient durations** (marquee, hero breathing, background loops) are not tokenised — they are recipe-specific. Values like `55s` and `65s` are approved constants inside named keyframe recipes only. They must always pause under `prefers-reduced-motion`.

---

# 3. Motion Categories

Six categories cover every animation in JioGames. Each category has a fixed duration range, easing, and platform rule.

### 1 — Micro Feedback

Tap, press, chip select, focus ring appearance.

| | Value |
|---|---|
| Duration | `--dur-instant` to `--dur-fast` (90–120ms) |
| Easing | `--spring` |
| Property | `transform: scale()` or `box-shadow` |
| TV | Focus glow only — no press bounce |

### 2 — State Transition

Default → selected, hover, error, success, disabled.

| | Value |
|---|---|
| Duration | `--dur-fast` to `--dur-default` (120–200ms) |
| Easing | `--spring` (state change) · `--spring-bounce` (success/selection) |
| Property | `border-color`, `background`, `transform`, `box-shadow` |
| TV | Glow change only — no scale on state |

### 3 — Content Entrance

Cards, sections, hero content, preference tiles entering a screen.

| | Value |
|---|---|
| Duration | `--dur-enter` (420ms) with stagger |
| Easing | `--spring` |
| Property | `opacity`, `transform: translateY()` · `transform: scale()` |
| TV | 500–600ms; larger translate distance (32px vs 20px) |

### 4 — Navigation Transition

Screen slide, modal open, sheet open, sheet close.

| | Value |
|---|---|
| Duration | `--dur-screen` / `--dur-sheet` (420ms / 400ms) |
| Easing | `--ease-screen` (screen slide) · `--spring` (sheet) |
| Property | `transform: translateX/Y()` · `opacity` (backdrop) |
| TV | No sheets — full-screen transitions only |

### 5 — Ambient Motion

Hero breathing, parallax, marquee strips, background loops.

| | Value |
|---|---|
| Duration | Recipe-specific (seconds to minutes) |
| Easing | `linear` — constant speed only (exception to linear ban) |
| Property | `transform` only — never `opacity` looping |
| TV | **Forbidden** — no ambient loops on TV |
| Reduced motion | Must pause completely |

### 6 — System Motion

Loading shimmer, skeleton, progress bar.

| | Value |
|---|---|
| Duration | `--dur-default` (shimmer cycle base) |
| Easing | `linear` (constant shimmer sweep) |
| Property | `transform: translateX()` (shimmer) · `transform: scaleX()` (progress) |
| TV | Skeleton only — no shimmer sweeps on TV |
| Reduced motion | Replace shimmer with static placeholder |

---

# 4. Motion Decision Tree

Start from the use case, not from an animation you want to use.

| Use case | Category | Pattern |
|---|---|---|
| Button or chip pressed | Micro | `scale(.96–.98)` · `--dur-fast` · `--spring` |
| Focus ring appears | Micro | `box-shadow` glow · `--dur-fast` |
| Card or tile selected | State | Green glow + `scale(1.03)` · `--spring-bounce` |
| OTP digit filled | Feedback | `box-pop` keyframe · `--dur-pop` · `--spring-bounce` |
| Error state triggered | Feedback | `shake` keyframe · `--dur-error` · one-shot only |
| Success / check icon | Feedback | `check-scale` keyframe · `--dur-pop` · `--spring-bounce` |
| New content enters screen | Enter | `fade-up` with stagger · `--dur-enter` · `--spring` |
| Genre / preference tiles enter | Enter | `tile-in` with stagger · `--dur-enter` · `--spring` |
| Screen changes | Navigation | Horizontal slide · `--dur-screen` · `--ease-screen` |
| Sheet opens | Navigation | `translateY` up · `--dur-sheet` · `--spring` + backdrop fade |
| Loading / waiting | System | Shimmer sweep or skeleton · `linear` |
| Progress bar fills | System | `transform: scaleX()` · `linear` |
| Hero ambient effect | Ambient | `breathe` or parallax · `linear` · reduced-motion safe |
| Marquee / scroll strip | Ambient | `marquee-fwd/rev` · `linear` · pauses in reduced-motion |
| TV focus moves to element | Micro | Glow ring + `scale(1.05)` · `--dur-fast` |

---

# 5. Component Motion Map

One component, one motion contract. Screens compose these — they do not invent new motion per component.

| Component | Motion | Token |
|---|---|---|
| Primary button | Press `scale(.97)` | `--dur-fast` · `--spring` |
| Small CTA | Press `scale(.96)` | `--dur-fast` · `--spring` |
| Ghost button | Press `opacity: .6` | `--dur-fast` |
| Action chip | Press `scale(.95)` | `--dur-fast` · `--spring` |
| Platform chip | Press `scale(.95)` + selected glow | `--dur-fast` · `--spring` |
| Genre tile | Selected `scale(1.03)` + glow | `--spring-bounce` · `--dur-fast` |
| OTP box — fill | `box-pop` | `--dur-pop` · `--spring-bounce` |
| OTP row — error | `shake` (once) | `--dur-error` |
| Text input — focus | `border-color` + glow | `--dur-fast` |
| Bottom sheet | `translateY(0)` + backdrop | `--dur-sheet` · `--spring` |
| Screen transition | `translateX` slide | `--dur-screen` · `--ease-screen` |
| Rail | Native scroll + snap — no custom drag | — |
| Pass card | Press `scale(.98)` | `--dur-fast` · `--spring` |
| Skeleton/shimmer | Shimmer sweep | `--dur-default` · `linear` |
| TV focusable | Glow + `scale(1.05)` | `--dur-fast` · `--spring` |
| Hero background | `breathe` or parallax | recipe-specific · pauses reduced-motion |
| Marquee strip | `marquee-fwd/rev` | recipe-specific · pauses reduced-motion |

---

# 6. Keyframe Library

All named keyframes used in JioGames. Import `tokens.css` and define these in your screen's `<style>`. Do not modify keyframe values — if a change is needed, propose it as an RFC.

```css
/* ── Content entrance ───────────────────────────────── */
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes slide-down {
  from { opacity: 0; transform: translateY(-12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes slide-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes tile-in {
  from { opacity: 0; transform: translateY(24px) scale(.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── Feedback ───────────────────────────────────────── */
@keyframes box-pop {
  /* Duration: --dur-pop (280ms) · Easing: --spring-bounce */
  0%   { transform: scale(1); }
  35%  { transform: scale(1.14); }
  65%  { transform: scale(.97); }
  100% { transform: scale(1); }
}
@keyframes check-scale {
  /* Duration: --dur-pop (280ms) · Easing: --spring-bounce */
  0%   { transform: scale(0); }
  60%  { transform: scale(1.2); }
  100% { transform: scale(1); }
}
@keyframes shake {
  /* Duration: --dur-error (380ms) · Easing: ease · One-shot only */
  0%,100% { transform: translateX(0); }
  18%     { transform: translateX(-7px); }
  36%     { transform: translateX(7px); }
  54%     { transform: translateX(-5px); }
  72%     { transform: translateX(5px); }
  88%     { transform: translateX(-2px); }
}

/* ── Navigation ─────────────────────────────────────── */
@keyframes sp-enter {
  /* Duration: --dur-enter · Easing: --spring */
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: none; }
}
@keyframes sim-in {
  from { opacity: 0; transform: translateY(10px) scale(.95); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── System ─────────────────────────────────────────── */
@keyframes shimmer {
  /* Use transform, not background-position — compositor only */
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}
@keyframes fact-bar {
  /* Progress bar: scaleX not width — compositor only */
  /* Apply with: transform-origin: left center */
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
@keyframes pulse-ring {
  0%   { opacity: .7; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.6); }
}
@keyframes otp-cursor {
  0%,100% { opacity: 1; }
  50%     { opacity: 0; }
}

/* ── Ambient ─────────────────────────────────────────── */
@keyframes breathe {
  /* Approved constant: 18s linear infinite — pauses in reduced-motion */
  0%,100% { transform: scale(1) translateX(-50%); opacity: .9; }
  50%     { transform: scale(1.12) translateX(-44%); opacity: 1; }
}
@keyframes marquee-fwd {
  /* Approved constant: 55s linear infinite */
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
@keyframes marquee-rev {
  /* Approved constant: 65s linear infinite */
  from { transform: translateX(-50%); }
  to   { transform: translateX(0); }
}
@keyframes logo-pop {
  /* Duration: --dur-enter · Easing: --spring */
  0%   { transform: scale(.8); opacity: 0; }
  60%  { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes gff-appear {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

**Adding a new keyframe:** propose via RFC (governance.md §3). Do not add keyframes directly to component files — add to this library and cross-reference from the component.

---

# 7. Screen Transitions

Screens slide horizontally. The exiting screen compresses left; the entering screen slides in from right.

```css
.screen {
  position: absolute; inset: 0;
  transform: translateX(105%);
  transition: transform var(--dur-screen) var(--ease-screen);
  will-change: transform;
}
.screen.active { transform: translateX(0); }
.screen.behind  { transform: translateX(-28%); }
```

**TV:** full-screen fade (`opacity` transition) instead of slide — `--ease-out`, `--dur-screen`.

```css
@media (min-width: 1280px) and (min-height: 720px) {
  .screen {
    transform: none;
    opacity: 0;
    transition: opacity var(--dur-screen) var(--ease-out);
  }
  .screen.active { opacity: 1; }
  .screen.behind  { opacity: 0; }
}
```

---

# 8. Content Stagger

When multiple elements enter at once, stagger by ~60ms per element to create visual flow.

```css
/* Named enter classes */
.enter-1 { animation: fade-up var(--dur-enter) var(--spring) 50ms  both; }
.enter-2 { animation: fade-up var(--dur-enter) var(--spring) 110ms both; }
.enter-3 { animation: fade-up var(--dur-enter) var(--spring) 170ms both; }
.enter-4 { animation: fade-up var(--dur-enter) var(--spring) 230ms both; }

/* Grid stagger (genre tiles, preference grids) */
.tile:nth-child(1) { animation: tile-in var(--dur-enter) var(--spring) 80ms  both; }
.tile:nth-child(2) { animation: tile-in var(--dur-enter) var(--spring) 140ms both; }
.tile:nth-child(3) { animation: tile-in var(--dur-enter) var(--spring) 200ms both; }
.tile:nth-child(4) { animation: tile-in var(--dur-enter) var(--spring) 260ms both; }
.tile:nth-child(5) { animation: tile-in var(--dur-enter) var(--spring) 320ms both; }
.tile:nth-child(6) { animation: tile-in var(--dur-enter) var(--spring) 380ms both; }
```

Rules:
- Always use `animation-fill-mode: both` — never leave elements invisible before animation fires.
- Max stagger depth: 6 items. Beyond 6, group remaining items with the last delay.
- TV: collapse stagger — all items enter simultaneously at the TV enter duration (500–600ms).

---

# 9. Performance Rules

### Animate only compositor-friendly properties

The browser compositor handles `transform` and `opacity` without triggering layout or paint. Everything else may cause reflow.

**For layout movement and continuous loops — compositor only:**
- `transform: translate() scale() rotate()`
- `opacity`

**For one-shot UI state changes — allowed when tokenised, not looped:**
- `border-color`, `background`, `box-shadow` (e.g. focus ring appearing, chip selecting)
- Keep duration ≤ `--dur-default` (200ms); never loop these properties

**Never animate in loops or scroll-linked contexts:**
- `width` / `height`
- `top` / `left` / `right` / `bottom`
- `margin` / `padding`
- `box-shadow blur radius` (glow `box-shadow` for one-shot state change is fine; never loop it)
- `filter` on large images
- `backdrop-filter` on TV (banned entirely — §10)

### Progress bar pattern

Use `scaleX`, not `width`:

```css
.progress-bar {
  transform-origin: left center;
  animation: fact-bar var(--dur-default) linear both;
}
/* @keyframes fact-bar: scaleX(0) → scaleX(1) — defined in §6 */
```

### Shimmer pattern

Use a translated overlay, not `background-position`:

```css
.shimmer-wrap { position: relative; overflow: hidden; }
.shimmer-wrap::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,.06) 50%, transparent 100%);
  animation: shimmer 1.6s linear infinite;
}
/* @keyframes shimmer: translateX(-100%) → translateX(100%) — defined in §6 */
```

### `will-change`

Use only on elements that are about to animate (add before, remove after). Never apply globally. Overuse creates layer pressure. Screen transition wrapper is the main legitimate use.

---

# 10. TV Motion Rules

TV users sit far away. Motion must be larger and slightly slower to read. But TV is **never a playground for decorative animation**.

### Allowed on TV

| Motion | Rule |
|---|---|
| Focus ring glow | Always — it is an affordance, not decoration |
| Focus `scale(1.05)` | Allowed **only** as a focus state, always paired with glow |
| Content entrance (`fade-up`) | 500–600ms, 32px translate (vs 20px mobile) |
| Screen fade transition | Full-screen `opacity` — no horizontal slide on TV |
| Skeleton placeholder | Static — no shimmer sweep |

### Forbidden on TV

| Motion | Reason |
|---|---|
| Decorative bounce / spring-bounce loops | Distracting at distance |
| Parallax / hero breathing | Performance; distraction |
| Marquee strips | Visual overload on large screen |
| Press/tap `scale` feedback | No direct input on TV — D-pad, no "press" |
| `backdrop-filter` | Performance on large canvas |
| Shimmer sweep animation | Too fast to read at distance |
| Stagger sequences | Collapse all items to enter simultaneously |

### TV enter pattern

```css
@media (min-width: 1280px) and (min-height: 720px) {
  .enter-1, .enter-2, .enter-3, .enter-4 {
    animation: fade-up 560ms var(--spring) both;
    /* Unified delay — no stagger on TV */
  }
}
```

---

# 11. Reduced Motion Governance

`tokens.css` collapses `--dur-fast`, `--dur-default`, and `--dur-enter` to `0ms` under `prefers-reduced-motion`. Components using these tokens are already compliant. The rules below handle cases the token collapse alone cannot cover.

### Screen transitions

Replace slide with fade:

```css
@media (prefers-reduced-motion: reduce) {
  .screen {
    transform: none;
    transition: opacity var(--dur-default) var(--ease-out);
  }
  .screen.active { opacity: 1; }
  .screen.behind  { opacity: 0; pointer-events: none; }
}
```

### Ambient motion — must stop completely

```css
@media (prefers-reduced-motion: reduce) {
  .marquee-row { animation: none; }
  .hero-bg     { animation: none; }
}
```

### OTP feedback

Replace `box-pop` with border colour change:

```css
@media (prefers-reduced-motion: reduce) {
  .otp-box.filled { animation: none; border-color: var(--jio); }
}
```

### Error shake

Replace `shake` with static error icon + `--negative` border:

```css
@media (prefers-reduced-motion: reduce) {
  .otp-row.error { animation: none; }
  /* Error message + icon must already be present — motion is never the only signal */
}
```

### Stagger — collapse

```css
@media (prefers-reduced-motion: reduce) {
  .enter-1, .enter-2, .enter-3, .enter-4,
  .tile { animation: fade-in 1ms both; animation-delay: 0ms; }
}
```

### Focus glow — never suppressed

Focus glow is an accessibility affordance. Do **not** remove `box-shadow` focus styles under reduced-motion.

### Shimmer / skeleton

Replace animated shimmer with static `--card-bg` fill:

```css
@media (prefers-reduced-motion: reduce) {
  .shimmer-wrap::after { animation: none; display: none; }
}
```

---

# 12. Anti-Patterns

| Pattern | Reason | Fix |
|---|---|---|
| `transition: all` | Catches unintended properties, expensive | List explicit properties |
| Raw `120ms` in component CSS | Bypasses token | `var(--dur-fast)` |
| Raw `cubic-bezier(…)` in component CSS | Bypasses token | `var(--spring)` etc. |
| `animation-fill-mode: none` on enter animations | Elements flash before firing | Always use `both` |
| Duration > 500ms on interactive UI | Feels sluggish | `≤var(--dur-enter)` for product UI |
| Linear easing on UI state transitions | Robotic, mechanical | `--spring` for state, `linear` only for constant-speed ambient/progress |
| Bounce that does not settle | Jello / unresolved feel | Use `--spring-bounce` which settles by design |
| Parallax without reduced-motion fallback | Motion sickness risk | `animation: none` under `prefers-reduced-motion` |
| Animating `width` for progress bars | Triggers layout reflow | `transform: scaleX()` — compositor only |
| `box-shadow` glow looping in a keyframe | Expensive paint each frame | One-shot state change only — never loop |
| Scale `> 1.1` in interactive feedback | Looks glitchy | Max `1.05` for focus (TV), `1.03` for selection, `1.14` peak inside `box-pop` only |
| Press bounce on TV | No press input on TV | Glow-only on TV focus/select |
| New keyframe added directly to a screen file | Ungoverned, can't be reused | Add to §6 library via RFC |
| Stagger depth > 6 | Last items wait > 400ms, feels broken | Group remaining at delay 6 |

---

# 13. Motion QA Checklist

| Check | Required |
|---|---|
| All transition durations use `var(--dur-*)` tokens | Yes |
| All easing uses `var(--spring)` / `var(--spring-bounce)` / `var(--ease-screen)` / `var(--ease-out)` | Yes |
| No `transition: all` | Yes |
| No raw `cubic-bezier(…)` in component CSS | Yes |
| Only `transform` and `opacity` animated in loops | Yes |
| Progress bars use `transform: scaleX()` not `width` | Yes |
| Shimmer uses `transform: translateX()` not `background-position` | Yes |
| Stagger uses `animation-fill-mode: both` on all items | Yes |
| Ambient loops pause under `prefers-reduced-motion` | Yes |
| Screen transition replaced with fade under `prefers-reduced-motion` | Yes |
| Error state has icon + message in addition to `shake` | Yes |
| Focus glow NOT removed under `prefers-reduced-motion` | Yes |
| TV: no ambient loops, marquee, backdrop-filter, or press bounce | If TV in scope |
| TV: content entrance uses 500–600ms with `fade-up` (no stagger) | If TV in scope |
| New keyframes added to §6 library, not to screen file | If new keyframe |

---

# 14. Pre-Ship Release Gate

> A screen or component ships only if:

- [ ] Motion uses approved tokens and named keyframe recipes — no raw values
- [ ] No `transition: all` anywhere
- [ ] Animated properties are `transform` / `opacity` only (loops)
- [ ] Reduced-motion state implemented: ambient stops, slides become fades, shimmer becomes static
- [ ] Focus glow present and NOT suppressed in reduced-motion
- [ ] Error state uses motion + icon + message — motion is not the only signal
- [ ] TV behaviour defined: no decorative animation, focus `scale(1.05)` + glow only
- [ ] Stagger uses `animation-fill-mode: both` and depth ≤ 6
- [ ] Any new keyframe added to §6 library via RFC — not inline in screen
- [ ] `tokens/validate.sh` passes with exit 0
