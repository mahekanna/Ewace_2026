"""
ghost_diag.py — WHY does a forecaster have (no) edge? Read-only breakdown.
=========================================================================
Same causal walk as ghost_forward.py, but tabulates the calls by their `kind` and
by the forecaster's own `confidence`, and checks next-candle direction split by
trend-agreement and median bars-to-resolution. This is the tool that exposes a
"mechanical / no-information" signal. Pure stdlib.

USAGE
  python3 ghost_diag.py --data DATA.json --forecaster my_model.py:forecast [--roll 400 --resolve 32]
"""
import argparse
import os
import statistics as st
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf


def bucket(c):
    return ("conf <40%" if c < 0.40 else "conf 40-55%" if c < 0.55
            else "conf 55-70%" if c < 0.70 else "conf >=70%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--forecaster", required=True)
    ap.add_argument("--roll", type=int, default=400)
    ap.add_argument("--forward", default="all")
    ap.add_argument("--resolve", type=int, default=32)
    ap.add_argument("--trend-lookback", type=int, default=20)
    a = ap.parse_args()

    bars, symbol, interval = gf.load_bars(a.data)
    forecaster = gf.load_forecaster(a.forecaster)
    by = defaultdict(lambda: defaultdict(int))
    cf = defaultdict(lambda: {"n": 0, "ok": 0, "tot": 0, "HIT": 0, "INVALIDATED": 0})
    trend = {"with": [0, 0], "against": [0, 0]}
    hb, ib = [], []
    none = 0

    # need indexable access to compute the trend-agreement lookback
    n = len(bars)
    fwd = n if a.forward in ("all", None) else int(a.forward)
    start = max(a.roll, n - fwd)
    for t in range(start, n - a.resolve):
        window = bars[max(0, t + 1 - a.roll):t + 1]
        fc = gf._norm(forecaster(window))
        if fc is None:
            none += 1
            continue
        d = by[fc.kind or "(unlabelled)"]
        d["n"] += 1
        d["up"] += int(fc.direction == "up")
        outcome, nbar = gf.resolve(fc, bars[t + 1:t + 1 + a.resolve], bars[t][4])
        d[outcome] += 1
        b2 = cf[bucket(fc.confidence)]
        b2["n"] += 1
        if outcome in ("HIT", "INVALIDATED"):
            b2[outcome] += 1
            (hb if outcome == "HIT" else ib).append(nbar)
        if t + 1 < n:
            up = bars[t + 1][4] >= bars[t][4]
            ok = (fc.direction == "up") == up
            d["nc_ok"] += ok
            d["nc_tot"] += 1
            b2["ok"] += ok
            b2["tot"] += 1
            tl = bars[t - a.trend_lookback][4] if t - a.trend_lookback >= 0 else bars[0][4]
            key = "with" if (fc.direction == "up") == (bars[t][4] >= tl) else "against"
            trend[key][1] += 1
            trend[key][0] += ok

    print(f"\n================  {symbol} {interval}  (n={n})  ================")
    print(f"{'forecast kind':30s}{'count':>7s}{'%up':>5s}{'nextC':>7s}{'HIT':>6s}{'INVAL':>7s}{'stale':>7s}{'OPEN':>7s}")
    for k, d in sorted(by.items(), key=lambda kv: -kv[1]["n"]):
        nc = f"{d['nc_ok']/d['nc_tot']:.0%}" if d["nc_tot"] else "-"
        print(f"{k:30s}{d['n']:7d}{d['up']/max(d['n'],1)*100:4.0f}%{nc:>7s}"
              f"{d['HIT']:6d}{d['INVALIDATED']:7d}{d['stale']:7d}{d['OPEN']:7d}")
    if none:
        print(f"{'(no forecast)':30s}{none:7d}")
    print(f"next-candle by trend-agreement: with={trend['with'][0]}/{trend['with'][1]}="
          f"{trend['with'][0]/max(trend['with'][1],1):.0%}  "
          f"against={trend['against'][0]}/{trend['against'][1]}={trend['against'][0]/max(trend['against'][1],1):.0%}")
    print("by confidence:")
    for k in ("conf <40%", "conf 40-55%", "conf 55-70%", "conf >=70%"):
        b2 = cf.get(k)
        if not b2 or not b2["n"]:
            continue
        dec = b2["HIT"] + b2["INVALIDATED"]
        nc = f"{b2['ok']/b2['tot']:.0%}" if b2["tot"] else "-"
        hr = f"{b2['HIT']/dec:.0%}" if dec else "n/a (0 resolved)"
        print(f"   {k:12s} n={b2['n']:6d}  next-candle={nc}  target-hit={hr}")
    if hb and ib:
        print(f"   median bars-to-resolution: HIT={st.median(hb):.0f}  INVALIDATED={st.median(ib):.0f}  (horizon={a.resolve})")


if __name__ == "__main__":
    main()
