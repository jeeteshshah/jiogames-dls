#!/usr/bin/env bash
# ============================================================
# JioGames DLS — install git hooks
# Run once after cloning the repo:  bash tools/install-hooks.sh
# ============================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$ROOT/.git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "✗ Not a git repo (no .git/hooks found). Run: git init" >&2
  exit 1
fi

cp "$ROOT/tools/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo "✓ Pre-commit hook installed at $HOOKS_DIR/pre-commit"
echo "  Blocks commits when tokens.css is stale or staged files have violations."
