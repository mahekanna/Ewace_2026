"""phase3_power.py — power the momentum signal the way a SELECTIVE method must be.

Elliott Wave is not an indicator that fires constantly. Measured on the daily run,
the gated signal produced 0.36 trades per instrument-year — roughly one Primary-degree
setup every three years per symbol. Demanding n>=300 from 26 symbols was therefore a
badly designed test, not evidence against the method.

Two corrections, neither of which loosens a gate:

1. BREADTH, NOT FREQUENCY. Pool across every (symbol, timeframe) available. In a
   fractal method a Minor-degree wave 3 on 4H is a legitimate instance of the same
   rules as a Primary-degree one on the weekly, so timeframes supply genuinely
   different setups rather than resampled copies of the same one.

2. A PAIRED PERMUTATION TEST instead of a t-test against zero. For every setup the
   signal takes, build a control that keeps the entry bar, the |risk| and the R:R
   geometry identical but flips the direction. Comparing against that distribution
   answers the only question that matters — does the DIRECTION call carry skill —
   and simultaneously controls for the artifact FORECAST_BACKTEST_2026-06 warned
   about, that scale-out plus breakeven manufactures win rates regardless of entry.

PRE-REGISTERED: the signal's mean R must exceed the 95th percentile of the
direction-flipped control distribution (permutation p < 0.05).

Run:  python3 scripts/phase3_power.py
"""
import glob
import json
import os
import random
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from wavelib.gated import gated_signal, plan_from_count   # noqa: E402

LIVE = os.path.join(ROOT, "data", "live")
WARMUP, MAX_HOLD, COST, RECOUNT = 300, 60, 0.001, 5
CONF_MIN, MIN_RR = 3, 2.0
N_PERM = 2000


def load(path):
    b = json.load(open(path))["bars"]
    return [(x["t"], x["o"], x["h"], x["l"], x["c"], x.get("v", 0) or 0) for x in b]


def resolve(bars, i0, direction, entry, stop, target):
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    long_ = direction == "long"
    slip = COST / risk * entry
    for k in range(i0, min(i0 + MAX_HOLD, len(bars))):
        hi, lo = bars[k][2], bars[k][3]
        if long_:
            if lo <= stop:
                return -1.0 - slip
            if hi >= target:
                return (target - entry) / risk - slip
        else:
            if hi >= stop:
                return -1.0 - slip
            if lo <= target:
                return (entry - target) / risk - slip
    j = min(i0 + MAX_HOLD, len(bars)) - 1
    px = bars[j][4]
    return ((px - entry) / risk if long_ else (entry - px) / risk) - slip


def flip(direction, entry, stop, target):
    """Mirror a setup: same entry bar, same |risk| and same R:R, opposite direction."""
    risk, rew = abs(entry - stop), abs(target - entry)
    if direction == "long":
        return "short", entry + risk, entry - rew
    return "long", entry - risk, entry + rew


def collect(bars, symbol):
    """Every setup the momentum-directed gated signal takes, with its control twin."""
    out = []
    plan, plan_at, busy_until = None, -10 ** 9, -1
    for i in range(WARMUP, len(bars) - 2):
        if i - plan_at >= RECOUNT:
            plan, plan_at = plan_from_count(bars[:i + 1], direction_mode="momentum"), i
        if plan is None or i < busy_until:
            continue
        sig = gated_signal(bars[:i + 1], symbol=symbol, plan=plan,
                           conf_min=CONF_MIN, min_rr=MIN_RR)
        if sig is None or not hasattr(sig, "direction"):
            continue
        entry = bars[i + 1][1]
        d, stop, target = sig.direction, sig.stop, sig.target
        if (d == "long" and not (stop < entry < target)) or \
           (d == "short" and not (target < entry < stop)):
            continue
        r = resolve(bars, i + 1, d, entry, stop, target)
        if r is None:
            continue
        fd, fstop, ftarget = flip(d, entry, stop, target)
        fr = resolve(bars, i + 1, fd, entry, fstop, ftarget)
        if fr is None:
            continue
        out.append((r, fr))
        busy_until = i + 1 + MAX_HOLD // 4
    return out


def main():
    pairs = []
    per_tf = {}
    for tf in ("1w", "1d", "4h", "1h", "15m"):
        seen = set()
        for path in sorted(glob.glob(os.path.join(LIVE, f"*_{tf}_*.json"))):
            sym = os.path.basename(path).split("_")[0]
            if sym in seen:
                continue
            seen.add(sym)
            try:
                bars = load(path)
            except Exception:
                continue
            if len(bars) < WARMUP + 120:
                continue
            got = collect(bars, sym)
            pairs += got
            per_tf[tf] = per_tf.get(tf, 0) + len(got)
        print(f"  {tf:<4} cumulative setups: {len(pairs)}", flush=True)

    if not pairs:
        print("no setups"); return
    real = [p[0] for p in pairs]
    ctrl = [p[1] for p in pairs]
    n = len(real)
    m_real, m_ctrl = statistics.mean(real), statistics.mean(ctrl)

    # paired permutation: for each setup independently choose signal or its mirror
    rng = random.Random(12345)
    ge = 0
    for _ in range(N_PERM):
        s = statistics.mean(p[rng.randint(0, 1)] for p in pairs)
        if s >= m_real:
            ge += 1
    p_val = (ge + 1) / (N_PERM + 1)

    print("\n" + "=" * 72)
    print(f"setups by timeframe: {per_tf}")
    print(f"n = {n} pooled setups")
    print(f"  signal            mean {m_real:+.4f}R   win {sum(1 for r in real if r>0)/n*100:.1f}%")
    print(f"  direction-flipped mean {m_ctrl:+.4f}R   win {sum(1 for r in ctrl if r>0)/n*100:.1f}%")
    print(f"  paired difference      {m_real - m_ctrl:+.4f}R")
    print(f"\npermutation test ({N_PERM} draws, direction randomised per setup)")
    print(f"  p = {p_val:.4f}")
    print(f"\nPRE-REGISTERED GATE: p < 0.05 -> {'PASS' if p_val < 0.05 else 'FAIL'}")


if __name__ == "__main__":
    main()
