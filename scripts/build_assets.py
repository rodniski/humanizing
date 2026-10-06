"""Generate the README images in assets/ (light and dark variants).

    python3 scripts/build_assets.py

Stdlib only. The hero animates once with CSS and rests on its final frame;
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


# Hero: a clean-at-the-word-level AI answer, its three structural tells lit
# one by one, then the restructured version. Each line is a list of
# (text, css class) runs; "sup:N" renders a small marker.
BEFORE = [
    [("I looked into the login timeouts. ", ""),
     ("First I checked the logs, then the load", "t1")],
    [("balancer, then the connection pool.", "t1"), ("sup:1", "t1"),
     (" As experienced engineers often say, it's", "t2")],
    [("usually the simplest thing.", "t2"), ("sup:2", "t2"),
     (" In the end, it was the pool size. ", ""), ("Ultimately,", "t3")],
    [("this shows how small details can have a big impact on reliability.", "t3"),
     ("sup:3", "t3")],
]
AFTER = [
    [("Login times out because the DB pool caps at 10", "f1"), ("sup:1", "f1"),
     (" (", ""), ("config/db.go:42", "f2"), (").", "")],
    [("Raised it to 50; p99 fell from ", ""), ("8.1 s", "f2"), (" to ", ""),
     ("240 ms", "f2"), (".", ""), ("sup:2", "f2")],
    [("Not checked:", "f3"), ("sup:3", "f3"),
     (" whether the cache hides the same limit under real load.", "")],
]
BEFORE_TAGS = [("1", "discovery order", "t1"), ("2", "vague allusion", "t2"),
               ("3", "moral at the end", "t3")]
AFTER_TAGS = [("1", "conclusion first", "f1"), ("2", "named, not alluded", "f2"),
              ("3", "open end, stated", "f3")]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line(runs, x, y):
    out = [f'<text x="{x}" y="{y}" class="mono">']
    raised = False
    for text, cls in runs:
        c = f' class="{cls}"' if cls else ""
        if text.startswith("sup:"):
            out.append(f'<tspan{c} dy="-6" font-size="10">{text[4:]}</tspan>')
            raised = True
        else:
            dy = ' dy="6"' if raised else ""
            out.append(f"<tspan{c}{dy}>{esc(text)}</tspan>")
            raised = False
    out.append("</text>")
    return "".join(out)


def tags(items, y, kind):
    out = []
    for i, (n, label, cls) in enumerate(items):
        x = 48 + i * 230
        out.append(
            f'<g class="tag {cls}-tag"><circle cx="{x + 6}" cy="{y - 4}" r="8" class="{cls}-dot"/>'
            f'<text x="{x + 6}" y="{y}" class="num" text-anchor="middle">{n}</text>'
            f'<text x="{x + 22}" y="{y}" class="label">{esc(label)}</text></g>'
        )
    return "".join(out)


def hero(t):
    w, h = 880, 450
    # Timeline in seconds: before fades in, tells light up, before dims,
    # after fades in line by line, fix tags appear.
    css = f"""
    .card{{fill:{t['bg']};stroke:{t['border']}}}
    .mono{{font:14.5px {MONO};fill:{t['ink']}}}
    .head{{font:600 15px {SANS};fill:{t['ink']}}}
    .sub{{font:13px {SANS};fill:{t['muted']}}}
    .cap{{font:600 11px {SANS};letter-spacing:.12em;fill:{t['muted']}}}
    .label{{font:13px {SANS};fill:{t['ink']}}}
    .num{{font:700 10.5px {SANS};fill:{t['bg']}}}
    .rule{{stroke:{t['border']}}}
    .t1,.t2,.t3{{fill:{t['tell']}}}
    .f1,.f2,.f3{{fill:{t['fix']}}}
    .t1-dot,.t2-dot,.t3-dot{{fill:{t['tell']}}}
    .f1-dot,.f2-dot,.f3-dot{{fill:{t['fix']}}}
    .before-dim{{opacity:.7}}
    @keyframes in{{from{{opacity:0;transform:translateY(4px)}}}}
    @keyframes lit{{from{{fill:{t['ink']}}}}}
    @keyframes dim{{from{{opacity:1}}}}
    .before-in{{animation:in .6s ease-out .2s backwards}}
    .t1{{animation:lit .35s ease-out 1.2s backwards}}
    .t2{{animation:lit .35s ease-out 1.9s backwards}}
    .t3{{animation:lit .35s ease-out 2.6s backwards}}
    .t1-tag{{animation:in .35s ease-out 1.2s backwards}}
    .t2-tag{{animation:in .35s ease-out 1.9s backwards}}
    .t3-tag{{animation:in .35s ease-out 2.6s backwards}}
    .before-dim{{animation:dim .6s ease-out 3.4s backwards}}
    .a0{{animation:in .5s ease-out 3.8s backwards}}
    .a1{{animation:in .5s ease-out 4.05s backwards}}
    .a2{{animation:in .5s ease-out 4.3s backwards}}
    .after-cap{{animation:in .5s ease-out 3.6s backwards}}
    .after-tags{{animation:in .5s ease-out 4.8s backwards}}
    @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
    """
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="An AI-written answer with three structural tells highlighted, then the restructured version.">',
        f"<style>{css}</style>",
        f'<rect class="card" x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14"/>',
        '<text x="48" y="50" class="head">humanizing</text>',
        f'<text x="{w - 48}" y="50" class="sub" text-anchor="end">structure, not vocabulary</text>',
        f'<line class="rule" x1="48" x2="{w - 48}" y1="70" y2="70"/>',
        '<g class="before-in"><g class="before-dim">',
        '<text x="48" y="102" class="cap">BEFORE</text>',
    ]
    parts += [line(r, 48, 132 + i * 24) for i, r in enumerate(BEFORE)]
    parts.append("</g>")
    parts.append(tags(BEFORE_TAGS, 242, "t"))
    parts.append("</g>")
    parts.append(f'<line class="rule" x1="48" x2="{w - 48}" y1="270" y2="270"/>')
    parts.append('<text x="48" y="302" class="cap after-cap">AFTER</text>')
    parts += [f'<g class="a{i}">{line(r, 48, 332 + i * 24)}</g>' for i, r in enumerate(AFTER)]
    parts.append(f'<g class="after-tags">{tags(AFTER_TAGS, 418, "f")}</g>')
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
    w, h = 880, 420
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
    .note{{font:11.5px {SANS};fill:{t['muted']}}}
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
        f'<text x="48" y="{h - 26}" class="note">Schematic after StoryScope Fig. 2 (first two linear discriminants of 257 narrative features, style removed).</text>',
        f'<text x="48" y="{h - 10}" class="note">Centroids read off the published figure; points are illustrative, not the paper\'s data.</text>',
        "</svg>",
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (ASSETS / f"hero-{name}.svg").write_text(hero(t))
        (ASSETS / f"map-{name}.svg").write_text(map_svg(t))
    print("wrote", sorted(p.name for p in ASSETS.glob("*.svg")))
