"""
forward_diag.py  —  WHY does the ghost forward forecast have no edge?
====================================================================
Read-only diagnostic that walks the same causal steps as forward_test.py and
breaks the forecast down by (1) forecast TYPE and (2) the engine's own CONFIDENCE,
then checks next-candle direction, target-hit, and resolution speed for each.

It does not modify the engine or any data. Run:
  python3 scripts/forward_diag.py [avgo mrvl ...]      (default: avgo mrvl)

Backs the observations in docs/FORWARD_GHOST_TEST_FINDINGS.md.
"""
import json, os, sys, statistics as st
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import wavelib as wl

ROLL, RESOLVE = 400, 32


def load(sym):
    d = json.load(open(os.path.join(ROOT, "data", "live", f"{sym}_15m_2026-06.json")))
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]


def resolve(fc, future, price):
    """Same classification forward_test uses (stale / HIT / INVALIDATED / OPEN)."""
    if not fc or not fc.targets:
        return "no-forecast", 0
    up = fc.direction == "up"
    tgt = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
    inv = fc.invalidation
    if up and not (tgt > price and inv < price):
        return "stale", 0
    if (not up) and not (tgt < price and inv > price):
        return "stale", 0
    for i, b in enumerate(future):
        hi, lo = b[2], b[3]
        if up:
            if lo <= inv:
                return "INVALIDATED", i + 1
            if hi >= tgt:
                return "HIT", i + 1
        else:
            if hi >= inv:
                return "INVALIDATED", i + 1
            if lo <= tgt:
                return "HIT", i + 1
    return "OPEN", RESOLVE


def cat(nw):
    if nw.startswith("new impulse"):
        return "new-impulse (trend-resume)"
    if nw.startswith("corrective"):
        return "corrective A-B-C (counter-trend)"
    if nw.startswith("post-triangle"):
        return "triangle thrust"
    return "other"


def bucket(c):
    return ("conf <40%" if c < 0.40 else "conf 40-55%" if c < 0.55
            else "conf 55-70%" if c < 0.70 else "conf >=70%")


def run(sym):
    bars = load(sym); n = len(bars)
    by = defaultdict(lambda: defaultdict(int))
    cf = defaultdict(lambda: {"n": 0, "ok": 0, "tot": 0, "HIT": 0, "INVALIDATED": 0})
    trend = {"with": [0, 0], "against": [0, 0]}
    hb, ib = [], []
    none = 0
    for t in range(ROLL, n - RESOLVE):
        fc = wl.forecast_waves(bars[:t + 1], window=ROLL)
        if not fc:
            none += 1
            continue
        c, d = cat(fc.next_wave), by[cat(fc.next_wave)]
        d["n"] += 1
        d["up"] += 1 if fc.direction == "up" else 0
        o, nb = resolve(fc, bars[t + 1:t + 1 + RESOLVE], bars[t][4])
        d[o] += 1
        b2 = cf[bucket(fc.confidence)]; b2["n"] += 1
        if o in ("HIT", "INVALIDATED"):
            b2[o] += 1
            (hb if o == "HIT" else ib).append(nb)
        if t + 1 < n:
            up = bars[t + 1][4] >= bars[t][4]
            ok = (fc.direction == "up") == up
            d["nc_ok"] += ok; d["nc_tot"] += 1
            b2["ok"] += ok; b2["tot"] += 1
            k = "with" if (fc.direction == "up") == (bars[t][4] >= bars[t - 20][4]) else "against"
            trend[k][1] += 1; trend[k][0] += ok
    print(f"\n================  {sym.upper()}  (n={n})  ================")
    print(f"{'forecast type':36s}{'count':>7s}{'%up':>5s}{'nextC':>7s}{'HIT':>6s}{'INVAL':>7s}{'stale':>7s}{'OPEN':>7s}")
    for c, d in sorted(by.items(), key=lambda kv: -kv[1]["n"]):
        nc = f"{d['nc_ok']/d['nc_tot']:.0%}" if d["nc_tot"] else "-"
        print(f"{c:36s}{d['n']:7d}{d['up']/d['n']*100:4.0f}%{nc:>7s}{d['HIT']:6d}{d['INVALIDATED']:7d}{d['stale']:7d}{d['OPEN']:7d}")
    print(f"{'(no clean count)':36s}{none:7d}")
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
        print(f"   {k:12s} n={b2['n']:5d}  next-candle={nc}  target-hit={hr}")
    if hb and ib:
        print(f"   median bars-to-resolution: HIT={st.median(hb):.0f}  INVALIDATED={st.median(ib):.0f}  (horizon={RESOLVE})")


def main():
    syms = [a.lower() for a in sys.argv[1:]] or ["avgo", "mrvl"]
    for s in syms:
        run(s)


if __name__ == "__main__":
    main()
