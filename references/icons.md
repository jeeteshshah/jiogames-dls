# JioGames Icon Governance

> Use the official Jio icon library. Do not substitute Lucide, Material, or any third-party icon set. Raw px sizes in icon CSS use approved icon-size constants (§3) — not spacing tokens.

**Structure**

1. Icon Library Source
2. Naming Convention
3. Sizing
4. Style Spec
5. Colour Rules
6. JioGames Icon Set (required icons by surface)
7. Icon Wrappers
8. Accessibility
9. Platform Rules
10. Forbidden Patterns
11. Icon QA Checklist

---

# 1. Icon Library Source

JioGames uses the **official Jio Core Icons** library from the Jio Token Design System.

| Library | Figma file | Node | Use |
|---|---|---|---|
| **Core** | `9IRfFnQ90DAQDhgK7DCdEm` | `9185:136168` | Common, frequently used icons — use first |
| **Extended** | `9IRfFnQ90DAQDhgK7DCdEm` | `11:5` | 1,500+ specialised icons — use when Core doesn't cover the need |

All icons are SVG symbols, 24×24px base grid, outline stroke style. They follow the same visual language — do not mix with other icon sets.

**Do not use Lucide, Material Icons, Heroicons, or any external icon library.** If a needed icon doesn't exist in Core or Extended, request it through the Jio icon contribution process (documented in the Figma file under `_info/Icons-Contribution-Intro`).

### Getting icons into your project

41 JioGames core icons are pre-mapped and ready to export. Run once after install:

```bash
pip install requests
python3 tools/export-icons.py --token YOUR_FIGMA_TOKEN
```

Get token: **figma.com/settings → Personal access tokens → Generate new token**

This exports all icons to `icons/svg/` and generates `icons/sprite.svg`. Use in HTML:

```html
<svg width="24" height="24" aria-hidden="true">
  <use href="icons/sprite.svg#ic_play_circle"/>
</svg>
```

To add more icons: `python3 tools/export-icons.py --token TOKEN --extra ic_name:NODE_ID`

---

# 2. Naming Convention

All icons follow this pattern:

```
ic_{category}_{descriptor}
```

Examples:
- `ic_gaming_controllers` — gaming category, controllers variant
- `ic_play_circle` — play category, circle variant
- `ic_go_back_10` — back-seek 10s
- `ic_bookmark_add` — bookmark with add action

Use the exact name as the SVG symbol ID / filename. The name is the canonical reference — do not rename icons.

---

# 3. Sizing

Base grid is 24×24px. Scale by context — always whole numbers.

### Approved icon sizes (use these exact values)

| Context | Size | CSS |
|---|---|---|
| Inline with body text | 16px | `width: 16px; height: 16px` |
| Input prefix / field icon | 18px | `width: 18px; height: 18px` |
| Standard UI icon | 24px | `width: 24px; height: 24px` ← base |
| Platform chip icon | 22px | `width: 22px; height: 22px` |
| Action icon button | 24px | `width: 24px; height: 24px` |
| Card meta icon | 14px | `width: 14px; height: 14px` |
| Perk check mark | 16px | `width: 16px; height: 16px` |
| Small badge / dot | 9px | `width: 9px; height: 9px` |

These are approved icon-size constants. They do not map to spacing tokens — icon optical sizes are independent of the 8px layout scale.

### TV sizes (always larger — users sit far away)

| Context | Mobile | TV |
|---|---|---|
| Nav bar icon | 24px | 40px |
| Card meta icon | 14px | 28px |
| Focusable control icon | 24px | 36px |
| Action button icon | 24px | 40px |

---

# 4. Style Spec

All icons: outline stroke, round caps, round joins, `currentColor`.

```css
svg.icon {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex-shrink: 0;           /* never let icon compress in flex containers */
}

/* Emphasis variant — check marks, active arrows, success states */
svg.icon-emphasis {
  fill: none;
  stroke: var(--jio);
  stroke-width: 2.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  flex-shrink: 0;
}

/* Filled variant — for solid states (heart liked, bookmark saved) */
svg.icon-filled {
  fill: currentColor;
  stroke: none;
}
```

**Stroke widths:**
- `1.8` — all standard icons
- `2.5` — emphasis: check marks, primary action arrows, success icons

Never mix stroke widths on icons at the same hierarchy level.

---

# 5. Colour Rules

Icons inherit `currentColor` by default — set colour on the parent element, not the SVG directly.

| State | Token | Notes |
|---|---|---|
| Default (on dark bg) | `rgba(255,255,255,.45)` | Semi-transparent — icons are supporting, not primary |
| Active / selected | `var(--jio)` | Full brand green |
| Muted / disabled | `var(--text3)` | Decorative context only |
| On green surface | `var(--text-inv)` | Never raw `#000` |
| Check / success | `var(--jio)` | Use `icon-emphasis` class |
| Error state | `var(--negative)` | Paired with error text |
| Ultimate Pass context | `var(--ultimate)` | Replaces `--jio` for Ultimate surfaces |

```css
/* Transition stroke colour on state change */
.platform-chip svg {
  stroke: rgba(255,255,255,.45);
  transition: stroke var(--dur-fast);   /* not raw .15s */
}
.platform-chip.selected svg { stroke: var(--jio); }

/* Tab bar icons */
.tab svg  { stroke: var(--text3); }
.tab.active svg { stroke: var(--jio); }
```

---

# 6. JioGames Icon Set

Required icons by surface. All from the Jio icon library.

### Navigation & Shell

| Icon name | Use |
|---|---|
| `ic_go_back` | Back navigation |
| `ic_os_nav_home` | Home |
| `ic_local_search` | Search |
| `ic_notification` | Notifications (Core) |
| `ic_profile_male` / `ic_profile_female` | User avatar fallback |
| `ic_menu_card` | Hamburger / more |

### Game Rail & Cards

| Icon name | Use |
|---|---|
| `ic_play_circle` | Primary play action |
| `ic_play_pause` | Inline play/pause |
| `ic_go_forward_10` | Skip forward 10s |
| `ic_go_back_10` | Skip back 10s |
| `ic_bookmark_add` | Save to library |
| `ic_star_add` | Add to favourites |
| `ic_media_share` | Share game |
| `ic_download_fast` | Download |
| `ic_resume_watching` | Continue card indicator |

### Game Detail

| Icon name | Use |
|---|---|
| `ic_gaming_controllers` | Platform — controller |
| `ic_gaming_cloud` | Cloud gaming |
| `ic_gaming_profile` | Player profile |
| `ic_tv_play` | Play on TV |
| `ic_mobile_data` | Mobile play |
| `ic_laptop_screen` | PC play |
| `ic_racing_car` | Racing category |
| `ic_fantasy_games` | Fantasy category |
| `ic_sci_fiction` | Sci-fi category |

### Pass & Subscription

| Icon name | Use |
|---|---|
| `ic_status_successful` | Pass activated / success |
| `ic_status_fail` | Error state |
| `ic_status_loading` | Loading / processing |
| `ic_payment_plan` | Plan card |
| `ic_premium_number` | Premium badge |

### TV

| Icon name | Use |
|---|---|
| `ic_tv_channels` | Browse channels |
| `ic_tv_play` | Play on TV |
| `ic_remote_universal` | Remote control |
| `ic_cast_screen` | Cast |
| `ic_screen_full` | Fullscreen |

---

# 7. Icon Wrappers

Use these exact wrapper patterns — radius and sizing use approved values.

### Circular wrapper (action dots, sim icon)

```css
.icon-circle {
  width: 26px; height: 26px;      /* approved icon-size constant — see §3 */
  border-radius: 50%;             /* circles only — never on card/tile */
  background: var(--jio);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Rounded-square wrapper (feature icons)

```css
.icon-sq {
  width: var(--space-5); height: var(--space-5);  /* 40px = --space-5 */
  border-radius: var(--r3);                        /* 12px — compact container */
  background: var(--jio-soft);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
```

### Glassy genre-tile icon

```css
.gt-icon {
  width: 26px; height: 26px;     /* approved icon constant */
  border-radius: var(--r2);      /* 10px — small container */
  background: rgba(0,0,0,.5);
  backdrop-filter: blur(6px);
  border: 1px solid var(--border-subtle);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.genre-tile.selected .gt-icon {
  background: var(--jio-soft);
  border-color: rgba(0,168,89,.45);
}
.genre-tile.selected .gt-icon svg { stroke: var(--jio-bright); }
```

### Icon + text pairing

```css
.icon-label {
  display: flex;
  align-items: center;
  gap: var(--space-0-5);   /* 4px — tight icon↔label */
}
/* Prevent icon from scaling with text zoom */
.icon-label svg { flex-shrink: 0; }
```

---

# 8. Accessibility

| Icon type | Requirement |
|---|---|
| Decorative (in card, rail, alongside text) | `aria-hidden="true"` on `<svg>` |
| Action button (icon only, no visible label) | `aria-label="Play"` on `<button>` |
| Status / check mark | `role="img" aria-label="Included"` on `<svg>` |
| TV focusable icon button | `tabindex="0"`, `role="button"`, `aria-label` |

Minimum tap target:
- Mobile: `min-width/height: var(--touch-min)` (44px) — icon can be 24px visually, pad to 44px
- TV: `min-width/height: var(--touch-min)` (60px)

```css
/* Icon button — 24px visual, 44px tap target */
.icon-btn {
  min-width: var(--touch-min);
  min-height: var(--touch-min);
  display: flex; align-items: center; justify-content: center;
  background: none; border: none; cursor: pointer;
}
```

---

# 9. Platform Rules

### Mobile

- All icons from Jio icon library, 24px base
- Tap target: `min-width/height: var(--touch-min)` (44px)
- `backdrop-filter` on glassy wrappers is fine

### Web

- Same as mobile
- Hover state: `stroke: var(--jio)` transition on interactive icons
- Pointer target minimum: 32px (no `--touch-min` token needed — pointer is precise)

### TV

- Scale up: use TV sizes from §3 (40px nav, 28px meta, 36px focusable)
- No `backdrop-filter` on icon wrappers — remove `.gt-icon` blur on TV
- Focus ring on icon buttons: `box-shadow: 0 0 0 3px var(--jio), 0 0 24px rgba(0,200,100,.4)`
- All icon buttons must be focusable: `tabindex="0"`

```css
@media (min-width: 1280px) and (min-height: 720px) {
  .gt-icon { backdrop-filter: none; }
  .nav-icon svg { width: 40px; height: 40px; }
  .icon-btn { min-width: var(--touch-min); min-height: var(--touch-min); } /* 60px on TV */
}
```

---

# 10. Forbidden Patterns

| Pattern | Fix |
|---|---|
| Lucide, Material, Heroicons, or any external icon set | Use Jio icon library |
| `stroke: #000` on green surface | `stroke: var(--text-inv)` |
| `stroke: #6B7280` | `stroke: var(--text3)` |
| `transition: stroke .15s` | `transition: stroke var(--dur-fast)` |
| `border-radius: 9px` or `7px` on wrappers | Use `var(--r2)` (10px) or `var(--r3)` (12px) |
| `gap: 5px` icon+text | `gap: var(--space-0-5)` (4px) |
| `fill: none; stroke: var(--jio-bright)` on standard icon | `--jio-bright` is for glow/gradient, not strokes — use `var(--jio)` |
| Icon without `flex-shrink: 0` in flex container | Add `flex-shrink: 0` |
| Icon-only button without `aria-label` | Always add `aria-label` |
| `background: rgba(0,168,89,.18)` on wrapper | `background: var(--jio-soft)` |

---

# 11. Icon QA Checklist

| Check | Required |
|---|---|
| All icons from Jio Core or Extended library — no external sets | Yes |
| Icon names match official `ic_category_descriptor` convention | Yes |
| Stroke width 1.8 (standard) or 2.5 (emphasis) — no other values | Yes |
| `stroke: currentColor` in base style — colour set on parent | Yes |
| Active/selected icons use `var(--jio)` stroke | Yes |
| On-green icons use `stroke: var(--text-inv)` | Yes |
| State transitions use `var(--dur-fast)` — not raw `.15s` | Yes |
| Icon wrapper radius uses `var(--r*)` token — no raw px | Yes |
| Decorative icons have `aria-hidden="true"` | Yes |
| Icon-only buttons have `aria-label` | Yes |
| All icon buttons meet `var(--touch-min)` tap target | Yes |
| TV: no `backdrop-filter` on icon wrappers | If TV in scope |
| TV: icon sizes scaled to TV sizes from §3 | If TV in scope |
| TV: all icon buttons focusable with `tabindex="0"` | If TV in scope |
