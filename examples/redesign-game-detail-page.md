# Example: Redesign a Game Detail Page

## User prompt

> "Redesign the game detail page — it looks too generic."

---

## Step 1 — Classify platform

| Decision | Value |
|---|---|
| Platform | Mobile (primary) — check if web/TV scope needed |
| Screen type | Full screen — game detail |
| Primary action | Play game |
| Required states | Default, heart liked/unliked, tab switching (overview/details/similar) |
| Input model | Touch |

---

## Step 2 — References to read

- `references/screens-and-navigation.md §7` — Game Detail Page patterns
- `references/anti-ai-slop.md` — what makes generic patterns wrong
- `references/craft-details.md` — cinematic image handling, depth
- `references/typography.md` — heading roles for game title, section heads

---

## Step 3 — Key decisions

| Element | Token / pattern |
|---|---|
| Top bar (transparent) | `background: transparent` → scrolled: `rgba(6,8,15,.88)` + `backdrop-filter: blur(16px)` |
| Hero height | `55vw; min-height: 220px; max-height: 340px` (screens §12 constants) |
| Hero gradient | Approved overlay recipe — colour-governance.md §9 |
| Game title | Weight 900, negative letter-spacing — NOT weight 700 |
| Section heads | Weight 900 with italic `em` in `var(--jio)` |
| Play CTA height | `var(--ctrl-h)` — never `48px` |
| Play CTA bg | `var(--jio)` |
| Play CTA text | `var(--text-inv)` — never `#000` |
| Heart button | Same `var(--ctrl-h)` for alignment |
| Rating stars | `var(--gold-laurel)` — NOT green, NOT `var(--jio)` |
| Genre dash | `::before { background: var(--jio-2) }` — NOT hardcoded `#22C16C` |
| Metadata key | Weight 500 `var(--text2)` — never weight 400 (banned) |
| Metadata value | Weight 700 `var(--text)` |
| Screenshot cards | `border-radius: var(--r7)`, `width: 140px` (screens §12 constant) |

---

## Step 4 — Anti-slop checks (run before presenting)

From `references/anti-ai-slop.md`:
- Hero has cinematic gradient overlay — not just a dark bg
- Game title uses weight 900 with negative tracking
- Section headings have italic `em` accent in `var(--jio)`
- Metadata uses gold stars, not green stars
- No generic card layout with centre-aligned everything
- Genre uses leading `--jio-2` dash, not a dot or pill

---

## Step 5 — Common mistakes

- `font-weight: 700` on game title → must be `900`
- `color: var(--jio)` on rating stars → must be `var(--gold-laurel)`
- `height: 48px` on play button → fix to `var(--ctrl-h)`
- `border-radius: 12px` on screenshot cards → fix to `var(--r7)` (20px)
- `backdrop-filter` on TV → remove if TV in scope

---

## Step 6 — Final response

```
Files: index.html, styles.css, README.md, qa-report.md
Design: Game detail page — cinematic hero, play CTA, tabbed content,
        metadata grid, screenshot rail, similar games.
Components: Button (primary + icon), Rail (screenshots, similar), Card (similar 2:3)
Validation: Exit 0
Assumptions: Tomb Raider used as sample game; artwork as gradient placeholder
Manual checks: Hero image contrast on different artwork; test accordion on real device
```
