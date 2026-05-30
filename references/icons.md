# JioGames Icons Guide

Icons in JioGames are functional, SVG-based, outline stroke style.

---

## 1. Style

| Property | Value |
|---|---|
| Style | Outline (stroke) |
| Stroke width | `1.8` (standard), `2.5` (emphasis / check icons) |
| Stroke cap | `round` |
| Stroke join | `round` |
| Fill | `none` (outline) or solid for filled variants |
| Colour | `currentColor` by default |

```css
/* Standard icon */
svg.icon {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Emphasis icon (check marks, arrows in active states) */
svg.icon-emphasis {
  fill: none;
  stroke: var(--jio);
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

---

## 2. Sizing

| Context | Size |
|---|---|
| Inline with body (14px) | 16px |
| Input prefix / sim icon | 17px |
| Platform chip | 22px |
| Action arrow in chip | 13px |
| Genre tile info icon | 14px |
| OTP cursor block | 2×24px (not icon) |
| Perk check | 16px |
| Small badge dot | 9px |

TV — double mobile sizes:
| Context | Size |
|---|---|
| Nav bar | 40px |
| Card meta | 28px |
| Focusable controls | 36px |

---

## 3. Colour Rules

| State | Stroke Colour |
|---|---|
| Default | `rgba(255,255,255,.45)` |
| Active / selected | `var(--jio)` |
| Muted / disabled | `var(--text3)` = `#6B7280` |
| On green surface | `#000` |
| Check/success | `var(--jio)` = `#00A859` |
| Arrow in sim chip | `#000` (on green circle bg) |

```css
/* Transition stroke colour on state change */
.platform-chip svg {
  stroke: rgba(255,255,255,.45);
  transition: stroke .15s;
}
.platform-chip.selected svg { stroke: var(--jio); }
```

---

## 4. Icon Wrappers

### Circular icon wrapper (sim icon, action dots)

```css
.icon-circle {
  width: 26px; height: 26px;
  border-radius: 50%;
  background: var(--jio);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Rounded-square icon wrapper (sim card icon)

```css
.icon-sq {
  width: 34px; height: 34px;
  border-radius: 9px;
  background: rgba(0,168,89,.18);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Genre tile icon (glassy)

```css
.gt-icon {
  width: 26px; height: 26px;
  border-radius: 7px;
  background: rgba(0,0,0,.5);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,.13);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.genre-tile.selected .gt-icon {
  background: rgba(0,168,89,.28);
  border-color: rgba(0,168,89,.45);
}
.genre-tile.selected .gt-icon svg { stroke: var(--jio-bright); }
```

---

## 5. Icon + Text Pairing

```css
/* Ensure vertical alignment */
.icon-label {
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Icon should never overpower the text */
.promo-pill svg { flex-shrink: 0; }
.gff-label svg { width: 9px; height: 9px; flex-shrink: 0; }
```

---

## 6. Accessibility

| Icon Type | Requirement |
|---|---|
| Decorative (in card, rail) | `aria-hidden="true"` |
| Action button (icon only) | `aria-label` on the `<button>` |
| Status / check mark | `role="img" aria-label="included"` |
| TV focusable icon button | `tabindex="0"`, `role="button"`, `aria-label` |

Minimum tap target (mobile): 44×44px  
Minimum focus target (TV): 60×60px

---

## 7. Recommended Library

For any icons beyond what's custom-drawn in the prototype, use **Lucide** (outline, SVG, 24×24 base). Matches the stroke style of existing JioGames icons.

```html
<!-- Lucide via CDN (prototyping only) -->
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

Adjust stroke-width to `1.8` to match JioGames style.

---

## Pre-Ship Checklist

- [ ] All icons: `stroke-linecap: round; stroke-linejoin: round`
- [ ] Decorative icons: `aria-hidden="true"`
- [ ] Icon-only buttons: `aria-label` present
- [ ] Active state icons switch stroke to `var(--jio)`
- [ ] No mixed icon styles (outline + solid in same context)
- [ ] TV icons at least 2× mobile size
