# JioGames DLS — Changelog

All notable changes to the design language system. Most recent first.

---

## [Unreleased] — 2026-06-14 (patch 4)

### Added
- **`references/_core-rules.md`** — New authoritative source for all universal non-negotiables: dark-only, JioType-only, token-first (replacement table), green-first, no generic AI UI, solid-glyph icons only, no silent deviation (with exact ask format), heading/type rules, glow-over-shadow, platform input models. Read first for every task.
- **`references/_task-router.md`** — New file mapping every task type to the minimum files to read. Never read all reference files — only `_core-rules.md` + what the task requires.
- **SKILL.md: TOKEN BUDGET RULE** — Explicit rule: read `_core-rules.md` + task-specific files only; start from templates; search `icons/index.json` not all SVGs; read examples only if stuck.

### Changed
- **SKILL.md: 538 → 159 lines** — Stripped all content now owned by `_core-rules.md` (brand rules, do/don't list, JioGames look summary, ambiguity handling, asset fallback rules, detailed workflows, version history details). Kept: hard stops, session contract, token budget rule, generation decision gate, output contract, validation, task routing quick-ref, reference index, companion skills.
- **`references/` (all 14 files)** — Added `> Inherits _core-rules.md` note after heading. Global rule boilerplate removed from 5 files: `tokens-and-components.md` (1 line), `colour-governance.md` (2 table rows), `typography.md` (1 line), `icons.md` (4 lines — third-party policy section), `motion.md` (1 line from Core Principles).
- **README.md** — Added `_core-rules.md` and `_task-router.md` to structure listing.

## [Unreleased] — 2026-06-14 (patch 3)

### Added
- **SKILL.md: SKILL LOCK / SESSION PERSISTENCE RULE** — Once skill activates in a session, it locks ON for all remaining turns. Cannot deactivate by omission.
- **SKILL.md: Activation Behaviour** — Defines how skill triggers, what to read on first activation, and what NOT to ask.
- **SKILL.md: Generation Decision Gate** — 5-step mental decision tree to run before writing any UI/code. Gates on contracted component, token, icon, motion token, and logo.
- **SKILL.md: Strict Generation Mode** — Documents `--strict` flag behavior: WARNs→ERRs, plus checks for missing imports, qa-report.md, README.md.
- **SKILL.md: Post-Activation Default** — Explicit rule that every design/UI/icon/logo/colour/motion/copy response follows the DLS after activation, even with no explicit skill mention.
- **SKILL.md: Task Routing expanded** — 15-row table covering: generate UI, use component, icon, colour, spacing, motion, logo, task outside DLS, review, redesign, TV, pass screen, rail, token change, icon audit.
- **SKILL.md: Final Response Rule** — Mandatory 4-file output contract (index.html, styles.css, README.md, qa-report.md) with explicit "never omit qa-report.md" rule.
- **`tokens/validate.sh`: `--strict` mode** — Upgrades all WARNs to ERRs. Adds 3 strict-only checks: missing tokens.css import, missing qa-report.md, missing README.md in screen output directories.
- **`templates/`** — Starter templates: base-mobile-screen, base-web-screen, base-tv-screen (index.html + styles.css each), plus components/ (appbar.css, button.css, card.css, rail.css). All token-only CSS, no raw values.

### Changed
- **SKILL.md: NON-NEGOTIABLE ADHERENCE RULE** — Moved from bottom of file to top (immediately after HARD STOPS) so it is encountered first in every session.
- **`examples/create-mobile-pass-screen.md`** — Removed raw hex values (`#0e1a14`, `#0a1f14`, `#ffcf5c`) from Key decisions table; replaced with references to colour-governance.md §9. Fixed perk check icon from `stroke: var(--jio)` to `fill: currentColor` (DLS is solid-glyph, no stroke). Pass naming: "Ultimate" → "All Screen".
- **`examples/redesign-game-detail-page.md`** — Removed raw `rgba(6,8,15,.88)` from scrolled AppBar entry; replaced with reference to appbar.md scrolled bg spec.

## [Unreleased] — 2026-06-14 (patch 2)

### Added
- **SKILL.md: NON-NEGOTIABLE ADHERENCE RULE** — Hard design contract block. Defines exact STOP format when DLS has a gap; no UI generated until user approves direction.
- **SKILL.md: `references/icons.md`** added to "How This Skill Is Organised" table.
- **SKILL.md: Icon task routing** — Add/choose icons and audit icon library entries added to Task Routing table.
- **`tools/audit-icons.py`: SVG content checks** — New `STROKE_ICON` and `HARDCODED_FILL` categories check SVG file contents, not just filenames.
- **`tools/ci.sh`: Icon audit step** — Step 1b runs `audit-icons.py` and fails CI on high-risk violations.
- **`tools/ci.sh`: Golden screenshot guard** — CI fails if `tests/goldens/` is missing or empty outside `GOLDEN_UPDATE=1` mode.
- **`tools/ci.sh`: Playwright binary detection** — Separate checks for Python package missing vs. browser binary not installed.
- **`README.md`** — Expanded from 1 line to full documentation: install, structure, token pipeline, CI, icon library, platforms, pass tiers, governance.

### Changed
- **SKILL.md: Companion skills** — Changed from mandatory ("every generation session") to optional ("when relevant to the task").
- **SKILL.md: "11 component contracts"** — Corrected to **12** (AppBar was added).
- **SKILL.md: Pass naming** — "Ultimate Pass" → "Mobile Pass · All Screen Pass · Connect & Play Pass" throughout.
- **`references/appbar.md`: AppBar class names** — `appbar-detail` / `appbar-inner` → `appbar--detail` / `appbar--inner` (BEM double-dash, matches component-contracts.md canonical).
- **`tools/audit-icons.py`: Near-duplicate detection** — Reduced noise: only flags when one name is a strict prefix of another with exactly 1 extra token (previously flagged too many false positives).
- **`tools/audit-icons.py`: High-risk exit code** — Now exits 1 when `STROKE_ICON`, `HARDCODED_FILL`, `CASE`, or `TRAILING_SPACE` issues found (previously always exited 0).
- **`tools/audit-icons.py`: Manifest fallback** — Falls back to `icons/index.json` when `icons/icons-manifest.json` doesn't exist.
- **`tools/ci.sh`: Step count** — Updated from `[2/3]`/`[3/3]` to `[2/4]`/`[4/4]`.

## [Unreleased] — 2026-06-14 (patch 1)

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
