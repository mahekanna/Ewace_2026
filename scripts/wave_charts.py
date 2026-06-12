"""
wave_charts.py  —  render the engine's actual Elliott/NeoWave COUNT onto price charts.
=====================================================================================
For visually auditing whether the automated wave application is sensible: for each
(symbol, timeframe) it plots the full available price history and overlays the
engine's primary count at TWO degrees — the top-degree labels (gold: 1-2-3-4-5 /
A-B-C / W-X-Y) and each leg's sub-waves (cyan) — plus a Fibonacci retracement of
the dominant leg and the next-wave forecast. Saves PNGs (no HTML).

Run:  python3 scripts/wave_charts.py [SYM ...]
"""
import json
import os
import sys
from datetime import datetime, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")
OUT = os.path.join(ROOT, "charts", "png")

SYMS = [("avgo", "AVGO · Broadcom"), ("nvda", "NVDA · Nvidia"),
        ("amd", "AMD"), ("mrvl", "MRVL · Marvell"), ("tsm", "TSM · TSMC")]
# (label, tag, scales)
TFS = [("1W", "1w", (0.05, 0.10, 0.18, 0.30)),
       ("1D", "1d", (0.04, 0.08, 0.14, 0.22)),
       ("4H", "4h", (0.03, 0.06, 0.10, 0.16)),
       ("1H", "1h", (0.02, 0.04, 0.07, 0.12)),
       ("15M", "15m", (0.015, 0.03, 0.05, 0.09))]

GOLD, CYAN, RED, GREEN, GRID, INK, BG = (
    "#f2b134", "#27e0c4", "#ff5d57", "#48d97a", "#1c252b", "#e8eef0", "#0a0d0f")


def load(tag, slug):
    p = os.path.join(LIVE, f"{slug}_{tag}_2026-06.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]


def dt(t):
    return datetime.fromtimestamp(t, tz=timezone.utc)


def adaptive_zigzag(bars, target=28):
    """Causal zigzag whose threshold is chosen so the FULL history reduces to a
    readable number of major swings (~target), spanning start->end."""
    best = []
    for pct in (0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30):
        piv = [p for p in wl.zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
        if not best or abs(len(piv) - target) < abs(len(best) - target):
            best = piv
        if len(piv) <= target:
            break
    return best


def subseq(pattern, n):
    if pattern in ("IMPULSE", "DIAGONAL"):
        s = "12345"
    elif pattern == "TRIANGLE":
        s = "ABCDE"
    elif pattern == "WXY":
        s = "WXY"
    else:
        s = "ABC"
    return [s[i] if i < len(s) else "·" for i in range(n)]


def build_chart(slug, name, tf_label, tag, scales, outpath):
    bars = load(tag, slug)
    if not bars or len(bars) < 60:
        return None
    closes = [b[4] for b in bars]
    dates = [dt(b[0]) for b in bars]
    counts = wl.wave_counts(bars, scales=scales, max_alternates=0)
    pc = counts[0] if counts else None

    fig, ax = plt.subplots(figsize=(16, 9), dpi=110)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.plot(dates, closes, color="#3aa6ff", lw=0.9, alpha=0.55, label="price (close)")

    use_log = (max(closes) / max(min(closes), 1e-9)) > 3
    if use_log:
        ax.set_yscale("log")

    # --- NeoWave per-swing labels (BELOW each pivot, cyan): :5/:3/:c3/... over a
    #     coarse causal zigzag spanning the entire history start->end. ---
    piv = adaptive_zigzag(bars)
    if len(piv) >= 3:
        zx = [dt(p.t) for p in piv]
        zy = [p.price for p in piv]
        ax.plot(zx, zy, color=RED, lw=1.5, alpha=0.9, zorder=5,
                label="major-swing path (full range)")
        ax.scatter(zx, zy, color=RED, s=14, zorder=6)
        lab = wl.label_monowaves(piv)
        for (w, l) in lab:
            ax.annotate(l.split("(")[0], (dt(w.end.t), w.end.price),
                        textcoords="offset points", xytext=(0, -15),
                        ha="center", color=CYAN, fontsize=8, alpha=0.95, zorder=7)

    # --- ELLIOTT WAVE count (ABOVE pivots, gold): the engine's PRIMARY top-down
    #     count — its labelled top-degree legs (1-2-3-4-5 / A-B-C / A-E) drawn as a
    #     bold path, with each leg's sub-waves where they subdivide. ---
    cov = conf = 0.0
    patt = degl = "n/a"
    if pc and pc.labels:
        patt, degl, conf, cov = pc.pattern, pc.degree_label, pc.confidence, pc.coverage
        nodes = [n for _l, n in pc.labels]
        ex = [dt(nodes[0].start.t)] + [dt(n.end.t) for n in nodes]
        ey = [nodes[0].start.price] + [n.end.price for n in nodes]
        ax.plot(ex, ey, color=GOLD, lw=2.4, alpha=0.95, zorder=8,
                label=f"primary count: {patt} @ {degl}")
        ax.scatter(ex, ey, color=GOLD, s=42, zorder=9, edgecolor=BG, linewidth=1)
        for lab, n in pc.labels:
            ax.annotate(lab, (dt(n.end.t), n.end.price), textcoords="offset points",
                        xytext=(0, 22), ha="center", va="center", color=GOLD,
                        fontsize=13, fontweight="bold", zorder=10,
                        bbox=dict(boxstyle="circle,pad=0.16", fc="#11161a", ec=GOLD, lw=1.3))
            if len(n.children) >= 2:                # sub-wave labels for this leg
                seq = subseq(n.pattern, len(n.children))
                for i, ch in enumerate(n.children):
                    ax.annotate(seq[i], (dt(ch.end.t), ch.end.price),
                                textcoords="offset points", xytext=(0, 12), ha="center",
                                color="#ffd479", fontsize=9, fontweight="bold", zorder=8)
        # Fib retracement of the dominant leg of the primary count (LEFT-edge labels)
        dom = max(nodes, key=lambda n: abs(n.end.price - n.start.price))
        a, b = dom.start.price, dom.end.price
        for r in (0.382, 0.5, 0.618):
            lv = b - (b - a) * r
            ax.axhline(lv, color=GREEN, lw=0.8, ls=":", alpha=0.4)
            ax.annotate(f"{r:.3f}  {lv:,.1f}", (dates[0], lv), color=GREEN,
                        fontsize=8, ha="left", va="bottom", alpha=0.75)

    # forecast next move
    fc = None
    try:
        fc = wl.forecast_waves(bars)
    except Exception:
        fc = None
    if fc and fc.targets:
        tgt = fc.targets[0][1]
        ax.annotate("", xy=(dates[-1], tgt), xytext=(dates[-1], closes[-1]),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.8))
        ftxt = ("FORECAST  " + fc.next_wave + "\n"
                + "  ".join(f"{l} {p:,.1f}" for l, p in fc.targets)
                + f"\ninvalidation {fc.invalidation:,.1f}   conf {fc.confidence:.0%}")
        ax.text(0.985, 0.035, ftxt, transform=ax.transAxes, color=INK, fontsize=9,
                va="bottom", ha="right",
                bbox=dict(boxstyle="round,pad=0.5", fc="#11161a", ec=GOLD, alpha=0.9))

    span = f"{dates[0].date()} → {dates[-1].date()}"
    ax.set_title(f"{name}   ·   {tf_label}   ·   {span}   ·   {len(bars)} bars\n"
                 f"Elliott + NeoWave wave count (full range)   ·   engine's best single "
                 f"Elliott read: {patt} @ {degl}, conf {conf:.0%} / coverage {cov:.0%}"
                 + ("   [LOG scale]" if use_log else ""),
                 color=INK, fontsize=13, pad=14)
    ax.tick_params(colors="#7c8a91", labelsize=9)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.grid(color=GRID, lw=0.5, alpha=0.5)
    ax.legend(loc="upper left", facecolor="#11161a", edgecolor=GRID,
              labelcolor=INK, fontsize=9)
    sub = ("GOLD path = ELLIOTT primary count (top-down): circled 1-2-3-4-5 / A-B-C "
           "top-degree legs + smaller sub-waves   ·   BELOW pivots = NeoWave swing "
           "labels (cyan :5/:3/:c3…)   ·   dotted green = Fib   ·   gold arrow = forecast")
    fig.text(0.5, 0.012, sub, ha="center", color="#7c8a91", fontsize=8.5)
    fig.text(0.99, 0.012, "analysis tooling only — not advice", ha="right",
             color="#4a565c", fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    fig.savefig(outpath, facecolor=BG)
    plt.close(fig)
    return outpath


def main():
    want = [a.lower() for a in sys.argv[1:]]
    syms = [(s, n) for s, n in SYMS if not want or s in want]
    made = []
    for slug, name in syms:
        for tf_label, tag, scales in TFS:
            out = os.path.join(OUT, f"{slug}_{tag}.png")
            r = build_chart(slug, name, tf_label, tag, scales, out)
            print(("wrote " + r) if r else f"skip {slug} {tag} (no data)")
            if r:
                made.append(r)
    print(f"\n{len(made)} charts written to {OUT}")


if __name__ == "__main__":
    main()
