# JioGames AppBar — Component Spec

**File:** `jiogames-header.html`

---

## Variants

| Variant | Class | Use case |
|---|---|---|
| Home — transparent | `.appbar` | Over hero image, page top |
| Home — scrolled | `.appbar.header-scrolled` | After scroll past 80px |
| Home — hidden | `.appbar.header-hidden` | Scrolling down past threshold |
| Game detail | `.appbar.appbar--detail` | Over game hero, back button only |
| Inner page | `.appbar.appbar--inner` | Notifications, profile, etc. |

---

## Scroll Behaviour

- **Scroll down** past 80px → header hides (`translateY(-110%)`)
- **Scroll up** → header reveals immediately
- **Back near top** (<80px) → glass drops, returns to transparent
- Jitter guard: ignores movements `< 8px`

---

## Anatomy

### Home
```
[ JioGames logo ] [ PASS badge? ]  ·····spacer·····  [ Search ] [ Bell ]
```

### Game detail
```
[ ← Back ]
```
Back button has frosted glass: `rgba(0,0,0,.45)` + `blur(8px)`.  
Container fully transparent (overlays hero image).

### Inner page
```
[ ← Back ]  [ Page title ]  ·····flex-1·····  [ ⋮ Kebab ]
```
Solid `var(--bg)` background + 1px bottom border.

---

## Tokens & Spec

| Property | Token | Value |
|---|---|---|
| Container padding | — | `8px` top · `--gutter` sides · `14px` bottom |
| Logo height | — | `26px`, width auto, never distort |
| Icon button size | `--icon-wrapper-sm` | `40×40px` |
| Icon button radius | — | `50%` circular |
| Icon button bg | `--hairline` | `rgba(255,255,255,.04)` + 1px border |
| Icon SVG size | `--icon-size-xs` | `14px` · `fill: currentColor` |
| Notification dot | `--jio` `--bg` | `7×7px` · top 8 right 8 · ring `0 0 0 2px var(--bg)` |
| Scrolled bg | — | `rgba(0,0,0,.7)` + `blur(14px)` |
| Hide threshold | — | `scrollTop > 80px` + scrolling down |
| Delta guard | — | `8px` jitter filter |
| Transition | `--dur-default` `--spring` | `200ms cubic-bezier(.22,1,.36,1)` |
| Hide transform | — | `translateY(-110%)` |
| z-index | — | `40` |
| Active press | `--dur-fast` | `scale(.95)` · bg `rgba(255,255,255,.08)` |

---

## Icons (DLS library)

All icons from `/jiogames-dls/icons/svg/`. 24×24 viewBox, solid fill paths, no stroke.

| Icon | File | Used in |
|---|---|---|
| Search | `ic_search.svg` | Home |
| Notification | `ic_notification.svg` | Home |
| Back / chevron left | `ic_chevron_left.svg` | Game detail, Inner page |
| Kebab / more | `ic_more_vertical.svg` | Inner page |

**Icon colour pattern:**
```css
.icon-btn          { color: var(--text); }
.icon-btn svg      { fill: currentColor; }
```
Never use `fill="<hex>"` or `stroke` on DLS icons.

---

## States: Notification dot

Add `.has-notification` to `.icon-btn` (bell button) to show green dot.

```html
<button class="icon-btn has-notification" aria-label="Notifications, new">
  ...
  <span class="dot"></span>
</button>
```

Dot: `7×7px`, `background: var(--jio)`, ring `0 0 0 2px var(--bg)`, positioned `top: 8px; right: 8px`.

---

## States: PASS badge

```html
<span class="mp-badge">PASS</span>
```

Placed immediately after logo. Hide by setting `display: none`.
