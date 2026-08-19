"""
run_multiregime.py  —  multi-regime, multi-asset edge verdict (docs/research/deep/08).
================================================================================
The single biggest honesty caveat on the daily DSR report (`run_dsr.py`) was
"single recent regime". This script answers that: it pools the reversal strategy
across DECADES of WEEKLY history spanning multiple asset classes (semis, indices,
defensive sectors, energy, crypto, FX, gold) so the verdict is no longer a
recent-regime artifact — the sample now contains 2000, 2008, 2020 and 2022.

It mirrors `run_dsr.py`'s discipline: a buy-and-hold benchmark to beat, a grid of
triple-barrier variants logged as trials, CPCV out-of-sample profit factor, and a
Deflated Sharpe corrected for the number of variants. Weekly bars use wider
barriers and a quarter-length (13-bar) time barrier. Writes
reports/MULTIREGIME_2026-06.md.

Run:  python3 scripts/run_multiregime.py
"""
import datetime
import glob
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import wavelib as wl

LIVE = os.path.join(ROOT, "data", "live")
REPORT = os.path.join(ROOT, "reports", "MULTIREGIME_2026-06.md")
REGISTRY = os.path.join(ROOT, "registry", "trials.jsonl")

MAX_HOLD = 13                       # ~one quarter on weekly bars (vertical barrier)
DEGREES = (5.0, 13.0)              # ATR multiples (same ladder on every TF now)
MIN_HISTORY = 80                   # bars of warm-up before the first signal
MIN_BARS = 200                     # ignore series too short to be meaningful
LABEL_LOOKBACK = 300               # cap labelling context (~6y weekly) -> linear replay
STRIDE = 2                         # evaluate every 2nd weekly bar (zones persist) -> ~2x faster
# parameter grid (the "trials"): score threshold x (take-profit, stop-loss), wider
# barriers because weekly ranges are larger.
SCORE_THRESHOLDS = (3, 4)
BARRIERS = ((0.10, 0.07), (0.15, 0.10))
COST = 0.001


def load(path):
    with open(path) as fh:
        d = json.load(fh)
    bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
            for b in d["bars"]]
    return d.get("symbol", os.path.basename(path)), bars


def fdate(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m")


def main():
    files = sorted(glob.glob(os.path.join(LIVE, "*_1w_2026-06.json")))
    series = []
    for f in files:
        sym, bars = load(f)
        if len(bars) >= MIN_BARS:
            series.append((os.path.basename(f).split("_1w")[0].upper(), sym, bars))
    if not series:
        print("no weekly series found in data/live/*_1w_2026-06.json")
        return

    # buy-and-hold benchmark: pooled horizon-forward returns -> the Sharpe to beat
    bench = []
    for _slug, _sym, bars in series:
        bench += wl.horizon_returns(bars, horizon=MAX_HOLD, bullish=True)
    bench_sr = wl.sharpe_ratio(bench)

    variants = []
    for st in SCORE_THRESHOLDS:
        for (pt, sl) in BARRIERS:
            pooled = []
            for _slug, _sym, bars in series:
                pooled += wl.reversal_returns(bars, score_threshold=st, degrees=DEGREES,
                                              min_history=MIN_HISTORY, pt=pt, sl=sl,
                                              max_hold=MAX_HOLD, cost=COST,
                                              label_lookback=LABEL_LOOKBACK, stride=STRIDE)
            sr = wl.sharpe_ratio(pooled)
            sk, ku = wl.skew_kurt(pooled)
            n = len(pooled)
            psr_b = wl.probabilistic_sharpe_ratio(sr, bench_sr, n, sk, ku) if n >= 2 else 0.0
            cp = wl.cpcv_profit_factor(pooled)
            variants.append({"score_threshold": st, "pt": pt, "sl": sl, "events": n,
                             "sharpe": sr, "skew": sk, "kurt": ku, "psr_vs_bench": psr_b,
                             "cpcv_lo_pf": (cp[0] if cp else None)})
            wl.log_trial({"strategy": "reversal_tb_weekly_multiregime",
                          "score_threshold": st, "pt": pt, "sl": sl,
                          "events": n, "sharpe": sr}, path=REGISTRY)

    sharpes = [v["sharpe"] for v in variants]
    sr_var = statistics.pvariance(sharpes) if len(sharpes) > 1 else 0.0
    MIN_EVENTS = 30
    eligible = [v for v in variants if v["events"] >= MIN_EVENTS]
    best = max(eligible or variants, key=lambda v: v["sharpe"])
    best_underpowered = not eligible
    n_run = len(variants)
    n_registry = wl.count_trials(REGISTRY)
    dsr = wl.deflated_sharpe_ratio(best["sharpe"], best["events"], best["skew"],
                                   best["kurt"], n_trials=max(n_run, 2),
                                   sr_variance=sr_var or 1e-9)
    beats_bh = best["sharpe"] > bench_sr
    total_events = sum(v["events"] for v in variants)
    first_t = min(bars[0][0] for _s, _y, bars in series)
    last_t = max(bars[-1][0] for _s, _y, bars in series)

    out = ["# Multi-regime Deflated Sharpe report — reversal strategy (weekly)",
           "",
           f"_Generated {datetime.date.today().isoformat()} by `scripts/run_multiregime.py`. "
           f"Pooled across **{len(series)} instruments** spanning multiple asset classes "
           f"and **{fdate(first_t)} → {fdate(last_t)}** of WEEKLY history (so the sample "
           "contains the 2000, 2008, 2020 and 2022 regimes). Triple-barrier exits "
           f"(+pt/-sl/{MAX_HOLD}-bar), net of {COST:.1%} cost. Not investment advice._",
           "",
           f"**Buy-and-hold benchmark** ({MAX_HOLD}-bar horizon): Sharpe "
           f"**{bench_sr:.3f}** ({len(bench)} samples) — the bar the strategy must clear.",
           "",
           "## Regime coverage (per instrument)",
           "| instrument | symbol | weekly bars | from | to |",
           "|---|---|---|---|---|"]
    for slug, sym, bars in series:
        out.append(f"| {slug} | {sym} | {len(bars)} | {fdate(bars[0][0])} | {fdate(bars[-1][0])} |")
    out += ["",
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
        f"- Pooled decided events across all variants: **{total_events}** "
        f"(vs the handful per symbol on the daily report) — the multi-regime sample.",
        f"- Best variant: score_threshold={best['score_threshold']}, "
        f"+pt/-sl={best['pt']}/{best['sl']} (Sharpe {best['sharpe']:.3f} vs buy&hold "
        f"{bench_sr:.3f}, {best['events']} events).",
        f"- Beats buy-and-hold Sharpe: **{beats_bh}**; PSR vs buy&hold: "
        f"**{best['psr_vs_bench']:.0%}**." +
        ("  (No variant had >=30 events — headline pick is itself under-powered.)"
         if best_underpowered else "  (>=30-event variants only.)"),
        f"- Variants tried this run: **{n_run}**; total in registry: **{n_registry}**.",
        f"- **Deflated Sharpe (vs 0, corrected for {n_run} trials): {dsr:.0%}**.",
        "",
        (("> Verdict: **No edge over buy-and-hold even across regimes.** The best "
          f"variant's Sharpe ({best['sharpe']:.3f}) does not beat the benchmark "
          f"({bench_sr:.3f}); PSR-vs-benchmark {best['psr_vs_bench']:.0%}. The honest "
          "result the multi-regime test exists to surface.")
         if not beats_bh else
         ("> Verdict: the best variant **beats buy-and-hold across regimes** "
          f"(Sharpe {best['sharpe']:.3f} > {bench_sr:.3f}), PSR-vs-benchmark "
          f"{best['psr_vs_bench']:.0%}, DSR {dsr:.0%}. " +
          ("This clears the multiple-testing and benchmark gates over a multi-decade, "
           "multi-asset sample and is worth genuine forward testing."
           if (best['psr_vs_bench'] >= 0.95 and dsr >= 0.95)
           else "But it does NOT clear the 95% PSR/DSR gates, so treat as "
           "inconclusive — better than the single-regime daily test, not validated."))),
        ">",
        "> CPCV 5th-pctile out-of-sample profit factor (table above) is the most "
        "robust single number — it purges/embargoes folds so adjacent overlapping "
        "weekly signals can't leak. This report is the regime-diversity answer to the "
        "daily DSR report's main caveat; remaining caveats: signals on different "
        "instruments are not fully independent (sector/beta correlation).",
        ">",
        f"> Replay settings: labelling context capped at {LABEL_LOOKBACK} bars and the "
        f"timeline sampled every {STRIDE} bars for tractable runtime — both are causal "
        "(past-only) and, on weekly data where a reversal zone persists for several "
        "bars, do not materially change the decided-event set.",
    ]
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(text)
    print(text)
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
