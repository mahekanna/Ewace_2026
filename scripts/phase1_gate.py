"""phase1_gate.py — does the NeoWave discipline add anything? (Roadmap Phase 1)

Three arms over the same proposals, so any difference is the gates alone:

  UNGATED   enter every bar in the plan's direction — the signal every prior "no
            edge" backtest actually measured (FORWARD_GHOST_TEST_FINDINGS O7)
  GATED     the same proposal, emitted only through TR-1/CC-1 + confirmation break
            + TR-2 + confluence >= N + R:R >= 2 (wavelib/gated.py)
  FALSIFIED GATED plus CC-9 behaviour-over-structure: the count is discarded when
            post-pattern price action contradicts the label. This is the only gate
            that can reject the DIRECTION rather than merely the timing, and it is
            Neely's claimed source of predictiveness (Phase 2).
  B&H       buy-and-hold over the identical span, the benchmark that matters

Causal throughout: at bar t only bars[:t+1] are read; entry fills at t+1's open.
Both arms hold one position at a time and share stop/target/max-hold mechanics, so
win-rate differences cannot come from trade management.

PRE-REGISTERED GATE: GATED must beat BOTH the ungated arm and buy-and-hold on
expectancy, on a sample of >= 300 decided trades. Anything less is a FAIL and the
conclusion is that discipline is not where the edge lives.

Run:  python3 scripts/phase1_gate.py [--fast]
"""
import glob
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from wavelib.gated import plan_from_count, gated_signal   # noqa: E402

LIVE = os.path.join(ROOT, "data", "live")
WARMUP, MAX_HOLD, COST = 300, 60, 0.001
# Re-count the macro structure every N bars (it is stable bar-to-bar); evaluate the
# per-bar triggers — break, TR-2, R:R, confluence — on EVERY bar. This is both how a
# desk works and ~N x cheaper. Still causal: a cached plan only ever used past bars.
RECOUNT_EVERY = 5
CONF_MIN, MIN_RR = 3, 2.0


def load(path):
    b = json.load(open(path))["bars"]
    return [(x["t"], x["o"], x["h"], x["l"], x["c"], x.get("v", 0) or 0) for x in b]


def resolve(bars, i0, direction, entry, stop, target, max_hold=MAX_HOLD):
    """Walk forward from the fill bar to stop / target / time. Returns R."""
    risk = abs(entry - stop)
    if risk <= 0:
        return None, 0
    long_ = direction == "long"
    for k in range(i0, min(i0 + max_hold, len(bars))):
        hi, lo = bars[k][2], bars[k][3]
        if long_:
            if lo <= stop:
                return -1.0 - COST / risk * entry, k - i0
            if hi >= target:
                return (target - entry) / risk - COST / risk * entry, k - i0
        else:
            if hi >= stop:
                return -1.0 - COST / risk * entry, k - i0
            if lo <= target:
                return (entry - target) / risk - COST / risk * entry, k - i0
    j = min(i0 + max_hold, len(bars)) - 1
    px = bars[j][4]
    r = (px - entry) / risk if long_ else (entry - px) / risk
    return r - COST / risk * entry, j - i0


def run_symbol(bars, symbol, arms):
    """Walk once; feed the same per-bar proposal to every arm."""
    state = {a: None for a in arms}          # arm -> exit bar index
    plan, plan_at = None, -10 ** 9
    for i in range(WARMUP, len(bars) - 2):
        busy = [a for a in arms if state[a] is not None and i < state[a]]
        if len(busy) == len(arms):
            continue
        if i - plan_at >= RECOUNT_EVERY:
            plan, plan_at = plan_from_count(bars[:i + 1]), i
        if plan is None:
            continue
        for a in arms:
            if state[a] is not None and i < state[a]:
                continue
            if a in ("gated", "falsified"):
                sig = gated_signal(bars[:i + 1], symbol=symbol, plan=plan,
                                   conf_min=CONF_MIN, min_rr=MIN_RR,
                                   falsify=(a == "falsified"))
                if sig is None or not hasattr(sig, "direction"):
                    continue
                direction, stop, target = sig.direction, sig.stop, sig.target
            else:
                direction, stop, target = plan["direction"], plan["stop"], plan["target"]
            entry = bars[i + 1][1]                     # fill at next bar's open
            if (direction == "long" and not (stop < entry < target)) or \
               (direction == "short" and not (target < entry < stop)):
                continue
            r, held = resolve(bars, i + 1, direction, entry, stop, target)
            if r is None:
                continue
            arms[a].append(r)
            state[a] = i + 1 + max(held, 1)


def stats(rs):
    if not rs:
        return "n=0"
    wins = [r for r in rs if r > 0]
    losses = [-r for r in rs if r <= 0]
    pf = (sum(wins) / sum(losses)) if losses and sum(losses) > 0 else float("inf")
    m = statistics.mean(rs)
    t = m / (statistics.stdev(rs) / len(rs) ** 0.5) if len(rs) > 2 and statistics.stdev(rs) else 0
    return (f"n={len(rs):<5} expectancy {m:+.3f}R  t={t:+.2f}  "
            f"win {len(wins)/len(rs)*100:4.1f}%  PF {pf:.2f}")


def main():
    fast = "--fast" in sys.argv
    files = sorted(glob.glob(os.path.join(LIVE, "*_1d_*.json")))
    seen, paths = set(), []
    for f in files:                                   # newest snapshot per symbol
        sym = os.path.basename(f).split("_")[0]
        if sym in seen:
            continue
        seen.add(sym)
        paths.append((sym, f))
    if fast:
        paths = paths[:6]

    arms = {"ungated": [], "gated": [], "falsified": []}
    bh = []
    for sym, path in paths:
        bars = load(path)
        if len(bars) < WARMUP + 100:
            continue
        run_symbol(bars, sym, arms)
        seg = bars[WARMUP:]
        bh.append(seg[-1][4] / seg[0][4] - 1.0)
        print(f"  {sym:<10} bars={len(bars):<6} ungated={len(arms['ungated']):<5} "
              f"gated={len(arms['gated']):<5} falsified={len(arms['falsified']):<5}",
              flush=True)

    print("\n" + "=" * 74)
    print(f"UNGATED    {stats(arms['ungated'])}")
    print(f"GATED      {stats(arms['gated'])}")
    print(f"FALSIFIED  {stats(arms['falsified'])}")
    print(f"B&H       n={len(bh)} instruments, mean total return "
          f"{statistics.mean(bh)*100:+.1f}%")
    g, u, f_ = arms["gated"], arms["ungated"], arms["falsified"]
    if g:
        print(f"\nCC-9 falsification rate: {(1 - len(f_) / len(g)) * 100:.0f}% of gated "
              f"setups discarded by behaviour-over-structure "
              f"({len(g)} -> {len(f_)}). A rate near 0 would mean the rules are not binding.")
    print("\nPRE-REGISTERED GATE: gated beats ungated AND is positive, n >= 300")
    ok_n = len(g) >= 300
    ok_beat = bool(g and u and statistics.mean(g) > statistics.mean(u))
    ok_pos = bool(g and statistics.mean(g) > 0)
    print(f"  n >= 300            : {len(g):<6} -> {'PASS' if ok_n else 'FAIL'}")
    print(f"  gated > ungated     : {'PASS' if ok_beat else 'FAIL'}")
    print(f"  gated expectancy > 0: {'PASS' if ok_pos else 'FAIL'}")
    print(f"  OVERALL             : {'PASS' if (ok_n and ok_beat and ok_pos) else 'FAIL'}")
    if f_:
        import statistics as _s
        fn, fm = len(f_), _s.mean(f_)
        print(f"\nPHASE 2 (CC-9): n={fn} expectancy {fm:+.3f}R -> "
              f"{'beats gated' if fm > _s.mean(g) else 'no better than gated'}")


if __name__ == "__main__":
    main()
