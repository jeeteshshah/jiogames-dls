#!/usr/bin/env python3
"""
JioGames DLS — Visual regression test.

Usage:
  python3 tools/visual-test.py           # compare against goldens
  python3 tools/visual-test.py --update  # capture new goldens

Requirements:
  pip install playwright pillow
  playwright install chromium

Exit: 0 = pass, 1 = failures found
"""

import sys, os, json, argparse
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
SHOWCASE = ROOT / "tests" / "showcase.html"
GOLDEN_DIR = ROOT / "tests" / "golden"
DIFF_DIR   = ROOT / "tests" / "diff"
REPORT     = ROOT / "tests" / "report.json"

# Pixel diff threshold — fraction of pixels allowed to differ (0.002 = 0.2%)
THRESHOLD = 0.002
# Per-channel delta tolerance (0–255) — ignores sub-pixel antialiasing noise
DELTA_TOL = 8

COMPONENTS = [
    "button",
    "otp",
    "input",
    "chip",
    "card-wide",
    "card-square",
    "genre-tile",
    "pass-card",
    "eyebrow",
    "toast",
    "colour-palette",
]


def ensure_deps():
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image, ImageChops
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("  Run: pip install playwright pillow && playwright install chromium")
        sys.exit(2)


def screenshot_components(page, viewport_w=393):
    """Return dict of component_name → PNG bytes."""
    shots = {}
    for name in COMPONENTS:
        el = page.locator(f"[data-component='{name}']")
        if el.count() == 0:
            print(f"  ⚠ Component not found in showcase: {name}")
            continue
        shots[name] = el.screenshot()
    # Full page as well
    shots["full-page"] = page.screenshot(full_page=True)
    return shots


def pixel_diff(golden_path, actual_bytes, name):
    """Compare golden PNG to actual PNG. Returns (pass, diff_ratio, diff_image_or_None)."""
    from PIL import Image, ImageChops, ImageFilter
    import io

    actual_img = Image.open(io.BytesIO(actual_bytes)).convert("RGB")

    if not golden_path.exists():
        return None, 0.0, None   # no golden — treat as new

    golden_img = Image.open(golden_path).convert("RGB")

    # Size mismatch = immediate fail
    if golden_img.size != actual_img.size:
        return False, 1.0, actual_img

    diff = ImageChops.difference(golden_img, actual_img)
    import struct

    pixels = list(diff.getdata())
    total  = len(pixels)
    changed = sum(
        1 for r, g, b in pixels
        if r > DELTA_TOL or g > DELTA_TOL or b > DELTA_TOL
    )
    ratio = changed / total

    # Create highlighted diff image
    from PIL import ImageDraw
    diff_vis = golden_img.copy()
    draw = ImageDraw.Draw(diff_vis)
    w, h = golden_img.size
    for i, (r, g, b) in enumerate(pixels):
        if r > DELTA_TOL or g > DELTA_TOL or b > DELTA_TOL:
            x, y = i % w, i // w
            diff_vis.putpixel((x, y), (255, 0, 0))

    passed = ratio <= THRESHOLD
    return passed, ratio, diff_vis


def run(update=False):
    ensure_deps()
    from playwright.sync_api import sync_playwright

    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    if not update:
        DIFF_DIR.mkdir(parents=True, exist_ok=True)

    url = SHOWCASE.as_uri()
    results = {}
    failures = []

    print(f"\nJioGames DLS — visual {'update' if update else 'test'}")
    print(f"Showcase: {SHOWCASE.relative_to(ROOT)}")
    print("─" * 44)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 393, "height": 852})
        page.goto(url)
        page.wait_for_load_state("networkidle")

        shots = screenshot_components(page)
        browser.close()

    for name, png_bytes in shots.items():
        golden = GOLDEN_DIR / f"{name}.png"

        if update:
            golden.write_bytes(png_bytes)
            print(f"  ✓ updated  {name}.png")
            results[name] = "updated"
            continue

        passed, ratio, diff_img = pixel_diff(golden, png_bytes, name)

        if passed is None:
            # No golden yet
            golden.write_bytes(png_bytes)
            print(f"  ◆ new      {name}.png  (golden created)")
            results[name] = "new"
        elif passed:
            pct = ratio * 100
            print(f"  ✓ pass     {name}  ({pct:.3f}% changed)")
            results[name] = "pass"
        else:
            pct = ratio * 100
            diff_path = DIFF_DIR / f"{name}-diff.png"
            diff_img.save(diff_path)
            print(f"  ✗ FAIL     {name}  ({pct:.2f}% changed > {THRESHOLD*100:.1f}% threshold)")
            print(f"             diff → {diff_path.relative_to(ROOT)}")
            results[name] = f"FAIL ({pct:.2f}%)"
            failures.append(name)

    print("─" * 44)

    # Write JSON report
    REPORT.write_text(json.dumps({
        "mode": "update" if update else "test",
        "threshold": THRESHOLD,
        "results": results,
        "failures": failures,
    }, indent=2))

    if update:
        print(f"✓ Goldens updated — {len(shots)} images in tests/golden/")
        return 0

    if failures:
        print(f"✗ {len(failures)} component(s) failed: {', '.join(failures)}")
        print(f"  Report: tests/report.json")
        return 1

    print(f"✓ All {len(shots)} components pass")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JioGames DLS visual regression")
    parser.add_argument("--update", action="store_true",
                        help="Capture new golden screenshots")
    args = parser.parse_args()
    sys.exit(run(update=args.update))
