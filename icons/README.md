# JioGames DLS — Icons

SVG icons exported from the official Jio icon library.

## Setup (first time)

You need a Figma personal access token:
1. Go to figma.com/settings → Personal access tokens
2. Click **Generate new token** → copy it

Then run:

```bash
pip install requests
python3 tools/export-icons.py --token YOUR_TOKEN_HERE
```

This exports 41 JioGames core icons to `icons/svg/` and builds `icons/sprite.svg`.

## Adding more icons

Find the icon node ID from Figma (right-click → Copy link, extract `node-id`), then:

```bash
python3 tools/export-icons.py --token YOUR_TOKEN --extra ic_my_icon:NODE_ID
```

Or add it permanently to the `JIOGAMES_ICONS` dict in `tools/export-icons.py`.

## Using icons in HTML

```html
<!-- Option A: External sprite (recommended) -->
<svg width="24" height="24" aria-hidden="true">
  <use href="icons/sprite.svg#ic_play_circle"/>
</svg>

<!-- Option B: Inline individual SVG -->
<!-- Paste contents of icons/svg/ic_play_circle.svg directly -->
```

## Available icons

| Name | Category |
|---|---|
| `ic_go_back` | Navigation |
| `ic_os_nav_home` | Navigation |
| `ic_local_search` | Navigation |
| `ic_play_circle` | Media |
| `ic_play_pause` | Media |
| `ic_pause_circle` | Media |
| `ic_go_forward_10` | Media |
| `ic_go_back_10` | Media |
| `ic_go_forward_30` | Media |
| `ic_go_back_30` | Media |
| `ic_bookmark_add` | Actions |
| `ic_star_add` | Actions |
| `ic_media_share` | Actions |
| `ic_download_fast` | Actions |
| `ic_resume_watching` | Actions |
| `ic_gaming_controllers` | Gaming |
| `ic_gaming_cloud` | Gaming |
| `ic_gaming_profile` | Gaming |
| `ic_tv_play` | Platform |
| `ic_tv_channels` | Platform |
| `ic_mobile_data` | Platform |
| `ic_laptop_screen` | Platform |
| `ic_racing_car` | Genre |
| `ic_fantasy_games` | Genre |
| `ic_sci_fiction` | Genre |
| `ic_status_successful` | Status |
| `ic_status_fail` | Status |
| `ic_status_loading` | Status |
| `ic_payment_plan` | Pass |
| `ic_premium_number` | Pass |
| `ic_cast_screen` | TV |
| `ic_screen_full` | TV |
| `ic_remote_universal` | TV |
| `ic_sort_handle` | UI |
| `ic_drag_handle` | UI |
| `ic_arrow_down` | UI |
| `ic_arrow_up` | UI |
| `ic_chevron_right_circle` | UI |
| `ic_chevron_left_circle` | UI |
| `ic_smiley_delighted` | Feedback |
| `ic_smiley_neutral` | Feedback |
