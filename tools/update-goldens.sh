#!/usr/bin/env bash
# ============================================================
# JioGames DLS — capture / refresh golden screenshots.
# Run this after any intentional visual change to the DLS.
# Goldens are committed to the repo — they are the source of
# truth for what components should look like.
#
# Usage: bash tools/update-goldens.sh
# ============================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "JioGames DLS — updating goldens…"
echo "══════════════════════════════════"

# Check deps
if ! python3 -c "import playwright" 2>/dev/null; then
  echo "Installing Playwright…"
  pip3 install playwright pillow --quiet
  playwright install chromium --quiet
fi

python3 tools/visual-test.py --update

echo ""
echo "Next steps:"
echo "  1. Review changed images in tests/golden/"
echo "  2. git add tests/golden/ && git commit -m 'chore: update visual goldens'"
