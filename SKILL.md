---
name: jiogames-dls
description: >
  Create, edit, review, and validate JioGames UI designs across Mobile, Web, and TV using the
  official JioGames Design Language System. Use whenever the user mentions JioGames UI, JioGames
  design, JioGames prototype, JioGames screens, JioGames components, or asks to build/review any
  screen that should look like JioGames. Also trigger when the user references JioGames brand
  colors (green #00A859), JioType font, dark gaming UI, JioGames Pass (Mobile or Ultimate),
  the home rail layout, the login/OTP flow, genre/platform preferences, or any JioGames
  sub-surface (game detail, pass upsell, preferences). This skill covers design tokens,
  component patterns, mobile/web/TV breakpoints, typography, motion, and craft polish.
  Use even if the user just says "make it look like JioGames" or "JioGames style."
---

## ⛔ HARD STOPS

**Before any code:** read `references/_core-rules.md` + task-specific files from `references/_task-router.md`. Classify platform. List required states.

**While writing CSS — if about to write any of these, STOP:**

| Write | Replace with |
|---|---|
| Any raw hex | `var(--jio)` or correct token |
| `Inter`, `Outfit`, any non-JioType font | `JioType` only |
| `font-weight: 400/600/800` | `300`, `500`, `700`, or `900` |
| `transition: all` | Explicit properties only |
| `box-shadow` with grey | `var(--jio-glow)` |
| `background: white` / any light surface | `var(--bg)` or dark token |
| `54px` / `36px` in height/width | `var(--ctrl-h)` / `var(--ctrl-h-sm)` |

**After code:** `bash tokens/validate.sh path/to/generated/` → fix all ERRs → then respond.

---

## 🔒 SESSION CONTRACT

**Activates on any JioGames task. Stays locked ON for the full session.**

Triggers: `/jiogames-dls`, "use JioGames DLS", or any JioGames UI/icon/logo/colour/motion/copy task.

Rules after activation:
- Every turn follows this skill — even without explicit skill mention
- This skill overrides `frontend-design` for all token/colour/spacing/radius decisions
- Deactivate only by explicit "stop using JioGames DLS"
- No silent deviation — if DLS does not define something, STOP and ask (format: `references/_core-rules.md` → "No silent deviation")

---

## ⚡ TOKEN BUDGET RULE

Read minimum. Read deep only when needed.

1. **Always first:** `references/_core-rules.md`
2. **Task-specific only:** see `references/_task-router.md` for exact file list
3. **Generate from templates:** start from `templates/` — never reinvent structure
4. **Icons:** search `icons/index.json` — do not load all SVGs
5. **Examples:** read only if stuck — do not read preemptively

---

## Generation Decision Gate

Run mentally before any UI or code:

```
1. Component contracted in component-contracts.md?
   → YES: Use contracted spec. Never re-implement from scratch.

2. Token exists for this value?
   → YES: Use it. No raw value.
   → NO: Check governance docs. Still no token? → STOP, ask (_core-rules.md format).

3. Icon in icons/svg/?
   → YES: fill:currentColor, no stroke.
   → NO: Use closest. Document gap in qa-report.md.

4. Motion token for this animation?
   → YES: Use it.
   → NO: → STOP, ask (_core-rules.md format).

5. Logo needed?
   → Use logos/ SVGs only. Never recreate or recolour.
```

---

## Output Contract

Every generation delivers 4 files:

| File | Requirement |
|---|---|
| `index.html` | `<link rel="stylesheet" href="tokens/tokens.css">` first. No inline styles. |
| `styles.css` | `var(--token)` only. No raw hex or controlled-dimension px. |
| `README.md` | Platform declared. Components used. All assumptions documented. |
| `qa-report.md` | `validate.sh` exit code. ERRs resolved. WARNs listed with status + reason. |

Component-only tasks may omit `index.html`. Never omit `qa-report.md`.

---

## Validation

```bash
bash tokens/validate.sh path/to/generated/      # standard — fix all ERRs before responding
bash tokens/validate.sh --strict path/to/file   # before shipping externally (WARNs → ERRs)
```

After validation passes: `bash tools/version.sh save <screen-name> "<message>"`

---

## Task Routing

Full file list per task: `references/_task-router.md`

Quick reference:
- **Mobile/web UI:** `_core-rules.md` → `tokens-and-components.md` → `component-contracts.md` → `templates/`
- **TV UI:** add `sizing-scale.md`, `motion.md` (TV sections), `screens-and-navigation.md`
- **Colour:** `colour-governance.md`
- **Icon:** `icons.md` + search `icons/index.json`
- **Motion:** `motion.md`
- **Logo:** `logos.md`
- **AppBar:** `appbar.md`
- **Review UI:** run `validate.sh` + write `qa-report.md`

---

## Reference Index

| File | When to read |
|---|---|
| `references/_core-rules.md` | **Always first** |
| `references/_task-router.md` | To find the exact file list for any task |
| `references/tokens-and-components.md` | Building any UI — token quick-ref, component CSS patterns |
| `references/colour-governance.md` | Colour decisions |
| `references/typography.md` | Type roles, `.text-*` classes |
| `references/spacing-and-grid.md` | 8px scale, gutters, rails |
| `references/radius-governance.md` | Component→radius canonical map |
| `references/sizing-scale.md` | Control heights, TV overrides |
| `references/motion.md` | Easing + duration tokens, TV motion |
| `references/icons.md` | Icon wrappers, naming, accessibility |
| `references/component-contracts.md` | 12 contracted components |
| `references/screens-and-navigation.md` | App shell, pass screens, cinematic layout |
| `references/appbar.md` | AppBar spec — all 3 variants |
| `references/logos.md` | Logo variants, clear space, minimum size |
| `references/craft-details.md` | Polish — focus states, TV nav, image handling |
| `references/anti-ai-slop.md` | Patterns that break the JioGames look |
| `references/governance.md` | RFC, semver, deprecation, release checklist |
| `templates/` | Starter files — always use for new screens |
| `icons/index.json` | Searchable icon index — use instead of browsing SVGs |
| `CHANGELOG.md` | Version history |

---

## Companion Skills

- **`frontend-design`** — generation quality (hierarchy, depth, craft). This skill overrides it for all token/colour/spacing/radius decisions.
- **`caveman`** — compresses design discussion to terse token-dense language. Activate with `/caveman` at session start.
