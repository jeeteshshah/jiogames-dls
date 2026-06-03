#!/usr/bin/env python3
"""
JioGames DLS — token generator.
Reads tokens.json (single source of truth) and emits tokens.css.
tokens.css is a GENERATED artifact — never hand-edit it.

Usage:  python3 tokens/build.py
        python3 tokens/build.py --check   # verify tokens.css is up to date (CI)

Curated CSS var names are irregular vs JSON paths, so the mapping is explicit
below. Add a token to tokens.json AND to the relevant EMIT list here.
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "tokens.json")
OUT  = os.path.join(HERE, "tokens.css")

def load():
    with open(SRC) as f:
        return json.load(f)

def val(tok, *path):
    node = tok
    for p in path:
        node = node[p]
    return node["$value"]

# (css-var, json-path) — order = emission order within a section
def build_css(t):
    g = lambda *p: val(t, *p)

    sections = [
        ("Brand green", [
            ("--jio", g("color","brand","jio")),
            ("--jio-2", g("color","brand","jio-2")),
            ("--jio-3", g("color","brand","jio-3")),
            ("--jio-bright", g("color","brand","jio-bright")),
            ("--jio-glow", g("color","brand","jio-glow")),
            ("--jio-soft", g("color","brand","jio-soft")),
        ]),
        ("Pass / premium", [
            ("--ultimate", g("color","pass","ultimate")),
            ("--ultimate-glow", g("color","pass","ultimate-glow")),
            ("--popular-gold", g("color","pass","popular-gold")),
        ]),
        ("Functional accents", [
            ("--gold", g("color","functional","gold")),
            ("--gold-laurel", g("color","functional","gold-laurel")),
            ("--amber", g("color","functional","amber")),
            ("--amber-soft", g("color","functional","amber-soft")),
            ("--red", g("color","functional","red")),
            ("--pink", g("color","functional","pink")),
            ("--cyan", g("color","functional","cyan")),
            ("--violet", g("color","functional","violet")),
            ("--negative", g("color","functional","negative")),
            ("--positive", g("color","functional","positive")),
        ]),
        ("Backgrounds", [
            ("--bg", g("color","bg","base")),
            ("--card-bg", g("color","bg","card")),
            ("--sheet-bg", g("color","bg","sheet")),
            ("--sheet-top", g("color","bg","sheet-top")),
        ]),
        ("Surface ladder (opaque)", [
            ("--surface-1", g("color","surface","1")),
            ("--surface-2", g("color","surface","2")),
            ("--surface-3", g("color","surface","3")),
            ("--surface-4", g("color","surface","4")),
        ]),
        ("Glass surfaces", [
            ("--glass-1", g("color","glass","1")),
            ("--glass-2", g("color","glass","2")),
            ("--chip-bg", g("color","glass","chip")),
        ]),
        ("Text", [
            ("--text", g("color","text","primary")),
            ("--text2", g("color","text","secondary")),
            ("--text3", g("color","text","muted")),
            ("--text4", g("color","text","faint")),
            ("--text-inv", g("color","text","inverse")),
        ]),
        ("Borders", [
            ("--border", g("color","border","default")),
            ("--border-strong", g("color","border","strong")),
            ("--border-subtle", g("color","border","subtle")),
            ("--border-ultimate", g("color","border","ultimate")),
            ("--divider", g("color","border","divider")),
            ("--hairline", g("color","border","hairline")),
            ("--hairline-2", g("color","border","hairline-2")),
        ]),
        ("Overlay", [
            ("--overlay-scrim", g("color","overlay","scrim")),
        ]),
        ("Spacing scale (8px base)", [
            (f"--space-{k}", g("space", k)) for k in
            ["0","0-25","0-5","1","1-5","2","3","4","5","6","8","10","12"]
        ]),
        ("Semantic spacing aliases (mobile base; see @media below)", [
            ("--gutter", g("layout","gutter")),
            ("--section-gap", g("layout","section-gap")),
            ("--rail-gap", "var(--section-gap)"),
            ("--card-gap", g("layout","card-gap")),
            ("--component-padding", g("layout","component-padding")),
            ("--card-padding", g("layout","card-padding")),
            ("--sheet-padding", g("layout","sheet-padding")),
            ("--hero-gap", g("layout","hero-gap")),
        ]),
        ("Radius", [
            (f"--r{n}", g("radius", f"r{n}")) for n in range(1,10)
        ] + [("--pill", g("radius","pill"))]),
        ("Layout / grid", [
            ("--frame-mobile-w", g("layout","frame-mobile-w")),
            ("--frame-mobile-h", g("layout","frame-mobile-h")),
            ("--container-web", g("layout","container-web")),
            ("--tv-safe", g("layout","tv-safe")),
            ("--web-grid-gap", g("layout","web-grid-gap")),
            ("--hero-text-max", g("layout","hero-text-max")),
            ("--grid-cols-mobile", g("layout","grid-columns-mobile")),
            ("--grid-cols-web", g("layout","grid-columns-web")),
            ("--grid-cols-tv", g("layout","grid-columns-tv")),
            ("--safe-top", "env(safe-area-inset-top, 0px)"),
            ("--safe-bot", "env(safe-area-inset-bottom, 0px)"),
        ]),
        ("Control sizes (mobile base; TV overrides via @media)", [
            ("--ctrl-h",       g("control","ctrl-h")),
            ("--ctrl-h-sm",    g("control","ctrl-h-sm")),
            ("--ctrl-h-ghost", g("control","ctrl-h-ghost")),
            ("--touch-min",    g("control","touch-min")),
            ("--otp-box-w",    g("control","otp-box-w")),
            ("--otp-box-h",    g("control","otp-box-h")),
            ("--card-wide-w",  g("control","card-wide-w")),
            ("--card-sq",      g("control","card-sq")),
            ("--genre-tile-h", g("control","genre-tile-h")),
            ("--tab-bar-h",    g("control","tab-bar-h")),
            ("--app-bar-h",    g("control","app-bar-h")),
            ("--icon-size-xs",       g("control","icon-size-xs")),
            ("--icon-size-sm",       g("control","icon-size-sm")),
            ("--icon-size-md",       g("control","icon-size-md")),
            ("--icon-size-base",     g("control","icon-size-base")),
            ("--icon-size-lg",       g("control","icon-size-lg")),
            ("--icon-size-xl",       g("control","icon-size-xl")),
            ("--icon-color-default", g("control","icon-color-default")),
            ("--icon-color-active",  g("control","icon-color-active")),
            ("--icon-color-muted",   g("control","icon-color-muted")),
            ("--icon-wrapper-sm",    g("control","icon-wrapper-sm")),
            ("--icon-wrapper-md",    g("control","icon-wrapper-md")),
        ]),
        ("Font", [
            ("--jio-font", g("font","family")),
        ]),
        ("Motion — easing", [
            ("--spring",        g("motion","spring")),
            ("--spring-bounce", g("motion","spring-bounce")),
            ("--ease-screen",   g("motion","ease-screen")),
            ("--ease-out",      g("motion","ease-out")),
            ("--ease-error",    g("motion","ease-error")),
        ]),
        ("Motion — duration (use tokens; raw ms only inside approved keyframe recipes)", [
            ("--dur-instant", g("motion","dur-instant")),
            ("--dur-fast",    g("motion","dur-fast")),
            ("--dur-default", g("motion","dur-default")),
            ("--dur-pop",     g("motion","dur-pop")),
            ("--dur-error",   g("motion","dur-error")),
            ("--dur-sheet",   g("motion","dur-sheet")),
            ("--dur-enter",    g("motion","dur-enter")),
            ("--dur-screen",   g("motion","dur-screen")),
            ("--dur-tv-enter",     g("motion","dur-tv-enter")),
            ("--dur-shimmer",      g("motion","dur-shimmer")),
            ("--dur-icon-spin",    g("motion","dur-icon-spin")),
            ("--dur-reduced-fade",    g("motion","dur-reduced-fade")),
            ("--dur-reduced-instant", g("motion","dur-reduced-instant")),
            ("--stagger-start",    g("motion","stagger-start")),
            ("--stagger-step",     g("motion","stagger-step")),
        ]),
    ]

    out = []
    out.append("/* ============================================================")
    out.append("   JioGames DLS — tokens.css")
    out.append("   GENERATED by tokens/build.py from tokens.json. DO NOT EDIT.")
    out.append("   Run: python3 tokens/build.py")
    out.append("   ============================================================ */\n")

    # @font-face
    for w, file in [("300","Light"),("300","LightItalic"),("500","Medium"),
                    ("500","MediumItalic"),("700","Bold"),("900","Black")]:
        ital = "font-style:italic; " if "Italic" in file else ""
        out.append(f"@font-face {{ font-family:'JioType'; src:url('/Assets/font/JioType-{file}.ttf'); font-weight:{w}; {ital}font-display:swap; }}")
    out.append("")

    out.append(":root {")
    for title, items in sections:
        out.append(f"  /* {title} */")
        for name, value in items:
            out.append(f"  {name}: {value};")
        out.append("")
    out[-1] = "}"  # replace trailing blank with close
    out.append("")

    # platform @media overrides
    plats = t.get("$platforms", {})
    for key in ("web", "tv"):
        if key not in plats: continue
        p = plats[key]
        out.append(f"/* {key.upper()} overrides */")
        out.append(f"@media {p['media']} {{")
        out.append("  :root {")
        for tok, v in p["tokens"].items():
            out.append(f"    --{tok}: {v};")
            if tok == "section-gap":
                out.append("    --rail-gap: var(--section-gap);")
        out.append("  }")
        out.append("}")
    out.append("")

    # reduced motion — collapse all interaction durations; keep sheet at 100ms for perceived continuity
    out.append("@media (prefers-reduced-motion: reduce) {")
    out.append("  :root {")
    out.append("    --dur-instant: 0ms; --dur-fast: 0ms; --dur-default: 0ms; --dur-tv-enter: 0ms;")
    out.append("    --dur-pop: 0ms; --dur-error: 0ms;")
    out.append("    --dur-enter: 0ms; --dur-screen: 0ms; --dur-sheet: 100ms;")
    out.append("  }")
    out.append("  /* Ambient loops must be stopped in component CSS — tokens alone cannot pause infinite animations. */")
    out.append("  /* See motion.md §11 for ambient, shimmer, and stagger reduced-motion patterns. */")
    out.append("}")
    out.append("")

    # stack utilities
    out.append("/* ============================================================")
    out.append("   Stack utilities — vertical rhythm from parent gap, not child margins.")
    out.append("   ============================================================ */")
    for cls, gap, note in [
        ("page-stack","var(--section-gap)","major sections"),
        ("hero-stack","var(--hero-gap)","hero / major break"),
        ("component-stack","var(--component-padding)","components in a section"),
        ("content-stack","var(--space-1-5)","related elements (title+body)"),
        ("tight-stack","var(--space-1)","tight group (label+value)"),
    ]:
        out.append(f".{cls} {{ display: flex; flex-direction: column; gap: {gap}; }}  /* {note} */")
    out.append("")
    return "\n".join(out)

def main():
    t = load()
    css = build_css(t)
    check = "--check" in sys.argv
    if check:
        cur = open(OUT).read() if os.path.exists(OUT) else ""
        if cur.strip() != css.strip():
            print("✗ tokens.css is OUT OF DATE — run: python3 tokens/build.py")
            sys.exit(1)
        print("✓ tokens.css is up to date with tokens.json")
        return
    with open(OUT, "w") as f:
        f.write(css)
    print(f"✓ generated {OUT} from tokens.json")

if __name__ == "__main__":
    main()
