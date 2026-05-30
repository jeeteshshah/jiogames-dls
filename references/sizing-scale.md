# JioGames Sizing Scale

> Control heights and component dimensions are tokens, not magic numbers. Use `var(--ctrl-h)` not `54px`. The TV platform gets its sizes automatically — no manual overrides needed.

Component heights, card dimensions, and minimum touch targets all live in `tokens/tokens.json` under `"control"` and are generated into `tokens/tokens.css`. This document governs **which token to use, when, and why**.

**Structure**

1. Token Reference
2. Platform-Aware Tokens
3. Fixed-Size Tokens
4. Decision Tree
5. Visual Height vs Touch/Focus Target
6. TV Compact Size Guard
7. When Not to Create a New Size
8. Forbidden Patterns
9. Sizing QA Checklist

---

# 1. Token Reference

| Token | Mobile | TV | Platform-aware | Use |
|---|---:|---:|:---:|---|
| `--ctrl-h` | 54px | 72px | ✓ | Primary control height — button, main CTA |
| `--ctrl-h-sm` | 36px | **n/a** | — | Small CTA — mobile/web only |
| `--ctrl-h-ghost` | 40px | **n/a** | — | Ghost/skip button — mobile/web only |
| `--touch-min` | 44px | 60px | ✓ | Minimum tap/focus target dimension |
| `--otp-box-w` | 50px | — | — | OTP digit box width |
| `--otp-box-h` | 64px | — | — | OTP digit box height |
| `--card-wide-w` | 272px | 400px | ✓ | Landscape game card width |
| `--card-sq` | 96px | 96px | — | Square game card (width = height) |
| `--genre-tile-h` | 156px | 156px | — | Genre selection tile height |
| `--tab-bar-h` | 64px | — | — | Floating pill tab bar height |
| `--app-bar-h` | 64px | — | — | Sticky site/app header height |

Sheet handle nub (`40×4px`, `border-radius: 2px`) is a hard-coded optical exception — see component-contracts.md Bottom Sheet.

---

# 2. Platform-Aware Tokens

Three tokens resolve automatically via the TV `@media` block in `tokens.css`. **No component-level media query needed.**

| Token | Mobile/Web | TV |
|---|---:|---:|
| `--ctrl-h` | 54px | 72px |
| `--touch-min` | 44px | 60px |
| `--card-wide-w` | 272px | 400px |

Rule: never write `@media { .btn-primary { height: 72px } }` in component CSS. If a component uses `var(--ctrl-h)`, it is already correct on every platform. Writing the TV value in component CSS is a violation — it bypasses the token and breaks future-proofing.

---

# 3. Fixed-Size Tokens

These tokens have the same value on all platforms:

| Token | Why fixed |
|---|---|
| `--ctrl-h-sm` (36px) | Small CTA — mobile/web only, not used on TV |
| `--ctrl-h-ghost` (40px) | Ghost button — mobile/web only, not used on TV |
| `--otp-box-w` / `--otp-box-h` | OTP flow is mobile/web only |
| `--card-sq` (96px) | Square card unchanged across platforms |
| `--genre-tile-h` (156px) | Genre tile unchanged across platforms |
| `--tab-bar-h` (64px) | Tab bar is mobile/web only |
| `--app-bar-h` (64px) | App bar is web only |

Even fixed tokens must use `var(--token)`. If a value ever needs a platform override, it can be added to `$platforms` in `tokens.json` without touching any component CSS.

---

# 4. Decision Tree

```
What height or width are you setting?
│
├── A primary button / main CTA
│     → height: var(--ctrl-h)   [auto 72px on TV]
│
├── A small pill CTA
│     → height: var(--ctrl-h-sm)   [mobile/web only — see §6]
│
├── A ghost or skip button
│     → height: var(--ctrl-h-ghost)   [mobile/web only — see §6]
│
├── An OTP digit box
│     → width: var(--otp-box-w); height: var(--otp-box-h)
│
├── A landscape game card (16:9)
│     → width: var(--card-wide-w)   [auto 400px on TV]
│
├── A square game card (1:1)
│     → width: var(--card-sq); height: var(--card-sq)
│
├── A genre selection tile
│     → height: var(--genre-tile-h)
│
├── The floating tab bar
│     → height: var(--tab-bar-h)
│
├── The sticky site/app header
│     → height: var(--app-bar-h)
│
├── A minimum tap or focus target
│     → min-width/min-height: var(--touch-min)   [44px mobile, 60px TV]
│     → This is the target area, not the visual height — see §5
│
└── None of the above
      → Check spacing-and-grid.md §2 first (8px scale).
        If still not covered → governance request. See §7.
```

---

# 5. Visual Height vs Touch/Focus Target

Visual height and touch/focus target are **independent concerns**. A compact control can be visually small and still meet accessibility requirements.

### Visual height

The rendered height of the element — controlled by `--ctrl-h`, `--ctrl-h-sm`, etc.

### Touch/focus target

The tappable or focusable area — must always meet `--touch-min`:
- Mobile: 44px minimum
- TV: 60px minimum
- Web (pointer): 32px minimum (not tokenized — pointer-driven targets are inherently precise)

### How they coexist

A visually compact element achieves `--touch-min` through **transparent padding** — the visual element stays small, but the interactive area is padded to meet the minimum.

```css
/* Small CTA — visually 36px, touch target 44px */
.btn-cta-sm {
  height: var(--ctrl-h-sm);          /* 36px visual */
  padding-block: calc((var(--touch-min) - var(--ctrl-h-sm)) / 2);
  /* Adds 4px transparent padding top + bottom → 44px total target */
}

/* Icon-only button — visually 24px icon, touch target 44px */
.btn-icon {
  min-width: var(--touch-min);       /* 44px target width */
  min-height: var(--touch-min);      /* 44px target height */
  display: flex; align-items: center; justify-content: center;
  /* Icon inside is 20–24px; surrounding space is transparent hit area */
}
```

### Rules

- Never shrink the touch target to match visual height.
- Never inflate the visual height to match the touch target.
- Ghost buttons (40px) on mobile: add 2px transparent padding-block → 44px target.
- Icon buttons: always `min-width/min-height: var(--touch-min)` regardless of icon size.
- TV focus targets: every focusable element must meet `var(--touch-min)` (60px) in both dimensions.

---

# 6. TV Compact Size Guard

`--ctrl-h-sm` (36px) and `--ctrl-h-ghost` (40px) are both below TV's `--touch-min` of 60px. They are **mobile/web-only controls** and must not be used on TV.

### Why they have no TV token

These controls do not appear in TV flows. TV uses full-screen navigation, large focus rings, and primary CTAs (`--ctrl-h: 72px`). There is no "small CTA" or "skip" pattern in the TV interaction model.

Adding a TV override (e.g. `ctrl-h-sm: 60px`) would create false confidence — the component would technically meet touch-min but the pattern itself is wrong for TV.

### What to do on TV instead

| Mobile/Web pattern | TV equivalent |
|---|---|
| Small CTA (36px) | Primary CTA (`--ctrl-h`: 72px) or omit |
| Ghost/skip button (40px) | Back navigation via D-pad; or omit |

### Enforcement

- Component contracts for Button mark TV behaviour explicitly for sm/ghost variants.
- If a screen includes `--ctrl-h-sm` or `--ctrl-h-ghost` in a TV context, treat it as a contract violation.
- The validator (check #10) will flag `height: 36px` and `height: 40px` as raw literals — if they are present in TV-targeted CSS it is doubly wrong.

---

# 7. When Not to Create a New Size

Before adding any new component height or dimension, work through this checklist:

**Step 1 — Can an existing token solve it?**

| Need | Try |
|---|---|
| A button-like control | `--ctrl-h`, `--ctrl-h-sm`, `--ctrl-h-ghost` |
| A tile or card height | `--genre-tile-h`, `--card-sq` — or if it's card width: `--card-wide-w` |
| A navigation surface | `--tab-bar-h`, `--app-bar-h` |
| A minimum target size | `--touch-min` |
| A vertical dimension that matches the spacing scale | `--space-*` (8px scale) |

If an existing token fits, use it. Do not create a new token for the same semantic purpose.

**Step 2 — Is this a one-screen special case?**

If the dimension appears only on one screen and has no reuse potential, it is a one-off layout value, not a design system token. Document it as a screen-level constant in a comment — do not add it to `tokens.json`.

```css
/* Screen-level constant — not a DLS token */
.promo-banner { height: 180px; }
```

**Step 3 — Is this genuinely reusable across 2+ components or surfaces?**

If yes, it belongs in the token system. Follow the governance process:

1. Confirm no existing token covers the need
2. Propose the name, value, mobile/web/TV values, and which components will use it
3. Requires approval from 2 DLS owners
4. Add to `tokens.json "control"` section — never hardcode in CSS first
5. Update `build.py` sections list with the new token
6. Regenerate `tokens.css` via `python3 tokens/build.py`
7. Update this document's §1 Token Reference
8. Update relevant component contracts

**Hard rule:** a raw dimension in component CSS that is not in the 8px spacing scale and not in `tokens.css` is always a violation. Fix it one of two ways: map to an existing token, or add a new token via governance.

---

# 8. Forbidden Patterns

| Pattern | Reason | Fix |
|---|---|---|
| `height: 54px` in component CSS | Raw value — bypasses TV override | `height: var(--ctrl-h)` |
| `height: 72px` anywhere | TV-only raw value — token handles it | Remove; use `var(--ctrl-h)` |
| `height: 36px` or `height: 40px` | Raw compact control size | `var(--ctrl-h-sm)` / `var(--ctrl-h-ghost)` |
| `min-height: 44px` or `min-height: 60px` | Raw touch target | `min-height: var(--touch-min)` |
| `width: 272px` or `width: 400px` on `.wide-card` | Raw card width | `width: var(--card-wide-w)` |
| `width: 96px; height: 96px` on square card | Raw card size | `var(--card-sq)` both |
| `height: 156px` on genre tile | Raw tile height | `var(--genre-tile-h)` |
| `--ctrl-h-sm` or `--ctrl-h-ghost` in TV context | Below TV `--touch-min` (60px) | Use `--ctrl-h` or omit |
| TV `@media` overriding a height already owned by a token | Duplicates token logic; will drift | Remove override, token handles it |
| New height added directly to component CSS without a token | Ungoverned magic number | Governance process (§7) |
| Visual height inflated to match touch target | Wrong approach | Use transparent padding instead |

---

# 9. Sizing QA Checklist

| Check | Required |
|---|---|
| All button heights use `var(--ctrl-h)`, `var(--ctrl-h-sm)`, or `var(--ctrl-h-ghost)` | Yes |
| No raw `54`, `36`, `40`, `72`, `44`, `50`, `64`, `96`, `156`, `272`, `400` px in height/width | Yes |
| `.wide-card` uses `var(--card-wide-w)` | Yes |
| `.sq-card` uses `var(--card-sq)` | Yes |
| `.genre-tile` uses `var(--genre-tile-h)` | Yes |
| Visually compact elements have transparent padding to reach `var(--touch-min)` | Yes |
| Icon-only buttons have `min-width/min-height: var(--touch-min)` | Yes |
| TV context: no `--ctrl-h-sm` or `--ctrl-h-ghost` | If TV in scope |
| TV context: no component-level `@media` overriding heights already in token pipeline | If TV in scope |
| New dimension added to `tokens.json` via governance before use | If new size |
| `tokens/validate.sh` passes with exit 0 (check #10 = no raw control literals) | Yes |
