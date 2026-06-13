# JioGames DLS — Templates

Templates are **starter files** for building new screens and components. They are not finished screens — they provide the structural scaffold and token wiring so you start from a correct baseline rather than blank HTML.

---

## Available templates

### `base-mobile-screen/`
Phone frame at 393×852px. Use this for all mobile prototype screens (login, home, game detail, pass flows).

- `index.html` — frame + screen wrapper + status bar spacer + zone markers
- `styles.css` — layout rules for `.phone-frame`, `.screen`, `.status-bar`, `.screen-content`

**How to use:** Duplicate the folder, rename it, then fill in the HERO, RAILS, and BOTTOM SHEET zones. AppBar goes between the status bar spacer and the hero zone.

---

### `base-web-screen/`
Full-width web layout with a max-width container (1280px). Use for web platform screens.

- `index.html` — skip link + `.page` + `.container` + `.page-content`
- `styles.css` — layout rules including `.skip-to-main` accessibility link

**How to use:** Duplicate the folder, rename it, add an AppBar above `.container`, then populate `.page-content`.

---

### `base-tv-screen/`
1920×1080px TV frame with safe-area inset. Use for the TV/CTV platform.

- `index.html` — `.tv-frame` + `.tv-safe` + sidebar nav placeholder + `.tv-content`
- `styles.css` — layout rules + mandatory `.focusable` focus-ring pattern

**How to use:** Duplicate the folder, rename it. Add sidebar nav in `.tv-safe` before `.tv-content`. Every interactive element **must** carry `class="focusable"` to get the required focus ring. TV is D-pad only — no hover states, no touch sheets, no bottom nav.

---

### `components/`
Standalone CSS files for individual components. Import the one(s) you need after `tokens.css`.

| File | What it covers |
|---|---|
| `appbar.css` | `.appbar` (home/scrolled/hidden), `.appbar--detail`, `.appbar--inner`, `.icon-btn`, `.mp-badge`, notification dot |
| `button.css` | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-sm` |
| `card.css` | `.card`, `.card--landscape`, `.card--portrait`, `.card--square`, `.card__art`, `.card__meta`, `.card__title` |
| `rail.css` | `.rail`, `.rail__header`, `.rail__track`, `.rail__item` |

**How to use:** Copy the relevant file into your screen folder and link it after `tokens.css`. Adjust layout widths (e.g. card sizes) by assigning values to the token variables — never override with raw values.

---

## What must NOT be changed

1. **`../../tokens/tokens.css` import** — the relative path `../../tokens/tokens.css` is load-bearing. All `var(--token)` references resolve through this file. Do not inline token values, do not copy-paste hex colours, do not substitute raw `px` values.

2. **JioType fonts** — the `@font-face` declarations in each `index.html` load from `/Assets/font/JioType-{Light|Medium|Bold|Black}.ttf`. Do not swap in Inter, Outfit, or any other font. If the font path must change, update the `@font-face` src — do not change `font-family:'JioType'`.

3. **Dark background** — all templates use `var(--bg)` and `var(--bg2)`. There are no white or light backgrounds in the JioGames DLS.

---

## See also

- [SKILL.md](../SKILL.md) — full DLS skill reference, design principles, and platform rules
- `references/appbar.md` — AppBar variants with measurements
- `tokens/tokens.css` — full token definitions (read only)
