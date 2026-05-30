#!/usr/bin/env bash
# ============================================================
# JioGames DLS — drift validator (zero dependencies)
# Greps CSS/HTML for violations of the design system.
# Usage:  ./validate.sh <file-or-dir> [<file-or-dir> ...]
# Exit:   0 = clean, 1 = violations found
# Excludes tokens.css (the one place literals are allowed).
# ============================================================
set -uo pipefail

targets=("$@")
[ ${#targets[@]} -eq 0 ] && targets=(".")

fail=0
RED=$'\033[31m'; YEL=$'\033[33m'; GRN=$'\033[32m'; DIM=$'\033[2m'; OFF=$'\033[0m'

# Collect .css/.html files, skipping the token source itself
files=$(find "${targets[@]}" -type f \( -name '*.css' -o -name '*.html' \) 2>/dev/null | grep -v 'tokens.css' || true)
[ -z "$files" ] && { echo "No .css/.html files found."; exit 0; }

report() { # severity, label, grep-result
  local sev="$1" label="$2" hits="$3"
  [ -z "$hits" ] && return
  if [ "$sev" = "ERR" ]; then fail=1; echo "${RED}✗ ERROR${OFF}  $label"; else echo "${YEL}⚠ WARN ${OFF}  $label"; fi
  echo "$hits" | sed "s/^/    ${DIM}/;s/\$/${OFF}/"
}

scan() { grep -nEi "$1" $files 2>/dev/null | grep -viE 'tokens\.(css|json)'; }

echo "JioGames DLS — validating drift…"
echo "────────────────────────────────"

# 1. Page background literal black — should be --bg (ERROR)
report ERR "background:#000 — page bg must be --bg (#06080F), never pure black" \
  "$(scan 'background:\s*(#000\b|#000000\b|black\b)')"

# 1b. Other pure black/white literals — WARN (legit for CTA text / text-over-image, but prefer tokens)
report WARN "Pure black/white literal — use --text-inv (CTA text) or --text; #fff over images is OK" \
  "$(scan ':\s*(#fff\b|#ffffff\b|#000\b|#000000\b)' | grep -viE 'background:\s*#000|stroke=|fill=|stroke:#|fill:#')"

# 2. Blue / indigo / purple as accent — banned (JioGames is green)
report ERR "Blue/indigo/purple value — JioGames is green end-to-end" \
  "$(scan '#(6366f1|8b5cf6|7c3aed|3b82f6|6478ff)|rgba\(\s*(80|100),\s*1[0-2][0-9]')"

# 3. transition: all — banned (perf, list properties)
report ERR "transition: all — list explicit properties" \
  "$(scan 'transition:\s*all')"

# 4. Non-token font substitution
report ERR "Non-JioType font (Inter/Outfit/Roboto/Helvetica)" \
  "$(scan 'font-family:[^;]*(Inter|Outfit|Roboto|Helvetica)')"

# 5. Soft grey SaaS shadow on resting elements (warn — may be intentional lift)
report WARN "Soft grey box-shadow — use coloured glow for state, deep shadow only for lift" \
  "$(scan 'box-shadow:[^;]*rgba\(0,\s*0,\s*0,\s*0?\.(0[0-9]|1[0-5])')"

# 6. Raw hex in component files (warn — should be a token). Skips var()/url()/gradients meta.
report WARN "Raw hex literal — prefer var(--token) from tokens.css" \
  "$(scan '#[0-9a-f]{3,6}\b' | grep -viE 'var\(|@font-face|src:|url\(')"

# 7. Unauthorized font weight — only 300/500/700/900 exist (ERROR)
report ERR "Unauthorized font-weight — JioType allows only 300/500/700/900" \
  "$(scan 'font-weight:\s*(100|200|400|600|800)\b')"

# 8. Light weight on small text — warn (300 legal but risky small)
report WARN "font-weight:300 — illegible on small dark text, prefer 500" \
  "$(scan 'font-weight:\s*300\b')"

# 9. Off-scale spacing — warn. Scale: 0/2/4/8/12/16/24/32/40/48/64/80/96 (+aliases 20/60).
# Only padding/margin/gap/offsets — NOT radius/width/height/font/border.
report WARN "Off-scale spacing — use --space-* (8px scale: 4/8/12/16/24/32…) or a layout alias (20px banned)" \
  "$(scan '(padding|margin|gap|row-gap|column-gap|inset)[^:]*:\s*[^;{]*\b(5|6|7|9|10|11|14|18|20|22|26|28|30|36|44|52|56)px')"

# 10. Raw control-size literals in height/width — all have tokens now; raw px bypasses TV overrides (ERROR)
# Values: 54=--ctrl-h  44=--touch-min  40=--ctrl-h-ghost  36=--ctrl-h-sm  72=TV --ctrl-h
#         50=--otp-box-w  64=--otp-box-h/--tab-bar-h/--app-bar-h  96=--card-sq
#         156=--genre-tile-h  272=--card-wide-w  400=TV --card-wide-w
report ERR "Raw control-size literal in height/width — use var(--ctrl-h/--card-wide-w/--card-sq/etc.)" \
  "$(scan '(height|width|min-height|min-width)\s*:\s*(54|44|40|36|72|50|64|96|156|272|400)px')"

echo "────────────────────────────────"
if [ $fail -eq 0 ]; then
  echo "${GRN}✓ No blocking violations.${OFF}"
else
  echo "${RED}✗ Blocking violations found — fix before shipping.${OFF}"
fi
exit $fail
