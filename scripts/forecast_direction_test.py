"""
forecast_direction_test.py  —  does the wave forecast even pick the right DIRECTION?
====================================================================================
The cleanest possible test of EW/NeoWave's predictive claim, stripped of all entry,
stop, target and position-management choices (which are discretionary and can flatter
or flatter-to-deceive a result). At each bar it takes ONLY the forecast's predicted
direction, "enters" at the next bar, holds a fixed horizon, exits — no stop, no
target — and measures the mean return SIGNED by the forecast direction.

If the forecast has directional skill, the signed mean / Sharpe should be positive
and beat always-long (buy-and-hold). Causal: direction at bar t uses bars[:t+1].

Run:  python3 scripts/forecast_direction_test.py
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl
from wavelib.forecast_backtest import _setup_at

LIVE = os.path.join(ROOT, "data", "live")
HOLD = 13
WINDOW = 300
STRIDE = 2
MIN_HISTORY = 80
MIN_BARS = 250


def main():
    pooled, bench = [], []
    for f in sorted(glob.glob(os.path.join(LIVE, "*_1w_2026-06.json"))):
        d = json.load(open(f))
        bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
                for b in d["bars"]]
        if len(bars) < MIN_BARS:
            continue
        cl = [b[4] for b in bars]
        for t in range(MIN_HISTORY, len(bars) - HOLD, STRIDE):
            s = _setup_at(bars[:t + 1], WINDOW)
            if s is None:
                continue
            dirn = s[0]
            pooled.append((cl[t + HOLD] - cl[t]) / cl[t] * dirn)   # signed by forecast
        bench += wl.horizon_returns(bars, horizon=HOLD, bullish=True)

    n = len(pooled)
    m = sum(pooled) / n
    bm = sum(bench) / len(bench)
    print(f"PURE DIRECTION TEST (weekly, next-bar entry, {HOLD}-bar hold, no stop/target)")
    print(f"  forecast-directed trades: {n}")
    print(f"  mean signed return: {m:.4f} ({m * 100:.2f}%)")
    print(f"  Sharpe(signed):     {wl.sharpe_ratio(pooled):.3f}")
    print(f"  win rate:           {100 * sum(1 for r in pooled if r > 0) / n:.1f}%")
    print(f"  buy-and-hold mean:  {bm:.4f}  Sharpe {wl.sharpe_ratio(bench):.3f}")
    print("  => forecast direction beats always-long? "
          + ("YES" if m > bm else "NO"))


if __name__ == "__main__":
    main()
