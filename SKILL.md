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

## ⛔ HARD STOPS — Read Before Anything Else

These are non-negotiable blockers. If any condition below is true during generation, STOP and fix before continuing. Do not proceed past a violation.

### Before writing a single line of code, confirm:
- [ ] I have read `references/tokens-and-components.md`
- [ ] I have read `references/component-contracts.md`
- [ ] Platform is classified (Mobile / Web / TV)
- [ ] Required states are listed

### While writing CSS, if I am about to write any of these — STOP and replace:

| I was about to write | Replace with |
|---|---|
| `#00A859` or any hex | `var(--jio)` or correct token |
| `#06080F` | `var(--bg)` |
| `#111115` | `var(--card-bg)` |
| `#F4F2EE` or `white` or `#fff` | `var(--text)` |
| `#A8ADBA` | `var(--text2)` |
| `54px` or `36px` | `var(--ctrl-h)` or `var(--ctrl-h-sm)` |
| `100px` or `50%` on buttons | `var(--pill)` |
| `14px` or `20px` border-radius | `var(--r4)` or `var(--r7)` |
| `Inter` or `Outfit` or any font | `JioType` only |
| `font-weight: 400` or `600` or `800` | Use `300`, `500`, `700`, or `900` only |
| `transition: all` | List explicit properties |
| `color: white` or `color: #fff` | `color: var(--text)` |
| `box-shadow` with grey | `var(--jio-glow)` |
| `background: white` or any light surface | `var(--bg)` or dark token |

### After writing code, before responding — STOP and run:
```bash
bash tokens/validate.sh path/to/generated/
```

If exit code is non-zero → fix all ERRORs → re-run → only then respond. If validate.sh does not exist → manually audit every line of styles.css against the table above before responding.

---

# JioGames Design Language System

You are creating, editing, or reviewing UI that follows JioGames' design language. This skill gives you tokens, components, platform rules, and craft standards — plus a mandatory validation loop to catch violations before presenting work.

**Critical rule:** JioType is the sole typeface. Never substitute Inter, Outfit, or any other font. Load from `/Assets/font/JioType-{Light|Medium|Bold|Black}.ttf`.

---

## Companion Skills

This skill works with two companion skills. Use them when relevant to the task — they are optional, not required for every session.

### `frontend-design` — generation quality layer

When generating HTML/CSS, invoke the `frontend-design` skill alongside this one. It provides:
- Production-grade frontend craft (no generic AI patterns)
- Strong visual hierarchy and layout decisions
- Avoidance of flat, formless, or over-padded layouts

**How to compose:** `frontend-design` drives the generation quality. `jiogames-dls` drives the token system, governance, and validation. The result must satisfy both: visually distinctive AND token-compliant.

If `frontend-design` proposes a colour, size, or radius that conflicts with this skill's tokens — **this skill wins**. Replace with the correct token.

### `caveman` — communication mode

`caveman` compresses all design discussion and reviews to terse, token-dense language. This is the recommended mode for JioGames DLS sessions — design systems have exact vocabulary and caveman preserves it without filler.

Activate with `/caveman` at the start of a session. Level `full` is the default. Use `/caveman ultra` for maximum compression during long multi-screen builds.

---

## Single Source of Truth

All token values live in **`tokens/tokens.json`** → generated into **`tokens/tokens.css`** by `tokens/build.py`. Every screen imports `tokens.css` and uses `var(--token)` — **never raw hex/px literals** in component CSS.

```html
<link rel="stylesheet" href="tokens/tokens.css">
```

- Edit values in `tokens.json` → run `python3 tokens/build.py` → one change propagates to all platforms.
- **Never hand-edit `tokens.css`** — it is overwritten on next build.
- CI gate: `bash tools/ci.sh` (token pipeline + drift validator + visual regression).
- If a doc shows a literal value and `tokens.json` disagrees — **`tokens.json` wins**.

---

## Output Contract

When creating JioGames UI, always produce these four files:

| File | Contents |
|---|---|
| `index.html` | Markup — semantic HTML, no inline styles, imports `tokens/tokens.css` |
| `styles.css` | Component styles — `var(--token)` only, no raw hex/px literals |
| `README.md` | Platform classification, components used, design decisions, assumptions |
| `qa-report.md` | Validation output — ERRORs, WARNs, and resolution status |

**Version history** is saved automatically to `./versions/<screen-name>/` in your project (not the skill folder). Use `tools/version.sh` — see Version History section below.

**Generated UI must:**
- Import `tokens/tokens.css` via `<link>`
- Use `var(--token)` exclusively in `styles.css` — no raw hex, no raw px except approved exceptions listed in `references/tokens-and-components.md` (Approved Structural Exceptions)
- Avoid inline `style=""` attributes
- Avoid Tailwind unless explicitly requested
- Use contracted component patterns only — do not invent new variants or re-implement contracted CSS. Screen-level layout CSS is allowed in `styles.css`; component styling must follow component-contracts.md exactly.
- Implement all required states: default, hover (web), focus, active, disabled, loading
- Include responsive behaviour for the classified platform

---

## Mandatory Generation Loop

After creating or editing UI — **before presenting as complete**:

1. Run `bash tokens/validate.sh path/to/generated/` on all generated files
2. Fix every **ERROR** (blocking — do not present with unresolved ERRORs)
3. Review every **WARN** — resolve or document in `qa-report.md` with reason
4. Re-run validation — confirm no ERRORs. WARNs do not fail the script; document each remaining WARN in `qa-report.md` with justification.
5. Write `qa-report.md` with: validation output, resolved ERRORs, remaining WARNs with justification, manual checks needed
6. Present work only after validation passes
7. **Auto-save version** — run `bash <skill-path>/tools/version.sh save <screen-name> "<what changed>"` after validation passes. First save = `v1`, each iteration = `v1.1`, `v1.2` etc.

---

## Version History

Every generated screen is auto-versioned. Versions live in `./versions/` inside **your project** — not the skill folder. Each team member's history stays in their own project.

### Version scheme
```
v1       ← first generation (auto)
v1.1     ← first iteration
v1.2     ← second iteration
v2       ← major new direction (manual bump)
v2.1     ← iteration on v2
```

### Commands
```bash
# Auto-save after generation (Claude runs this automatically)
bash <skill>/tools/version.sh save home-screen "initial hero layout"

# List all saved versions
bash <skill>/tools/version.sh list home-screen

# Restore a version (non-destructive — saves current state first)
bash <skill>/tools/version.sh restore home-screen v1.2

# Compare two versions
bash <skill>/tools/version.sh diff home-screen v1 v1.2

# Queue a major version bump (next save becomes v2)
bash <skill>/tools/version.sh major home-screen

# Show current version info
bash <skill>/tools/version.sh status home-screen
```

### Restore is non-destructive
Restoring `v1` does not delete `v1.1` or `v1.2`. Full history is always preserved. Next save after a restore continues from the latest version number — so rolling back to `v1` and saving creates `v1.3`, not `v1.1` again.

---

## Before Creating UI — Classify Platform

Before writing a single line of code, determine:

| Decision | Options |
|---|---|
| **Platform** | Mobile (393px) / Web (768px+) / TV (1280px+) / Responsive |
| **Screen type** | Full screen / Component / Rail / Modal / Bottom sheet / Flow / State variant |
| **Primary user action** | Play, subscribe, browse, select, log in, search |
| **Required states** | Default, loading, error, empty, selected, disabled, focus |
| **Input model** | Touch (mobile) / Pointer + keyboard (web) / D-pad (TV) |

TV has no hover and no bottom sheets. D-pad focus is the primary affordance. Mobile has no hover. Web has both pointer and keyboard. Do not mix input models.

---

## Task Routing

| User asks to | Do this |
|---|---|
| Create a new screen | Classify platform → read references → build → validate → deliver 4 files |
| Redesign an existing screen | Identify violations → fix against governance docs → validate |
| Build a component | Read component-contracts.md first → compose contracted component |
| Review a design | Run `bash tokens/validate.sh path/to/file` → check each governance QA checklist → write qa-report.md |
| Build TV UI | Read TV sections in motion.md, screens-and-navigation.md, sizing-scale.md before writing code |
| Build a pass or subscription screen | Read Pass & Upgrade Screens in `references/screens-and-navigation.md` + Pass Card contract in `references/component-contracts.md` |
| Build a rail | Read Rail System in `references/spacing-and-grid.md` + Rail contract in `references/component-contracts.md` before writing code |
| Add or change a token | Edit tokens.json → run build.py → update CHANGELOG.md |
| Add or choose icons | Read `references/icons.md` → use only `icons/svg/` or `icons/sprite.svg` → no Lucide / third-party icons |
| Audit icon library | Run `python3 tools/audit-icons.py` → fix high-risk (exit 1) issues before shipping |

---

## How This Skill Is Organised

| Reference File | When to Read |
|---|---|
| `references/tokens-and-components.md` | Building any JioGames UI — token quick-ref, component CSS patterns, exception registry |
| `references/colour-governance.md` | Colour decisions — full token index, decision tree, surface ladder, state mapping, gradient recipes, forbidden combos |
| `references/typography.md` | Type roles, `.text-*` classes, platform scale, screen examples, accessibility |
| `references/spacing-and-grid.md` | 8px scale, layout aliases, vertical rhythm, rail rules, grid system |
| `references/radius-governance.md` | Component→radius canonical map, inner-radius nesting rule |
| `references/sizing-scale.md` | Control height tokens, touch target rules, TV compact guard, governance process |
| `references/motion.md` | Easing + duration tokens, keyframe library, component motion map, performance rules, TV rules, reduced motion |
| `references/icons.md` | Icon governance — official solid glyph library, naming, sizing, wrappers, accessibility, manifest, third-party icon ban |
| `references/component-contracts.md` | 12 component contracts — tokens, radius, sizing, states, platform, a11y, owner |
| `references/screens-and-navigation.md` | App shell, navigation, screen patterns, pass screens, cinematic techniques, approved layout constants |
| `references/governance.md` | Ownership, RFC process, semver, CHANGELOG, deprecation policy, release checklist |
| `references/anti-ai-slop.md` | Quality check — patterns that break the JioGames look |
| `references/craft-details.md` | Polish — focus states, TV nav, image handling, glow system |
| `references/logos.md` | Logo governance — approved variants (White/Black), when to use each, clear space, minimum size, forbidden treatments |
| `logos/` | Approved JioGames logo SVG files — use only these, never recreate or override colours |
| `CHANGELOG.md` | Version history |
| `examples/create-mobile-pass-screen.md` | Worked example: mobile subscription screen — token decisions, common mistakes, expected output |
| `examples/redesign-game-detail-page.md` | Worked example: game detail page — anti-slop checks, cinematic patterns, element tokens |
| `examples/create-tv-rail.md` | Worked example: TV home + rail — D-pad rules, what to omit, focus patterns |
| `examples/review-existing-ui.md` | Worked example: UI review — full QA checklist by governance layer, qa-report.md template |

---

## The JioGames Look — Quick Summary

> **Use token names in generated code. Literal values below are explanatory only.**
> Write `var(--bg)` not `#06080F`. Write `var(--ctrl-h)` not `54px`. Write `var(--text-inv)` not `#000`.

### Tokens for the most common decisions

| Decision | Token to use | Do NOT use |
|---|---|---|
| Page background | `var(--bg)` | `#06080F`, `#000`, `black` |
| Card surface | `var(--card-bg)` | `#111115` |
| Primary CTA bg | `var(--jio)` | `#00A859` |
| CTA text | `var(--text-inv)` | `#000`, `black` |
| Primary text | `var(--text)` | `#F4F2EE`, `white`, `#fff` |
| Body text | `var(--text2)` | `#A8ADBA` |
| Caption / meta | `var(--text2)` | `var(--text3)` (except decorative) — `--text3` is ~3.5:1 contrast, not safe for readable small text |
| Active glow | `var(--jio-glow)` | `rgba(0,200,100,.35)` |
| Primary button height | `var(--ctrl-h)` | `54px`, `72px` |
| Small CTA height | `var(--ctrl-h-sm)` | `36px` |
| Button radius | `var(--pill)` | `100px`, `50%` |
| Card radius | `var(--r4)` or `var(--r7)` | `14px`, `20px` |
| Sheet radius | `var(--r9) var(--r9) 0 0` | `24px`, `28px` |
| Spring easing | `var(--spring)` | `cubic-bezier(.22,1,.36,1)` |
| Fast transition | `var(--dur-fast)` | `120ms`, `.12s` |

### Brand rules (always)

- **Dark only.** No light mode. No white surfaces.
- **One primary accent: green.** `var(--jio)` for CTAs, borders, checks, eyebrows, active states.
- **Pass tiers: Mobile Pass · All Screen Pass · Connect & Play Pass.** All Screen Pass uses `var(--ultimate)`. Never blue on any pass tier.
- **Weight 900 for all headings.** 300/500/700/900 only — 400/600/800 banned.
- **Negative letter-spacing** on text ≥16px.
- **JioType only.** No Inter, Outfit, Roboto.
- **Glow over shadow.** `var(--jio-glow)` on active/selected. No soft grey drop-shadows.

### Platform frames

| Platform | Frame | Input | Notes |
|---|---|---|---|
| Mobile | 393×852px | Touch | `var(--frame-mobile-w)` × `var(--frame-mobile-h)`, screens `position:absolute;inset:0` |
| Web | max-width 1280px | Pointer + keyboard | `var(--container-web)`, gutter `var(--gutter)` |
| TV | 1920×1080px | D-pad | `var(--tv-safe)` 80px, no hover, no sheets |

---

## Ambiguity Handling

If details are missing, make the safest JioGames-compliant assumption and document it in `README.md`. Do not stop generation for:

- Missing copy → use clearly marked placeholder text in `var(--text2)`
- Missing game artwork → use dark gradient placeholder (see Asset Fallback Rules below)
- Missing price → `₹--` placeholder in `var(--text)` weight 900
- Missing game names → `[Game Title]` in weight 900

**Platform ambiguity:** default to Responsive with Mobile-first structure unless the request clearly implies TV or Web. Document the assumption in `README.md`. Do not stop generation — the wrong platform assumption is fixable; no output is not.

Stop and ask only when:
- TV vs Mobile/Web is explicitly unclear and the work would be unusable if wrong (TV has no sheets, no hover, D-pad only)
- A new component is needed that has no contract and cannot be approximated by composition

---

## NON-NEGOTIABLE ADHERENCE RULE

This skill is a design contract, not inspiration.

When generating, editing, or reviewing JioGames UI:

1. Follow the existing DLS exactly.
2. Do not invent new colours, spacing, radius, typography, motion, icon styles, component variants, or layout patterns.
3. Do not silently "improve," "modernise," "reinterpret," or "simplify" the system.
4. Do not use generic AI defaults when the DLS already defines a rule.
5. Do not replace a missing rule with a personal design decision.
6. Do not create one-off exceptions.

**If the requested output cannot be created using the current DLS, STOP and use this exact format:**

> The current JioGames DLS does not define this clearly.
> I need your approval before changing or extending the system.
>
> Missing / conflicting area:
>
> * [state the gap]
>
> Recommended options:
>
> 1. Use the closest existing DLS rule: [option]
> 2. Add a new governed rule: [option]
> 3. Treat this as a one-off exception: [option]
>
> Which direction should I follow?

Until the user answers, do not generate the final UI.

---

## Asset Fallback Rules

When artwork is not provided:

- Use dark gradient placeholders — approved gradient recipes in `references/colour-governance.md`
- Preserve required aspect ratios: 16:9 (landscape cards), 2:3 (portrait cards), 1:1 (square cards)
- Do not use external image URLs (Unsplash, Picsum, etc.)
- Do not invent official game logos or trademarks
- Mark placeholders: `data-asset-placeholder="true"` on the container
- Always apply approved hero overlay gradient before placing text on image areas
- Use `var(--card-bg)` as fallback base with subtle gradient:

```css
.art-placeholder {
  background: linear-gradient(135deg, var(--surface-2) 0%, var(--card-bg) 100%);
}
```

---

## Do / Don't

### DO

1. Use `var(--bg)` for background — never `#000` or pure black
2. Use weight 900 for all headings, titles, prices, card names
3. Use negative letter-spacing on all text ≥16px
4. Use `rgba(255,255,255,…)` borders via `var(--border)` — never solid white
5. Use `var(--jio-glow)` box-shadow on active inputs/cards — not grey shadows
6. Use `var(--pill)` for primary buttons and action chips
7. Use uppercase + `letter-spacing: 1.5px` for eyebrow labels, always `color: var(--jio)`
8. Use `var(--spring)` as default easing for enter animations
9. Add `scroll-snap-type: x mandatory` to all horizontal rails
10. For TV: always add visible focus ring with `var(--jio-glow)` + `scale(1.05)`
11. Run `bash tokens/validate.sh path/to/generated/` before presenting any generated UI

### DON'T

1. Don't use light mode — no white backgrounds anywhere
2. Don't use Inter, Outfit, or any font other than JioType
3. Don't use blue/indigo/purple — JioGames is green end-to-end, including all Pass tiers
4. Don't use heavy drop shadows — use `var(--jio-glow)` instead
5. Don't use `border-radius: 50%` on cards — only avatars and circular icon wrappers
6. Don't use `color: #fff` or `color: white` for body copy — use `var(--text)`
7. Don't use `transition: all` — always list explicit properties with duration tokens
8. Don't skip `overscroll-behavior: contain` on scrollable sheets/modals
9. Don't use `var(--text3)` for captions, terms, timers, nav labels, or helper text — use `var(--text2)`. Reason: `--text3` is ~3.5:1 contrast, below WCAG AA for small text. Reserve for decorative/non-essential metadata only.
10. Don't use raw `54px`, `36px`, `100px` etc. — use `var(--ctrl-h)`, `var(--ctrl-h-sm)`, `var(--pill)`
11. Don't use Unsplash or external image URLs as placeholders

---

## Workflow — Building JioGames UI

1. **Classify platform and screen type** (see Before Creating UI above)
2. **Route the task** (see Task Routing above)
3. **Read this summary** for overall feel and token quick-ref
4. **Read `references/tokens-and-components.md`** for component CSS patterns
5. **Read `references/screens-and-navigation.md`** if building a full screen, navigation, or cinematic hero
6. **Read `references/spacing-and-grid.md`** for layout — spacing scale, grid, gutters, rails
7. **Read `references/typography.md`** for type roles and `.text-*` classes
8. **Read `references/motion.md`** if adding animation or screen transitions
9. **Read `references/component-contracts.md`** — compose contracted components, never re-implement
10. **Build** — `index.html` + `styles.css` using tokens and contracted components. Apply `frontend-design` skill quality principles during generation (strong hierarchy, no generic padding-heavy layouts, purposeful depth). Override any `frontend-design` output that uses raw values with the correct token.
11. **Run mandatory generation loop** — validate.sh → fix ERRORs → review WARNs → qa-report.md
12. **Polish pass** — `references/craft-details.md` for glow, TV focus, image handling
13. **Anti-slop check** — `references/anti-ai-slop.md` checklist

## Workflow — Reviewing JioGames UI

1. Run `bash tokens/validate.sh path/to/file` — fix ERRORs, document WARNs
2. Check against Do/Don't list above
3. Check `--text3` usage — only decorative, never for readable content
4. Check all token names are used — no raw hex/px
5. Check component contracts are followed — no re-implemented components
6. Write `qa-report.md` with findings

---

## Final Self-Review — Before Responding

**STOP. Do not respond until each item below is confirmed true:**

1. No raw hex (`#xxxxxx`), raw px for controlled dimensions (`54px`, `36px`, etc.), or banned font weights (`400`, `600`, `800`) in `styles.css`
2. No light surfaces — all backgrounds use dark tokens (`var(--bg)`, `var(--card-bg)`, etc.)
3. Primary CTA uses `var(--jio)` with `color: var(--text-inv)` — not `#000`
4. All text uses approved `.text-*` classes or explicit token-matched roles — no hardcoded `font-size` in component CSS
5. Platform behaviour matches classified input model — TV has no hover, no sheets; mobile has no hover
6. `qa-report.md` exists, reflects final validation state, and lists any remaining WARNs with justification
7. `README.md` documents platform, components used, and all assumptions made

---

## Final Response Format

When work is complete, respond with:

1. **Files created or changed** — names and one-line description of each
2. **What the design does** — screen purpose, user flow, primary action
3. **Components used** — list contracted components composed
4. **Validation result** — exit code, ERRORs resolved, WARNs with status
5. **Assumptions made** — anything inferred from ambiguous input
6. **Manual checks remaining** — things validate.sh cannot catch (visual QA, content review, device testing)
