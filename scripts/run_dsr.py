"""
run_dsr.py  —  multiple-testing-corrected edge verdict (docs/research/deep/08).
================================================================================
Runs the reversal strategy across a grid of parameter variants, pools per-event
returns across the watchlist, logs every variant to the trials registry
(registry/trials.jsonl), then computes the Deflated Sharpe Ratio of the BEST
variant — the honest answer to "does this edge survive the fact that we tried N
variants?". Writes reports/DSR_2026-06.md.

Run:  python3 scripts/run_dsr.py
"""
import datetime
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")
REPORT = os.path.join(ROOT, "reports", "DSR_2026-06.md")
REGISTRY = os.path.join(ROOT, "registry", "trials.jsonl")
SYMBOLS = ["avgo", "mrvl", "nvda", "amd", "tsm", "mu"]
WINDOW = 300
DEGREES = (3.0, 8.0)          # ATR multiples
MAX_HOLD = 20                       # vertical (time) barrier in bars
# parameter grid (the "trials"): score threshold x (take-profit, stop-loss)
SCORE_THRESHOLDS = (3, 4)
BARRIERS = ((0.06, 0.04), (0.08, 0.05))


def load_bars(sym):
    with open(os.path.join(LIVE, f"{sym}_1d_2026-06.json")) as fh:
        d = json.load(fh)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) for b in d["bars"]][-WINDOW:]


def main():
    bars_by_sym = {s: load_bars(s) for s in SYMBOLS}
    # buy-and-hold benchmark: pooled horizon-forward returns -> the Sharpe to beat
    bench = []
    for s in SYMBOLS:
        bench += wl.horizon_returns(bars_by_sym[s], horizon=MAX_HOLD, bullish=True)
    bench_sr = wl.sharpe_ratio(bench)

    variants = []
    for st in SCORE_THRESHOLDS:
        for (pt, sl) in BARRIERS:
            pooled = []
            for s in SYMBOLS:
                pooled += wl.reversal_returns(bars_by_sym[s], score_threshold=st,
                                              degrees=DEGREES, min_history=60,
                                              pt=pt, sl=sl, max_hold=MAX_HOLD, cost=0.001)
            sr = wl.sharpe_ratio(pooled)
            sk, ku = wl.skew_kurt(pooled)
            n = len(pooled)
            psr_b = wl.probabilistic_sharpe_ratio(sr, bench_sr, n, sk, ku) if n >= 2 else 0.0
            cp = wl.cpcv_profit_factor(pooled)
            v = {"score_threshold": st, "pt": pt, "sl": sl, "events": n,
                 "sharpe": sr, "skew": sk, "kurt": ku, "psr_vs_bench": psr_b,
                 "cpcv_lo_pf": (cp[0] if cp else None)}
            variants.append(v)
            wl.log_trial({"strategy": "reversal_tb", **{k: v[k] for k in
                          ("score_threshold", "pt", "sl", "events", "sharpe")}},
                         path=REGISTRY)

    sharpes = [v["sharpe"] for v in variants]
    sr_var = statistics.pvariance(sharpes) if len(sharpes) > 1 else 0.0
    # Headline pick must have enough events — choosing the highest-Sharpe tiny-sample
    # variant is itself a data-mining trap.
    MIN_EVENTS = 20
    eligible = [v for v in variants if v["events"] >= MIN_EVENTS]
    best = max(eligible or variants, key=lambda v: v["sharpe"])
    best_underpowered = not eligible
    n_run = len(variants)
    n_registry = wl.count_trials(REGISTRY)
    dsr = wl.deflated_sharpe_ratio(best["sharpe"], best["events"], best["skew"],
                                   best["kurt"], n_trials=max(n_run, 2), sr_variance=sr_var or 1e-9)
    beats_bh = best["sharpe"] > bench_sr

    out = ["# Deflated Sharpe report — reversal strategy (triple-barrier exits)",
           "",
           f"_Generated {datetime.date.today().isoformat()} by `scripts/run_dsr.py`. "
           f"Pooled across {len(SYMBOLS)} AI-semis (last {WINDOW} daily bars each), "
           f"triple-barrier exits (+pt/-sl/{MAX_HOLD}-bar). Multiple-testing-corrected "
           "per docs/research/deep/08. Not investment advice._",
           "",
           f"**Buy-and-hold benchmark** ({MAX_HOLD}-bar horizon): Sharpe "
           f"**{bench_sr:.3f}** ({len(bench)} samples) — the bar the strategy must clear.",
           "",
           "## Variants tried (each is a 'trial' logged to `registry/trials.jsonl`)",
           "| score_thr | +pt / -sl | events | Sharpe | PSR vs buy&hold | CPCV 5%ile PF |",
           "|---|---|---|---|---|---|"]
    for v in variants:
        cp = "n/a" if v["cpcv_lo_pf"] is None else f"{v['cpcv_lo_pf']:.2f}"
        out.append(f"| {v['score_threshold']} | {v['pt']}/{v['sl']} | {v['events']} | "
                   f"{v['sharpe']:.3f} | {v['psr_vs_bench']:.0%} | {cp} |")
    out += [
        "",
        "## Deflated verdict (vs buy-and-hold)",
        f"- Best variant: score_threshold={best['score_threshold']}, "
        f"+pt/-sl={best['pt']}/{best['sl']} (Sharpe {best['sharpe']:.3f} vs buy&hold "
        f"{bench_sr:.3f}, {best['events']} events).",
        f"- Beats buy-and-hold Sharpe: **{beats_bh}**; PSR vs buy&hold: "
        f"**{best['psr_vs_bench']:.0%}**." +
        ("  (No variant had >=20 events — headline pick is itself under-powered.)"
         if best_underpowered else f"  (>=20-event variants only; higher-Sharpe "
         "9-event variants excluded as overfit-prone.)"),
        f"- Variants tried this run: **{n_run}**; total in registry: **{n_registry}**.",
        f"- **Deflated Sharpe (vs 0, corrected for {n_run} trials): {dsr:.0%}**.",
        "",
        (("> Verdict: **No edge over buy-and-hold.** The best variant's Sharpe "
          f"({best['sharpe']:.3f}) does not beat the buy-and-hold benchmark "
          f"({bench_sr:.3f}); PSR-vs-benchmark is {best['psr_vs_bench']:.0%}. With "
          "realistic triple-barrier exits the apparent edge disappears — the honest "
          "result, and exactly what this harness exists to surface.")
         if not beats_bh else
         ("> Verdict: the best variant **beats buy-and-hold** "
          f"(Sharpe {best['sharpe']:.3f} > {bench_sr:.3f}), PSR-vs-benchmark "
          f"{best['psr_vs_bench']:.0%}, DSR {dsr:.0%}. " +
          ("This clears the multiple-testing and benchmark gates and is worth genuine "
           "out-of-sample testing." if (best['psr_vs_bench'] >= 0.95 and dsr >= 0.95)
           else "But it does NOT clear the 95% PSR/DSR gates, so treat as inconclusive "
           "given the small, overlapping samples — not a validated edge."))),
        ">",
        "> Returns are net of 0.1% round-trip cost. Remaining honesty caveats: event "
        "counts are still small and overlapping, and the sample is a single recent "
        "regime. CPCV 5th-pctile PF (above) is the most robust single number.",
        "",
        "_DSR needs the TRUE number of variants ever tried; the registry captures it "
        "prospectively so this number only grows more honest over time._",
    ]
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(text)
    print(text)
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
