# JioGames Logo Governance

> **Inherits `_core-rules.md`** — dark-only, JioType-only, token-first, no Lucide, no silent deviation rules are not repeated here.


> Logos are not icons. Never apply `currentColor`, never override colours via CSS, never use as a mask or background. The logo is a fixed brand asset — only the approved files in `logos/` may be used.

**Structure**

1. Available Logo Files
2. When to Use Each Variant
3. Implementation Rules
4. Clear Space
5. Minimum Size
6. Approved Backgrounds
7. Forbidden Treatments
8. Logo QA Checklist

---

# 1. Available Logo Files

```
logos/
  JioGames_ServiceLogo_Horizontal_White.svg   ← default for JioGames dark UI
  JioGames_ServiceLogo_Horizontal_Black.svg   ← for light surfaces or co-brand contexts
```

| File | Wordmark colour | Dot | When to use |
|---|---|---|---|
| `…Horizontal_White.svg` | White (`#fff`) | Jio green (`#00a859`) | **Default** — JioGames dark UI, dark backgrounds, hero surfaces |
| `…Horizontal_Black.svg` | Black | Jio green (`#00a859`) | Light backgrounds, external co-brand contexts, print |

JioGames is a dark-only product. **White variant is the default** in all in-product use.

---

# 2. When to Use Each Variant

| Surface | Variant |
|---|---|
| App bar / nav header | White |
| Login / splash screen | White |
| Hero / cinematic overlay | White |
| Pass card (on dark bg) | White |
| Email header (dark) | White |
| Email header (light) | Black |
| External landing page (light) | Black |
| Co-branded partner material | Black (unless dark background) |
| Print on white | Black |

Rule: choose based on background lightness. Dark bg → White. Light bg → Black. Never place White logo on a white background or Black logo on a dark background.

---

# 3. Implementation Rules

### Use the SVG file directly

```html
<!-- In-product — white variant on dark bg -->
<img
  src="logos/JioGames_ServiceLogo_Horizontal_White.svg"
  alt="JioGames"
  class="app-logo"
/>
```

```css
.app-logo {
  width: var(--logo-width-default);   /* see Approved Logo Sizes below */
  height: auto;                        /* preserve aspect ratio — never distort */
}
```

### Approved logo display sizes

Logo dimensions are brand asset constants — not spacing tokens. These approved widths correspond to platform minimum sizes and common usage contexts.

| CSS variable | Value | Context |
|---|---:|---|
| `--logo-width-xs` | 80px | Mobile in-app minimum |
| `--logo-width-default` | 100px | Web header default |
| `--logo-width-lg` | 120px | Splash / login screen |
| `--logo-width-tv` | 140px | TV safe-zone minimum |

Add to your screen's CSS — these are not in `tokens.css` (logo sizes are brand asset constants, not layout tokens):

```css
:root {
  --logo-width-xs:      80px;
  --logo-width-default: 100px;
  --logo-width-lg:      120px;
  --logo-width-tv:      140px;
}
```

Never use raw `px` widths for logos in component CSS — always reference these variables.

### Never override logo colours

```css
/* ✗ Wrong — destroys brand colours */
.app-logo path { fill: currentColor; }
.app-logo path { fill: var(--jio); }
.app-logo { filter: invert(1); }
.app-logo { color: white; }

/* ✓ Correct — use the SVG as-is */
/* No CSS colour overrides on logo elements */
```

### Inline SVG — only when technically required

If you must inline (e.g. for animation or print fallback), do not modify any `fill` or `class` attributes. Paste the exact file contents. Do not normalise to `currentColor` — logos are intentionally multi-colour.

### Dark-only product note

JioGames has no light mode. The White variant is therefore used in all in-product screens. The Black variant is reserved for external use, co-branding, and print. Do not switch variants based on component state or theme.

---

# 4. Clear Space

Maintain minimum clear space around the logo on all sides equal to the height of the Jio dot (the green circle in the logo).

```
┌─────────────────────────────────┐
│    [1× dot height clearance]    │
│                                 │
│   [dot] J i o G a m e s        │
│                                 │
│    [1× dot height clearance]    │
└─────────────────────────────────┘
```

The dot height = 32px at the file's native `viewBox="0 0 93.12 32"` — so the dot height = 32 CSS units. Scale clear space proportionally.

No text, icons, UI elements, or decorative elements may enter the clear space zone.

---

# 5. Minimum Size

| Platform | Min width |
|---|---|
| Mobile (in-app) | 80px |
| Web (header) | 100px |
| TV (safe zone) | 140px |
| Favicon / small mark | Do not use horizontal logo — use Jio dot mark only |

At sizes below minimum, the wordmark becomes illegible. Use the Jio dot mark (circular symbol) standalone instead of scaling the full lockup down.

---

# 6. Approved Backgrounds

| Background | White variant | Black variant |
|---|:---:|:---:|
| `var(--bg)` `#06080F` | ✓ | ✗ |
| `var(--card-bg)` `#111115` | ✓ | ✗ |
| `var(--jio)` green | ✓ | ✗ |
| Photography / hero image with overlay | ✓ | ✗ |
| White `#fff` | ✗ | ✓ |
| Light grey | ✗ | ✓ |
| Busy/patterned background | ✗ (both) | ✗ (both) |

Do not place either variant on a busy or patterned background without a solid backing panel that provides sufficient contrast.

---

# 7. Forbidden Treatments

| Treatment | Why forbidden |
|---|---|
| Stretching or squashing | Destroys proportions — always `height: auto` |
| Rotation or flip | Brand asset must always appear horizontal |
| Colour override via CSS (`fill`, `currentColor`, `filter`) | Logo colours are fixed brand assets |
| Adding drop shadow | Creates visual clutter — logo must be clean |
| Adding glow or outline | Same reason |
| Cropping the dot off | Dot + wordmark is the full lockup — never partial |
| Replacing Jio green with a different colour | Dot is always `#00a859` |
| Opacity below 100% | Never dim the logo |
| Placing on a gradient that reduces contrast | Must meet clear legibility |
| Using as a button or interactive element | Logo is identity, not a control |
| Animating logo paths | No motion on brand assets |
| Inverting via `filter: invert()` | Use the correct variant instead |

---

# 8. Logo QA Checklist

| Check | Required |
|---|---|
| Logo file used is from `logos/` — no recreated or third-party versions | Yes |
| White variant on dark backgrounds, Black variant on light | Yes |
| No CSS `fill`, `stroke`, or `color` overrides on logo elements | Yes |
| No `filter` applied to logo | Yes |
| `height: auto` — aspect ratio preserved | Yes |
| Width at or above minimum for platform | Yes |
| Clear space maintained — no UI elements in clearance zone | Yes |
| Logo not used as a button, link anchor, or interactive control | Yes |
| Logo not animated | Yes |
| Logo not placed on a busy or low-contrast background | Yes |
