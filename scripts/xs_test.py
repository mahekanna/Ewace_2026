"""xs_test.py — does the wave forecast carry CROSS-SECTIONAL information?

The time-series direction test (reports/FORECAST_BACKTEST_2026-06.md) killed the
forecast: 48%/52% win, Sharpe -0.013/+0.023, worse than always-long. But that
test is long-biased and drift-polluted — every positive number in it is the
equity risk premium, as the report itself says.

This asks a different question with the SAME feature, so the only thing that
changes is the confound: on a given day, does the forecast rank instruments
correctly against EACH OTHER? A dollar-neutral long-short spread has no drift to
capture, so any surviving signal is relative structural information, not beta.

PRE-REGISTERED before looking at any result:
  universe   18 tradeable equities (no indices/FX/crypto/VIX — not comparable)
  feature    signed conviction = +confidence if forecast up, -confidence if down
             (exactly the composite that failed time-series)
  causality  forecast recomputed from bars <= rebalance date only, window=750 so
             every instrument is counted over the same amount of history
  rebalance  every 21 trading days; >= 8 instruments required to score a date
  primary    mean cross-sectional Spearman rank IC vs 21-bar forward return
  PASS       mean IC > 0 AND |t| >= 2.0
  secondary  top-tercile minus bottom-tercile spread > 0 with t >= 2
  trials     3 (horizons 5/21/63 on one feature) — logged, DSR-relevant
  control    scores shuffled within each date; IC must collapse to ~0

Run:  python3 scripts/xs_test.py
"""
import json
import os
import statistics
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl
from wavelib.validation import log_trial, count_trials

LIVE = os.path.join(ROOT, "data", "live")
UNIVERSE = ["amat", "amd", "arm", "asml", "avgo", "jnj", "jpm", "ko", "lrcx",
            "mrvl", "mu", "nvda", "pg", "qcom", "smci", "tsm", "wmt", "xom"]
WINDOW, REBAL, MIN_N = 750, 21, 8
HORIZONS = [5, 21, 63]
PRIMARY_H = 21


def load(sym):
    for snap in ("2026-06", "2026-08"):
        p = os.path.join(LIVE, f"{sym}_1d_{snap}.json")
        if os.path.exists(p):
            b = json.load(open(p))["bars"]
            return [(x["t"], x["o"], x["h"], x["l"], x["c"]) for x in b]
    return None


def day(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).date()


def rank(xs):
    """Average ranks, ties shared."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(ra)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    return None if da == 0 or db == 0 else num / (da * db)


def tstat(xs):
    if len(xs) < 3:
        return 0.0
    sd = statistics.stdev(xs)
    return 0.0 if sd == 0 else statistics.mean(xs) / (sd / len(xs) ** 0.5)


def main():
    data = {}
    for s in UNIVERSE:
        b = load(s)
        if b:
            data[s] = {"bars": b, "idx": {day(x[0]): i for i, x in enumerate(b)}}
    print(f"loaded {len(data)}/{len(UNIVERSE)} instruments")

    # rebalance calendar: every REBAL trading days of the longest series
    spine = max(data.values(), key=lambda d: len(d["bars"]))["bars"]
    dates = [day(x[0]) for x in spine][::REBAL]

    ic = {h: [] for h in HORIZONS}
    ic_ctrl = {h: [] for h in HORIZONS}
    spread = {h: [] for h in HORIZONS}
    bench = {h: [] for h in HORIZONS}
    universe_sizes = []
    scored_dates = []

    for d in dates:
        scores, fwd = {}, {h: {} for h in HORIZONS}
        for s, dd in data.items():
            i = dd["idx"].get(d)
            if i is None or i < WINDOW:
                continue
            bars = dd["bars"][:i + 1]                    # causal: nothing after d
            f = wl.forecast_waves(bars, window=WINDOW)
            if f is None or not f.direction:
                continue
            sgn = 1.0 if f.direction == "up" else -1.0
            c0 = dd["bars"][i][4]
            ok = False
            for h in HORIZONS:
                if i + h < len(dd["bars"]):
                    fwd[h][s] = dd["bars"][i + h][4] / c0 - 1.0
                    ok = True
            if ok:
                scores[s] = sgn * f.confidence
        if len(scores) < MIN_N:
            continue
        scored_dates.append(d)
        universe_sizes.append(len(scores))
        for h in HORIZONS:
            syms = [s for s in scores if s in fwd[h]]
            if len(syms) < MIN_N:
                continue
            sc = [scores[s] for s in syms]
            fr = [fwd[h][s] for s in syms]
            v = spearman(sc, fr)
            if v is not None:
                ic[h].append(v)
            # control: same scores, deterministically permuted (no RNG needed)
            v2 = spearman(sc[1:] + sc[:1], fr)
            if v2 is not None:
                ic_ctrl[h].append(v2)
            # tercile spread, dollar-neutral
            order = sorted(syms, key=lambda s: scores[s])
            k = max(1, len(order) // 3)
            lo, hi = order[:k], order[-k:]
            spread[h].append(sum(fwd[h][s] for s in hi) / len(hi)
                             - sum(fwd[h][s] for s in lo) / len(lo))
            bench[h].append(sum(fr) / len(fr))

    print(f"rebalance dates scored: {len(scored_dates)}  "
          f"({scored_dates[0]} -> {scored_dates[-1]})")
    print(f"universe per date: min {min(universe_sizes)} "
          f"median {int(statistics.median(universe_sizes))} max {max(universe_sizes)}\n")

    print(f"{'H':>4} {'n':>5} {'meanIC':>8} {'t(IC)':>7} {'ctrlIC':>8} "
          f"{'spread%':>9} {'t(sp)':>7} {'bench%':>8}")
    for h in HORIZONS:
        n = len(ic[h])
        if n == 0:
            continue
        print(f"{h:>4} {n:>5} {statistics.mean(ic[h]):>8.4f} {tstat(ic[h]):>7.2f} "
              f"{statistics.mean(ic_ctrl[h]):>8.4f} "
              f"{statistics.mean(spread[h]) * 100:>9.3f} {tstat(spread[h]):>7.2f} "
              f"{statistics.mean(bench[h]) * 100:>8.3f}")

    # overlapping forward windows inflate |t|: consecutive obs share (H/REBAL-1)/
    # (H/REBAL) of their window. Report the deflated figure, not the raw one.
    def adj(h, t):
        return t * (1.0 / max(1.0, h / REBAL)) ** 0.5

    print("\noverlap-adjusted t (H/REBAL overlapping windows):")
    for h in HORIZONS:
        if ic[h]:
            print(f"  H={h:>3}  t(IC) {adj(h, tstat(ic[h])):+.2f}   "
                  f"t(spread) {adj(h, tstat(spread[h])):+.2f}")

    # every horizon is a trial — DSR needs the honest total
    for h in HORIZONS:
        if ic[h]:
            log_trial({"study": "xs_forecast_ic", "date": str(scored_dates[-1]),
                       "feature": "signed_conviction", "horizon": h,
                       "universe": len(data), "n_dates": len(ic[h]),
                       "mean_ic": round(statistics.mean(ic[h]), 5),
                       "t_ic_raw": round(tstat(ic[h]), 3),
                       "t_ic_adj": round(adj(h, tstat(ic[h])), 3),
                       "spread_pct": round(statistics.mean(spread[h]) * 100, 4),
                       "t_spread_adj": round(adj(h, tstat(spread[h])), 3),
                       "result": "fail"})
    print(f"\ntrials logged; registry total now {count_trials()}")

    m, t = statistics.mean(ic[PRIMARY_H]), tstat(ic[PRIMARY_H])
    ms, ts = statistics.mean(spread[PRIMARY_H]), tstat(spread[PRIMARY_H])
    print(f"\nPRE-REGISTERED GATE (H={PRIMARY_H}): mean IC > 0 and |t| >= 2.0")
    print(f"  mean IC {m:+.4f}, t = {t:+.2f}  -> "
          f"{'PASS' if (m > 0 and abs(t) >= 2.0) else 'FAIL'}")
    print(f"  secondary spread {ms*100:+.3f}%, t = {ts:+.2f}  -> "
          f"{'PASS' if (ms > 0 and ts >= 2.0) else 'FAIL'}")


if __name__ == "__main__":
    main()
