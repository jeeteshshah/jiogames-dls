# JioGames DLS — Changelog

All notable changes to the design language system. Most recent first.

---

## [Unreleased] — 2026-06-14

### Added
- **SKILL.md hard stops** — Non-negotiable pre-code checklist, CSS violation replacement table, and post-code `validate.sh` gate. Final Self-Review is now a hard block, not a suggestion. (`36dcda8`)
- **`references/appbar.md`** — Dedicated AppBar component spec: all 3 variants, scroll behaviour, icon table, PASS badge, `.has-notification` pattern. (`336c480`)
- **AppBar contract — 3 variants fully specced** — `appbar` (home), `appbar--detail` (game detail, dark-glass back button), `appbar--inner` (settings/notifications, solid bg + title). (`ed73520`)
- **`.icon-btn--dark` modifier** — For back button overlaying hero images. Dark glass (`rgba(0,0,0,.45)` + `blur(8px)`), distinct from standard light-glass `.icon-btn`. (`ed73520`)
- **`--status-bar-h: 44px` token** — iOS safe-area height. Distinct from `--touch-min`. Added to `tokens.json`, `build.py`, `tokens.css`. (`1fef049`)
- **`validate.sh` HTML audit checks (11–14)** — Check 11: `stroke-width` in CSS (ERR). Check 12: `fill:none` on SVG (WARN). Check 13: `--s-N` aliases (WARN). Check 14: `outline:none` without glow (ERR). (`7e80e11`)
- **AppBar component contract** — Scroll-hide behaviour, platform rules, icon governance note. (`bc39bdd`)

### Changed
- **AppBar icon button jitter guard** — Corrected from 6px to **8px** delta filter. (`ed73520`)
- **Shared `.icon-btn` spec contracted** — Identical across all AppBar variants. Variant-specific classes (e.g. `gd-icon-btn`) are now drift violations. (`0502cdf`)
- **AppBar forbidden elements** — Avatar and heart/wishlist explicitly banned from all AppBar variants. (`7c7da68`)
- **Component owners assigned** — All 11 component contracts now owned by Jeetesh Shah (previously `[unassigned]`). (`27af44d`)

---

## v1.1.0 — 2026-06-01

### Added
- **Jio icon library** — 1,646 SVGs normalised to `fill="currentColor"`. Category sprites. Export scripts (`tools/audit-icons.py`). (`7c705cc`)
- **Logo governance** (`references/logos.md`) — White/Black variants, clear space, min sizes, forbidden treatments. Approved logo size variables: `--logo-width-xs/default/lg/tv`. (`af9353c`)
- **Design version history** (`tools/version.sh`) — `save`, `list`, `restore`, `diff`, `major`, `status` commands. Non-destructive, saves to `./versions/<screen>/`. (`3f4d0ef`)
- **Motion system — Apple-level upgrade** (`references/motion.md`) — 24 sections: Motion Personality, Spatial Continuity, Cause & Effect, Micro Interaction Pattern Table (21 rows), Platform Motion Matrix, Haptic Pairing, reduced-motion governance. (`cae9a28`)
- **New motion tokens** — `--ease-error`, `--dur-icon-spin`, `--dur-reduced-fade`, `--dur-reduced-instant`, `--dur-tv-enter`, `--dur-shimmer`, `--stagger-start`, `--stagger-step`. (`cae9a28`)
- **Icon namespace tokens** — `--icon-size-xs/sm/md/base/lg/xl`, `--icon-color-*`, `--icon-wrapper-sm/md`. (`af9353c`)

### Changed
- **Governance gaps resolved** — `--text3` rule unified (decorative/inactive only), `.text-caption-strong` / `.text-body-strong` formalised as CSS classes, raw values in examples marked explanatory-only, `--ultimate-glow` for Ultimate Pass surfaces. (`3bfab8c`)
- **Icon system rewrite** — Solid glyph only (`fill:currentColor`, no stroke). In-house Jio library only, no Lucide. (`af9353c`)

---

## v1.0.0 — 2026-06-01

Initial release. Token pipeline, component contracts, governance docs, CI gate.

### Included
- `tokens/tokens.json` — W3C format token source. Color, space, layout, radius, font, motion, control, icon tokens.
- `tokens/build.py` — Generator with `--check` mode for CI.
- `tokens/tokens.css` — Generated CSS custom properties with Web/TV `@media` overrides.
- `tokens/validate.sh` — 10 drift checks (exit 0/1).
- `tools/ci.sh` — CI gate: tokens + drift + visual regression.
- `references/` — Governance docs: colour, typography, motion, icons, logos, component contracts, craft details, screens & navigation, tokens & components.
- `examples/` — 4 worked examples: mobile pass screen, game detail page, TV rail, existing UI review.
- `SKILL.md` — Skill entry point with output contract, mandatory generation loop, platform classification, task routing.
