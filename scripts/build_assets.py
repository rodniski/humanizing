"""Generate the README images in assets/ (light and dark variants).

    python3 scripts/build_assets.py

Stdlib only. social-preview.svg is rasterized to the 1280x640 PNG that goes
in Settings > Social preview with any Chromium, e.g.

    chromium --headless --window-size=1280,640 --screenshot=assets/social-preview.png assets/social-preview.svg
 The hero animates once with CSS and rests on its final frame;
prefers-reduced-motion skips straight to that frame.
"""

import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": dict(bg="#fbfaf7", border="#e4e1da", ink="#1c1b19", muted="#8a857c",
                  tell="#b4442a", fix="#2f6f5e", dot="#9a958c"),
    "dark": dict(bg="#151514", border="#2c2b28", ink="#ecebe6", muted="#8f8b82",
                 tell="#e2805f", fix="#6fc2a8", dot="#77736b"),
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


# Hero: a clean-at-the-word-level AI answer with its three structural tells
# marked, then the restructured version. Each line is a list of
# (text, css class) runs; "sup:N" renders a small marker.
#
# Every element is visible in the base styles. The animation only recolors
# (tells light up in sequence, then the fixes), so a renderer that freezes
# at t=0 or ignores CSS animation still shows the full text.
BEFORE = [
    [("I looked into the login timeouts. ", ""), ("First I checked the logs,", "t1")],
    [("then the load balancer, then the connection pool.", "t1"), ("sup:1", "t1"),
     (" As experienced", "t2")],
    [("engineers often say, it's usually the simplest thing.", "t2"), ("sup:2", "t2"),
     (" In the end,", "")],
    [("it was the pool size. ", ""), ("Ultimately, this shows how small details", "t3")],
    [("can have a big impact on reliability.", "t3"), ("sup:3", "t3")],
]
AFTER = [
    [("Login times out because the DB pool caps at 10.", "f1"), ("sup:1", "f1")],
    [("Raised it to 50 (", ""), ("config/db.go:42", "f2"), ("); p99 fell from ", ""),
     ("8.1 s", "f2")],
    [("to ", ""), ("240 ms", "f2"), (".", ""), ("sup:2", "f2"), (" ", ""),
     ("Not checked:", "f3"), ("sup:3", "f3"), (" whether the cache hides", "")],
    [("the same limit under real load.", "")],
]
BEFORE_TAGS = [("1", "discovery order", "t1"), ("2", "vague allusion", "t2"),
               ("3", "moral at the end", "t3")]
AFTER_TAGS = [("1", "conclusion first", "f1"), ("2", "named, not alluded", "f2"),
              ("3", "open end, stated", "f3")]

LINE = 30


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line(runs, x, y):
    out = [f'<text x="{x}" y="{y}" class="mono">']
    raised = False
    for text, cls in runs:
        c = f' class="{cls}"' if cls else ""
        if text.startswith("sup:"):
            out.append(f'<tspan{c} dy="-7" font-size="12">{text[4:]}</tspan>')
            raised = True
        else:
            dy = ' dy="7"' if raised else ""
            out.append(f"<tspan{c}{dy}>{esc(text)}</tspan>")
            raised = False
    out.append("</text>")
    return "".join(out)


def tags(items, y):
    out = []
    for i, (n, label, cls) in enumerate(items):
        x = 48 + i * 262
        out.append(
            f'<circle cx="{x + 9}" cy="{y - 5}" r="10" class="{cls}-dot"/>'
            f'<text x="{x + 9}" y="{y}" class="num" text-anchor="middle">{n}</text>'
            f'<text x="{x + 28}" y="{y}" class="label">{esc(label)}</text>'
        )
    return "".join(out)


def hero(t):
    w = 880
    by = 104
    tag1 = by + LINE * len(BEFORE) + 14
    rule = tag1 + 34
    ay = rule + 82
    tag2 = ay + LINE * len(AFTER) + 14
    h = tag2 + 44
    # Timeline in seconds: tells light up 1-2-3, the before text dims, then the
    # fixes light up 1-2-3.
    css = f"""
    .card{{fill:{t['bg']};stroke:{t['border']}}}
    .mono{{font:17px {MONO};fill:{t['ink']}}}
    .cap{{font:600 12.5px {SANS};letter-spacing:.12em;fill:{t['muted']}}}
    .sub{{font:14px {SANS};fill:{t['muted']}}}
    .label{{font:15.5px {SANS};fill:{t['ink']}}}
    .num{{font:700 12px {SANS};fill:{t['bg']}}}
    .rule{{stroke:{t['border']}}}
    .t1,.t2,.t3{{fill:{t['tell']}}}
    .f1,.f2,.f3{{fill:{t['fix']}}}
    .t1-dot,.t2-dot,.t3-dot{{fill:{t['tell']}}}
    .f1-dot,.f2-dot,.f3-dot{{fill:{t['fix']}}}
    .before{{opacity:.72}}
    @keyframes ink{{from{{fill:{t['ink']}}}
    @keyframes off{{from{{fill:{t['border']}}}
    @keyframes dim{{from{{opacity:1}}
    .t1,.t1-dot{{animation:ink .35s ease-out .8s backwards}}
    .t2,.t2-dot{{animation:ink .35s ease-out 1.5s backwards}}
    .t3,.t3-dot{{animation:ink .35s ease-out 2.2s backwards}}
    .before{{animation:dim .6s ease-out 3s backwards}}
    .f1,.f1-dot{{animation:ink .35s ease-out 3.5s backwards}}
    .f2,.f2-dot{{animation:ink .35s ease-out 4.1s backwards}}
    .f3,.f3-dot{{animation:ink .35s ease-out 4.7s backwards}}
    .t1-dot,.t2-dot,.t3-dot,.f1-dot,.f2-dot,.f3-dot{{animation-name:off}}
    @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="An AI-written answer with three structural tells highlighted, then the restructured version.">',
        f"<style>{css}</style>",
        f'<rect class="card" x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14"/>',
        '<text x="48" y="58" class="cap">BEFORE</text>',
        f'<text x="{w - 48}" y="58" class="sub" text-anchor="end">structure, not vocabulary</text>',
        '<g class="before">',
    ]
    parts += [line(r, 48, by + i * LINE) for i, r in enumerate(BEFORE)]
    parts.append("</g>")
    parts.append(tags(BEFORE_TAGS, tag1 + 22))
    parts.append(f'<line class="rule" x1="48" x2="{w - 48}" y1="{rule + 14}" y2="{rule + 14}"/>')
    parts.append(f'<text x="48" y="{rule + 52}" class="cap">AFTER</text>')
    parts += [line(r, 48, ay + i * LINE) for i, r in enumerate(AFTER)]
    parts.append(tags(AFTER_TAGS, tag2 + 22))
    parts.append("</svg>")
    return "\n".join(parts)


# Map: a schematic of StoryScope Fig. 2. Centroids and spreads are read off
# the published figure by eye; the points are synthetic.
CLUSTERS = [
    # name, cx, cy, sx, sy, n, human?
    ("Human", -3.6, 0.9, 1.25, 1.15, 230, True),
    ("Claude", -0.3, -2.6, 0.95, 0.95, 80, False),
    ("GPT", 0.55, -0.5, 0.9, 0.95, 80, False),
    ("Kimi", 0.7, 0.45, 0.9, 0.9, 80, False),
    ("DeepSeek", 1.05, 0.9, 0.9, 0.85, 80, False),
    ("Gemini", 1.2, 1.0, 0.9, 0.85, 80, False),
]


def map_svg(t):
    w, h = 880, 380
    px0, px1, py0, py1 = 48, w - 48, 104, 352
    xmin, xmax, ymin, ymax = -7.5, 4.5, -5.5, 3.6
    sx = lambda x: px0 + (x - xmin) / (xmax - xmin) * (px1 - px0)
    sy = lambda y: py1 - (y - ymin) / (ymax - ymin) * (py1 - py0)
    rng = random.Random(7)
    css = f"""
    .card{{fill:{t['bg']};stroke:{t['border']}}}
    .h{{fill:{t['tell']};opacity:.55}}
    .a{{fill:{t['dot']};opacity:.5}}
    .c{{stroke:{t['bg']};stroke-width:1.5}}
    .hc{{fill:{t['tell']}}} .ac{{fill:{t['ink']}}}
    .big{{font:600 15px {SANS};fill:{t['ink']}}}
    .small{{font:12.5px {SANS};fill:{t['muted']}}}
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="Schematic scatter: human stories spread across the left; five AI models overlap in one cluster on the right.">',
        f"<style>{css}</style>",
        f'<rect class="card" x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14"/>',
    ]
    for name, cx, cy, sdx, sdy, n, human in CLUSTERS:
        cls = "h" if human else "a"
        for _ in range(n):
            x, y = rng.gauss(cx, sdx), rng.gauss(cy, sdy)
            if xmin < x < xmax and ymin < y < ymax:
                parts.append(f'<circle class="{cls}" cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="2.3"/>')
    for name, cx, cy, *_rest, human in CLUSTERS:
        x, y = sx(cx), sy(cy)
        parts.append(f'<rect class="c {"hc" if human else "ac"}" x="{x - 5:.1f}" y="{y - 5:.1f}" '
                     f'width="10" height="10" transform="rotate(45 {x:.1f} {y:.1f})"/>')
    parts += [
        '<text x="48" y="50" class="big">Human authors</text>',
        '<text x="48" y="70" class="small">10,272 writers, spread out</text>',
        f'<text x="{w - 48}" y="50" class="big" text-anchor="end">Five models</text>',
        f'<text x="{w - 48}" y="70" class="small" text-anchor="end">GPT, Gemini, DeepSeek, Kimi, Claude</text>',
        f'<text x="{sx(-0.3) + 12:.0f}" y="{sy(-2.6) + 4:.0f}" class="small">Claude, the outlier</text>',
        "</svg>",
    ]
    return "\n".join(parts)


PAIRS = [("moral at the end", "end on the fact"),
         ("discovery order", "conclusion first"),
         ("vague allusion", "name the thing"),
         ("everything resolved", "say what is open")]


def social(t):
    w, h = 1280, 640
    rows = []
    for i, (bad, good) in enumerate(PAIRS):
        y = 352 + i * 50
        rows.append(f'<text x="96" y="{y}" class="m"><tspan class="bad">{bad}</tspan>'
                    f'<tspan class="arrow">  \u2192  </tspan><tspan class="good">{good}</tspan></text>')
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f"""<style>
        .title{{font:700 96px {SANS};fill:{t['ink']};letter-spacing:-.02em}}
        .tag{{font:32px {SANS};fill:{t['muted']}}}
        .m{{font:28px {MONO}}}
        .bad{{fill:{t['tell']}}} .good{{fill:{t['fix']}}} .arrow{{fill:{t['muted']}}}
        .foot{{font:22px {SANS};fill:{t['muted']}}}
        </style>""",
        f'<rect width="{w}" height="{h}" fill="{t['bg']}"/>',
        '<text x="96" y="178" class="title">humanizing</text>',
        '<text x="96" y="238" class="tag">Structural AI-writing fixes that word lists miss.</text>',
        *rows,
        f'<text x="96" y="{h - 56}" class="foot">Agent skill \u00b7 grounded in StoryScope (COLM 2026)</text>',
        "</svg>",
    ])


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (ASSETS / f"hero-{name}.svg").write_text(hero(t))
        (ASSETS / f"map-{name}.svg").write_text(map_svg(t))
    (ASSETS / "social-preview.svg").write_text(social(THEMES["dark"]))
    print("wrote", sorted(p.name for p in ASSETS.glob("*.svg")))
