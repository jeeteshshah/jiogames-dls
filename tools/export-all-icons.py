#!/usr/bin/env python3
"""
JioGames DLS — Bulk Icon Exporter
Exports ALL 1,648 icons from Jio Core + Extended libraries.
Saves individual SVGs to icons/svg/ and builds category sprite files.

Usage:
  python3 tools/export-all-icons.py --token YOUR_FIGMA_TOKEN

Get token: figma.com/settings → Personal access tokens → File content (read only)

Requirements: pip install requests
Estimated time: ~5-10 minutes (1,648 icons, batched API calls)
"""

import os, sys, re, json, time, argparse
from pathlib import Path
from typing import Optional, Dict
from collections import defaultdict

try:
    import requests
except ImportError:
    print("✗ Missing: pip install requests")
    sys.exit(1)

FILE_KEY   = "9IRfFnQ90DAQDhgK7DCdEm"
HERE       = Path(__file__).parent
ROOT       = HERE.parent
ICONS_DIR  = ROOT / "icons" / "svg"
SPRITE_DIR = ROOT / "icons" / "sprites"
INDEX_OUT  = ROOT / "icons" / "index.json"

BATCH_SIZE = 150   # Figma API limit per request


def load_icon_map() -> Dict[str, str]:
    """Load pre-extracted icon name → node ID map."""
    core_path = Path("/tmp/core_icons.json")
    ext_path  = Path("/tmp/extended_icons.json")

    if not core_path.exists() or not ext_path.exists():
        print("✗ Icon maps not found. Run this first in Claude session to regenerate them.")
        sys.exit(1)

    core = json.loads(core_path.read_text())
    ext  = json.loads(ext_path.read_text())
    merged = {**ext, **core}   # core overrides extended for duplicates
    return merged


def batch(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def fetch_urls(token: str, node_ids: list) -> Dict[str, str]:
    """Fetch SVG export URLs for a batch of node IDs."""
    headers = {"X-Figma-Token": token}
    ids_str = ",".join(n.replace(":", "-") for n in node_ids)
    r = requests.get(
        f"https://api.figma.com/v1/images/{FILE_KEY}",
        headers=headers,
        params={"ids": ids_str, "format": "svg", "scale": 1},
        timeout=60,
    )
    if r.status_code == 403:
        print("✗ 403 — token invalid or expired. Generate a new one.")
        sys.exit(1)
    if r.status_code == 429:
        print("  Rate limited — waiting 60s…")
        time.sleep(60)
        return fetch_urls(token, node_ids)  # retry
    r.raise_for_status()
    return r.json().get("images", {})


def clean_svg(svg: str) -> str:
    """Normalise SVG for use as a UI icon."""
    svg = re.sub(r'<\?xml[^>]+\?>', '', svg).strip()
    svg = re.sub(r'width="[^"]*"',  'width="24"',  svg)
    svg = re.sub(r'height="[^"]*"', 'height="24"', svg)
    # Replace hardcoded colours on path/shape elements with currentColor
    for tag in ['path', 'circle', 'rect', 'polygon', 'polyline', 'ellipse', 'line']:
        svg = re.sub(
            rf'(<{tag}[^>]*)\sfill="#[0-9a-fA-F]{{3,6}}"',
            r'\1 fill="currentColor"', svg)
        svg = re.sub(
            rf'(<{tag}[^>]*)\sstroke="#[0-9a-fA-F]{{3,6}}"',
            r'\1 stroke="currentColor"', svg)
        svg = re.sub(
            rf'(<{tag}[^>]*)\sfill="(?:black|white)"',
            r'\1 fill="currentColor"', svg)
    return svg


def download_svg(name: str, url: str, dest: Path) -> Optional[str]:
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        svg = clean_svg(r.text)
        (dest / f"{name}.svg").write_text(svg, encoding="utf-8")
        return svg
    except Exception as e:
        return None


def get_category(name: str) -> str:
    """Derive category from ic_category_descriptor naming."""
    parts = name.lstrip("ic_").split("_")
    return parts[0] if parts else "misc"


def build_sprites(icons_content: Dict[str, str]):
    """Build per-category sprite files + one combined sprite."""
    SPRITE_DIR.mkdir(parents=True, exist_ok=True)

    # Group by category
    by_category = defaultdict(dict)
    for name, svg in icons_content.items():
        by_category[get_category(name)][name] = svg

    # Per-category sprites
    for cat, cat_icons in by_category.items():
        symbols = []
        for name, svg in cat_icons.items():
            inner = re.sub(r'<svg[^>]*>', '', svg)
            inner = re.sub(r'</svg>', '', inner).strip()
            symbols.append(
                f'  <symbol id="{name}" viewBox="0 0 24 24">\n'
                f'    {inner}\n'
                f'  </symbol>'
            )
        sprite = (
            f'<!-- JioGames DLS — {cat} icons ({len(cat_icons)} icons) -->\n'
            '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
            + '\n'.join(symbols)
            + '\n</svg>\n'
        )
        (SPRITE_DIR / f"{cat}.svg").write_text(sprite, encoding="utf-8")

    # Combined sprite (all icons)
    all_symbols = []
    for name, svg in icons_content.items():
        inner = re.sub(r'<svg[^>]*>', '', svg)
        inner = re.sub(r'</svg>', '', inner).strip()
        all_symbols.append(
            f'  <symbol id="{name}" viewBox="0 0 24 24">\n'
            f'    {inner}\n'
            f'  </symbol>'
        )
    combined = (
        f'<!-- JioGames DLS — All icons ({len(icons_content)} icons). Generated. DO NOT EDIT. -->\n'
        '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
        + '\n'.join(all_symbols)
        + '\n</svg>\n'
    )
    (ROOT / "icons" / "sprite.svg").write_text(combined, encoding="utf-8")


def build_index(icons_content: Dict[str, str]):
    """Write icons/index.json — name → category lookup."""
    index = {
        name: get_category(name)
        for name in sorted(icons_content.keys())
    }
    INDEX_OUT.write_text(json.dumps(index, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Export all Jio icons")
    parser.add_argument("--token", required=True, help="Figma personal access token")
    args = parser.parse_args()

    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    icon_map = load_icon_map()
    names    = sorted(icon_map.keys())
    total    = len(names)

    print(f"JioGames DLS — Bulk Icon Export")
    print(f"Total icons: {total}")
    print(f"Batches: {(total + BATCH_SIZE - 1) // BATCH_SIZE} × {BATCH_SIZE}")
    print(f"Destination: {ICONS_DIR.relative_to(ROOT)}/")
    print("─" * 44)

    icons_content = {}
    done = 0

    for b, name_batch in enumerate(batch(names, BATCH_SIZE), 1):
        node_ids = [icon_map[n] for n in name_batch]
        print(f"Batch {b}: fetching {len(name_batch)} URLs…", end=" ", flush=True)

        id_to_url = fetch_urls(args.token, node_ids)
        print(f"got {len(id_to_url)}")

        for name, node_id in zip(name_batch, node_ids):
            url = id_to_url.get(node_id) or id_to_url.get(node_id.replace(":", "-"))
            if not url:
                continue
            svg = download_svg(name, url, ICONS_DIR)
            if svg:
                icons_content[name] = svg
                done += 1

        print(f"  Progress: {done}/{total}", flush=True)
        # Be polite to Figma API
        time.sleep(1)

    print("─" * 44)
    print(f"Building sprites by category…")
    build_sprites(icons_content)
    cats = len(set(get_category(n) for n in icons_content))
    print(f"  {cats} category sprites → icons/sprites/")
    print(f"  Combined sprite → icons/sprite.svg")

    print(f"Building index…")
    build_index(icons_content)
    print(f"  icons/index.json")

    print("─" * 44)
    print(f"✓ {done}/{total} icons exported")
    print(f"✓ {cats} category sprites")
    failed = total - done
    if failed:
        print(f"⚠ {failed} failed — check node IDs or re-run")


if __name__ == "__main__":
    main()
