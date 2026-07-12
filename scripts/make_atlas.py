#!/usr/bin/env python3
"""
make_atlas.py — generate docs/atlas/SOW_PATTERN_ATLAS.html
==========================================================
OUR OWN pattern atlas: every pattern and setup taught visually in the SOW
instructor materials, redrawn as original SVG schematics with the rules stated
in our own words and mapped to the exact validator + test that enforces them.
Source citations refer to docs/research/SOW_METHOD.md and sow_deep_read/*.
Regenerate with:  python3 scripts/make_atlas.py
"""
import os

# palette validated with the dataviz six-checks (dark surface):
BLUE, GREEN, AMBER, RED = "#2f8fe6", "#28a35a", "#bd8514", "#f0524a"
INK, DIM, PATH = "#e8eef0", "#7c8a91", "#aab8be"


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" style="width:100%;height:auto">{body}</svg>')


def pl(pts, color=PATH, sw=2, dash=None, opac=1.0):
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"'
            f'{dd} stroke-linejoin="round" stroke-linecap="round" opacity="{opac}"/>')


def txt(x, y, s, color=DIM, size=11, anchor="start", bold=False):
    w = ' font-weight="700"' if bold else ""
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-family="system-ui,sans-serif" text-anchor="{anchor}"{w}>{s}</text>')


def dot(x, y, color=INK, r=2.6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def wave(pts, labels=None, color=PATH, lab_color=INK):
    """Polyline + pivot dots + pivot labels (labels: list aligned to pts, '' skips)."""
    out = [pl(pts, color)]
    for i, (x, y) in enumerate(pts):
        lab = labels[i] if labels and i < len(labels) else ""
        if lab:
            out.append(dot(x, y))
            up = i == 0 or y <= pts[i - 1][1]
            out.append(txt(x, y - 7 if up else y + 15, lab, lab_color, 12,
                           "middle", bold=True))
    return "".join(out)


def arrow(x1, y1, x2, y2, color=INK, sw=2):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h = 7
    p1 = (x2 - h * math.cos(a - 0.45), y2 - h * math.sin(a - 0.45))
    p2 = (x2 - h * math.cos(a + 0.45), y2 - h * math.sin(a + 0.45))
    return (pl([(x1, y1), (x2, y2)], color, sw)
            + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" '
              f'fill="{color}"/>')


# --------------------------------------------------------------------------- #
# Diagram builders (each returns an SVG string)
# --------------------------------------------------------------------------- #
def d_impulse():
    p = [(20, 170), (75, 105), (105, 138), (200, 40), (230, 78), (295, 22)]
    b = wave(p, ["0", "1", "2", "3", "4", "5"])
    b += pl([(20, 170), (160, 116)], AMBER, 1.6, "6 4")          # 0-2 line
    b += txt(312, 148, "0-2 line — W1/W3 never close below it", AMBER, 10, "end")
    b += pl([(105, 138), (300, 66)], GREEN, 1.6, "6 4")           # 2-4 line
    b += txt(312, 52, "2-4 line — W3/W5 never break it", GREEN, 10, "end")
    return svg(320, 200, b)


def d_extensions():
    out = []
    panels = [("1st extension (x1)", [(10, 90), (55, 18), (68, 45), (86, 30),
                                      (95, 40), (110, 26)], "x1 longest; 3 &amp; 5 shrink"),
              ("3rd extension (x3)", [(10, 90), (35, 62), (45, 76),
                                                    (95, 12), (104, 32), (118, 20)],
               "x3 ≥ 1.618× next; 5 ≈ 1"),
              ("5th extension (x5)", [(10, 90), (32, 66), (42, 78), (66, 48),
                                      (76, 60), (120, 8)],
               "x5 breaks channel; deep retrace")]
    for title, pts, note in panels:
        b = wave(pts, ["", "1", "2", "3", "4", "5"])
        b += txt(6, 104, title, INK, 10, bold=True) + txt(6, 116, note, DIM, 9)
        out.append(svg(130, 122, b))
    return '<div class="row3">' + "".join(out) + "</div>"


def d_terminal():
    p = [(20, 175), (95, 70), (120, 118), (185, 48), (205, 92), (255, 38)]
    b = wave(p, ["0", "1", "2", "3", "4", "5"])
    b += pl([(95, 70), (270, 30)], DIM, 1.2, "3 4")     # 1-3 upper
    b += pl([(120, 118), (270, 66)], GREEN, 1.6, "6 4") # 2-4 lower
    b += pl([(95, 70), (300, 70)], RED, 1, "2 3")       # W1 top level
    b += txt(262, 66, "W4 overlaps W1", RED, 10, "end")
    b += arrow(258, 42, 292, 150, RED)
    b += txt(292, 165, "full retrace in ¼–½ of W5's time", RED, 10, "end")
    return svg(320, 200, b)


def d_alternation():
    ok = wave([(8, 95), (48, 25), (62, 72), (108, 12), (118, 22), (124, 16),
               (130, 24), (136, 18), (146, 8)],
              ["", "1", "2", "3", "", "", "", "4", "5"])
    ok += txt(60, 88, "W2 sharp+deep (61.8%)", DIM, 9)
    ok += txt(100, 40, "W4 flat+shallow (38.2%)", DIM, 9)
    ok += txt(8, 110, "&#10003; alternation in depth, shape, time", GREEN, 10, bold=True)
    bad = wave([(8, 95), (48, 30), (62, 62), (104, 10), (118, 44), (146, 4)],
               ["", "1", "2", "3", "4", "5"])
    bad += txt(8, 110, "&#10007; W2 and W4 same depth+shape", RED, 10, bold=True)
    return ('<div class="row2">' + svg(160, 120, ok) + svg(160, 120, bad) + "</div>")


def d_time_rule():
    ok = wave([(8, 95), (44, 25), (86, 62), (140, 6)], ["0", "1", "2", "3"])
    ok += pl([(44, 100), (86, 100)], GREEN, 2)
    ok += txt(100, 112, "W2 ≥ W1 time", GREEN, 9, "middle")
    ok += pl([(8, 105), (44, 105)], DIM, 2) + txt(26, 117, "W1: 10d", DIM, 9, "middle")
    bad = wave([(8, 95), (44, 25), (58, 60), (140, 6)], ["0", "1", "2", "3"])
    bad += pl([(44, 100), (58, 100)], RED, 2)
    bad += txt(80, 112, "W2 5d &lt; W1 10d: NOT valid", RED, 8.5, "middle")
    return '<div class="row2">' + svg(160, 122, ok) + svg(160, 122, bad) + "</div>"


def d_two_four_setup():
    p = [(15, 175), (70, 110), (95, 140), (170, 55), (190, 92), (240, 40)]
    b = wave(p, ["0", "1", "2", "3", "4", "5"])
    b += pl([(95, 140), (300, 63)], GREEN, 1.8, "6 4")
    b += txt(312, 150, "stage 1: break of 2-4 line in ≤ time of W5", GREEN, 10, "end")
    b += pl([(190, 92), (312, 92)], AMBER, 1.2, "2 3")
    b += txt(312, 82, "stage 2: back to W4 level", AMBER, 10, "end")
    b += arrow(245, 44, 268, 120, INK)
    return svg(320, 200, b)


def d_zigzag():
    p = [(20, 30), (105, 130), (150, 88), (240, 178)]
    b = wave(p, ["0", "a", "b", "c"])
    b += pl([(20, 30), (300, 132)], AMBER, 1.8, "6 4")
    b += txt(305, 118, "0-B line", AMBER, 10, "end")
    b += arrow(245, 172, 285, 95, GREEN)
    b += txt(305, 30, "BUY at the break: stage-1 ≤ time of c;", GREEN, 10, "end")
    b += txt(305, 42, "stage-2 beyond b", GREEN, 10, "end")
    b += txt(40, 88, "internals 5-3-5", DIM, 10)
    b += txt(305, 58, "b &lt; 61.8% of a; b time ≥ a time", DIM, 10, "end")
    b += txt(160, 197, "c targets: 0.618×a · 1×a · 1.618×a (elongated)", DIM, 9.5, "middle")
    return svg(320, 205, b)


def d_flats():
    def mini(title, pts, note):
        b = wave(pts, ["0", "a", "b", "c"])
        b += pl([(6, pts[0][1]), (150, pts[0][1])], DIM, 0.8, "2 3")
        b += txt(6, 106, title, INK, 9.5, bold=True) + txt(6, 117, note, DIM, 8.5)
        return svg(156, 122, b)
    return ('<div class="row3">'
            + mini("Regular (weak b)", [(10, 20), (60, 80), (105, 32), (145, 92)],
                   "b = 61.8–100% of a; c ≈ a")
            + mini("Irregular (strong b)", [(10, 25), (60, 80), (105, 10), (145, 95)],
                   "b &gt; 100% of a; c = 1–1.382×a")
            + mini("C-failure", [(10, 20), (60, 85), (105, 30), (145, 62)],
                   "c fails to pass a — strength signal")
            + mini("Double failure", [(10, 25), (60, 80), (105, 32), (145, 60)],
                   "b &lt; 100% and c &lt; a")
            + mini("Running flat", [(10, 30), (60, 78), (105, 8), (145, 42)],
                   "c holds above origin — very strong trend")
            + mini("Time rule (all flats)", [(10, 25), (60, 80), (118, 30), (148, 88)],
                   "b takes MORE time than a")
            + "</div>")


def d_triangles():
    def base(pts, labels):
        return wave(pts, labels)
    out = []
    # contracting
    c = base([(8, 15), (30, 95), (58, 35), (82, 82), (102, 48), (118, 70)],
             ["", "a", "b", "c", "d", "e"])
    c += pl([(30, 95), (140, 62)], BLUE, 1.6, "6 4")
    c += txt(148, 92, "B-D line: CLEAN", BLUE, 9, "end")
    c += arrow(118, 70, 138, 18, GREEN)
    c += txt(148, 14, "thrust ≤ time of e", GREEN, 8.5, "end")
    c += txt(6, 112, "Contracting — E smallest", INK, 9, bold=True)
    out.append(svg(150, 120, c))
    # expanding
    e = base([(30, 55), (48, 70), (66, 42), (86, 82), (106, 28), (128, 95)],
             ["", "a", "b", "c", "d", "e"])
    e += pl([(20, 60), (140, 18)], DIM, 1, "3 4") + pl([(20, 68), (140, 105)], DIM, 1, "3 4")
    e += txt(6, 112, "Expanding — spikes", INK, 9, bold=True)
    out.append(svg(150, 120, e))
    # neutral
    n = base([(10, 30), (35, 78), (58, 45), (84, 100), (108, 38), (128, 72)],
             ["", "a", "b", "c", "d", "e"])
    n += txt(6, 112, "Neutral — C, D longest", INK, 9, bold=True)
    out.append(svg(150, 120, n))
    # extracting
    x = base([(10, 25), (32, 88), (56, 62), (82, 98), (108, 40), (126, 78)],
             ["", "a", "b", "c", "d", "e"])
    x += pl([(32, 88), (130, 34)], BLUE, 1.4, "6 4")
    x += txt(6, 112, "Extracting", INK, 9, bold=True)
    out.append(svg(150, 120, x))
    return '<div class="row2">' + "".join(out) + "</div>"


def d_diametric():
    p = [(15, 25), (52, 105), (80, 48), (104, 92), (128, 60), (160, 118),
         (205, 40), (250, 130)]
    b = wave(p, ["", "a", "b", "c", "d", "e", "f", "g"])
    b += pl([(52, 105), (128, 78)], DIM, 1, "3 4") + pl([(128, 78), (250, 128)], DIM, 1, "3 4")
    b += pl([(80, 48), (128, 55)], DIM, 1, "3 4") + pl([(128, 55), (205, 38)], DIM, 1, "3 4")
    b += txt(128, 20, "bow-tie: contracts to d, then expands", DIM, 10, "middle")
    b += pl([(104, 92), (280, 52)], BLUE, 1.6, "6 4")
    b += txt(278, 46, "D-F boundary", BLUE, 10, "end")
    b += arrow(252, 126, 288, 70, GREEN)
    b += txt(300, 90, "break ≤ time of g", GREEN, 9.5, "end")
    b += txt(160, 155, "pairs: g ≈ a · f ≈ b · e ≈ c (price OR time, [0.5–1.7] / [⅓–3])",
             DIM, 10, "middle")
    b += txt(160, 170, "all 7 legs are :3s with similar duration", DIM, 10, "middle")
    return svg(320, 180, b)


def d_complex():
    w = wave([(10, 20), (60, 95), (85, 60), (130, 130), (155, 95), (200, 165)],
             ["", "W", "X", "Y", "X", "Z"])
    w += txt(10, 190, "W-X-Y (one X) or W-X-Y-X-Z (two X) — NEVER more than 2 X waves",
             INK, 10, bold=True)
    w += txt(10, 204, "X = any corrective or a monowave; X usually &lt; 61.8% of prior pattern",
             DIM, 9.5)
    big = wave([(220, 160), (262, 40), (276, 66), (290, 52), (302, 62), (312, 55)],
               ["W", "X", "", "", "", "y=2"])
    big += txt(268, 20, "LARGE X ≥ 1.618×W", RED, 10, bold=True, anchor="middle")
    big += txt(268, 32, "→ reassess degree, relabel", RED, 9, "middle")
    return svg(330, 212, w + big)


def d_ichimoku():
    cloud_top = [(10, 120), (80, 105), (150, 88), (220, 72), (310, 55)]
    cloud_bot = [(10, 140), (80, 128), (150, 112), (220, 96), (310, 80)]
    area = ("M" + " L".join(f"{x},{y}" for x, y in cloud_top)
            + " L" + " L".join(f"{x},{y}" for x, y in reversed(cloud_bot)) + " Z")
    b = f'<path d="{area}" fill="{GREEN}" opacity="0.18"/>'
    b += pl(cloud_top, GREEN, 1, "2 3", 0.7) + pl(cloud_bot, GREEN, 1, "2 3", 0.7)
    b += txt(30, 135, "cloud (senkou A/B, displaced 26 → causal at t)", GREEN, 9)
    b += pl([(10, 96), (80, 78), (130, 88), (190, 52), (240, 64), (310, 26)], PATH, 2)
    b += pl([(10, 100), (310, 44)], BLUE, 1.3, "5 3")
    b += pl([(10, 108), (310, 56)], AMBER, 1.3, "5 3")
    b += txt(305, 38, "tenkan (9)", BLUE, 9, "end") + txt(305, 66, "kijun (26)", AMBER, 9, "end")
    b += arrow(130, 92, 150, 70, GREEN) + arrow(240, 68, 260, 46, GREEN)
    b += txt(160, 170, "LONG filter: price ABOVE cloud + tenkan &amp; kijun rising together;",
             INK, 10, "middle", bold=True)
    b += txt(160, 184, "pullbacks to the lines are re-entries (mirror for shorts). "
                       "Chikou excluded (not causal).", DIM, 9.5, "middle")
    return svg(320, 195, b)


# --------------------------------------------------------------------------- #
# Page assembly
# --------------------------------------------------------------------------- #
def card(title, diagram, rules, refs):
    rr = "".join(f"<li>{r}</li>" for r in rules)
    chips = "".join(f'<span class="chip">{c}</span>' for c in refs)
    return (f'<section class="card"><h2>{title}</h2>{diagram}'
            f'<ul>{rr}</ul><div class="refs">{chips}</div></section>')


FIBO_TABLE = """
<table><tr><th>pattern</th><th>rule / relation</th></tr>
<tr><td>Impulse</td><td>3rd usually extended = 1.618 / 2.618 × W1 · W5 ≈ W1 when 3rd extends · W2 ≤ 61.8% of W1 · W4↔W2 relate by Fib</td></tr>
<tr><td>Wave-3 targets</td><td>extension grid anchored at the W2 low; worked example targeted the 2.618–3.0 band</td></tr>
<tr><td>Zigzag</td><td>b ≤ 61.8% of a (rule) · c ≈ a, = 0.618×a, or = 1.618×a (elongated)</td></tr>
<tr><td>Flat</td><td>b ≥ 61.8% of a · c = a or ≈ 1.382×a</td></tr>
<tr><td>Triangle</td><td>legs relate ~50% Fib to the prior leg · thrust 100–125% of widest leg</td></tr>
<tr><td>Diametric</td><td>g ≈ a (or 61.8% of a) · f ≈ b · e ≈ c — price OR time</td></tr>
<tr><td>X wave</td><td>&lt; 61.8% of prior pattern; ≥ 1.618×W ⇒ LARGE-X regime</td></tr>
<tr><td>Retracements</td><td>roll the grid swing-by-swing; reactions terminate at 50–61.8%</td></tr></table>
"""

METHOD = """
<ol>
<li><b>Context</b> (trading cycle): global indices/DXY/yields/metals check → relative strength &amp; sector leadership → run scanner, pick candidates.</li>
<li><b>Start top-down</b>: weekly → daily → hourly → 15m; log scale for multi-year counts; every bar gets a label.</li>
<li><b>Draw the channel first.</b> A neatly channeled, overlapping "trend" of threes is a COMBINATION, not an impulse — impulses don't channel.</li>
<li><b>Impulse or corrective?</b> Run the 16-rule checklist (card 1). Time + subdivision + channel-fit discriminate.</li>
<li><b>If corrective, diagnose by WAVE B:</b> b faster than a → triangle / diametric; b slower → zigzag / flat most likely; then b-retracement splits zigzag (&lt;61.8%) from flat (≥61.8%).</li>
<li><b>Count from the faster retracement</b>; keep alternate labels alive on the chart until price resolves them.</li>
<li><b>Draw the confirmation line the moment a pattern is suspected</b> (2-4 / 0-B / B-D / D-F) — nothing is complete until the line breaks IN TIME (two stages).</li>
<li><b>Plot Ichimoku</b> (9/26/52): trade only with cloud + tenkan/kijun agreement.</li>
<li><b>Drop to hourly/15m (5m Ichimoku) to execute</b>: entry at the line-break / micro-pattern trigger, SL at the pattern invalidation, targets from Fib extensions / leg equality / channel; <b>R:R ≥ 1:2 written down BEFORE entry — else no trade.</b></li>
<li><b>Time cycles</b> (54/108-day, 85/141/272-week; weakness in the 2nd half of the 108-day cycle; ±10% leeway) — in this platform they arrive via the chakra_quant <code>CycleSignal</code> seam, never re-implemented here.</li>
</ol>
"""

CSS = """
body{background:#0a0d0f;color:#e8eef0;font-family:system-ui,Segoe UI,sans-serif;margin:0;padding:24px}
.wrap{max-width:1000px;margin:0 auto}
h1{font-size:24px;margin:0 0 4px} .sub{color:#7c8a91;font-size:12.5px;margin-bottom:18px;line-height:1.5}
.card{background:#11161a;border:1px solid #1c252b;border-radius:10px;padding:18px 20px;margin-bottom:16px}
.card h2{font-size:15px;color:#27e0c4;margin:0 0 12px}
.card > svg{max-width:620px;display:block;margin:0 auto}
.card ul{margin:10px 0 0;padding-left:18px} .card li{font-size:12.5px;color:#cdd6da;line-height:1.65;margin-bottom:4px}
.refs{margin-top:10px}
.chip{display:inline-block;background:#1c252b;color:#9fb0b6;border-radius:20px;padding:2px 10px;font-size:10.5px;margin:2px 4px 0 0;font-family:ui-monospace,monospace}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:12px} .row3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media(max-width:640px){.row2,.row3{grid-template-columns:1fr}}
table{width:100%;border-collapse:collapse;font-size:12px} th,td{text-align:left;padding:6px 8px;border-bottom:1px solid #1c252b} th{color:#7c8a91;font-weight:600}
ol{font-size:12.5px;color:#cdd6da;line-height:1.7;padding-left:20px} ol li{margin-bottom:6px}
code{background:#1c252b;padding:1px 5px;border-radius:4px;font-size:11px}
.foot{color:#7c8a91;font-size:10.5px;border-top:1px solid #1c252b;padding-top:12px;margin-top:8px;line-height:1.6}
"""


def build():
    cards = [
        card("1 · Impulse — the 16-rule checklist and the two structural lines",
             d_impulse(),
             ["Structure 5-3-5-3-5; W2 ≤ 61.8% of W1 (NeoWave tightening; classic EW allows &lt;100%); "
              "W3 never the shortest; W4 stays out of W2's territory (NW; EW says W1's).",
              "0-2 line: no part of W1/W3 closes across it — redraw it as a complex W2 evolves. "
              "2-4 line: no part of W3/W5 breaks it (terminal excepted).",
              "Only one of W1/W3/W5 extends; the extended wave ≥ 1.618× the next longest and is the one "
              "that visibly subdivides; the two unextended waves tend to equality.",
              "Touch-point rule: only 4 of 6 possible channel touches (manual charting heuristic — "
              "documented, not automated).",
              "TIME: W2 takes ≥ time of W1, W4 ≥ time of W3 — a 5-day W2 after a 10-day W1 kills the count."],
             ["RULESET §B/§C", "rules.elliott.elliott_hard_rules", "rules.engine.validate_impulse",
              "corrections.correction_time_rules", "test_phase3 / test_phase9_doctrine"]),
        card("2 · Extensions — which wave is the long one", d_extensions(),
             ["Usually the 3rd: 1.618 or 2.618 × W1; when the 3rd extends, W5 ≈ W1 and 5th-failure is possible.",
              "After a 5th-wave extension expect a deep, fast retracement back toward W4/channel base.",
              "The small correction sits NEXT to the extended wave (alternation predicts the extension)."],
             ["RULESET §C", "rules.neowave (equality/extension guidelines)", "FIBO sheet"]),
        card("3 · Terminal impulse (ending diagonal) — the reversal pattern", d_terminal(),
             ["Only in W5 or WC; every leg is a :3 (3-3-3-3-3); W4 MUST overlap W1; W3 &gt; W1; "
              "W2 may retrace &gt; 61.8% here; the impulse time rule is waived.",
              "Completion ⇒ expect FULL retracement of the terminal in ~¼–½ of the time W5 took."],
             ["RULESET §D", "diagonals.terminal_rules", "diagonals.is_terminal", "test_phase9_doctrine"]),
        card("4 · Alternation — W2 vs W4 must differ", d_alternation(),
             ["Alternate in retracement depth, price, TIME, pattern and complexity; "
              "a deep sharp W2 predicts a shallow sideways W4 (and vice versa)."],
             ["RULESET §C", "rules.engine.validate_impulse (guidelines)", "SOW deck p28"]),
        card("5 · The impulse time rule — counts die on time alone", d_time_rule(),
             ["W2 must take the same or more time than W1; W4 same-or-more than W3; "
              "corrections generally consume MORE time than the move they correct "
              "(exceptions: triangle, terminal, diametric, symmetrical)."],
             ["RULESET §I.5", "corrections.correction_time_rules", "test_phase9_doctrine"]),
        card("6 · Two-stage confirmation — the 2-4 line SETUP", d_two_four_setup(),
             ["Stage 1: the 2-4 line breaks within ≤ the time W5 took — else the impulse is NOT over.",
              "Stage 2: price returns to the W4 area within a comparable window.",
              "Trade template: position on the stage-1 break; invalidation = a new extreme beyond W5."],
             ["RULESET §F", "neowave.two_four_test", "neowave.two_four_confirmation",
              "neowave.confirm_completion"]),
        card("7 · Zigzag + the 0-B line SETUP (the mentorship 'Buy' chart)", d_zigzag(),
             ["5-3-5; b &lt; 61.8% of a (can be as little as 1%); c must pass the end of a "
              "(shortfall ⇒ truncated-c warning); b takes ≥ the time of a.",
              "0-B line from the correction's origin through b: stage 1 = break in ≤ time of c; "
              "stage 2 = beyond b's extreme. The instructor marks the BUY at the stage-1 break.",
              "If c ends ON the channel line — expect an x-wave; escalate to a complex correction."],
             ["RULESET §B/§I.5", "corrections.classify_correction", "corrections.zigzag_c_check",
              "neowave.zero_b_confirmation", "test_phase9_doctrine"]),
        card("8 · The flat family — read strength from wave b", d_flats(),
             ["b-retracement bands classify the flat and forecast strength: weak 61.8–80%, "
              "normal 80–100%, strong &gt;100% (irregular); failures and running flats are "
              "trend-strength signals in the direction of the larger trend."],
             ["RULESET §B/§I.4", "corrections.flat_b_band", "corrections.classify_correction",
              "test_phase9_doctrine"]),
        card("9 · Triangles — four species, one clean B-D line", d_triangles(),
             ["All: 3-3-3-3-3; E smallest; ≥3 legs retrace &gt;50% of the prior leg; "
              "B-D base line must be CLEAN (no part of C or E through it); cannot form in W2 "
              "(except inside terminals); 4-of-6 touch limit.",
              "Confirmation: B-D breaks in ≤ the time of E; thrust = 100–125% of the widest leg "
              "(irregular: of b).",
              "Draw the second line A-C when C &lt; B, C-E when C &gt; B."],
             ["RULESET §E/§I.2", "triangles._classify_triangle", "triangles.triangle_subrules",
              "neowave.bd_line_test", "neowave.bd_confirmation", "triangles.is_extracting_triangle",
              "triangles.is_neutral_triangle"]),
        card("10 · Diametric — 7 legs, bow-tie, paired sizes", d_diametric(),
             ["a–g all :3s; first half contracts into d, second half expands (bow-tie) or the mirror "
              "(diamond); running variant slants with the trend.",
              "Pairs: g ≈ a, f ≈ b, e ≈ c — satisfied in PRICE or TIME; legs show time similarity.",
              "Completion only at g; after e still expect f and g before reversing. "
              "Boundary (D-F) break within ~the time of g confirms."],
             ["RULESET §I.1", "corrections.diametric_pair_checks",
              "neowave.diametric_boundary_confirmation", "test_phase9_doctrine"]),
        card("11 · Complex corrections and the LARGE-X regime", d_complex(),
             ["W-X-Y or W-X-Y-X-Z; maximum TWO X waves — a third means the degree/segmentation is wrong.",
              "X connects standard corrective patterns and is usually &lt; 61.8% of the prior pattern.",
              "X ≥ 1.618×W ⇒ LARGE-X: what follows is a higher-degree structure — stop and relabel "
              "(REF, never an automated gate)."],
             ["RULESET §I.3", "triangles.x_wave_check", "corrections.max_x_count_check",
              "corrections.classify_complex_correction"]),
        card("12 · The Fibo system — one table, per pattern", FIBO_TABLE,
             ["Roll retracement grids forward swing-by-swing; counter-trend reactions terminate at "
              "50–61.8%; leg-equality relations ((e)=(c); time of III→IV = time of I) mark completions."],
             ["RULESET §C/§I", "rules.fib", "patterns.candidates._fib_score", "FIBO sheet"]),
        card("13 · Ichimoku Cloud — the SOW trade filter (9 / 26 / 52)", d_ichimoku(),
             ["Long only when price is above the cloud AND tenkan &amp; kijun point up together "
              "(mirror for shorts); pullbacks to the lines while the relationship holds are re-entries.",
              "Causality: the cloud at bar t was computed 26 bars earlier (displacement forward) — "
              "usable; the chikou span looks BACK and is excluded from every decision.",
              "In this platform: features.indicators.ichimoku + the opt-in confluence strand "
              "(default OFF in the validated signal path; ON in the SOW report as display)."],
             ["RULESET §I scope", "features.indicators.ichimoku", "confluence.ichimoku_trend",
              "test_phase9_doctrine (prefix-invariance)"]),
        card("14 · The method — order of operations (Day-2 'Steps' + trading cycle)", METHOD,
             ["This is the sequence the SOW report page (reporting/sow_report.py) follows card-by-card.",
              "Automation boundary: everything above is analysis (REF); only the validated wave-3 "
              "confirmation entry trades, through the risk gates, with live trading failing closed."],
             ["docs/research/SOW_METHOD.md", "reporting/sow_report.py", "docs/WAVE3_RESULT.md"]),
    ]
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>SOW Pattern Atlas — Ewace 2026</title>"
            f"<style>{CSS}</style></head><body><div class='wrap'>"
            "<h1>SOW Pattern Atlas</h1>"
            "<div class='sub'>Original diagrams and rule statements authored for this repo, "
            "distilled from the Sutra-of-Waves training materials (full page-cited notes: "
            "docs/research/sow_deep_read/). Every card names the RULESET section, validator "
            "function and test that enforce its rules. Regenerate: "
            "<code>python3 scripts/make_atlas.py</code></div>"
            + "".join(cards) +
            "<div class='foot'>Analysis reference only — REF outputs never gate automation. "
            "The platform trades only the validated wave-3 confirmation entry "
            "(docs/WAVE3_RESULT.md); time cycles arrive via the chakra_quant CycleSignal seam; "
            "Gann levels and the touch-point rule are documented as manual heuristics.</div>"
            "</div></body></html>")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "atlas", "SOW_PATTERN_ATLAS.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(html)
    print(f"wrote {out} ({len(html):,} bytes, {len(cards)} cards)")


if __name__ == "__main__":
    build()
