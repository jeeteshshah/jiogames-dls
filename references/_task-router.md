# JioGames DLS — Task Router

**Read only `_core-rules.md` + the files listed here. Never read all reference files.**

`_core-rules.md` is always first. Then read only what the task requires.

---

## Generate mobile UI

1. `references/_core-rules.md`
2. `references/tokens-and-components.md`
3. `references/component-contracts.md`
4. `references/spacing-and-grid.md`
5. Start from `templates/base-mobile-screen/`
6. Validate: `bash tokens/validate.sh path/to/generated/`

If needed: `references/typography.md` · `references/colour-governance.md` · `references/radius-governance.md`

---

## Generate web UI

Same as mobile, start from `templates/base-web-screen/` instead.

---

## Generate TV UI

1. `references/_core-rules.md`
2. `references/tokens-and-components.md`
3. `references/component-contracts.md`
4. `references/sizing-scale.md` — TV overrides, D-pad touch targets
5. `references/motion.md` — TV Motion section only
6. `references/screens-and-navigation.md` — TV shell, sidebar nav
7. Start from `templates/base-tv-screen/`

---

## Build a specific component

| Component | Read |
|---|---|
| AppBar (any variant) | `references/appbar.md` |
| Pass card / subscription | Pass Card in `references/component-contracts.md` + Pass sections in `references/screens-and-navigation.md` |
| Rail | Rail System in `references/spacing-and-grid.md` + Rail contract in `references/component-contracts.md` |
| Button, Card, TabBar, Toast | `references/component-contracts.md` |
| Any contracted component | `references/component-contracts.md` first — never re-implement |

---

## Choose or apply a colour

1. `references/_core-rules.md`
2. `references/colour-governance.md`

Use token only. No raw hex. No token for the needed colour → STOP, use No-Silent-Deviation format.

---

## Choose or find an icon

1. `references/_core-rules.md`
2. `references/icons.md` (naming, wrapper patterns, accessibility)
3. Search `icons/index.json` for the icon name

Do NOT load all SVGs. `icons/index.json` is the searchable index.
No token → use closest available, document gap in `qa-report.md`.

---

## Set spacing or layout

1. `references/_core-rules.md`
2. `references/spacing-and-grid.md`

8px-scale tokens. No raw px for grid/spacing values.

---

## Add motion or animation

1. `references/_core-rules.md`
2. `references/motion.md`

Use easing and duration tokens. No raw `cubic-bezier()` or raw `ms`.

---

## Use a logo

1. `references/_core-rules.md`
2. `references/logos.md`

Use `logos/` SVGs only. Never recreate, recolour, or scale below minimum size.

---

## Review or audit existing UI

1. Run `bash tokens/validate.sh path/to/file`
2. Check against `references/_core-rules.md`
3. Before shipping externally: `bash tokens/validate.sh --strict path/to/file`
4. Write `qa-report.md`: ERRs fixed, WARNs resolved/accepted with reason

---

## Add or change a token

1. Edit `tokens/tokens.json`
2. Run `python3 tokens/build.py`
3. Update `CHANGELOG.md`

---

## Task outside DLS scope

STOP. Use No-Silent-Deviation format from `references/_core-rules.md`. Get approval. No personal design decision.

---

## Audit icon library

Run `python3 tools/audit-icons.py`. Fix high-risk (exit 1) violations before shipping.
