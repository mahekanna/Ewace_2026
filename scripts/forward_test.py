"""
forward_test.py  —  ghost-feeding forward test of the wave forecast (intraday).
==============================================================================
Backtests pool stats and hide the real-time decision. This instead SIMULATES
real time: it walks the most-recent candles one at a time, and at EACH candle
computes the LIVE forecast (next-wave direction + Fibonacci target zone +
invalidation + NeoWave time window) from bars[:t] ONLY — then "ghost-feeds" the
next candles to observe whether the forecast played out.

Outputs:
  * reports/FORWARD_TEST_<SYM>_<TF>.md  — per-step log + an honest summary
  * charts/png/forward/<sym>_<tf>_step_*.png — snapshots showing, at a moment in
    time, the count + the PROJECTED next wave, with the REALIZED (ghost-fed)
    candles overlaid so you can SEE forecast vs reality.

CAUSAL: every forecast at candle t uses only data <= t. Run:
  python3 scripts/forward_test.py [SYM] [TF]      (default AVGO 15m)
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
OUTDIR = os.path.join(ROOT, "charts", "png", "forward")
BG, INK, GRID = "#0a0d0f", "#e8eef0", "#1c252b"
BLUE, GOLD, RED, GREEN, AMBER = "#3aa6ff", "#f2b134", "#ff5d57", "#48d97a", "#ffd479"

ROLL = 400          # rolling history window the live forecast is built from
FORWARD = 260       # how many recent candles to forward-test over
RESOLVE = 32        # max candles to let a forecast play out (ghost-feed horizon)
N_SNAPSHOTS = 6     # how many forecast-vs-reality charts to render


def load(sym, tf):
    d = json.load(open(os.path.join(LIVE, f"{sym}_{tf}_2026-06.json")))
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]


def dt(t):
    return datetime.fromtimestamp(t, tz=timezone.utc)


def resolve(fc, future, price):
    """Ghost-feed `future` candles and classify the forecast outcome.

    STALE/unusable if the target is already on the wrong side of current price (or
    invalidation on the wrong side) — that happens when the count's last CONFIRMED
    pivot lags price, so the projection is degenerate and would register a trivial
    instant 'hit'. Those are excluded, not counted as wins."""
    if not fc or not fc.targets:
        return "no-forecast", None, 0
    up = fc.direction == "up"
    tgt = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
    inv = fc.invalidation
    if up and not (tgt > price and inv < price):
        return "stale", None, 0
    if (not up) and not (tgt < price and inv > price):
        return "stale", None, 0
    for i, b in enumerate(future):
        hi, lo = b[2], b[3]
        if up:
            if lo <= inv:
                return "INVALIDATED", b[0], i + 1
            if hi >= tgt:
                return "HIT", b[0], i + 1
        else:
            if hi >= inv:
                return "INVALIDATED", b[0], i + 1
            if lo <= tgt:
                return "HIT", b[0], i + 1
    return "OPEN", None, len(future)


def snapshot(sym, tf, bars, t, fc, path):
    """Chart: history+count up to t, the projected next wave, and the realized
    (ghost-fed) candles overlaid."""
    hist = bars[max(0, t - 200):t + 1]
    future = bars[t + 1:t + 1 + RESOLVE]
    fig, ax = plt.subplots(figsize=(15, 8), dpi=110)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.plot([dt(b[0]) for b in hist], [b[4] for b in hist], color=BLUE, lw=1.1,
            label="known history (causal)")
    # primary count legs (gold)
    cs = wl.wave_counts(bars[max(0, t - ROLL):t + 1], max_alternates=0)
    if cs and cs[0].labels:
        ns = [n for _l, n in cs[0].labels]
        xs = [dt(ns[0].start.t)] + [dt(n.end.t) for n in ns]
        ys = [ns[0].start.price] + [n.end.price for n in ns]
        ax.plot(xs, ys, color=GOLD, lw=2.0, alpha=0.9, zorder=6,
                label=f"count: {cs[0].pattern} @ {cs[0].degree_label}")
        for lab, n in cs[0].labels:
            ax.annotate(lab, (dt(n.end.t), n.end.price), color=GOLD, fontsize=11,
                        fontweight="bold", ha="center", va="center",
                        bbox=dict(boxstyle="circle,pad=0.15", fc="#11161a", ec=GOLD, lw=1))
    now_t, now_p = bars[t][0], bars[t][4]
    # projected next wave
    if fc and fc.targets:
        tgt = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
        span_s = (fc.time_lo_days or 1) * 86400.0
        ax.annotate("", xy=(dt(now_t + span_s), tgt), xytext=(dt(now_t), now_p),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))
        lo_t = min(tgt, now_p)
        ax.axhspan(lo_t, max(tgt, now_p), xmin=0.62, alpha=0.06, color=GOLD)
        ax.axhline(tgt, color=GREEN, ls=":", lw=1, alpha=0.7)
        ax.annotate(f"target {tgt:,.2f}", (dt(hist[0][0]), tgt), color=GREEN, fontsize=9,
                    ha="left", va="bottom")
        ax.axhline(fc.invalidation, color=RED, ls=":", lw=1, alpha=0.7)
        ax.annotate(f"invalidation {fc.invalidation:,.2f}", (dt(hist[0][0]), fc.invalidation),
                    color=RED, fontsize=9, ha="left", va="top")
    # realized future candles (ghost-fed) — what ACTUALLY happened
    if future:
        ax.plot([dt(b[0]) for b in future], [b[4] for b in future], color=AMBER,
                lw=1.6, ls="--", zorder=7, label="REALIZED next candles (ghost-fed)")
        outcome, _, nbar = resolve(fc, future, bars[t][4])
        ax.annotate(f"OUTCOME: {outcome}" + (f" in {nbar} candles" if outcome in ("HIT", "INVALIDATED") else ""),
                    (dt(future[-1][0]), future[-1][4]), color=AMBER, fontsize=10,
                    fontweight="bold", ha="right", va="bottom")
    ax.axvline(dt(now_t), color="#7c8a91", lw=0.8, ls="--", alpha=0.6)
    nxt = fc.next_wave if fc else "n/a"
    conf = f"{fc.confidence:.0%}" if fc else "-"
    ax.set_title(f"{sym.upper()} {tf} — FORECAST as of {dt(now_t):%Y-%m-%d %H:%M}  ·  price ${now_p:,.2f}\n"
                 f"next: {nxt}  ·  conf {conf}  ·  vertical line = 'now' (everything right of it is ghost-fed)",
                 color=INK, fontsize=12, pad=12)
    ax.tick_params(colors="#7c8a91", labelsize=8)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.grid(color=GRID, lw=0.4, alpha=0.5)
    ax.legend(loc="upper left", facecolor="#11161a", edgecolor=GRID, labelcolor=INK, fontsize=8)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, facecolor=BG)
    plt.close(fig)


def main():
    sym = (sys.argv[1] if len(sys.argv) > 1 else "avgo").lower()
    tf = (sys.argv[2] if len(sys.argv) > 2 else "15m").lower()
    forward = int(sys.argv[3]) if len(sys.argv) > 3 else FORWARD  # optional 3rd arg widens the walk
    bars = load(sym, tf)
    n = len(bars)
    start = max(ROLL, n - forward)
    end = n - RESOLVE                      # leave room to ghost-feed the resolution
    steps = list(range(start, end))
    if not steps:
        print("not enough bars"); return

    rows, hit = [], {"HIT": 0, "INVALIDATED": 0, "OPEN": 0, "no-forecast": 0}
    dir_correct = dir_total = 0
    for t in steps:
        fc = wl.forecast_waves(bars[:t + 1], window=ROLL)
        future = bars[t + 1:t + 1 + RESOLVE]
        outcome, _, nbar = resolve(fc, future, bars[t][4])
        hit[outcome] = hit.get(outcome, 0) + 1
        # next-candle directional check
        if fc and fc.targets and t + 1 < n:
            moved_up = bars[t + 1][4] >= bars[t][4]
            if (fc.direction == "up") == moved_up:
                dir_correct += 1
            dir_total += 1
        rows.append((bars[t][0], bars[t][4], fc, outcome, nbar))

    # snapshot charts at evenly spaced steps
    os.makedirs(OUTDIR, exist_ok=True)
    snap_idx = [steps[int(i * (len(steps) - 1) / (N_SNAPSHOTS - 1))] for i in range(N_SNAPSHOTS)]
    snaps = []
    for k, t in enumerate(snap_idx):
        fc = wl.forecast_waves(bars[:t + 1], window=ROLL)
        p = os.path.join(OUTDIR, f"{sym}_{tf}_step_{k+1}.png")
        snapshot(sym, tf, bars, t, fc, p)
        snaps.append(p)

    decided = hit["HIT"] + hit["INVALIDATED"]
    hr = hit["HIT"] / decided if decided else 0.0
    da = dir_correct / dir_total if dir_total else 0.0
    stale = hit.get("stale", 0)
    mod = max(8, len(rows) // 120)         # keep the log readable for long walks
    out = [f"# Forward test (ghost-feeding) — {sym.upper()} {tf}",
           "",
           f"_Simulated real time: at each of {len(steps)} candles "
           f"({dt(bars[steps[0]][0]):%Y-%m-%d %H:%M} → {dt(bars[steps[-1]][0]):%Y-%m-%d %H:%M}) "
           f"the LIVE forecast is built from the prior {ROLL} candles only, then the next "
           f"{RESOLVE} candles are ghost-fed to resolve it. Causal; not advice._",
           "",
           "## Summary",
           f"- **STALE/unusable forecasts: {stale}** of {len(steps)} "
           f"({stale / max(len(steps), 1):.0%}) — the target was already on the wrong "
           "side of price because the count's confirmed pivot lags (intraday lag). These "
           "are EXCLUDED, not counted as instant wins.",
           f"- Usable forecasts resolved: **{decided}** (HIT {hit['HIT']} / INVALIDATED "
           f"{hit['INVALIDATED']}); OPEN {hit['OPEN']}; no-forecast {hit['no-forecast']}.",
           f"- **Target-hit rate among USABLE forecasts: {hr:.0%}.**",
           f"- Next-candle directional accuracy: **{da:.0%}** of {dir_total} (coin-flip = 50%).",
           f"- Snapshots (forecast vs realized): " + ", ".join(f"`{os.path.relpath(s, ROOT)}`" for s in snaps),
           "",
           f"## Live forecast log (every {mod}th candle)",
           "| time | price | forecast | conf | target | invalid | outcome |",
           "|---|---|---|---|---|---|---|"]
    for i, (t, px, fc, outcome, nbar) in enumerate(rows):
        if i % mod:
            continue
        if fc and fc.targets:
            tgt = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
            out.append(f"| {dt(t):%m-%d %H:%M} | {px:,.2f} | {fc.next_wave} | {fc.confidence:.0%} | "
                       f"{tgt:,.2f} | {fc.invalidation:,.2f} | {outcome}"
                       + (f" ({nbar})" if outcome in ('HIT', 'INVALIDATED') else "") + " |")
        else:
            out.append(f"| {dt(t):%m-%d %H:%M} | {px:,.2f} | (no clean count) | - | - | - | - |")
    rep = os.path.join(ROOT, "reports", f"FORWARD_TEST_{sym.upper()}_{tf}.md")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("\n".join(out) + "\n")
    print("\n".join(out[:14]))
    print(f"\nwrote {rep}\nwrote {len(snaps)} snapshot charts to {OUTDIR}")


if __name__ == "__main__":
    main()
