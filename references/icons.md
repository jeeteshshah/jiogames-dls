# JioGames Icon Governance

> **In-house solid glyph library only.** The official Jio SVG icon library is the sole approved source. All icons are solid filled glyphs — not outline stroke icons. Lucide and all third-party icon libraries are banned. Lucide is outline-based and does not match this icon system's visual language; it must not be used in any governed output, review, demo, or production code.

**Structure**

1. Library Source
2. Naming Convention
3. Visual Style Rules
4. Implementation Rules
5. Token-Based Sizing & Colour
6. Icon Wrappers
7. Accessibility Rules
8. Platform Rules
9. icons-manifest.json Structure
10. Filename Audit & Migration Map
11. Anti-Patterns
12. Icon QA Checklist

---

# 1. Library Source

| Library | Figma file | Node | When to use |
|---|---|---|---|
| **Core** | `9IRfFnQ90DAQDhgK7DCdEm` | `9185:136168` | Common icons — check here first |
| **Extended** | `9IRfFnQ90DAQDhgK7DCdEm` | `11:5` | 1,600+ icons — use when Core doesn't cover |

Exported SVGs live in `icons/svg/` (1,646 files). Sprite at `icons/sprite.svg`. Category sprites in `icons/sprites/`.

### Getting icons

```bash
# Export / refresh from Figma (needs token)
python3 tools/export-icons.py --token YOUR_TOKEN        # core set (41 icons)
python3 tools/export-all-icons.py --token YOUR_TOKEN    # full library (1,646 icons)
```

### Using in HTML

```html
<!-- Preferred: sprite reference — size via CSS, not SVG attributes -->
<svg class="icon icon-size-base" aria-hidden="true" focusable="false">
  <use href="icons/sprite.svg#ic_play_circle"/>
</svg>
<!-- Note: sprite.svg symbols must have fill="currentColor" on all paths.
     The export script normalises individual SVGs — sprite generation applies
     the same normalisation to every <symbol>. If a symbol has hardcoded fill,
     CSS cannot override it via color on the parent. -->
```

<!-- Alternative: inline SVG -->
<!-- Paste contents of icons/svg/ic_play_circle.svg -->
```

### Third-party icon library policy

Lucide is outline-based. It does not match the solid glyph style of this library and must not be used in any context. No third-party icon library is approved as a substitute or fallback.

If an icon does not exist in the Jio library, request it through the contribution process (`_info/Icons-Contribution-Intro` in the Figma file). Do not reach for Lucide or any external set.

---

# 2. Naming Convention

### Pattern

```
ic_[category]_[object]_[variant_or_state].svg
```

| Segment | Rules | Example |
|---|---|---|
| `ic` | Fixed prefix — always present | `ic_` |
| `category` | Domain group — single word | `gaming`, `media`, `nav`, `status` |
| `object` | What the icon depicts — one or two words | `play`, `play_circle`, `bookmark` |
| `variant_or_state` | Optional — only when needed to disambiguate | `off`, `on`, `add`, `remove`, `selected`, `disabled` |

### Rules

- All lowercase. No camelCase, PascalCase, or mixed case.
- Words separated by single underscore. No double underscores.
- No trailing underscore.
- Numbers as digits, not words. `ic_4g_bar_4` not `ic_4g_bar_four`.
- Abbreviations only when universally understood (`lte`, `4g`, `hd`, `tv`). When ambiguous, spell out.
- State suffixes: `_off`, `_on`, `_add`, `_remove`, `_selected`, `_disabled`. Do not use `_outline` or `_filled` — all icons are solid by default.
- Colour word `_coloured` is allowed when an icon has a brand-specific multi-colour fill that cannot be overridden by `currentColor`.

### Scope

**New icons must follow this convention.** Existing 1,646 icons in `icons/svg/` remain valid through manifest aliases until a major version migration. Do not rename existing files directly — add an alias in `icons/icons-manifest.json` first and migrate consumers before any rename.

### Good examples (for new icons)

```
ic_gaming_controller.svg
ic_media_play_circle.svg
ic_nav_search.svg
ic_status_success.svg
ic_status_fail.svg
ic_network_4g_bar_4.svg        ← digit, not word
ic_connectivity_lte.svg        ← lowercase
ic_network_vonr.svg            ← lowercase (not VoNR)
ic_apparel_clothing.svg        ← corrected spelling (not aparell)
```

---

# 3. Visual Style Rules

The Jio icon library is a **solid glyph system**. All icons are filled path shapes — not outline stroke icons. There is no outline variant, no stroke-based icon, and no mixed-stroke icon in this library.

| Style | Library source | CSS mechanism |
|---|---|---|
| **Solid filled** (default) | All Jio icons | `fill: currentColor` |
| Stroke icons | Not currently in this library | Do not define stroke-based defaults |

The library is solid today. If the library expands to include outline or mixed icons in a future version, this governance will be updated. Until then, solid is the only valid visual style and all icon CSS must reflect that.

### Optical weight

Solid icons carry more visual weight than outline icons at the same size. Account for this in implementation:

- **Use smaller sizes** (`var(--icon-size-sm)`, `var(--icon-size-md)`) when icons appear alongside dense text or in compact rails. The base 24px can overpower small text.
- **Use `color: var(--icon-color-default)`** for supporting icons that are not the primary affordance. Full `--icon-color-active` (= `--jio`) only for the single active or action icon per surface.
- **Use fewer icons** per surface. A solid icon rail with 5+ icons in active green creates visual noise — only one icon per surface should be active green.
- **Use opacity for disabled state** — `opacity: .32` on the icon wrapper, not a different colour. This preserves semantic meaning while communicating unavailability.
- **Avoid stacking icons** (icon + icon without label) — a solid icon alone reads heavier than an outline equivalent. Add a label or reduce the icon count.

### Normalisation rule

Exported SVGs from Figma have hardcoded colours. Replace with `currentColor` so the same SVG renders in any semantic token colour:

```svg
<!-- Before (hardcoded — breaks theming) -->
<path fill="#000000" d="..."/>

<!-- After (normalised — renders in any color) -->
<path fill="currentColor" d="..."/>
```

Also remove hardcoded `width` and `height` from the `<svg>` root — size is controlled by CSS, not SVG attributes:

```svg
<!-- Before (hardcoded size — remove these) -->
<svg width="24" height="24" viewBox="0 0 24 24">

<!-- After -->
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
```

Keep `viewBox` always — it defines the internal coordinate space and cannot be removed.

---

# 4. Implementation Rules

### Base icon CSS

All icons in this library are solid glyphs. The default rendering is `fill: currentColor`. No stroke rules apply.

```css
/* Base — all Jio solid icons */
.icon {
  display: inline-block;
  flex-shrink: 0;           /* never compress in flex containers */
  vertical-align: middle;
}

/* Colour inherited from parent via currentColor */
.icon path,
.icon circle,
.icon rect,
.icon polygon {
  fill: currentColor;
}
```

Do not write `.icon-outline` or `.icon stroke` CSS classes — there are no outline icons in this library.

### Icon size utility classes

Add these to your screen's stylesheet. They match the `--icon-size-*` token namespace exactly:

```css
.icon-size-xs   { width: var(--icon-size-xs);   height: var(--icon-size-xs); }
.icon-size-sm   { width: var(--icon-size-sm);   height: var(--icon-size-sm); }
.icon-size-md   { width: var(--icon-size-md);   height: var(--icon-size-md); }
.icon-size-base { width: var(--icon-size-base); height: var(--icon-size-base); }
.icon-size-lg   { width: var(--icon-size-lg);   height: var(--icon-size-lg); }
.icon-size-xl   { width: var(--icon-size-xl);   height: var(--icon-size-xl); }
```

Use in HTML: `<svg class="icon icon-size-base" aria-hidden="true" focusable="false">`.
Never set `width`/`height` as SVG attributes — always use these classes.

### Setting colour

Set `color` on the parent element — never directly on the SVG or its paths:

```css
/* ✓ Correct — use icon colour tokens, not text tokens */
.tab-icon        { color: var(--icon-color-default); }
.tab-icon.active { color: var(--icon-color-active); }

/* ✓ Correct — muted supporting icon */
.card-meta-icon  { color: var(--icon-color-muted); }

/* ✓ Correct — disabled state via opacity */
.icon-disabled   { opacity: .32; pointer-events: none; }

/* ✗ Wrong — raw hex on SVG */
.tab-icon svg { fill: #00A859; }

/* ✗ Wrong — stroke on solid icons */
.icon path { stroke: currentColor; stroke-width: 1.8; }
```

### State transitions

```css
.icon-interactive {
  transition: color var(--dur-fast) var(--spring);
}
```

Never raw timing: `transition: color .15s` → violation. Always `var(--dur-fast)`.

### Forbidden in SVG files

After export and normalisation, SVG files must not contain:

- `fill="#xxxxxx"` — replace with `fill="currentColor"`
- `fill="black"` or `fill="white"` — replace with `fill="currentColor"`
- `stroke="#xxxxxx"` on path elements — remove; solid icons have no strokes
- `width="..."` or `height="..."` on `<svg>` root — remove; size set by CSS
- `rgba(...)` hardcoded on any element

### What SVG files must contain

```svg
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" d="..."/>
</svg>
```

- `viewBox` — always present
- `fill="currentColor"` on all path/shape elements
- No `width`, no `height`, no hardcoded colour

This rule applies to **both individual SVGs and sprite symbols**. The sprite generator (`tools/export-all-icons.py`) applies the same `currentColor` normalisation to every `<symbol>` before writing `icons/sprite.svg`. If a symbol has a hardcoded fill, the parent `color` CSS property cannot override it — `<use>` inherits `currentColor` only when the source symbol is clean.

---

# 5. Token-Based Sizing & Colour

### Icon size tokens

Icon optical sizes are independent of the 8px spacing scale. All live under the `icon` namespace in `tokens/tokens.json`.

> Token source uses dot notation (`icon.size.base`). Generated CSS uses `--icon-size-base`. Never use dot notation in CSS — always the generated `--icon-*` form.

| CSS token | Namespace | Value | Context |
|---|---|---:|---|
| `--icon-size-xs` | `icon.size.xs` | 14px | Card meta, timestamps, inline label |
| `--icon-size-sm` | `icon.size.sm` | 16px | Inline with body text, perk checks |
| `--icon-size-md` | `icon.size.md` | 20px | Standard chip, tab bar |
| `--icon-size-base` | `icon.size.base` | 24px | Default UI icon — base grid |
| `--icon-size-lg` | `icon.size.lg` | 32px | Feature icon, large action |
| `--icon-size-xl` | `icon.size.xl` | 40px | Hero context, TV nav |

### Icon colour tokens

Do not use `var(--text3)` as an icon colour proxy. Use the dedicated icon colour tokens:

| CSS token | Namespace | Value | Context |
|---|---|---|---|
| `--icon-color-default` | `icon.color.default` | `rgba(255,255,255,.45)` | Inactive icon on dark bg — semi-transparent supporting role |
| `--icon-color-active` | `icon.color.active` | `#00A859` | Selected / active icon (= `--jio`) |
| `--icon-color-muted` | `icon.color.muted` | `#6B7280` | Decorative-only icon (= `--text3`) |

And semantic overrides:

| State | Token |
|---|---|
| Default | `color: var(--icon-color-default)` |
| Active / selected | `color: var(--icon-color-active)` |
| Muted / decorative | `color: var(--icon-color-muted)` |
| On green surface | `color: var(--text-inv)` |
| Error | `color: var(--negative)` |
| Ultimate Pass | `color: var(--ultimate)` |

### Icon wrapper tokens

| CSS token | Namespace | Value | Context |
|---|---|---:|---|
| `--icon-wrapper-sm` | `icon.wrapper.sm` | 40px | Small wrapper — inline action |
| `--icon-wrapper-md` | `icon.wrapper.md` | 48px | Medium wrapper — feature icon |

```css
.icon-wrap-sm {
  width: var(--icon-wrapper-sm);
  height: var(--icon-wrapper-sm);
  border-radius: var(--r2);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.icon-wrap-md {
  width: var(--icon-wrapper-md);
  height: var(--icon-wrapper-md);
  border-radius: var(--r3);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
/* Background colour — always token */
.icon-wrap-brand  { background: var(--jio); color: var(--text-inv); }
.icon-wrap-tint   { background: var(--jio-soft); color: var(--icon-color-active); }
.icon-wrap-glass  { background: var(--glass-1); color: var(--icon-color-default); border: 1px solid var(--border-subtle); }
```

### Icon + text gap

```css
.icon-label {
  display: inline-flex;
  align-items: center;
  gap: var(--space-0-5);          /* 4px */
}
```

---

# 6. Icon Wrappers

### Approved optical exceptions

These raw values appear in wrapper CSS below. They are governed exceptions — not arbitrary choices. Do not change without an RFC.

`tokens/validate.sh` must allow these values **only** in the listed selectors. Any use of these values outside the specified selector is a violation — the exception table does not create a general permission.

| Value | Allowed selector | Token/reason |
|---|---|---|
| `26px` × `26px` | `.icon-circle`, `.icon-glass` only | Optical circular wrap — between `--space-3` (24px) and `--space-4` (32px); both wrong for tight icon circle |
| `rgba(0,0,0,.5)` | `.icon-glass` background only | Translucent overlay black — no token equivalent; approved for glass overlay context only |
| `blur(6px)` | `.icon-glass` backdrop only | Light frosted blur — approved for icon wrappers (lighter than tab bar 28px) |
| `rgba(0,168,89,.45)` | `.selected .icon-glass` border only | Extended tinted border; closest token is `--border-ultimate` but wrong colour; approved for selected genre tile only |

### Circular (action dots, avatar rings)

```css
.icon-circle {
  width: 26px; height: 26px;     /* approved optical exception — see table above */
  border-radius: 50%;
  background: var(--jio);
  color: var(--text-inv);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Rounded square (feature icons, USP)

```css
.icon-sq {
  width: var(--icon-wrapper-sm);
  height: var(--icon-wrapper-sm);
  border-radius: var(--r3);
  background: var(--jio-soft);
  color: var(--icon-color-active);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Glassy (genre tiles, overlay UI)

```css
.icon-glass {
  width: 26px; height: 26px;     /* approved optical exception — see table above */
  border-radius: var(--r2);
  background: rgba(0,0,0,.5);    /* approved optical exception */
  backdrop-filter: blur(6px);    /* approved optical exception */
  border: 1px solid var(--border-subtle);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.selected .icon-glass {
  background: var(--jio-soft);
  border-color: rgba(0,168,89,.45);   /* approved optical exception */
  color: var(--jio-bright);
}
```

---

# 7. Accessibility Rules

### Decorative icons (alongside text)

Icon adds no information — text carries the meaning.

```html
<button>
  <svg class="icon icon-size-base" aria-hidden="true" focusable="false">
    <use href="icons/sprite.svg#ic_play_circle"/>
  </svg>
  Play
</button>
```

Required: `aria-hidden="true"` + `focusable="false"` on SVG.

### Icon-only buttons

No visible label — icon must carry full meaning.

```html
<!-- ✓ Preferred — real <button>, keyboard/D-pad focus automatic -->
<button aria-label="Play game" class="icon-btn">
  <svg class="icon icon-size-base" aria-hidden="true" focusable="false">
    <use href="icons/sprite.svg#ic_play_circle"/>
  </svg>
</button>

<!-- Only when semantic element not possible — add role + tabindex -->
<div role="button" tabindex="0" aria-label="Play game" class="icon-btn">
  <svg class="icon icon-size-base" aria-hidden="true" focusable="false">
    <use href="icons/sprite.svg#ic_play_circle"/>
  </svg>
</div>
```

Required: `aria-label` on the interactive element (button or div). Icon gets `aria-hidden="true"`.
Tap target: `min-width: var(--touch-min); min-height: var(--touch-min)` (44px mobile, 60px TV).

### Status icons (success, warning, error)

Status must never rely on icon alone — pair with text label.

```html
<!-- Error: icon + text, never icon alone -->
<span class="error-msg" role="alert">
  <svg aria-hidden="true" focusable="false">
    <use href="icons/sprite.svg#ic_status_fail"/>
  </svg>
  <span>Payment failed. Try again.</span>
</span>
```

### Loading icons

```html
<span role="status" aria-label="Loading">
  <svg aria-hidden="true" focusable="false" class="icon-spin">
    <use href="icons/sprite.svg#ic_status_loading"/>
  </svg>
</span>
```

```css
/* 1s rotation is an approved ambient loop duration — see motion.md §3 Ambient category */
.icon-spin {
  animation: icon-rotate 1s linear infinite;
}
@keyframes icon-rotate {
  to { transform: rotate(360deg); }
}
@media (prefers-reduced-motion: reduce) {
  .icon-spin { animation: none; }
}
```

### TV icon controls

- Use a real `<button>` or `<a>` element first — keyboard and D-pad focus comes for free. Add `tabindex="0"` and `role="button"` only when a non-semantic element is unavoidable.
- All interactive icon elements (button or otherwise): `aria-label` required.
- Focus ring: `box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4)` — approved TV glow recipe (colour-governance.md).
- Min focus target: `min-width: var(--touch-min); min-height: var(--touch-min)` (60px on TV).
- No hover-only affordance — all hover effects must also apply on `:focus`.

---

# 8. Platform Rules

### Mobile

- Base size: `var(--icon-size-base)` (24px)
- Tap target: `min-width/height: var(--touch-min)` (44px)
- `backdrop-filter` on glassy wrappers: allowed

### Web

- Same sizes as mobile
- Hover: `color: var(--icon-color-active)` transition on interactive icons
- Pointer target: 32px minimum (no token needed — pointer is precise)

### TV

| Context | Token | Value on TV |
|---|---|---|
| Nav bar icon | `var(--icon-size-xl)` | 40px |
| Card meta icon | `var(--icon-size-lg)` | 32px |
| Focusable control | `var(--icon-size-xl)` | 40px |

```css
@media (min-width: 1280px) and (min-height: 720px) {
  .nav-icon       { width: var(--icon-size-xl); height: var(--icon-size-xl); }
  .card-meta-icon { width: var(--icon-size-lg); height: var(--icon-size-lg); }
  .icon-glass   { backdrop-filter: none; }   /* no backdrop-filter on TV */
}
```

---

# 9. icons-manifest.json Structure

Each icon should have an entry in `icons/icons-manifest.json`. This enables search, filtering, and AI-assisted icon selection.

### Schema

```json
{
  "ic_play_circle": {
    "filename": "ic_play_circle.svg",
    "cleanName": "Play Circle",
    "category": "media",
    "keywords": ["play", "start", "video", "music", "stream", "launch"],
    "allowedUse": ["game-card", "hero-cta", "video-player", "content-rail"],
    "state": "default",
    "visualStyle": "solid",
    "decorativeDefault": false,
    "labelWhenInteractive": "Play",
    "aliases": ["ic_play", "ic_play_button"],
    "notes": "Primary play affordance. Use ic_play_pause for toggle state."
  },
  "ic_separator_dot": {
    "filename": "ic_separator_dot.svg",
    "cleanName": "Separator Dot",
    "category": "ui",
    "keywords": ["dot", "separator", "divider", "meta"],
    "allowedUse": ["metadata-row"],
    "state": "default",
    "visualStyle": "solid",
    "decorativeDefault": true,
    "labelWhenInteractive": null,
    "aliases": [],
    "notes": "Always decorative — never used as an interactive control."
  }
}
```

### Field definitions

| Field | Type | Required | Description |
|---|---|:---:|---|
| `filename` | string | ✓ | Exact filename in `icons/svg/` |
| `cleanName` | string | ✓ | Human-readable display name |
| `category` | string | ✓ | Domain category (`media`, `gaming`, `nav`, `status`, `platform`, `ui`) |
| `keywords` | string[] | ✓ | Search terms — at least 3 |
| `allowedUse` | string[] | ✓ | Where this icon may appear in JioGames UI |
| `state` | enum | ✓ | `default` / `active` / `off` / `loading` / `error` |
| `visualStyle` | enum | ✓ | `solid` (default) · `brand_multicolour` · `logo` · `illustration_exception` |
| `decorativeDefault` | boolean | ✓ | `true` = almost always decorative; `false` = may be used as interactive control |
| `labelWhenInteractive` | string \| null | ✓ | Default `aria-label` when used as icon-only button. `null` if icon should never be used alone as a control. |
| `aliases` | string[] | — | Legacy filenames or alternate search terms for this icon |
| `notes` | string | — | Usage guidance, pairing rules, or deprecation notice |

`accessibilityLabel` is **not** required for every icon. Decorative icons (`decorativeDefault: true`) need `aria-hidden="true"` — no label. Labels are only required when an icon is used as an icon-only button, and that label goes on the `<button>`, not the SVG.

### Generating the manifest

Run after export to auto-generate a base manifest:

```bash
python3 tools/generate-manifest.py    # creates icons/icons-manifest.json
```

Manifest entries then need manual review for `decorativeDefault`, `labelWhenInteractive`, `allowedUse`, and `notes`.

---

# 10. Filename Audit & Migration Map

**Audits must be generated from the real `icons/svg/` directory** — never manually inferred. Run the audit script to get a current picture:

```bash
python3 tools/audit-icons.py
```

The script checks: spelling suspects, uppercase letters, trailing spaces, duplicate meanings, missing category prefix, numeric words, icons not in manifest, manifest entries whose files do not exist.

The migration map below was generated from the current library. Rerun the script after any export update.

**Do not rename files directly** — create aliases in manifest first, migrate consumers, then rename in a MAJOR version bump.

### Critical issues

| Old filename | Proposed filename | Issue | Risk | Alias needed |
|---|---|---|---|:---:|
| `ic_LTE.svg` | `ic_connectivity_lte.svg` | Uppercase — breaks case-sensitive systems | High | Yes |
| `ic_VoNR.svg` | `ic_network_vonr.svg` | Uppercase + category missing | High | Yes |
| `ic_aparell.svg` | `ic_apparel_clothing.svg` | Misspelling of "apparel"; no object word | High | Yes |
| `ic_arist_mic.svg` | `ic_artist_mic.svg` | Misspelling of "artist" | Medium | Yes |
| `ic_antibacteria.svg` | `ic_antibacterial.svg` | Misspelling — should be antibacterial | Medium | Yes |
| `ic_hiefer_abortion.svg` | `ic_heifer_abortion.svg` | Misspelling of "heifer" | Medium | Yes |
| `ic_hiefer_breeding.svg` | `ic_heifer_breeding.svg` | Misspelling of "heifer" | Medium | Yes |
| `ic_horzontal_swing.svg` | `ic_horizontal_swing.svg` | Misspelling of "horizontal" | Medium | Yes |
| `ic_vaccum_cleaner.svg` | `ic_vacuum_cleaner.svg` | Misspelling of "vacuum" | Medium | Yes |
| `ic_colour_palette .svg` | `ic_colour_palette.svg` | Trailing space in filename | High | No |

### Numeric word names

| Old filename | Proposed filename | Reason | Risk |
|---|---|---|---|
| `ic_4g_bar_four.svg` | `ic_network_4g_bar_4.svg` | Digit not word; add category | Low |
| `ic_4g_bar_three.svg` | `ic_network_4g_bar_3.svg` | Same | Low |
| `ic_4g_bar_two.svg` | `ic_network_4g_bar_2.svg` | Same | Low |
| `ic_4g_bar_one.svg` | `ic_network_4g_bar_1.svg` | Same | Low |
| `ic_analytics_pie_chart_two.svg` | `ic_analytics_pie_chart_2.svg` | Digit not word | Low |
| `ic_three_day.svg` | `ic_weather_3day.svg` | Digit + category | Low |

### Near-duplicates to resolve

| Names | Decision | Notes |
|---|---|---|
| `ic_adblock_plus` + `ic_adblocker` | Keep `ic_adblock_plus`; deprecate `ic_adblocker` | Plus is a recognised product name; blocker is generic |
| `ic_4g` + `ic_4g_lte` + `ic_4g_lte_data` | Keep all; document hierarchy in manifest | Different signal states |
| `ic_remote_universal_a` + `ic_remote_universal_b` + `ic_remote_universal_u` | Clarify in manifest — likely brand variants | Consult content team |
| `ic_vitamin_b` + `ic_vitamin_d` | Keep both — distinct health content | Not a duplicate |

### Unclear or vague names

| Old filename | Proposed filename | Reason |
|---|---|---|
| `ic_4g.svg` | `ic_network_4g.svg` | Add category |
| `ic_5g.svg` | `ic_network_5g.svg` | Add category |
| `ic_4k.svg` | `ic_media_4k.svg` | Add category |
| `ic_8k.svg` | `ic_media_8k.svg` | Add category |
| `ic_hd.svg` | `ic_media_hd.svg` | Add category |
| `ic_sd.svg` | `ic_storage_sd.svg` | Add category |
| `ic_tv.svg` | `ic_device_tv.svg` | Add category |
| `ic_vr.svg` | `ic_device_vr.svg` | Add category |
| `ic_av.svg` | `ic_media_av.svg` | Add category |
| `ic_cv.svg` | `ic_document_cv.svg` | Add category |
| `ic_id.svg` | `ic_identity_id.svg` | Add category |

---

# 11. Anti-Patterns

| Pattern | Reason | Fix |
|---|---|---|
| Using Lucide or any outline icon library | Wrong style — outline does not match solid glyph system | Replace with Jio icon from `icons/svg/` |
| `stroke: currentColor` on icon paths | Solid icons have no strokes | Remove all stroke rules from icon CSS |
| `stroke-width`, `stroke-linecap`, `stroke-linejoin` in CSS | Outline rules — invalid for solid library | Remove entirely |
| `.icon-outline` CSS class | No outline icons exist | Delete class; it is meaningless for this library |
| `fill: #00A859` or any hex on SVG path | Hardcodes colour, breaks theming | `fill: currentColor` + set `color` on parent |
| `fill="black"` or `fill="white"` in SVG file | Hardcoded — cannot be themed | Replace with `fill="currentColor"` in SVG source |
| `width="24" height="24"` left on `<svg>` root | Prevents CSS size control | Remove; set size in CSS |
| Multiple active icons on one surface | Solid icons are visually heavy — 3+ active icons = noise | Active icon uses `var(--icon-color-active)`; rest use `var(--icon-color-default)` or `var(--icon-color-muted)` |
| Full-size 24px icon next to small caption text | Optical weight mismatch | Step down to `var(--icon-size-sm)` (16px) or `var(--icon-size-md)` (20px) |
| Icon-heavy row without labels | Solid glyphs decode slower than outline without context | Always pair action icons with label or `aria-label` |
| Missing `aria-hidden="true"` on decorative SVG | Screen reader announces SVG unnecessarily | Add to every decorative `<svg>` |
| Icon-only button without `aria-label` | Screen reader reads nothing | `aria-label` on `<button>` |
| `font-size` used to size SVG | SVG is not text — font-size has no effect | Set `width/height` in CSS |
| `color: rgba(255,255,255,.45)` directly in CSS | Raw rgba — bypasses token | Use `color: var(--icon-color-default)` |
| `transition: color .15s` | Raw timing — bypasses token | `transition: color var(--dur-fast)` |
| `backdrop-filter` on TV icon wrappers | Performance — GPU-heavy on large canvas | Remove in TV `@media` block |
| `border-radius: 50%` on non-circular wrappers | Only for truly circular shapes | Use `var(--r*)` for pill/rounded wrappers |
| Icon added without manifest entry | Ungoverned — can't be found or audited | Add to `icons/icons-manifest.json` first |

---

# 12. Icon QA Checklist

| Check | Required |
|---|---|
| All icons from `icons/svg/` (Jio solid library) — no Lucide, no external icon sets | Yes |
| SVG root has no hardcoded `width` / `height` | Yes |
| All path/shape elements use `fill="currentColor"` — no hardcoded hex, black, or white | Yes |
| No `stroke` rules on solid icon paths — no `stroke-width`, `stroke-linecap`, `stroke-linejoin` in CSS | Yes |
| No `.icon-outline` CSS class present | Yes |
| `color` set on parent element in CSS — never `fill`/`stroke` directly on SVG in component CSS | Yes |
| Icon colour uses semantic token — no raw hex or rgba | Yes |
| State transition uses `var(--dur-fast)` — no raw timing | Yes |
| Icon size uses `var(--icon-size-*)` token | Yes |
| Wrapper radius uses `var(--r*)` token | Yes |
| Wrapper background uses colour token | Yes |
| Only one active icon per surface — supporting icons use `var(--icon-color-default)` or `var(--icon-color-muted)` | Yes |
| Action icons paired with label or `aria-label` — not icon alone | Yes |
| Decorative icons have `aria-hidden="true"` and `focusable="false"` | Yes |
| Icon-only buttons have `aria-label` on `<button>` | Yes |
| Status, error, loading icons paired with visible text | Yes |
| Loading spinner has `prefers-reduced-motion` fallback | Yes |
| New icon exists in `icons/svg/` before use in component | Yes |
| New icon has entry in `icons/icons-manifest.json` | Yes |
| Filename follows `ic_[category]_[object]_[variant].svg` pattern (new icons only) | Yes |
| Flagged filename uses manifest alias until formal rename | If using audited icon |
| TV: no `backdrop-filter` on wrappers | If TV in scope |
| TV: icon sizes use `var(--icon-size-xl)` or `var(--icon-size-lg)` | If TV in scope |
| TV: focusable icon buttons have `tabindex="0"` and `aria-label` | If TV in scope |
