#!/usr/bin/env python3
"""
JioGames DLS — Icon Exporter
Exports SVG icons from the official Jio icon library via Figma API.
Saves to icons/svg/ and generates icons/sprite.svg.

Usage:
  python3 tools/export-icons.py --token YOUR_FIGMA_TOKEN
  python3 tools/export-icons.py --token YOUR_FIGMA_TOKEN --extra ic_my_icon:NODE_ID

Get token: figma.com/settings → Personal access tokens → Generate new token

Requirements: pip install requests
"""

import os, sys, json, time, argparse, re
from pathlib import Path
from typing import Optional, Dict

try:
    import requests
except ImportError:
    print("✗ Missing: pip install requests")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────
FILE_KEY   = "9IRfFnQ90DAQDhgK7DCdEm"   # Jio Core Tokens file
HERE       = Path(__file__).parent
ROOT       = HERE.parent
ICONS_DIR  = ROOT / "icons" / "svg"
SPRITE_OUT = ROOT / "icons" / "sprite.svg"

# JioGames core icon set — name → node ID (Extended library)
JIOGAMES_ICONS = {
    # Navigation & shell
    "ic_go_back":              "4931:103394",
    "ic_os_nav_home":          "39008:2668",
    "ic_local_search":         "33136:144052",
    # Game rail & cards
    "ic_play_circle":          "4931:103217",
    "ic_play_pause":           "4931:103216",
    "ic_pause_circle":         "4931:103219",
    "ic_go_forward_10":        "4931:103323",
    "ic_go_back_10":           "4931:103225",
    "ic_go_forward_30":        "4931:103324",
    "ic_go_back_30":           "4931:103226",
    "ic_bookmark_add":         "7386:127790",
    "ic_star_add":             "7386:127831",
    "ic_media_share":          "9812:129827",
    "ic_download_fast":        "9812:129833",
    "ic_resume_watching":      "7386:127819",
    # Game detail & platform
    "ic_gaming_controllers":   "8453:127782",
    "ic_gaming_cloud":         "11926:133106",
    "ic_gaming_profile":       "11926:133108",
    "ic_tv_play":              "8453:127716",
    "ic_tv_channels":          "7386:127797",
    "ic_mobile_data":          "4919:101368",
    "ic_laptop_screen":        "10496:116957",
    # Genre categories
    "ic_racing_car":           "11926:132569",
    "ic_fantasy_games":        "38985:2634",
    "ic_sci_fiction":          "11926:132579",
    # Pass & subscription
    "ic_status_successful":    "8484:127716",
    "ic_status_fail":          "8484:127717",
    "ic_status_loading":       "8484:127715",
    "ic_payment_plan":         "9429:129584",
    "ic_premium_number":       "34733:144286",
    # TV & casting
    "ic_cast_screen":          "7386:127803",
    "ic_screen_full":          "4931:103392",
    "ic_remote_universal":     "10496:116936",
    # UI utilities
    "ic_sort_handle":          "7386:127817",
    "ic_drag_handle":          "57975:2516",
    "ic_arrow_down":           "8453:127602",
    "ic_arrow_up":             "8453:127601",
    "ic_chevron_right_circle": "8453:127607",
    "ic_chevron_left_circle":  "8453:127608",
    "ic_smiley_delighted":     "4932:100872",
    "ic_smiley_neutral":       "4932:100876",
}


def export_svgs(token: str, icons: Dict[str, str]) -> Dict[str, str]:
    """Call Figma images API, return name → svg_url dict."""
    headers = {"X-Figma-Token": token}
    ids     = ",".join(v.replace(":", "-") for v in icons.values())

    print(f"Requesting {len(icons)} icon URLs from Figma API…")
    r = requests.get(
        f"https://api.figma.com/v1/images/{FILE_KEY}",
        headers=headers,
        params={"ids": ids, "format": "svg", "scale": 1},
        timeout=30,
    )
    if r.status_code == 403:
        print("✗ 403 Forbidden — check your Figma token has read access")
        sys.exit(1)
    r.raise_for_status()
    data = r.json()

    # Map node_id → url (API returns colon format as keys)
    id_to_url = data.get("images", {})

    # Build name → url — try both colon and hyphen formats
    result = {}
    for name, node_id in icons.items():
        url = id_to_url.get(node_id) or id_to_url.get(node_id.replace(":", "-"))
        if url:
            result[name] = url
        else:
            print(f"  ⚠ No URL for {name} ({node_id})")
    return result


def download_svg(name: str, url: str, dest: Path) -> Optional[str]:
    """Download one SVG, clean it, return cleaned content."""
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        svg = r.text

        # Clean Figma export artefacts
        # Remove XML declaration if present
        svg = re.sub(r'<\?xml[^>]+\?>', '', svg).strip()
        # Ensure viewBox="0 0 24 24" and consistent size attrs
        svg = re.sub(r'width="[^"]*"', 'width="24"', svg)
        svg = re.sub(r'height="[^"]*"', 'height="24"', svg)
        # Replace hardcoded colours with currentColor on path/circle/rect/polygon elements
        # fill="none" on the <svg> root is correct — leave it; replace on child elements
        svg = re.sub(r'(<(?:path|circle|rect|polygon|polyline|ellipse|line)[^>]*)\sfill="#[0-9a-fA-F]{3,6}"', r'\1 fill="currentColor"', svg)
        svg = re.sub(r'(<(?:path|circle|rect|polygon|polyline|ellipse|line)[^>]*)\sstroke="#[0-9a-fA-F]{3,6}"', r'\1 stroke="currentColor"', svg)
        # Also handle fill="black" / fill="white" literals on child elements
        svg = re.sub(r'(<(?:path|circle|rect|polygon|polyline|ellipse|line)[^>]*)\sfill="(?:black|white)"', r'\1 fill="currentColor"', svg)

        out = dest / f"{name}.svg"
        out.write_text(svg, encoding="utf-8")
        return svg
    except Exception as e:
        print(f"  ✗ Failed {name}: {e}")
        return None


def build_sprite(icons_content: dict, out_path: Path):
    """Build an SVG sprite from individual icon SVG strings."""
    symbols = []
    for name, svg in icons_content.items():
        # Extract inner content of <svg>
        inner = re.sub(r'<svg[^>]*>', '', svg)
        inner = re.sub(r'</svg>', '', inner).strip()
        symbols.append(
            f'  <symbol id="{name}" viewBox="0 0 24 24" '
            f'xmlns="http://www.w3.org/2000/svg">\n'
            f'    {inner}\n'
            f'  </symbol>'
        )

    sprite = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- JioGames DLS — Icon Sprite\n'
        '     Generated by tools/export-icons.py. DO NOT EDIT.\n'
        '     Usage: <svg><use href="icons/sprite.svg#ic_play_circle"/></svg> -->\n'
        '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
        + '\n'.join(symbols)
        + '\n</svg>\n'
    )
    out_path.write_text(sprite, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Export JioGames icons from Figma")
    parser.add_argument("--token", required=True, help="Figma personal access token")
    parser.add_argument(
        "--extra", nargs="*", default=[],
        help="Extra icons to add: ic_name:NODE_ID (e.g. ic_wifi:1234:5678)"
    )
    args = parser.parse_args()

    # Merge extra icons
    icons = dict(JIOGAMES_ICONS)
    for extra in args.extra:
        if ":" not in extra:
            print(f"⚠ Skipping malformed extra icon: {extra} (expected ic_name:NODE_ID)")
            continue
        parts = extra.split(":", 1)
        icons[parts[0]] = parts[1]

    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: get download URLs
    url_map = export_svgs(args.token, icons)
    print(f"Got URLs for {len(url_map)}/{len(icons)} icons")

    # Step 2: download SVGs
    print(f"\nDownloading SVGs to {ICONS_DIR.relative_to(ROOT)}/")
    icons_content = {}
    for i, (name, url) in enumerate(url_map.items(), 1):
        print(f"  [{i}/{len(url_map)}] {name}", end="", flush=True)
        svg = download_svg(name, url, ICONS_DIR)
        if svg:
            icons_content[name] = svg
            print(" ✓")
        else:
            print(" ✗")
        # Polite rate limiting
        if i % 10 == 0:
            time.sleep(0.5)

    # Step 3: build sprite
    print(f"\nBuilding sprite → {SPRITE_OUT.relative_to(ROOT)}")
    build_sprite(icons_content, SPRITE_OUT)

    # Summary
    print(f"\n{'═'*44}")
    print(f"✓ {len(icons_content)} icons exported to icons/svg/")
    print(f"✓ Sprite: icons/sprite.svg")
    print(f"\nUsage in HTML:")
    print(f'  <!-- Load sprite once in <body> -->')
    print(f'  <div style="display:none">')
    print(f'    <!-- inject contents of icons/sprite.svg -->')
    print(f'  </div>')
    print(f'')
    print(f'  <!-- Use any icon -->')
    print(f'  <svg width="24" height="24" aria-hidden="true">')
    print(f'    <use href="icons/sprite.svg#ic_play_circle"/>')
    print(f'  </svg>')

    failed = len(icons) - len(icons_content)
    if failed:
        print(f"\n⚠ {failed} icon(s) failed — check node IDs in tools/export-icons.py")


if __name__ == "__main__":
    main()
