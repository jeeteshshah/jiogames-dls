#!/usr/bin/env bash
# ============================================================
# JioGames DLS — CI gate
# Runs all checks that block a merge:
#   1. tokens.css must be up to date with tokens.json
#   2. All .html/.css files must pass the drift validator
#   3. Visual regression against golden screenshots
#      (skipped when SKIP_VISUAL=1 or Playwright not installed)
#
# Usage:
#   ./tools/ci.sh                    # check everything
#   ./tools/ci.sh path/to/file.html  # check specific files (steps 1+2 only)
#   SKIP_VISUAL=1 ./tools/ci.sh      # skip visual check
#
# Exit: 0 = clean, 1 = violations found
# ============================================================
set -uo pipefail

RED=$'\033[31m'; GRN=$'\033[32m'; BLD=$'\033[1m'; OFF=$'\033[0m'

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0
SKIP_VISUAL="${SKIP_VISUAL:-0}"

# ── Step 1: token pipeline check ────────────────────────────
echo ""
echo "${BLD}[1/3] Token pipeline${OFF}"
if python3 "$ROOT/tokens/build.py" --check; then
  echo "${GRN}✓ tokens.css is current${OFF}"
else
  echo "${RED}✗ tokens.css is stale — run: python3 tokens/build.py${OFF}"
  fail=1
fi

# ── Step 1b: icon audit ─────────────────────────────────────
echo ""
echo "${BLD}[1b/4] Icon audit${OFF}"
if python3 "$ROOT/tools/audit-icons.py" > /dev/null 2>&1; then
  echo "${GRN}✓ No high-risk icon violations${OFF}"
else
  echo "${RED}✗ Icon audit found high-risk violations — run: python3 tools/audit-icons.py${OFF}"
  fail=1
fi

# ── Step 2: drift validator ──────────────────────────────────
echo ""
echo "${BLD}[2/4] Drift validator${OFF}"

if [ $# -gt 0 ]; then
  targets=("$@")
else
  targets=("$ROOT")
fi

if bash "$ROOT/tokens/validate.sh" "${targets[@]}"; then
  echo "${GRN}✓ No violations${OFF}"
else
  fail=1
fi

# ── Step 3: visual regression ────────────────────────────────
echo ""
echo "${BLD}[4/4] Visual regression${OFF}"

GOLDENS="$ROOT/tests/goldens"

if [ "$SKIP_VISUAL" = "1" ]; then
  echo "  skipped (SKIP_VISUAL=1)"
elif ! python3 -c "import playwright" 2>/dev/null; then
  echo "  skipped (playwright Python package missing — run: pip install playwright && playwright install chromium)"
elif ! python3 - 2>/dev/null <<'PYEOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    b.close()
PYEOF
  echo "  skipped (Playwright chromium binary not installed — run: playwright install chromium)"
elif [ $# -gt 0 ]; then
  echo "  skipped (file-targeted run — visual test runs on full repo only)"
elif [ ! -d "$GOLDENS" ] || [ -z "$(ls -A "$GOLDENS" 2>/dev/null)" ]; then
  echo "${RED}✗ No golden screenshots in tests/goldens/ — run: GOLDEN_UPDATE=1 ./tools/ci.sh to generate${OFF}"
  fail=1
else
  if python3 "$ROOT/tools/visual-test.py"; then
    echo "${GRN}✓ Visual regression passed${OFF}"
  else
    echo "${RED}✗ Visual regression failed — see tests/diff/ and tests/report.json${OFF}"
    fail=1
  fi
fi

# ── Result ───────────────────────────────────────────────────
echo ""
echo "════════════════════════════════"
if [ $fail -eq 0 ]; then
  echo "${GRN}${BLD}✓ CI passed${OFF}"
else
  echo "${RED}${BLD}✗ CI failed — fix violations before merging${OFF}"
fi
echo "════════════════════════════════"
exit $fail
