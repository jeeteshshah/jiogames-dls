# Example: Review Existing JioGames UI

## User prompt

> "Can you review this screen and tell me what's wrong?"

---

## Step 1 — Run automated validation first

```bash
bash tokens/validate.sh path/to/screen.html
```

Note every ERROR and WARN. ERRORs are blocking — they must be fixed. WARNs need review.

---

## Step 2 — Check against each governance layer

Work through these in order. Stop and document each finding.

### Colour

From `references/colour-governance.md §10` (Forbidden Combinations):
- [ ] `background: #000` or `black` → fix to `var(--bg)`
- [ ] Any blue/indigo/purple in brand or UI role → fix to green
- [ ] Ultimate Pass rendered in blue → must be `var(--ultimate)` green
- [ ] `color: #fff` or `white` for text → fix to `var(--text)`
- [ ] `--text3` on readable content (terms, timers, nav labels, helper text) → fix to `--text2`
- [ ] White or light product surface → fix to dark surface token

### Typography

From `references/typography.md`:
- [ ] Headings not weight 900 → must be 900
- [ ] `font-weight: 400`, `600`, or `800` → banned; fix to 300/500/700/900
- [ ] Non-JioType font → fix to JioType
- [ ] `.text-caption` using `--text3` → fix to `--text2` unless purely decorative
- [ ] `color: #000` on CTA text → fix to `var(--text-inv)`

### Spacing

From `references/spacing-and-grid.md`:
- [ ] `gap: 20px`, `padding: 20px`, `margin: 20px` → `20px` is banned, use `var(--space-2)` (16) or `var(--space-3)` (24)
- [ ] Raw spacing not on 8px scale → snap to nearest `var(--space-*)`
- [ ] Child `margin-bottom` for vertical rhythm → use parent `gap` with stack utility

### Radius

From `references/radius-governance.md §2`:
- [ ] Buttons not `var(--pill)` → fix
- [ ] Cards not `var(--r4)` (landscape) or `var(--r7)` (pass/editorial) → fix
- [ ] Sheets not `var(--r9) var(--r9) 0 0` → fix
- [ ] `border-radius: 50%` on non-avatar → fix

### Sizing

From `references/sizing-scale.md §8`:
- [ ] `height: 54px`, `72px`, `36px`, `40px` raw in CSS → fix to `var(--ctrl-h)`, etc.
- [ ] `width: 272px` or `400px` on landscape card → fix to `var(--card-wide-w)`
- [ ] Interactive element smaller than `var(--touch-min)` → add transparent padding

### Motion

From `references/motion.md §12`:
- [ ] `transition: all` → list explicit properties
- [ ] Raw `120ms`, `.22s`, etc. in component CSS → fix to `var(--dur-*)`
- [ ] Raw `cubic-bezier(…)` → fix to `var(--spring)`, etc.
- [ ] `width` animated in a loop → fix to `transform: scaleX()`
- [ ] No `prefers-reduced-motion` fallback on ambient animation → add it

### TV (if TV in scope)

- [ ] `:hover` styles present without `:focus` equivalent → TV has no hover
- [ ] `backdrop-filter` used → remove for TV
- [ ] Ambient loops present → remove for TV
- [ ] `--ctrl-h-sm` or `--ctrl-h-ghost` used → mobile/web only

---

## Step 3 — Write qa-report.md

Structure:

```md
# QA Report — [Screen Name] — [Date]

## Validation result
Exit code: [0 / 1]
ERRORs: [count]
WARNs: [count]

## ERRORs (must fix before ship)
| Finding | Location | Fix |
|---|---|---|
| … | … | … |

## WARNs (reviewed)
| Finding | Location | Resolution |
|---|---|---|
| … | … | Resolved / Accepted (reason) |

## Manual checks remaining
- …
```

---

## Step 4 — Final response

```
Validation: Exit [0/1] — [N] ERRORs, [N] WARNs
Critical issues: [list blocking ERRORs]
Recommended fixes: [ordered by severity]
qa-report.md: written with full findings
```
