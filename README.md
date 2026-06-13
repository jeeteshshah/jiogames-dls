# JioGames DLS

Official Design Language System for JioGames — tokens, component contracts, governance docs, icon library, and CI tooling.

Dark-only. Green-first. JioType-only. Token-first. Solid-icon-only. Anti-generic.

---

## Install

```bash
git clone https://github.com/jeeteshshah/jiogames-dls.git ~/.claude/skills/jiogames-dls
```

Claude Code auto-discovers skills in `~/.claude/skills/`. After clone, `/jiogames-dls` is live in any new session.

**Update:**
```bash
git -C ~/.claude/skills/jiogames-dls pull
```

---

## Structure

```
jiogames-dls/
├── SKILL.md                    ← Skill entry point (Claude reads this)
├── CHANGELOG.md                ← What changed and when
├── tokens/
│   ├── tokens.json             ← Single source of truth (W3C format)
│   ├── tokens.css              ← Generated — never hand-edit
│   ├── build.py                ← Generator (run after editing tokens.json)
│   └── validate.sh             ← 14 drift checks, exit 0/1
├── references/
│   ├── tokens-and-components.md
│   ├── colour-governance.md
│   ├── typography.md
│   ├── spacing-and-grid.md
│   ├── radius-governance.md
│   ├── sizing-scale.md
│   ├── motion.md
│   ├── component-contracts.md  ← 12 contracted components
│   ├── icons.md                ← Icon governance
│   ├── appbar.md               ← AppBar component spec (all 3 variants)
│   ├── screens-and-navigation.md
│   ├── logos.md
│   ├── craft-details.md
│   ├── anti-ai-slop.md
│   └── governance.md
├── icons/
│   ├── svg/                    ← 1,646 solid glyph SVGs
│   ├── sprite.svg              ← All icons as <symbol> elements
│   ├── sprites/                ← Per-category sprites
│   └── index.json              ← Icon index
├── logos/
│   ├── JioGames_ServiceLogo_Horizontal_White.svg   ← Default (dark UI)
│   └── JioGames_ServiceLogo_Horizontal_Black.svg   ← Light/print only
├── tools/
│   ├── ci.sh                   ← CI gate (4 steps)
│   ├── audit-icons.py          ← Icon filename + content auditor
│   ├── version.sh              ← Design version history
│   └── visual-test.py          ← Playwright visual regression
├── templates/
│   ├── README.md                   ← How to use templates
│   ├── base-mobile-screen/         ← Mobile 393×852px starter (index.html + styles.css)
│   ├── base-web-screen/            ← Web max-1280px starter (index.html + styles.css)
│   ├── base-tv-screen/             ← TV 1920×1080px starter (index.html + styles.css)
│   └── components/                 ← Component CSS starters (appbar, button, card, rail)
└── examples/
    ├── create-mobile-pass-screen.md
    ├── redesign-game-detail-page.md
    ├── create-tv-rail.md
    └── review-existing-ui.md
```

---

## Token Pipeline

Edit `tokens/tokens.json` → regenerate → validate:

```bash
python3 tokens/build.py                              # regenerate tokens.css
python3 tokens/build.py --check                      # CI mode (exit 1 if stale)
bash tokens/validate.sh .                            # lint for drift violations
bash tokens/validate.sh --strict path/to/generated/  # strict mode — WARNs become ERRs
```

**Never hand-edit `tokens.css`** — fully generated from `tokens.json`.

---

## CI

```bash
bash tools/ci.sh
```

Runs 4 checks in order:
1. Token pipeline — `tokens.css` up to date
2. Icon audit — no high-risk violations (stroke icons, hardcoded fills)
3. Drift validator — no token/style violations in `.html`/`.css`
4. Visual regression — Playwright screenshot diff against goldens

```bash
SKIP_VISUAL=1 bash tools/ci.sh                      # skip visual regression
bash tools/ci.sh path/to/file                        # check specific file (steps 1+2 only)
bash tokens/validate.sh --strict path/to/generated/  # strict mode (WARNs → ERRs + extra checks)
```

**First-time visual regression setup:**
```bash
pip install playwright && playwright install chromium
GOLDEN_UPDATE=1 bash tools/ci.sh    # generate golden screenshots
bash tools/ci.sh                    # subsequent runs diff against goldens
```

---

## Icon Library

1,646 solid glyph SVGs in `icons/svg/`. All normalised to `fill="currentColor"`.

```bash
python3 tools/audit-icons.py              # audit naming + content
python3 tools/audit-icons.py --json       # machine-readable output
python3 tools/audit-icons.py --migration  # migration table only
```

Exits 1 on high-risk violations: stroke icons, hardcoded fills, uppercase filenames.

---

## Platforms

| Platform | Frame | Notes |
|---|---|---|
| Mobile | 393×852px | Touch, scroll-hide AppBar, bottom sheets |
| Web | max-width 1280px | Pointer + keyboard, always-visible AppBar |
| TV | 1920×1080px | D-pad only, no hover, no sheets, sidebar nav |

---

## Pass Tiers

| Tier | Token | Usage |
|---|---|---|
| Mobile Pass | `var(--jio)` | Standard green |
| All Screen Pass | `var(--ultimate)` | Brighter green — never blue |
| Connect & Play Pass | `var(--jio)` | Standard green |

---

## Governance

See `references/governance.md` for RFC process, semver, deprecation policy, release checklist.

All changes documented in `CHANGELOG.md`. No undocumented changes.
