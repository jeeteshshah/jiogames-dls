# Installing the JioGames DLS Skill

## Prerequisites

- Claude Code installed and running
- `caveman` plugin installed (provides `/caveman` command)
- `frontend-design` plugin installed (provides generation quality layer)

---

## Install

### Option A — Project skill (recommended for the JioGames repo)

Place the `jiogames-dls/` folder inside your project's `.claude/skills/` directory:

```
your-project/
  .claude/
    skills/
      jiogames-dls/          ← this folder
        SKILL.md
        tokens/
        references/
        examples/
        tools/
        tests/
```

Claude Code auto-discovers skills in `.claude/skills/`. The skill activates when you describe JioGames UI work or say "JioGames style."

### Option B — Global skill (available in every project)

Copy the folder to your global Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -r ~/Desktop/Claude/jiogames-dls ~/.claude/skills/jiogames-dls
```

---

## Verify install

Open a new Claude Code session and type:

```
/jiogames-dls
```

Or describe a task that triggers it:

```
Create a JioGames mobile home screen
```

Claude should load the skill and begin with platform classification.

---

## Required companion skills

Install both before using the DLS skill:

### caveman

```bash
# If not already installed
/install caveman
```

Or via the plugin registry if your Claude Code supports it.

### frontend-design

```bash
# If not already installed
/install frontend-design
```

---

## Starting a session

Recommended session start for any JioGames UI work:

```
/caveman
/jiogames-dls
Create a [screen name] for [Mobile/Web/TV]
```

Or combined:

```
/caveman full
Build a JioGames game detail page for mobile
```

The skill will:
1. Activate caveman mode (terse, token-dense communication)
2. Load the DLS references
3. Classify platform before writing code
4. Generate UI with `frontend-design` quality principles
5. Run validation automatically
6. Deliver `index.html`, `styles.css`, `README.md`, `qa-report.md`

---

## Token pipeline setup (first time)

After cloning or copying the skill folder:

```bash
cd path/to/jiogames-dls

# Verify tokens.css is current
python3 tokens/build.py --check

# If stale, regenerate
python3 tokens/build.py

# Install git pre-commit hook (optional but recommended)
bash tools/install-hooks.sh
```

---

## Running validation manually

```bash
# Validate a specific file
bash tokens/validate.sh path/to/screen.html

# Validate a directory
bash tokens/validate.sh path/to/screens/

# Full CI gate (tokens + drift + visual regression)
bash tools/ci.sh
```

---

## Visual regression (optional)

Requires Playwright:

```bash
pip install playwright pillow
playwright install chromium

# Capture goldens (first time)
bash tools/update-goldens.sh

# Run visual diff in CI
python3 tools/visual-test.py
```

---

## File structure

```
jiogames-dls/
  SKILL.md                    ← skill entry point
  INSTALL.md                  ← this file
  CHANGELOG.md                ← version history
  .gitignore
  .github/
    workflows/
      dls-ci.yml              ← GitHub Actions CI
  tokens/
    tokens.json               ← source of truth (edit here)
    tokens.css                ← generated (never edit)
    build.py                  ← generator
    validate.sh               ← drift validator (10 checks)
  references/
    tokens-and-components.md
    colour-governance.md
    typography.md
    spacing-and-grid.md
    radius-governance.md
    sizing-scale.md
    motion.md
    component-contracts.md
    screens-and-navigation.md
    governance.md
    anti-ai-slop.md
    craft-details.md
    icons.md
  examples/
    create-mobile-pass-screen.md
    redesign-game-detail-page.md
    create-tv-rail.md
    review-existing-ui.md
  tools/
    ci.sh                     ← full CI gate
    pre-commit                ← git hook
    install-hooks.sh          ← hook installer
    update-goldens.sh         ← visual regression goldens
    visual-test.py            ← screenshot + pixel diff
    requirements.txt          ← playwright, pillow
  tests/
    showcase.html             ← component showcase for visual regression
    golden/                   ← golden screenshots (committed)
    diff/                     ← diff images (gitignored)
```
