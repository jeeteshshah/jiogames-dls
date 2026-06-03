#!/usr/bin/env python3
"""
JioGames DLS — Icon Filename Auditor
Generates a current audit of icons/svg/ against naming governance rules.
Cross-checks against icons/icons-manifest.json if it exists.

Usage:
  python3 tools/audit-icons.py
  python3 tools/audit-icons.py --json          # machine-readable output
  python3 tools/audit-icons.py --migration     # print migration table only

Do not manually edit icons.md migration map — run this script to regenerate it.
"""

import os, sys, re, json, argparse
from pathlib import Path
from collections import defaultdict

HERE  = Path(__file__).parent
ROOT  = HERE.parent
ICONS = ROOT / "icons" / "svg"
MANIFEST = ROOT / "icons" / "icons-manifest.json"

# Spelling suspects — known misspellings in current library
SPELLING_SUSPECTS = {
    "aparell":      "apparel",
    "arist":        "artist",
    "antibacteria": "antibacterial",
    "hiefer":       "heifer",
    "horzontal":    "horizontal",
    "vaccum":       "vacuum",
}

# Numeric words that should be digits
NUMERIC_WORDS = ["_one_", "_two_", "_three_", "_four_", "_five_",
                 "_six_", "_seven_", "_eight_", "_nine_", "_ten_",
                 "_one.", "_two.", "_three.", "_four."]  # end of name

# Known intentional word-numbers (not violations)
INTENTIONAL = {"ic_repeat_one", "ic_one_tap", "ic_table_tennis",
               "ic_tennis", "ic_vitamin_b", "ic_vitamin_d",
               "ic_remote_universal_a", "ic_remote_universal_b",
               "ic_remote_universal_u", "ic_a_to_z"}


def audit(svg_dir: Path):
    if not svg_dir.exists():
        print(f"✗ {svg_dir} not found. Run export-all-icons.py first.")
        sys.exit(1)

    files = sorted(svg_dir.glob("*.svg"))
    names = [f.stem for f in files]

    issues = defaultdict(list)

    for name in names:
        # 1. Uppercase letters
        if any(c.isupper() for c in name):
            issues["CASE"].append({
                "file": name,
                "proposed": name.lower(),
                "reason": "Contains uppercase — breaks case-sensitive systems",
                "risk": "high",
                "alias": True,
            })

        # 2. Trailing space (in filename itself)
        if name != name.strip():
            issues["TRAILING_SPACE"].append({
                "file": name,
                "proposed": name.strip(),
                "reason": "Trailing or leading space in filename",
                "risk": "high",
                "alias": False,
            })

        # 3. Spelling suspects
        for bad, good in SPELLING_SUSPECTS.items():
            if bad in name and name not in INTENTIONAL:
                issues["SPELLING"].append({
                    "file": name,
                    "proposed": name.replace(bad, good),
                    "reason": f"Probable misspelling of '{bad}' → '{good}'",
                    "risk": "medium",
                    "alias": True,
                })

        # 4. Numeric words
        if name not in INTENTIONAL:
            for w in NUMERIC_WORDS:
                check = w if not w.endswith(".") else w[:-1]
                if check in f"_{name}_":
                    issues["NUMERIC_WORD"].append({
                        "file": name,
                        "proposed": f"(replace word with digit)",
                        "reason": f"Word-form number '{check.strip('_')}' — use digit instead",
                        "risk": "low",
                        "alias": True,
                    })
                    break

        # 5. Too short / vague (≤2 chars after ic_)
        stem = name.replace("ic_", "", 1)
        if len(stem) <= 2:
            issues["TOO_SHORT"].append({
                "file": name,
                "proposed": f"ic_[category]_{stem}",
                "reason": "Name too vague — add category prefix",
                "risk": "low",
                "alias": True,
            })

    # 6. Near-duplicates (names within edit distance 1 of each other)
    name_set = set(names)
    seen_dupes = set()
    for name in names:
        for other in names:
            if name >= other:
                continue
            # Simple check: one contains the other minus one word
            n_parts = set(name.split("_"))
            o_parts = set(other.split("_"))
            if len(n_parts.symmetric_difference(o_parts)) <= 2:
                key = tuple(sorted([name, other]))
                if key not in seen_dupes:
                    seen_dupes.add(key)
                    issues["NEAR_DUPLICATE"].append({
                        "file": f"{name} ↔ {other}",
                        "proposed": "Decide which to keep; deprecate the other",
                        "reason": "Near-duplicate names — may confuse icon selection",
                        "risk": "low",
                        "alias": True,
                    })

    # 7. Manifest cross-check
    manifest = {}
    if MANIFEST.exists():
        try:
            manifest = json.loads(MANIFEST.read_text())
        except json.JSONDecodeError:
            pass

    # Icons not in manifest
    for name in names:
        if name not in manifest:
            issues["NOT_IN_MANIFEST"].append({
                "file": name,
                "proposed": "Add to icons/icons-manifest.json",
                "reason": "No manifest entry — ungoverned",
                "risk": "low",
                "alias": False,
            })

    # Manifest entries whose files don't exist
    for manifest_name in manifest:
        if manifest_name not in name_set:
            issues["MANIFEST_ORPHAN"].append({
                "file": manifest_name,
                "proposed": "Remove manifest entry or re-export icon",
                "reason": "Manifest entry has no corresponding SVG file",
                "risk": "medium",
                "alias": False,
            })

    return names, issues


def print_report(names, issues):
    total = sum(len(v) for k, v in issues.items()
                if k not in ("NOT_IN_MANIFEST",))  # skip manifest noise in summary

    print(f"\nJioGames DLS — Icon Filename Audit")
    print(f"Directory: icons/svg/")
    print(f"Total icons: {len(names)}")
    print(f"Issues (excl. manifest): {total}")
    print("─" * 56)

    order = ["CASE", "TRAILING_SPACE", "SPELLING", "NUMERIC_WORD",
             "TOO_SHORT", "NEAR_DUPLICATE", "MANIFEST_ORPHAN", "NOT_IN_MANIFEST"]

    for category in order:
        items = issues.get(category, [])
        if not items:
            continue
        label = {
            "CASE": "Uppercase letters",
            "TRAILING_SPACE": "Trailing/leading spaces",
            "SPELLING": "Probable misspellings",
            "NUMERIC_WORD": "Word-form numbers (use digits)",
            "TOO_SHORT": "Vague / missing category",
            "NEAR_DUPLICATE": "Near-duplicate names",
            "MANIFEST_ORPHAN": "Manifest entries without SVG file",
            "NOT_IN_MANIFEST": "Icons not in manifest",
        }.get(category, category)

        print(f"\n[{category}] {label} ({len(items)})")
        for item in items[:20]:  # cap output for large categories
            f = item["file"]
            p = item["proposed"]
            r = item["reason"]
            risk = item.get("risk", "")
            alias = "alias needed" if item.get("alias") else ""
            extras = " · ".join(filter(None, [risk, alias]))
            print(f"  {f}")
            print(f"    → {p}")
            print(f"    {r}" + (f" [{extras}]" if extras else ""))
        if len(items) > 20:
            print(f"  ... and {len(items)-20} more (run with --json for full list)")

    print("\n─" * 56)
    print("Run with --json for machine-readable output.")
    print("Run with --migration for migration table only.")
    print("Do not rename files directly — add manifest alias first.")


def print_migration_table(issues):
    """Print a markdown migration table for icons.md."""
    rows = []
    for category in ["CASE", "TRAILING_SPACE", "SPELLING", "NUMERIC_WORD", "TOO_SHORT"]:
        for item in issues.get(category, []):
            alias = "Yes" if item.get("alias") else "No"
            rows.append(
                f"| `{item['file']}` | `{item['proposed']}` "
                f"| {item['reason']} | {item.get('risk','').capitalize()} | {alias} |"
            )

    if not rows:
        print("No migration items found.")
        return

    print("\n| Old filename | Proposed filename | Reason | Risk | Alias needed |")
    print("|---|---|---|---|:---:|")
    for r in rows:
        print(r)


def main():
    parser = argparse.ArgumentParser(description="JioGames icon filename auditor")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--migration", action="store_true", help="Print migration table")
    args = parser.parse_args()

    names, issues = audit(ICONS)

    if args.json:
        out = {"total_icons": len(names), "issues": {k: v for k, v in issues.items()}}
        print(json.dumps(out, indent=2))
    elif args.migration:
        print_migration_table(issues)
    else:
        print_report(names, issues)


if __name__ == "__main__":
    main()
