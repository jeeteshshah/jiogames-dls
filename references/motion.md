# JioGames Motion Governance

> **Inherits `references/_core-rules.md`.** Rules in that file (dark-only, JioType-only, token-first, no Lucide, no silent deviation) are not repeated here.

> **Token-first.** Use `var(--dur-*)` and `var(--spring)` — never raw milliseconds or cubic-bezier strings in component CSS. Raw values are allowed only inside approved named keyframe recipes (§13) or the Approved Motion Constants table (§4).

JioGames motion is **calm, fluid, spatial, and purposeful**. Every animation earns its place. Motion communicates state, relationship, and feedback — not decoration.

**Structure**

1. Motion Personality
2. Core Principles
3. Token Reference
4. Approved Motion Constants
5. Motion Categories
6. Spatial Continuity Rules
7. Cause and Effect Rules
8. Soft Landing Rules
9. Motion Decision Tree
10. Micro Interaction Pattern Table
11. Platform Motion Matrix
12. Component Motion Map
13. Keyframe Library
14. Screen Transitions
15. Content Stagger
16. Performance Rules
17. TV Motion Rules
18. Haptic Pairing Rules
19. Animation Asset Rules
20. Do Not Animate
21. Reduced Motion Governance
22. Anti-Patterns
23. Motion QA Checklist
24. Pre-Ship Release Gate

---

# 1. Motion Personality

JioGames motion has a clear character. Every implementation decision should be tested against these qualities.

| Quality | What it means in practice |
|---|---|
| **Calm** | Nothing fights for attention. Motion happens quietly. The user is never startled. |
| **Fluid** | State changes feel continuous, not switched. Elements flow into position. |
| **Spatial** | Every element has a location. Motion respects origin and destination. |
| **Responsive** | Motion confirms input immediately. No delay between action and feedback. |
| **Cinematic but restrained** | Rich where it matters (hero, pass unlock, rewards). Invisible everywhere else. |
| **Fast but never abrupt** | Interactions complete quickly. Nothing snaps or cuts without cause. |
| **Game-native but not cartoonish** | Energy and presence. Not rubber-band physics or jelly bounces. |
| **Soft landing** | Elements settle cleanly. Spring easing, no repeated oscillation. |
| **Purposeful** | Every animation answers: what changed, why, and where to look next. |

### The benchmark

Use Apple-level restraint as the quality standard — not Apple visuals or platform UI. The goal: motion so well-matched to the interaction that users never notice it, but would feel its absence.

---

# 2. Core Principles

1. **Token-first.** Duration and easing tokens are the source of truth. Component CSS uses `var(--dur-fast)`, not `120ms`.
2. **Raw durations only in approved contexts.** Keyframe percentages and §4 Motion Constants may use raw values. Everything else uses tokens.
3. **Compositor properties for movement.** Use `transform` and `opacity` for layout movement and loops. One-shot state changes (`border-color`, `background`, `box-shadow`) are allowed when tokenised and not looped.
4. **Spring easing as default.** `--spring` for most enters. `--spring-bounce` only for one-shot celebration feedback (OTP fill, success).
5. **Reduced motion is mandatory.** Every animated component has a fallback. Focus glow is exempt — it is an affordance.
6. **Purposeful, not decorative.** If removing an animation makes the UI clearer, remove it.
7. **Interactive UI under 500ms.** TV enter up to `--dur-tv-enter` (560ms). Ambient loops exempt.
8. **Motion communicates state.** Not personality. Not brand energy. State.

---

# 3. Token Reference

All tokens live in `tokens/tokens.json`, generated into `tokens/tokens.css`.

### Easing

| Token | Value | Use |
|---|---|---|
| `--spring` | `cubic-bezier(.22,1,.36,1)` | Default enter — most UI elements |
| `--spring-bounce` | `cubic-bezier(.34,1.56,.64,1)` | One-shot celebration — OTP fill, success |
| `--ease-screen` | `cubic-bezier(.42,0,.18,1)` | Screen-to-screen slide |
| `--ease-out` | `cubic-bezier(0,0,.2,1)` | Fades, overlays, tooltip enter |
| `--ease-error` | `cubic-bezier(.36,.07,.19,.97)` | Error shake — tight, authoritative, no bounce |

`--spring-bounce` is for celebration, not default interaction. Use sparingly — one per flow maximum.

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
| `--dur-screen` | 420ms | Navigation | Screen-to-screen slide |
| `--dur-tv-enter` | 560ms | TV Enter | TV content entrance — larger canvas, slightly longer settle |
| `--dur-shimmer` | 1600ms | System | Shimmer/skeleton loop cycle |
| `--dur-icon-spin` | 1000ms | System | Loading icon rotation loop |
| `--dur-reduced-fade` | 100ms | Reduced motion | Gentle crossfade under reduced motion — NOT collapsed to 0ms |
| `--dur-reduced-instant` | 1ms | Reduced motion | Instant fallback — snap state change with technically non-zero duration |
| `--stagger-start` | 50ms | Stagger | First item delay |
| `--stagger-step` | 60ms | Stagger | Per-item delay increment |

**Ambient durations** (breathing, marquee) are recipe-specific constants in §4 — not tokenised.

---

# 4. Approved Motion Constants

Raw values allowed here and nowhere else. Each constant has a named owner and approved selector scope. Using these values outside the listed context is a violation.

| Constant | Value | Allowed context | Owner | Reason |
|---|---:|---|---|---|
| Shimmer animation | `var(--dur-shimmer)` | `.shimmer-wrap::after` | DLS Owner | Now tokenised — use `var(--dur-shimmer)` |
| Breathing / Ken Burns | `8s` | `.hero .bg` transition | DLS Owner | Ambient — not a UI interaction, no token |
| Marquee forward | `55s` | `.marquee-row.fwd` | DLS Owner | Ambient constant |
| Marquee reverse | `65s` | `.marquee-row.rev` | DLS Owner | Ambient constant — slightly slower for visual rhythm |
| Aurora drift | `12s` | `.aurora` | DLS Owner | Ambient decoration — cinematic hero only |
| Icon rotation | `var(--dur-icon-spin)` | `.icon-spin` | DLS Owner | Now tokenised — use `var(--dur-icon-spin)` |
| Reduced motion fade | `var(--dur-reduced-fade)` | `.screen` under reduced motion | DLS Owner | Now tokenised — intentionally not collapsed to 0ms |
| Shimmer gradient | `rgba(255,255,255,.06)` centre stop | `.shimmer-wrap::after` only | DLS Owner | No colour token for translucent white highlight; approved in this selector only. `tokens/validate.sh` must allow this value only in `.shimmer-wrap::after` — any use elsewhere is a violation. |
| Pulse ring | `2s` | `.wb-ring-expand`, `.pass-icon-wrap::before/::after` | DLS Owner | Pass-found / welcome-back pulse ring — ambient, not UI interaction |
| Spinner step | `0.75s` | `.step-progress` | DLS Owner | Indeterminate progress |
| Max stagger depth | `6 items` | Stagger sequences | DLS Owner | Beyond 6 = last item waits >400ms |

---

# 5. Motion Categories

Six categories cover every animation in JioGames. Each has a fixed duration range, easing, platform rule, and reduced motion handling.

### 1 — Micro Feedback

Tap, press, chip select, focus ring.

| | Value |
|---|---|
| Duration | `--dur-instant` to `--dur-fast` (90–120ms) |
| Easing | `--spring` |
| Properties | `transform: scale()`, `box-shadow` |
| TV | Focus glow only — no press scale |
| Reduced motion | Instant state change — no motion |

### 2 — State Transition

Default → hover → selected → error → disabled.

| | Value |
|---|---|
| Duration | `--dur-fast` to `--dur-default` (120–200ms) |
| Easing | `--spring` (state) · `--spring-bounce` (success only) |
| Properties | `border-color`, `background`, `transform`, `box-shadow` |
| TV | Glow change only — no scale on state |
| Reduced motion | Instant state change |

### 3 — Content Entrance

Cards, rails, hero text, tiles entering a screen.

| | Value |
|---|---|
| Duration | `--dur-enter` (420ms) with `--stagger-start` + `--stagger-step` |
| Easing | `--spring` |
| Properties | `opacity`, `transform: translateY()` |
| TV | `--dur-tv-enter` (560ms), no stagger, 32px translate distance |
| Reduced motion | `opacity` fade only, no translate, stagger collapses |

### 4 — Navigation Transition

Screen slide, sheet open/close, modal.

| | Value |
|---|---|
| Duration | `--dur-screen` / `--dur-sheet` (420ms / 400ms) |
| Easing | `--ease-screen` (slide) · `--spring` (sheet) |
| Properties | `transform: translateX/Y()`, `opacity` (backdrop) |
| TV | Fade only (`--ease-out`) — no slide |
| Reduced motion | Instant or opacity crossfade |

### 5 — Ambient Motion

Hero breathing, marquee, background loops.

| | Value |
|---|---|
| Duration | Constants from §4 (seconds to minutes) |
| Easing | `linear` — constant speed |
| Properties | `transform` only |
| TV | Forbidden |
| Reduced motion | Stop completely |

### 6 — System Motion

Shimmer, skeleton, progress.

| | Value |
|---|---|
| Duration | `var(--dur-shimmer)` (shimmer) |
| Easing | `linear` |
| Properties | `transform: translateX()` (shimmer), `transform: scaleX()` (progress) |
| TV | Static skeleton — no shimmer sweep |
| Reduced motion | Static placeholder |

---

# 6. Spatial Continuity Rules

Motion must respect space. Elements have an origin and a destination. Users should always understand where something came from and where it went.

### Rules

1. **Every motion has a source and destination.** If you can't name both, the motion is decorative — remove it.
2. **Sheets enter from bottom on mobile.** They originate below the viewport and return there on close.
3. **Screen transitions follow navigation direction.** Forward → slide left. Back → slide right (reverse).
4. **Returning to a previous screen reverses the original motion.** Never fade back to something that slid in.
5. **Cards come forward when focused or selected.** Scale up (`1.03` select, `1.05` TV focus) suggests physical proximity.
6. **Modals emerge from context when possible.** A modal triggered by a card should appear to emerge from that card's position, not from screen centre.
7. **Rail position is preserved after interaction.** A user who taps a card and returns should not find the rail has reset.
8. **Avoid random fade-ups when the element has a spatial source.** A chip appearing next to the input field that triggered it should slide from that direction, not fly up from nowhere.

### Spatial anti-patterns

- Content entering from outside the viewport when it was already partially visible
- Modals appearing from screen centre when triggered by a corner element
- Back navigation using forward slide direction
- Sheets sliding in from the side instead of bottom
- Focus ring appearing on elements the user did not navigate to

---

# 7. Cause and Effect Rules

Every animation must answer four questions. If it cannot, it should not exist.

| Question | If you cannot answer |
|---|---|
| **What triggered it?** | The motion is orphaned — remove it |
| **What changed?** | The motion communicates nothing — remove it |
| **Where should the user look next?** | The motion is directionally unclear — rewrite it |
| **What state is being communicated?** | The motion is decorative — remove it |

### Rules

1. **No orphan animation.** No motion runs without a user action or system event as its direct cause.
2. **No ambient UI motion.** The hero breathing is cinematic and expected. A card pulsing in a rail because it is "featured" is noise — use static visual hierarchy instead.
3. **Motion confirms, not announces.** A button press confirms the tap. A sheet opening is not a performance.
4. **Stagger communicates relationship.** Stagger a list of items that belong together. Do not stagger unrelated elements to make a screen feel animated.
5. **Error motion is purposeful.** `shake` tells the user: wrong input, try again. It is a message, not a visual effect. Play once, then stop.
6. **Success motion is brief.** `box-pop` on OTP, check icon scale on pass unlock. One beat. Done. Do not sustain success animation past the moment of confirmation.

---

# 8. Soft Landing Rules

Spring easing must produce mature, settled motion. Not bounce, not jello.

### Rules

1. **One oscillation, then settle.** Spring easing naturally overshoots slightly and returns. That one beat is the acceptable motion. Do not chain springs or apply bounce easing to produce multiple oscillations.
2. **No scale above approved limits:**
   - Touch press: `scale(.96–.98)` — barely perceptible pull
   - Selection: `scale(1.03)` — comes forward, does not lunge
   - TV focus: `scale(1.05)` — clear spatial shift on large screen
   - Pop keyframe peak: `scale(1.14)` inside `box-pop` keyframe only — not in component CSS
3. **`--spring-bounce` for one-shot celebration only.** OTP fill. Check icon. Pass unlock. Not for chip hover, card press, or scroll snap.
4. **Disable bounce under `prefers-reduced-motion`.** Replace with opacity change or instant state.
5. **Error shake settles immediately.** `shake` animation plays once via `animation-iteration-count: 1`. Not `infinite`. Not on hover.
6. **Selection glows and settles.** Border + glow appears (`--dur-fast`), then holds. It does not pulse or breathe.
7. **Loading does not bounce.** Rotation is linear. Progress is `scaleX`. Neither oscillates.

---

# 9. Motion Decision Tree

Start from the use case, not an animation you want to use.

| Use case | Category | Pattern |
|---|---|---|
| Button or chip pressed | Micro | `scale(.96–.98)` · `--dur-fast` · `--spring` |
| Focus ring appears | Micro | `box-shadow` · `--dur-fast` |
| Card or tile selected | State | Glow + `scale(1.03)` · `--spring-bounce` (one beat) |
| OTP digit filled | Feedback | `box-pop` · `--dur-pop` · `--spring-bounce` |
| Error state triggered | Feedback | `shake` · `--dur-error` · once only |
| Success / check icon | Feedback | `check-scale` · `--dur-pop` · `--spring-bounce` |
| New content enters screen | Enter | `fade-up` with stagger · `--dur-enter` · `--spring` |
| Genre tiles enter | Enter | `tile-in` with stagger · `--dur-enter` · `--spring` |
| Screen changes | Navigation | Horizontal slide · `--dur-screen` · `--ease-screen` |
| Navigating back | Navigation | Reverse of original motion (slide right) |
| Sheet opens | Navigation | `translateY` up · `--dur-sheet` · `--spring` + backdrop fade |
| Sheet closes | Navigation | `translateY` down · `--dur-sheet` · `--spring` |
| Loading / waiting | System | Shimmer · `var(--dur-shimmer)` · `linear` |
| Progress fills | System | `transform: scaleX()` · `linear` |
| Hero ambient | Ambient | `breathe` or Ken Burns · `linear` · `8s` (§4 constant) |
| Marquee | Ambient | `marquee-fwd/rev` · `linear` · §4 constants |
| TV focus moves | Micro | Glow + `scale(1.05)` · `--dur-fast` |
| Pass unlock | Feedback | `check-scale` + glow settle · `--dur-pop` · `--spring-bounce` |
| Reward celebration | Feedback | `rise` particles + `check-scale` · `--dur-enter` · once only |

---

# 10. Micro Interaction Pattern Table

One row per interaction. Use this as implementation spec. Nothing outside this table needs custom motion.

| Pattern | Intent | Platform | Motion | Duration | Easing | Properties | Reduced motion | ❌ Do not |
|---|---|---|---|---|---|---|---|---|
| **Primary button press** | Confirm tap | M | `scale(.97)` | `--dur-fast` | `--spring` | `transform` | None | Scale below .95 or bounce |
| **Primary button loading** | Signal processing | M/W | Spinner icon rotates | `var(--dur-icon-spin)` linear loop | `linear` | `transform` | Static spinner, no rotation | Pulse the button itself |
| **Primary button success** | Confirm completion | M/W | `check-scale` icon · brief glow | `--dur-pop` | `--spring-bounce` | `transform`, `box-shadow` | Instant state change | Keep animating after state set |
| **Small CTA press** | Confirm tap | M/W | `scale(.96)` | `--dur-fast` | `--spring` | `transform` | None | |
| **Chip select** | Confirm selection | M/W | Border + glow + `scale(1.01)` | `--dur-fast` | `--spring` | `border-color`, `box-shadow`, `transform` | Instant border change | Bounce or keep glowing |
| **Chip deselect** | Confirm removal | M/W | Border fades · glow fades | `--dur-fast` | `--spring` | `border-color`, `box-shadow` | Instant | |
| **Tab switch** | Signal navigation | M/W | Active indicator slides to new tab | `--dur-default` | `--spring` | `transform` (indicator) | Instant switch | Fade entire tab content |
| **Input focus** | Signal entry point | M/W | Border → `--jio` · glow appears | `--dur-fast` | `--spring` | `border-color`, `box-shadow` | Instant | Animate the input label |
| **Input error** | Signal mistake | M/W | `shake` once · border → `--negative` | `--dur-error` | `--ease-error` | `transform`, `border-color` | Instant border change | Loop shake or pulse |
| **OTP digit filled** | Confirm input | M/W | `box-pop` · bg tint | `--dur-pop` | `--spring-bounce` | `transform`, `background` | Instant tint | Continue bouncing |
| **Card press (mobile)** | Confirm tap | M | `scale(.98)` | `--dur-fast` | `--spring` | `transform` | None | Scale below .96 |
| **Card hover (web)** | Signal interactivity | W | Subtle glow + `scale(1.01)` | `--dur-default` | `--spring` | `transform`, `box-shadow` | Glow only, no scale (`transform: none`) | Lift card with margin/top |
| **Card focus (TV)** | Signal focusable | TV | `scale(1.05)` + strong glow | `--dur-fast` | `--spring` | `transform`, `box-shadow` | Glow remains; scale removed (`transform: none`) | Hover-based affordance |
| **Rail scroll (mobile)** | Navigate rail | M | Native horizontal touch scroll + snap | — | — | `scroll-behavior: smooth` | Same | Custom JS scroll, momentum override |
| **Rail scroll (web)** | Navigate rail | W | Wheel / pointer / keyboard-driven | — | — | `scroll-behavior: smooth` | Same | Forcing momentum on mouse wheel |
| **Rail focus (TV)** | Navigate rail | TV | D-pad focus moves active card — no scroll momentum | `--dur-fast` | `--spring` | `transform` on focused card | Instant focus move | Simulating touch momentum on TV |
| **Toast appear** | Notify | M/W | `fade-up` 8px | `--dur-default` | `--spring` | `opacity`, `transform` | Instant appear | Slide from side |
| **Toast dismiss** | Remove | M/W | Fade out | `--dur-default` | `--ease-out` | `opacity` | Instant remove | Slide away |
| **Bottom sheet open** | Navigate | M | `translateY(0)` + backdrop fade | `--dur-sheet` | `--spring` | `transform`, `opacity` | Instant show | Bounce at top |
| **Bottom sheet close** | Navigate | M | `translateY(100%)` + backdrop fade | `--dur-sheet` | `--spring` | `transform`, `opacity` | Instant hide | Fade instead of slide |
| **Game launch** | Signal start | M/W | Brief scale `.98` on card · screen cross-fade | `--dur-fast` + `--dur-screen` | `--spring` + `--ease-screen` | `transform`, `opacity` | Instant screen change | Long dramatic zoom |
| **Pass unlock** | Celebrate | M/W | `check-scale` icon + pulse ring + glow settle | `--dur-pop` | `--spring-bounce` | `transform`, `box-shadow` | Instant icon + static glow | Keep celebrating indefinitely |
| **Reward celebration** | Celebrate | M/W | `rise` particles + `check-scale` + glow | `--dur-enter` | `--spring` | `transform`, `opacity` | Static success state | Loop particles |

---

# 11. Platform Motion Matrix

Same interaction, different behaviour per platform. Input model drives the difference.

| Interaction | Mobile | Web | TV |
|---|---|---|---|
| **Button press** | `scale(.97)` on tap | Hover state + `scale(.97)` on click | Focus glow only — no press scale |
| **Button focus** | On field entry only | `:focus-visible` glow ring | Always visible, drives navigation |
| **Card press** | `scale(.98)` | `scale(.98)` on click | — (D-pad, no click) |
| **Card hover** | None | Subtle glow + `scale(1.01)` | None — hover does not exist |
| **Card focus (TV)** | — | — | `scale(1.05)` + strong glow ring |
| **Screen transition** | Horizontal slide | Horizontal slide or crossfade | Opacity crossfade — no slide |
| **Sheet** | Slides up from bottom | Modal or panel | Forbidden — full-screen patterns only |
| **Rail navigation** | Native touch scroll + snap | Touch scroll or keyboard-driven | D-pad focus moves active card only |
| **Content stagger** | 6-item stagger, `--stagger-step` 60ms | 6-item stagger | Collapsed — all items enter simultaneously |
| **Hover states** | None — touch has no hover | All hover states apply | None — D-pad has no hover |
| **Ambient loops** | Allowed in hero | Allowed in hero | Forbidden |
| **Press haptic** | Supported (see §18) | None | None |

### TV motion rules summary

- No hover states
- No ambient loops
- No press/bounce feedback
- No sheets
- No stagger — unified entrance at `--dur-tv-enter`
- Focus = `scale(1.05)` + glow — this is the entire interaction affordance
- Screen transitions = opacity fade, not slide
- No `backdrop-filter`

---

# 12. Component Motion Map

One component, one contracted motion. Do not invent motion per-screen.

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
| Rail | Native scroll + snap | — |
| Pass card | Press `scale(.98)` | `--dur-fast` · `--spring` |
| Skeleton/shimmer | Shimmer sweep | `var(--dur-shimmer)` · `linear` |
| TV focusable | Glow + `scale(1.05)` | `--dur-fast` · `--spring` |
| Hero | `breathe` or Ken Burns | `8s` · `linear` (§4 constant) |
| Marquee | `marquee-fwd/rev` | §4 constants |

---

# 13. Keyframe Library

All approved keyframes are defined here. For production screens, import this shared motion library. For prototypes, copy only approved keyframes from this section without modification.

Do not add new keyframes directly to a screen file — this section is the only valid source. Propose additions via RFC.

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
@keyframes tile-in {
  from { opacity: 0; transform: translateY(24px) scale(.96); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── Feedback ───────────────────────────────────────── */
@keyframes box-pop {
  /* --dur-pop (280ms) · --spring-bounce · one-shot */
  0%   { transform: scale(1); }
  35%  { transform: scale(1.14); }
  65%  { transform: scale(.97); }
  100% { transform: scale(1); }
}
@keyframes check-scale {
  /* --dur-pop (280ms) · --spring-bounce · one-shot */
  0%   { transform: scale(0); }
  60%  { transform: scale(1.2); }
  100% { transform: scale(1); }
}
@keyframes shake {
  /* --dur-error (380ms) · --ease-error · one-shot only */
  0%,100% { transform: translateX(0); }
  18%     { transform: translateX(-7px); }
  36%     { transform: translateX(7px); }
  54%     { transform: translateX(-5px); }
  72%     { transform: translateX(5px); }
  88%     { transform: translateX(-2px); }
}

/* ── Navigation ─────────────────────────────────────── */
@keyframes sp-enter {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: none; }
}

/* ── System ─────────────────────────────────────────── */
@keyframes shimmer {
  /* Use transform not background-position — compositor only */
  /* Duration: var(--dur-shimmer) · linear · infinite */
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}
@keyframes fact-bar {
  /* Progress: scaleX not width — compositor only */
  /* Apply with: transform-origin: left center */
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
@keyframes pulse-ring {
  0%   { opacity: .7; transform: scale(1); }
  100% { opacity: 0;  transform: scale(1.6); }
}
@keyframes otp-cursor {
  0%,100% { opacity: 1; }
  50%     { opacity: 0; }
}
@keyframes icon-rotate {
  /* Duration: var(--dur-icon-spin) · linear · infinite */
  to { transform: rotate(360deg); }
}

/* ── Ambient ─────────────────────────────────────────── */
@keyframes breathe {
  /* Duration: 8s (§4 constant) · linear · infinite */
  0%,100% { transform: scale(1) translateX(-50%); opacity: .9; }
  50%     { transform: scale(1.12) translateX(-44%); opacity: 1; }
}
@keyframes marquee-fwd {
  /* Duration: 55s (§4 constant) · linear · infinite */
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
@keyframes marquee-rev {
  /* Duration: 65s (§4 constant) · linear · infinite */
  from { transform: translateX(-50%); }
  to   { transform: translateX(0); }
}
@keyframes rise {
  /* Success particles */
  to { transform: translateY(-700px) scaleX(.5); opacity: 0; }
}
@keyframes draw-check {
  to { stroke-dashoffset: 0; }
}
@keyframes logo-pop {
  0%   { transform: scale(.8); opacity: 0; }
  60%  { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
/* ── Legacy keyframes ─────────────────────────────────────────────
   REVIEW BEFORE PRODUCTION. These keyframes exist only for specific
   prototype screens listed in their comments. Do NOT use them as
   general-purpose patterns in new UI. Do NOT reach for these when
   a standard keyframe (fade-up, box-pop, check-scale) exists.
   All require RFC review before promotion to the core library.    */

/* Welcome-back glow pulse — state 7 returning-user hero only
   Duration: --dur-enter · --spring · once
   Status: active, prototype-only */
@keyframes wb-breathe     { 50% { opacity: 1; transform: scale(1.08); } }

/* Pass-found icon concentric ring expand — pulse-ring variant
   Duration: 2s (§4 constant) · --ease-out · infinite
   Status: active, pass-found screen only */
@keyframes wb-ring-expand { to { transform: scale(1.5); opacity: 0; } }

/* Upgrade tab active dot — transform-only glow substitute
   Duration: --dur-default · --ease-out · infinite
   Note: uses opacity not box-shadow to comply with anti-pattern §22
   Status: active, upgrade tab only */
@keyframes nup-dot-pulse  { 50% { opacity: .6; transform: scale(1.3); } }

/* Fade-up enter alias — identical to fade-up; exists for legacy screens
   Use fade-up in all new work. RFC to remove this alias.
   Status: DEPRECATED — use @keyframes fade-up */
@keyframes riseIn         { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
```

**Adding a keyframe:** RFC required. Add here first, then reference from component.

---

# 14. Screen Transitions

Screens slide horizontally respecting navigation direction.

```css
.screen {
  position: absolute; inset: 0;
  transform: translateX(105%);
  transition: transform var(--dur-screen) var(--ease-screen);
  will-change: transform;
}
.screen.active  { transform: translateX(0); }
.screen.behind  { transform: translateX(-28%); }
/* Back navigation: entering screen comes from left (translateX(-105%)),
   exiting screen moves to right (translateX(105%)) — reverse of forward */
```

**TV:** opacity crossfade, no slide.

```css
@media (min-width: 1280px) and (min-height: 720px) {
  .screen {
    transform: none;
    opacity: 0;
    transition: opacity var(--dur-screen) var(--ease-out);
  }
  .screen.active { opacity: 1; }
  .screen.behind  { opacity: 0; pointer-events: none; }
}
```

---

# 15. Content Stagger

Stagger communicates relationship — items that belong together enter together but sequentially.

```css
/* Named stagger using tokens */
.enter-1 { animation: fade-up var(--dur-enter) var(--spring) var(--stagger-start)               both; }
.enter-2 { animation: fade-up var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step))       both; }
.enter-3 { animation: fade-up var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 2)   both; }
.enter-4 { animation: fade-up var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 3)   both; }
.enter-5 { animation: fade-up var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 4)   both; }
.enter-6 { animation: fade-up var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 5)   both; }

/* Grid stagger (genre tiles) */
.tile:nth-child(1) { animation: tile-in var(--dur-enter) var(--spring) var(--stagger-start)                         both; }
.tile:nth-child(2) { animation: tile-in var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step))     both; }
.tile:nth-child(3) { animation: tile-in var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 2) both; }
.tile:nth-child(4) { animation: tile-in var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 3) both; }
.tile:nth-child(5) { animation: tile-in var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 4) both; }
.tile:nth-child(6) { animation: tile-in var(--dur-enter) var(--spring) calc(var(--stagger-start) + var(--stagger-step) * 5) both; }
```

Rules:
- Always `animation-fill-mode: both`.
- Max depth: 6 items. Beyond 6, group at last delay.
- TV: collapse all stagger — unified entrance at `--dur-tv-enter`.

---

# 16. Performance Rules

### Use compositor-friendly properties only

**For movement and loops:** `transform` and `opacity` only.

**For one-shot state changes:** `border-color`, `background`, `box-shadow` allowed when tokenised and not looped.

**Never animate in loops:**
- `width`, `height`, `top`, `left`, `margin`, `padding`
- `box-shadow blur radius` in loops
- `filter` on large images
- `backdrop-filter` on TV

### Progress bar — `scaleX` not `width`

```css
.progress-bar {
  transform-origin: left center;
  animation: fact-bar var(--dur-default) linear both;
}
```

### Shimmer — translated overlay, not `background-position`

```css
.shimmer-wrap { position: relative; overflow: hidden; }
.shimmer-wrap::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,.06) 50%, transparent 100%);
  animation: shimmer var(--dur-shimmer) linear infinite;
}
```

### `will-change`

Use only on elements about to animate. Remove after animation completes. Main legitimate use: `.screen` transition wrapper.

---

# 17. TV Motion Rules

TV requires larger, slightly slower, and more restrained motion.

### Allowed on TV

| Motion | Rule |
|---|---|
| Focus glow | Always — it is an affordance |
| Focus `scale(1.05)` | Only as focus state, always with glow |
| Content entrance | `--dur-tv-enter` (560ms), `fade-up` 32px, no stagger |
| Screen crossfade | Opacity only — no horizontal slide |
| Skeleton | Static — no shimmer sweep |

### Forbidden on TV

- Decorative bounce / `--spring-bounce` in loops
- Parallax / hero breathing
- Marquee
- Press/tap scale feedback
- `backdrop-filter`
- Shimmer animation
- Stagger sequences

---

# 18. Haptic Pairing Rules

Haptics are optional enhancements on mobile. They reinforce motion state, not replace it.

| Trigger | Haptic | Notes |
|---|---|---|
| Primary CTA confirmed | Light impact | On button press-end, not press-start |
| Chip selected | Light selection | Instant — no delay |
| Error shake | Warning haptic | Fires with `shake` animation |
| Payment success | Success haptic | `ic_status_successful` + check-scale |
| Pass unlock | Success haptic | Single impact, not repeated |

### No haptics for

- Hover states
- Scroll (native scroll handles this)
- Loading / shimmer / ambient loops
- Repeated feedback (e.g. do not fire on each stagger item)
- Toast appearance
- Focus ring changes

### Implementation note

Haptics are handled natively (iOS `UIImpactFeedbackGenerator`, Android `HapticFeedbackConstants`). CSS/JS cannot trigger haptics directly in a web context — this is a native layer concern. Document intent here; implement in native shell.

---

# 19. Animation Asset Rules

Three tools, one context each. Do not mix.

### CSS — UI micro interactions

Use for all component-level animation. Button, chip, card, input, tab, sheet, toast, focus ring, skeleton.

- Governed by this document
- Token-driven
- `prefers-reduced-motion` handled via `tokens.css`
- No external files

### Rive — interactive state machines

Use for: controller pairing, reward progress visualisation, pass unlock ceremony, mascot reaction, game-style interaction.

- Only when animation has multiple states that respond to user input
- Must have a fallback static frame for reduced motion
- Do not use Rive on TV unless performance tested at 1080p/60fps
- Export as `.riv` with named state machine inputs

### Lottie — simple exported animation

Use for: success checkmark illustration, payment confirmation, empty state illustration, lightweight celebration, loading illustration.

- Only when animation is linear (no state machine needed)
- Must have a fallback `<img>` or static SVG for reduced motion
- Do not use Lottie on TV unless performance tested
- Export at 1× — no 2× or 3× needed for Lottie

### Decision: CSS vs Rive vs Lottie

```
Is it a UI state change on a contracted component?
  → CSS

Does it have multiple interactive states or respond to user input?
  → Rive

Is it a one-shot illustrative animation (no interaction)?
  → Lottie

Is it on TV?
  → CSS only (unless performance tested)
```

---

# 20. Do Not Animate

These elements must never animate. Motion on critical information creates false uncertainty.

| Element | Reason |
|---|---|
| Legal copy | Users must be able to read without interruption |
| Pricing amounts | Changing numbers must be immediately readable |
| Payment totals | User must not misread amount during animation |
| Subscription terms | Users are making a financial decision |
| Error recovery instructions | User needs to act — do not distract |
| Age restriction warnings | Regulatory — must be stable and readable |
| Network or safety warnings | Critical — must not feel dismissible |
| OTP digits after entry | Value must be stable once confirmed |
| Critical CTAs changing meaning mid-animation | User may tap during transition — unpredictable result |
| Data saving status in rapid repeat | Rapid successive animations for the same state signal = noise |

### Note on price animation

Do not animate `₹99 → ₹199` to "build excitement." Number counting animations feel manipulative and make the actual amount harder to read. Prices appear instantly and remain still.

---

# 21. Reduced Motion Governance

`tokens.css` collapses `--dur-fast`, `--dur-default`, `--dur-enter`, `--dur-tv-enter` to `0ms` under `prefers-reduced-motion`. Components using these tokens are already compliant for micro and enter animations.

`--dur-sheet` and `--dur-screen` are **not** collapsed to 0ms. These navigation durations are handled through explicit reduced-motion overrides:
- `--dur-screen`: screen transitions replace slide with opacity crossfade using `--dur-reduced-fade` (see below)
- `--dur-sheet`: sheets snap open/closed — override to `transition: none` in the reduced motion block:

```css
@media (prefers-reduced-motion: reduce) {
  .bottom-sheet { transition: none; }
}
```

`--dur-reduced-fade` (100ms) and `--dur-reduced-instant` (1ms) are intentionally excluded from the collapse — they exist specifically as reduced-motion fallback values.

**Reduced motion must feel designed — not broken.** The user should experience a calm, immediate interface, not a flickering or jumping one.

### Screen transitions → opacity crossfade

`--dur-default` collapses to 0ms under `prefers-reduced-motion`. Use `--dur-reduced-fade` (100ms) instead — it is intentionally excluded from the collapse, providing a gentle state change that does not flicker.

```css
@media (prefers-reduced-motion: reduce) {
  .screen {
    transform: none;
    transition: opacity var(--dur-reduced-fade) var(--ease-out);
  }
  .screen.active { opacity: 1; }
  .screen.behind  { opacity: 0; pointer-events: none; }
}
```

### Ambient motion → stop completely

```css
@media (prefers-reduced-motion: reduce) {
  .marquee-row, .hero-bg, .aurora, .cathero-orb, .spark {
    animation: none;
  }
}
```

### OTP fill → instant tint, no pop

```css
@media (prefers-reduced-motion: reduce) {
  .otp-box.filled {
    animation: none;
    background: var(--jio-soft);
    border-color: var(--jio);
  }
}
```

### Error shake → static border, no motion

```css
@media (prefers-reduced-motion: reduce) {
  .otp-row.error { animation: none; }
  /* Error message and --negative border must already be visible */
}
```

### Stagger → collapse, fade in only

```css
@media (prefers-reduced-motion: reduce) {
  .enter-1, .enter-2, .enter-3, .enter-4, .enter-5, .enter-6,
  .tile { animation: fade-in var(--dur-reduced-instant) both; animation-delay: 0ms; }
}
```

### Shimmer → static placeholder

```css
@media (prefers-reduced-motion: reduce) {
  .shimmer-wrap::after { animation: none; display: none; }
}
```

### TV focus → glow stays, scale removes

Focus glow is an accessibility affordance and must never be removed. The scale (`1.05`) is a spatial enhancement — it can be removed under reduced motion.

```css
@media (min-width: 1280px) and (min-height: 720px) and (prefers-reduced-motion: reduce) {
  .focusable:focus {
    transform: none;                         /* remove scale — motion */
    box-shadow: 0 0 0 3px var(--jio),
                0 0 24px rgba(0,200,100,.4); /* keep glow — affordance */
  }
}
```

### Focus glow — never suppress

Focus glow is an accessibility affordance on all platforms. Never remove `box-shadow` focus styles under reduced motion, regardless of platform.

### Rive / Lottie → fallback static frame

Both must show a `[data-reduced-motion]` static fallback. The running animation is paused or replaced.

---

# 22. Anti-Patterns

| Pattern | Fix |
|---|---|
| `transition: all` | List explicit properties with duration tokens |
| Raw `120ms` or `.22s` in component CSS | `var(--dur-fast)` |
| Raw `cubic-bezier(…)` in component CSS | `var(--spring)` etc. |
| `animation-fill-mode: none` on enter animations | Always `both` |
| Interactive UI over 500ms | `≤ var(--dur-enter)` |
| Linear easing on UI state transitions | `--spring` for state, `linear` for constant-speed ambient/progress only |
| `--spring-bounce` on hover or scroll | One-shot celebration only |
| Parallax without reduced-motion fallback | `animation: none` under `prefers-reduced-motion` |
| `width` animated for progress | `transform: scaleX()` — compositor only |
| Looped `box-shadow` glow | One-shot state only — never loop |
| `scale > 1.1` in interactive feedback | Max approved: `1.05` TV focus, `1.03` selection, `1.14` inside `box-pop` keyframe only |
| Press bounce on TV | Glow only — D-pad has no press |
| Motion on pricing, legal, or payment totals | Remove — critical information never animates |
| Fade-up when element has a spatial source | Use directional slide matching the element's origin |
| Stagger on unrelated elements | Stagger communicates relationship — do not use decoratively |
| Sustained success animation | One beat then settle — celebrate once |
| Random `fade-up` on everything | Reserve for content that actually enters from below |
| Animating OTP digits after entry | Digits are confirmed — no motion |
| Rive/Lottie without reduced-motion fallback | Static frame required |
| New keyframe added directly to screen file | Add to §13 library via RFC |

---

# 23. Motion QA Checklist

### Token compliance

- [ ] All transition durations use `var(--dur-*)` tokens
- [ ] All easing uses `var(--spring)` / `var(--spring-bounce)` / `var(--ease-screen)` / `var(--ease-out)`
- [ ] No `transition: all`
- [ ] Raw values exist only inside §13 keyframes or §4 Approved Motion Constants

### Spatial and causal

- [ ] Every motion has a named cause (user action or system event)
- [ ] Every motion has a spatial source — element does not appear from nowhere
- [ ] Screen back-navigation reverses the original transition direction
- [ ] Rail scroll position is preserved after interaction
- [ ] No orphan animations running without a trigger

### Settling and restraint

- [ ] Scale limits respected: `.96–.98` press, `1.03` select, `1.05` TV focus
- [ ] `--spring-bounce` used only for one-shot celebration (OTP, success)
- [ ] `shake` plays once — not looped
- [ ] Success animation settles after one beat
- [ ] No bounce or oscillation after state is set

### Performance

- [ ] Only `transform` and `opacity` animated in loops
- [ ] Progress bars use `transform: scaleX()`
- [ ] Shimmer uses `transform: translateX()` overlay
- [ ] No `width`/`height`/`top`/`left` in loops

### Platform

- [ ] TV: no ambient loops, no press bounce, no backdrop-filter, no stagger
- [ ] TV: content entrance uses `--dur-tv-enter`, no stagger
- [ ] TV: default focus = glow + `scale(1.05)`; under `prefers-reduced-motion`, glow remains and scale is removed (`transform: none`)
- [ ] Web: hover states exist; keyboard focus has equivalent affordance
- [ ] Mobile: haptic pairing intent documented (see §18)

### Reduced motion

- [ ] Ambient loops stop completely
- [ ] Screen transitions become opacity fades
- [ ] Stagger collapses to simultaneous fade
- [ ] Shimmer becomes static placeholder
- [ ] Focus glow is NOT removed
- [ ] Error state communicates via colour/icon — not motion alone
- [ ] Rive/Lottie assets have static frame fallback

### Do not animate

- [ ] No motion on pricing, payment totals, or subscription terms
- [ ] No motion on legal copy, age warnings, or safety warnings
- [ ] No motion on OTP digits after entry
- [ ] No motion on critical CTAs mid-state-change

### Motion clarity

- [ ] Motion has a clear cause
- [ ] Motion has a spatial source
- [ ] Motion settles cleanly — no jello, no sustained bounce
- [ ] Motion does not fight user input (no animation longer than user gesture)
- [ ] Motion does not delay task completion
- [ ] Reduced motion feels designed, not broken
- [ ] Critical information is never communicated by motion alone

---

# 24. Pre-Ship Release Gate

> A screen or component ships only if:

- [ ] Motion uses approved tokens and named keyframe recipes — no raw values
- [ ] No `transition: all`
- [ ] Animated properties are `transform` / `opacity` in loops
- [ ] Scale, bounce, and duration limits respected
- [ ] Spatial continuity rules followed — every motion has a source and destination
- [ ] Cause and effect rules met — every motion has an identifiable trigger
- [ ] Reduced motion: ambient stops, slides → fades, shimmer → static, stagger collapses
- [ ] Focus glow present and NOT removed under reduced motion
- [ ] Error/status/success state uses motion + static signal — motion never sole signal
- [ ] TV: no ambient, no press bounce, no backdrop-filter, focus + glow only
- [ ] Pricing, legal, payment amounts, OTP confirmed digits — not animated
- [ ] Rive/Lottie assets have fallback; not used on TV without performance test
- [ ] New keyframe added to §13 library via RFC — not inline in screen
- [ ] `tokens/validate.sh` passes with exit 0
