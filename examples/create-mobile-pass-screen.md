# Example: Create a Mobile JioGames Subscription Screen

## User prompt

> "Create a JioGames pass subscription screen for mobile."

---

## Step 1 — Classify platform

| Decision | Value |
|---|---|
| Platform | Mobile (393px) |
| Screen type | Full screen — subscription/pass upsell |
| Primary action | Subscribe / upgrade |
| Required states | Default, loading (CTA), disabled |
| Input model | Touch |

---

## Step 2 — References to read

- `references/screens-and-navigation.md §8` — Pass & Upgrade Screens patterns
- `references/component-contracts.md` — Pass Card, Button contracts
- `references/tokens-and-components.md §7` — Pass Upsell Card pattern
- `references/colour-governance.md §3` — `--ultimate` token for Ultimate tier

---

## Step 3 — Key decisions

| Element | Token / pattern |
|---|---|
| Screen bg | `var(--bg)` |
| Mobile pass card bg | `#0e1a14` (approved gradient — colour-governance.md §9) |
| Ultimate pass card bg | `linear-gradient(135deg, #0a1f14 …)` (approved recipe) |
| Pass name | `.text-card-title` weight 900 `var(--text)` |
| Price | `.text-price` weight 900 `var(--text)` — NOT `var(--text2)` |
| CTA bg | `var(--jio)` (Mobile) / `var(--ultimate)` (Ultimate) |
| CTA text | `var(--text-inv)` — never raw `#000` |
| CTA height | `var(--ctrl-h)` — never `54px` |
| CTA radius | `var(--pill)` — never `100px` |
| Ultimate accent | `var(--ultimate)` — never blue |
| Perk check icon | `stroke: var(--jio)` |
| "Most Popular" badge | `background: linear-gradient(90deg, var(--popular-gold), #ffcf5c)` (approved recipe) |
| Perks gap | `var(--space-1)` — never `8px` |
| Card radius | `var(--r7)` — never `20px` |
| Card padding | `var(--card-padding)` |

---

## Step 4 — What Claude should produce

```
index.html       — markup with Mobile pass screen
styles.css       — token-safe CSS only
README.md        — platform, components, assumptions
qa-report.md     — validate.sh output
```

---

## Step 5 — Common mistakes to avoid

- `color: #000` on CTA → fix to `var(--text-inv)`
- `height: 54px` → fix to `var(--ctrl-h)`
- `gap: 8px` → fix to `var(--space-1)`
- `font-weight: 600` on badge → fix to `700`
- `--text3` on perks text → fix to `var(--text2)`
- Ultimate Pass card with blue accent → fix to `var(--ultimate)` green

---

## Step 6 — Final response

```
Files: index.html, styles.css, README.md, qa-report.md
Design: Mobile subscription screen with Mobile Pass and Ultimate Pass cards,
        plan comparison, primary CTA, "Most Popular" badge on Ultimate.
Components: Pass Card (×2), Button (primary), Eyebrow label
Validation: Exit 0 — 0 ERRORs, 2 WARNs (approved gradient recipes, documented in qa-report)
Assumptions: Prices set to ₹99/mo and ₹199/mo — update with actual values
Manual checks: Test on real device for touch target sizes; verify JioType loads
```
