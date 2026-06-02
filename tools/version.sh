#!/usr/bin/env bash
# ============================================================
# JioGames DLS — Design Version History
#
# Operates in the CURRENT WORKING DIRECTORY (your project).
# Versions saved to ./versions/<screen-name>/<version>/
# The skill folder stays clean — all history lives in your project.
#
# Usage:
#   bash version.sh save <screen> [note]       Save current version (auto-increment)
#   bash version.sh list <screen>              List all saved versions
#   bash version.sh restore <screen> <ver>     Restore a version (non-destructive)
#   bash version.sh diff <screen> <v1> <v2>    Compare two versions (line diff)
#   bash version.sh major <screen>             Bump to next major version on next save
#   bash version.sh status <screen>            Show current version info
#
# Auto-save: first save = v1, then v1.1, v1.2... Major bump = v2, v2.1...
# Restore is non-destructive: restores files but next save continues from latest.
# Files saved: index.html + styles.css (the output contract files).
# ============================================================
set -uo pipefail

# ── Colours ─────────────────────────────────────────────────
GRN=$'\033[32m'; YEL=$'\033[33m'; RED=$'\033[31m'; BLD=$'\033[1m'; DIM=$'\033[2m'; OFF=$'\033[0m'

VERSIONS_DIR="./versions"

# ── Helpers ─────────────────────────────────────────────────

# Parse version string "v1.2" → major=1 minor=2 (minor=0 if "v1")
parse_ver() {
  local v="${1#v}"   # strip leading v
  local major="${v%%.*}"
  local minor="0"
  [[ "$v" == *.* ]] && minor="${v#*.}"
  echo "$major $minor"
}

# Build version string from major + minor
make_ver() {
  local major=$1 minor=$2
  [ "$minor" -eq 0 ] && echo "v${major}" || echo "v${major}.${minor}"
}

# Find latest version folder for a screen (highest v-number)
# Uses Python for version sort — macOS sort lacks -V (GNU only)
latest_ver() {
  local screen_dir="$1"
  [ ! -d "$screen_dir" ] && echo "" && return
  python3 - "$screen_dir" << 'PYEOF'
import os, sys, re
d = sys.argv[1]
try:
    vers = [v for v in os.listdir(d) if re.match(r'^v\d+(\.[0-9]+)?$', v)]
except FileNotFoundError:
    sys.exit(0)
if not vers:
    sys.exit(0)
def ver_key(v):
    parts = v.lstrip('v').split('.')
    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
print(sorted(vers, key=ver_key)[-1])
PYEOF
}

# Get the pending major override (set by `major` command)
pending_major_file() { echo "${1}/.next-major"; }

# ── Commands ────────────────────────────────────────────────

cmd_save() {
  local screen="${1:-}" note="${2:-}"
  [ -z "$screen" ] && { echo "${RED}Usage: version.sh save <screen-name> [note]${OFF}"; exit 1; }

  # Check files exist
  local has_html has_css
  has_html=$([ -f "./index.html" ] && echo "1" || echo "0")
  has_css=$([ -f "./styles.css" ] && echo "1" || echo "0")
  [ "$has_html" = "0" ] && { echo "${RED}✗ index.html not found in current directory${OFF}"; exit 1; }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  mkdir -p "$screen_dir"

  # Determine next version
  local current
  current=$(latest_ver "$screen_dir")
  local major minor next_ver

  # Check for pending major bump
  local major_file
  major_file=$(pending_major_file "$screen_dir")

  if [ -z "$current" ]; then
    # First save ever
    next_ver="v1"
  elif [ -f "$major_file" ]; then
    # Major bump requested
    read -r major minor <<< "$(parse_ver "$current")"
    next_ver="v$((major + 1))"
    rm -f "$major_file"
  else
    # Increment minor
    read -r major minor <<< "$(parse_ver "$current")"
    if [ "$minor" -eq 0 ]; then
      next_ver="v${major}.1"
    else
      next_ver="v${major}.$((minor + 1))"
    fi
  fi

  local save_dir="${screen_dir}/${next_ver}"
  mkdir -p "$save_dir"

  # Copy files
  cp "./index.html" "$save_dir/"
  [ "$has_css" = "1" ] && cp "./styles.css" "$save_dir/"

  # Write meta.json
  local restored_from=""
  [ -f "${screen_dir}/.last-restore" ] && {
    restored_from=$(cat "${screen_dir}/.last-restore")
    rm -f "${screen_dir}/.last-restore"
  }

  cat > "${save_dir}/meta.json" << EOF
{
  "version": "${next_ver}",
  "screen": "${screen}",
  "date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "note": "${note}",
  "restored_from": "${restored_from}",
  "files": ["index.html"$([ "$has_css" = "1" ] && echo ', "styles.css"' || echo "")]
}
EOF

  echo "${GRN}${BLD}✓ Saved${OFF} ${screen} → ${BLD}${next_ver}${OFF}"
  [ -n "$note" ] && echo "  ${DIM}${note}${OFF}" || true
  [ -n "$restored_from" ] && echo "  ${YEL}↩ Branched from ${restored_from}${OFF}" || true
  return 0
}

cmd_list() {
  local screen="${1:-}"
  [ -z "$screen" ] && {
    # List all screens
    [ ! -d "$VERSIONS_DIR" ] && { echo "${DIM}No versions saved yet.${OFF}"; return; }
    echo "${BLD}Screens with version history:${OFF}"
    ls "$VERSIONS_DIR" 2>/dev/null | grep -v '^\.' | while read -r s; do
      local latest
      latest=$(latest_ver "${VERSIONS_DIR}/${s}")
      local count
      count=$(ls "${VERSIONS_DIR}/${s}" 2>/dev/null | grep -cE '^v[0-9]' || true)
      echo "  ${BLD}${s}${OFF} — ${count} version(s), latest ${GRN}${latest}${OFF}"
    done
    return
  }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  [ ! -d "$screen_dir" ] && { echo "${RED}No versions found for '${screen}'${OFF}"; exit 1; }

  echo "${BLD}Version history: ${screen}${OFF}"
  echo "──────────────────────────────────"
  python3 - "$screen_dir" << 'PYEOF' \
    | while read -r ver; do
import os, sys, re
d = sys.argv[1]
try:
    vers = [v for v in os.listdir(d) if re.match(r'^v\d+(\.[0-9]+)?$', v)]
except FileNotFoundError:
    sys.exit(0)
def ver_key(v):
    parts = v.lstrip('v').split('.')
    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
for v in sorted(vers, key=ver_key):
    print(v)
PYEOF
      local meta="${screen_dir}/${ver}/meta.json"
      local note="" date="" restored=""
      if [ -f "$meta" ]; then
        note=$(python3 -c "import json,sys; d=json.load(open('$meta')); print(d.get('note',''))" 2>/dev/null || true)
        date=$(python3 -c "import json,sys; d=json.load(open('$meta')); print(d.get('date','')[:10])" 2>/dev/null || true)
        restored=$(python3 -c "import json,sys; d=json.load(open('$meta')); print(d.get('restored_from',''))" 2>/dev/null || true)
      fi
      local latest
      latest=$(latest_ver "$screen_dir")
      local marker=""
      [ "$ver" = "$latest" ] && marker=" ${GRN}← latest${OFF}"
      local restore_note=""
      [ -n "$restored" ] && restore_note=" ${YEL}(↩ from ${restored})${OFF}"
      echo "  ${BLD}${ver}${OFF}  ${DIM}${date}${OFF}  ${note}${restore_note}${marker}"
    done
  echo "──────────────────────────────────"
  echo "  Restore: bash version.sh restore ${screen} <version>"
  return 0
}

cmd_restore() {
  local screen="${1:-}" ver="${2:-}"
  [ -z "$screen" ] || [ -z "$ver" ] && {
    echo "${RED}Usage: version.sh restore <screen-name> <version>${OFF}"
    echo "Example: bash version.sh restore home-screen v1.2"
    exit 1
  }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  local restore_dir="${screen_dir}/${ver}"

  [ ! -d "$restore_dir" ] && {
    echo "${RED}✗ Version '${ver}' not found for screen '${screen}'${OFF}"
    echo "  Run: bash version.sh list ${screen}"
    exit 1
  }

  # Auto-save current state before restoring (non-destructive)
  local current_latest
  current_latest=$(latest_ver "$screen_dir")
  if [ -f "./index.html" ] && [ -n "$current_latest" ]; then
    echo "${YEL}Auto-saving current state before restore…${OFF}"
    cmd_save "$screen" "auto-save before restoring ${ver}"
  fi

  # Record what we restored from (for next save's meta)
  echo "$ver" > "${screen_dir}/.last-restore"

  # Copy restored files to working directory
  cp "${restore_dir}/index.html" "./index.html"
  [ -f "${restore_dir}/styles.css" ] && cp "${restore_dir}/styles.css" "./styles.css"

  echo "${GRN}${BLD}✓ Restored${OFF} ${screen} to ${BLD}${ver}${OFF}"
  echo "  ${DIM}Next save will record this as branched from ${ver}${OFF}"
  echo "  ${DIM}Previous versions are untouched — full history preserved${OFF}"
  return 0
}

cmd_diff() {
  local screen="${1:-}" v1="${2:-}" v2="${3:-}"
  [ -z "$screen" ] || [ -z "$v1" ] || [ -z "$v2" ] && {
    echo "${RED}Usage: version.sh diff <screen-name> <v1> <v2>${OFF}"
    exit 1
  }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  local f1="${screen_dir}/${v1}/index.html"
  local f2="${screen_dir}/${v2}/index.html"

  [ ! -f "$f1" ] && { echo "${RED}✗ ${v1}/index.html not found${OFF}"; exit 1; }
  [ ! -f "$f2" ] && { echo "${RED}✗ ${v2}/index.html not found${OFF}"; exit 1; }

  echo "${BLD}Diff: ${screen} ${v1} → ${v2}${OFF}"
  echo "──────────────────────────────────"
  diff --color=always -u "$f1" "$f2" || true
  echo "──────────────────────────────────"

  # Also diff styles.css if both exist
  local s1="${screen_dir}/${v1}/styles.css"
  local s2="${screen_dir}/${v2}/styles.css"
  if [ -f "$s1" ] && [ -f "$s2" ]; then
    echo "${BLD}Diff: styles.css${OFF}"
    diff --color=always -u "$s1" "$s2" || true
  fi
  return 0
}

cmd_major() {
  local screen="${1:-}"
  [ -z "$screen" ] && { echo "${RED}Usage: version.sh major <screen-name>${OFF}"; exit 1; }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  mkdir -p "$screen_dir"

  local current
  current=$(latest_ver "$screen_dir")
  local major minor next_major
  if [ -z "$current" ]; then
    next_major=1
  else
    read -r major minor <<< "$(parse_ver "$current")"
    next_major=$((major + 1))
  fi

  touch "$(pending_major_file "$screen_dir")"
  echo "${YEL}${BLD}Major bump queued${OFF} — next save will be ${BLD}v${next_major}${OFF}"
  echo "  ${DIM}Run: bash version.sh save ${screen} \"description\"${OFF}"
  return 0
}

cmd_status() {
  local screen="${1:-}"
  [ -z "$screen" ] && { echo "${RED}Usage: version.sh status <screen-name>${OFF}"; exit 1; }

  local screen_dir="${VERSIONS_DIR}/${screen}"
  local latest
  latest=$(latest_ver "$screen_dir")

  [ -z "$latest" ] && { echo "${DIM}No versions saved for '${screen}' yet.${OFF}"; return; }

  local meta="${screen_dir}/${latest}/meta.json"
  echo "${BLD}${screen}${OFF} — current: ${GRN}${latest}${OFF}"
  if [ -f "$meta" ]; then
    python3 -c "
import json, sys
d = json.load(open('$meta'))
print(f\"  Date:  {d.get('date','')[:19].replace('T',' ')}\")
print(f\"  Note:  {d.get('note','—')}\")
rf = d.get('restored_from','')
if rf: print(f\"  ↩ Branched from: {rf}\")
" 2>/dev/null || true
  fi

  # Show major-pending
  [ -f "$(pending_major_file "$screen_dir")" ] && \
    echo "  ${YEL}Major bump queued for next save${OFF}"
}

# ── Dispatch ────────────────────────────────────────────────
CMD="${1:-}"
shift 2>/dev/null || true

case "$CMD" in
  save)    cmd_save "$@" ;;
  list)    cmd_list "$@" ;;
  restore) cmd_restore "$@" ;;
  diff)    cmd_diff "$@" ;;
  major)   cmd_major "$@" ;;
  status)  cmd_status "$@" ;;
  *)
    echo "${BLD}JioGames DLS — Version History${OFF}"
    echo ""
    echo "Usage:"
    echo "  bash version.sh save <screen> [note]      Save current (auto-increment)"
    echo "  bash version.sh list [screen]             List all versions"
    echo "  bash version.sh restore <screen> <ver>   Restore (non-destructive)"
    echo "  bash version.sh diff <screen> <v1> <v2>  Compare two versions"
    echo "  bash version.sh major <screen>            Queue major version bump"
    echo "  bash version.sh status <screen>           Show current version"
    echo ""
    echo "Version scheme:  v1 → v1.1 → v1.2 → (major) → v2 → v2.1"
    echo "Versions saved to: ./versions/<screen>/ (in your project, not the skill)"
    ;;
esac
