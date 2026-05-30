# Changelog

All notable changes to the JioGames DLS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Motion tokens: `--ease-out`, `--dur-instant` (90ms), `--dur-pop` (280ms), `--dur-error` (380ms), `--dur-screen` (420ms)
- `motion.md` upgraded to full governance system: decision tree, component motion map, 6 motion categories, performance rules, TV rules, reduced-motion governance, keyframe library, QA checklist, release gate
- `tokens.css` reduced-motion block expanded to collapse all new duration tokens; ambient loop guidance added

### Changed
- `motion.md`: TV scale rule corrected — `scale(1.05)` allowed only as focus state paired with glow; decorative bounce/parallax/loops forbidden on TV
- `motion.md`: anti-pattern "Duration > 500ms" refined — interactive ≤500ms, TV enter ≤600ms, ambient loops exempt; linear easing clarified as allowed for constant-speed marquee/progress/shimmer only
- `motion.md`: `fact-bar` keyframe updated to `transform: scaleX()` from `width` (compositor-only)
- `tokens.css` reduced-motion block: now collapses `--dur-instant`, `--dur-pop`, `--dur-error`, `--dur-screen` in addition to existing tokens

### Added
- Visual regression: `tests/showcase.html` (11 components), `tools/visual-test.py` (screenshot + pixel diff), `tools/update-goldens.sh`, `.gitignore`
- GitHub Actions workflow updated to install Playwright and run visual regression on push/PR
- `tools/ci.sh` updated to 3-step gate (token pipeline + drift + visual); gracefully skips visual when Playwright not installed (`SKIP_VISUAL=1` override)
- `tools/requirements.txt` (playwright, Pillow)
- Governance: `references/governance.md` (ownership model, RFC process, semver, CHANGELOG format, deprecation policy, release checklist), `CHANGELOG.md`
- Control sizing scale: `--ctrl-h`, `--ctrl-h-sm`, `--ctrl-h-ghost`, `--touch-min`, `--otp-box-w`, `--otp-box-h`, `--card-wide-w`, `--card-sq`, `--genre-tile-h`, `--tab-bar-h`, `--app-bar-h` tokens; TV overrides for `--ctrl-h`/`--touch-min`/`--card-wide-w`
- Radius governance: `references/radius-governance.md`; component→token canonical map; inner-radius rule; Tab Bar contract added to component-contracts.md
- Colour governance: `references/colour-governance.md`; `--mint: #1CBABA` token added
- `validate.sh` check #10: raw control-size literals in height/width flagged as ERR
- `references/sizing-scale.md`: visual height vs touch target separation (§5), TV compact size guard (§6), new-size governance process (§7)

---

## [1.0.0] — 2026-05-29

Initial release of the JioGames Design Language System.

### Added

**Token pipeline**
- `tokens/tokens.json` — single source of truth for all design tokens (colour, spacing, radius, layout, font, motion, control sizes)
- `tokens/build.py` — generator; emits `tokens.css` from `tokens.json`; `--check` mode for CI
- `tokens/tokens.css` — generated CSS custom properties; never hand-edited
- `$platforms` block in `tokens.json` encoding responsive overrides (Web 768px / TV 1280px+) so platform values live in source, not hand-authored CSS

**Token categories**
- Brand green scale (`--jio`, `--jio-2`, `--jio-3`, `--jio-bright`, `--jio-glow`, `--jio-soft`)
- Pass/premium (`--ultimate`, `--ultimate-glow`, `--popular-gold`)
- Secondary brand accent: `--mint: #1CBABA`
- Full background, surface ladder, glass, text, border, overlay token sets
- 8px spacing scale (`--space-0` through `--space-12`) + semantic layout aliases (`--gutter`, `--section-gap`, `--card-gap`, etc.) with Web and TV platform overrides
- Radius scale (`--r1` through `--r9`, `--pill`)
- Control sizing scale (`--ctrl-h`, `--ctrl-h-sm`, `--ctrl-h-ghost`, `--touch-min`, `--otp-box-w`, `--otp-box-h`, `--card-wide-w`, `--card-sq`, `--genre-tile-h`, `--tab-bar-h`, `--app-bar-h`) with TV overrides for `--ctrl-h`, `--touch-min`, `--card-wide-w`
- Motion tokens (`--spring`, `--spring-bounce`, `--ease-screen`, `--dur-*`)
- Stack utility classes (`.page-stack`, `.hero-stack`, `.component-stack`, `.content-stack`, `.tight-stack`)

**Validator and CI**
- `tokens/validate.sh` — 10 drift checks; exit 0 = clean, exit 1 = blocking violations
- `tools/ci.sh` — full CI gate (token pipeline + drift validator)
- `tools/pre-commit` — git pre-commit hook (staged files only)
- `tools/install-hooks.sh` — one-time hook installer
- `.github/workflows/dls-ci.yml` — GitHub Actions workflow (push + PR to main)

**Reference documentation**
- `references/tokens-and-components.md` — Component Patterns & Token Index; all CSS component patterns using tokens
- `references/typography.md` — 14-section typography governance (type scale, roles, platform scaling, a11y, release gate)
- `references/spacing-and-grid.md` — 14-section spacing governance (8px scale, aliases, stack utilities, rail rules, screen checklist)
- `references/colour-governance.md` — 15-section colour governance (brand palette, decision tree, surface ladder, state mapping, gradient recipes, forbidden combos)
- `references/radius-governance.md` — 8-section radius governance (scale, component→token canonical map, inner-radius rule, forbidden patterns)
- `references/sizing-scale.md` — 9-section control sizing governance (token reference, platform-aware vs fixed, visual height vs touch target, TV compact guard, new-size governance)
- `references/component-contracts.md` — 11 component contracts (Button, Card, Text Input, OTP, Chip, Bottom Sheet, Rail, Tab Bar, Pass Card, Genre Tile, Toast); 7-part contract anatomy (Anatomy, Tokens, Radius, Sizing, States, Platform, A11y)
- `references/governance.md` — Governance process (ownership model, change classification, RFC process, semver, CHANGELOG format, deprecation policy, release checklist)

**Skill entry point**
- `SKILL.md` — Claude Code skill definition; triggers, quick summary, do/don't, workflow

### Deprecated

- `--cyan` (`#26D6C9`) — legacy decorative category token; prefer `--mint` for brand-approved secondary accent usage. Will be removed in v2.0.0.

---

## Version history

| Version | Date | Summary |
|---|---|---|
| 1.0.0 | 2026-05-29 | Initial release |
