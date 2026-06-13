"""
forward_wave3.py  —  ghost-feeding forward test of the WAVE-3 entry (the real trade).
====================================================================================
Unlike forward_test.py (which evaluates the every-candle next-leg projection), this
tests `wavelib.wave3.wave3_signal`: a selective, confirmation-triggered, risk-defined
wave-3 entry. At each candle the signal is built from bars <= t only; when it fires
(price breaks the wave-1 extreme out of a valid wave-1/wave-2 structure) the trade is
ghost-fed forward to a stop (wave-2 extreme) or the wave-3 target, one position at a
time. Reports expectancy in R — the metric that matters for an asymmetric setup.

Run:  python3 scripts/forward_wave3.py [SYM] [TF] [MAX_HOLD] [PCT]
      python3 scripts/forward_wave3.py avgo 15m 96 0.02
"""
import json
import os
import statistics
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")


def load(sym, tf):
    d = json.load(open(os.path.join(LIVE, f"{sym}_{tf}_2026-06.json")))
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0) for b in d["bars"]]


def dt(t):
    return datetime.fromtimestamp(t, tz=timezone.utc)


def resolve(sig, future):
    """Single-target ghost-feed; return (R_multiple, outcome, bars_held). Stop before
    target within a bar (conservative)."""
    entry, stop = sig.entry, sig.stop
    t1 = sig.targets[0][1]
    long = sig.direction == "long"
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    for i, b in enumerate(future):
        hi, lo = b[2], b[3]
        if long:
            if lo <= stop:
                return -1.0, "STOP", i + 1
            if hi >= t1:
                return (t1 - entry) / risk, "TARGET", i + 1
        else:
            if hi >= stop:
                return -1.0, "STOP", i + 1
            if lo <= t1:
                return (entry - t1) / risk, "TARGET", i + 1
    if future:                                   # time exit at last close
        last = future[-1][4]
        r = ((last - entry) if long else (entry - last)) / risk
        return r, "TIME", len(future)
    return None


def resolve_scaleout(sig, future):
    """Rule-faithful management (C-1/E-5/E-6): take 50% at T1 (1.618x), move stop to
    breakeven, run the rest to T2 (2.618x). S&B TIME BUDGET = 3x wave-1 duration
    (doc 02 §2.3) replaces any fixed bar count. Returns (R, outcome, bars_held)."""
    entry, stop, t1, t2 = sig.entry, sig.stop, sig.targets[0][1], sig.t2
    long = sig.direction == "long"
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    budget = min(len(future), 3 * max(sig.w1_bars, 1))   # S&B time, not 96 bars
    booked, rem, cur_stop, hit_t1 = 0.0, 1.0, stop, False
    for i in range(budget):
        b = future[i]
        hi, lo = b[2], b[3]
        adverse = (lo <= cur_stop) if long else (hi >= cur_stop)
        if adverse:
            booked += rem * (cur_stop - entry) / risk * (1 if long else -1)
            return booked, ("PARTIAL" if hit_t1 else "STOP"), i + 1
        reach_t1 = (hi >= t1) if long else (lo <= t1)
        if not hit_t1 and reach_t1:
            booked += 0.5 * (t1 - entry) / risk * (1 if long else -1)
            rem, hit_t1, cur_stop = 0.5, True, entry           # 50% off, stop -> breakeven
        reach_t2 = (hi >= t2) if long else (lo <= t2)
        if hit_t1 and reach_t2:
            booked += rem * (t2 - entry) / risk * (1 if long else -1)
            return booked, "WIN", i + 1
    if budget:                                               # time-budget exit at close
        last = future[budget - 1][4]
        booked += rem * (last - entry) / risk * (1 if long else -1)
        return booked, ("PARTIAL" if hit_t1 else "TIME"), budget
    return None


def main():
    sym = (sys.argv[1] if len(sys.argv) > 1 else "avgo").lower()
    tf = (sys.argv[2] if len(sys.argv) > 2 else "15m").lower()
    max_hold = int(sys.argv[3]) if len(sys.argv) > 3 else 96
    pct = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
    strict = "strict" in sys.argv                # rule-faithful signal + scale-out + S&B time
    bars = load(sym, tf)
    n = len(bars)
    ROLL = 400                                   # rolling window for the signal (bounds cost)
    trades = []
    t = 60
    while t < n - 1:
        if strict:
            sig = wl.wave3_signal_strict(bars[max(0, t - ROLL):t + 1], pct=pct)
        else:
            sig = wl.wave3_signal(bars[max(0, t - ROLL):t + 1], pct=pct)
        if sig is None:
            t += 1
            continue
        horizon = max(max_hold, 3 * getattr(sig, "w1_bars", max_hold) + 5)
        future = bars[t + 1:t + 1 + horizon]
        res = resolve_scaleout(sig, future) if strict else resolve(sig, future)
        if res is None:
            t += 1
            continue
        r, outcome, held = res
        trades.append({"t": bars[t][0], "dir": sig.direction, "r": r, "outcome": outcome,
                       "rr": sig.reward_risk, "held": held, "entry": sig.entry})
        t += held + 1                            # one position at a time

    out = [f"# Forward test — WAVE-3 entry (confirmation-triggered) — {sym.upper()} {tf}",
           "",
           f"_Causal ghost-feed of `wave3_signal` over {n} bars "
           f"({dt(bars[0][0]):%Y-%m-%d} → {dt(bars[-1][0]):%Y-%m-%d}); stop=wave-2 extreme, "
           f"target=1.618x wave-1, " + ("STRICT (pattern-ID + >=3 confluence strands + R:R>=2 + S&B-time scale-out)" if strict else f"max_hold={max_hold}, EWO-gated") + f", pct={pct}. "
           "Expectancy in R is the metric. Not advice._", ""]
    if not trades:
        out.append("**No wave-3 signals fired** (structure/confirmation/momentum filters too tight "
                   "for this data/scale).")
        print("\n".join(out))
        open(os.path.join(ROOT, "reports", f"FORWARD_WAVE3_{'STRICT_' if strict else ''}{sym.upper()}_{tf}.md"), "w").write("\n".join(out) + "\n")
        return
    rs = [x["r"] for x in trades]
    wins = [x for x in rs if x > 0]
    longs = sum(1 for x in trades if x["dir"] == "long")
    target = sum(1 for x in trades if x["outcome"] == "TARGET")
    gross_w = sum(x for x in rs if x > 0)
    gross_l = -sum(x for x in rs if x < 0)
    pf = gross_w / gross_l if gross_l else float("inf")
    out += [
        "## Summary",
        f"- **Signals (trades): {len(trades)}**  ({longs} long / {len(trades)-longs} short); "
        f"reached target {target}, stopped/time the rest.",
        f"- **Expectancy: {statistics.mean(rs):+.2f} R per trade**  (the headline number).",
        f"- Win rate: {len(wins)/len(trades):.0%}  ·  profit factor {pf:.2f}  ·  "
        f"median planned R:R {statistics.median(x['rr'] for x in trades):.2f}.",
        f"- Total R: {sum(rs):+.1f}  ·  avg bars held {statistics.mean(x['held'] for x in trades):.0f}.",
        "",
        "## Read",
        ("> **Positive expectancy.** The wave-3 entry (tight wave-2 stop, far wave-3 target) "
         f"shows {statistics.mean(rs):+.2f}R over {len(trades)} confirmation-triggered trades — "
         "the asymmetric, selective setup the next-leg projection never tested. Worth a "
         "multi-symbol confirm and live forward run."
         if statistics.mean(rs) > 0 else
         "> **No edge.** Even the proper wave-3 entry (confirmation break, structural stop, "
         f"1.618x target, EWO-gated) is {statistics.mean(rs):+.2f}R over {len(trades)} trades — "
         "not positive. The selective, asymmetric, textbook setup does not beat random here."),
        "",
        "## Trade log (first 25)",
        "| time | dir | R:R | outcome | R | held |",
        "|---|---|---|---|---|---|"]
    for x in trades[:25]:
        out.append(f"| {dt(x['t']):%Y-%m-%d %H:%M} | {x['dir']} | {x['rr']:.2f} | "
                   f"{x['outcome']} | {x['r']:+.2f} | {x['held']} |")
    rep = os.path.join(ROOT, "reports", f"FORWARD_WAVE3_{'STRICT_' if strict else ''}{sym.upper()}_{tf}.md")
    os.makedirs(os.path.dirname(rep), exist_ok=True)
    open(rep, "w").write("\n".join(out) + "\n")
    print("\n".join(out[:14]))
    print(f"\nwrote {rep}")


if __name__ == "__main__":
    main()
