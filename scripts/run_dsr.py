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
DEGREES = (0.05, 0.10)
# parameter grid (the "trials")
SCORE_THRESHOLDS = (3, 4)
MIN_REVERSALS = (0.04, 0.06)


def load_bars(sym):
    with open(os.path.join(LIVE, f"{sym}_1d_2026-06.json")) as fh:
        d = json.load(fh)
    return [(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) for b in d["bars"]][-WINDOW:]


def main():
    bars_by_sym = {s: load_bars(s) for s in SYMBOLS}
    variants = []
    for st in SCORE_THRESHOLDS:
        for mr in MIN_REVERSALS:
            pooled = []
            for s in SYMBOLS:
                pooled += wl.reversal_returns(bars_by_sym[s], score_threshold=st,
                                              min_reversal_pct=mr, degrees=DEGREES, min_history=60)
            sr = wl.sharpe_ratio(pooled)
            sk, ku = wl.skew_kurt(pooled)
            n = len(pooled)
            psr = wl.probabilistic_sharpe_ratio(sr, 0.0, n, sk, ku) if n >= 2 else 0.0
            cp = wl.cpcv_profit_factor(pooled)
            v = {"score_threshold": st, "min_reversal_pct": mr, "events": n,
                 "sharpe": sr, "skew": sk, "kurt": ku, "psr": psr,
                 "cpcv_lo_pf": (cp[0] if cp else None)}
            variants.append(v)
            wl.log_trial({"strategy": "reversal", **{k: v[k] for k in
                          ("score_threshold", "min_reversal_pct", "events", "sharpe")}},
                         path=REGISTRY)

    sharpes = [v["sharpe"] for v in variants]
    sr_var = statistics.pvariance(sharpes) if len(sharpes) > 1 else 0.0
    best = max(variants, key=lambda v: v["sharpe"])
    n_run = len(variants)
    n_registry = wl.count_trials(REGISTRY)
    dsr = wl.deflated_sharpe_ratio(best["sharpe"], best["events"], best["skew"],
                                   best["kurt"], n_trials=max(n_run, 2), sr_variance=sr_var or 1e-9)

    out = ["# Deflated Sharpe report — reversal strategy",
           "",
           f"_Generated {datetime.date.today().isoformat()} by `scripts/run_dsr.py`. "
           f"Pooled across {len(SYMBOLS)} AI-semis (last {WINDOW} daily bars each). "
           "Multiple-testing-corrected per docs/research/deep/08. Not investment advice._",
           "",
           "## Variants tried (each is a 'trial' logged to `registry/trials.jsonl`)",
           "| score_thr | min_reversal | events | Sharpe | PSR(>0) | CPCV 5%ile PF |",
           "|---|---|---|---|---|---|"]
    for v in variants:
        cp = "n/a" if v["cpcv_lo_pf"] is None else f"{v['cpcv_lo_pf']:.2f}"
        out.append(f"| {v['score_threshold']} | {v['min_reversal_pct']} | {v['events']} | "
                   f"{v['sharpe']:.3f} | {v['psr']:.0%} | {cp} |")
    out += [
        "",
        "## Deflated verdict",
        f"- Best variant: score_threshold={best['score_threshold']}, "
        f"min_reversal_pct={best['min_reversal_pct']} (Sharpe {best['sharpe']:.3f}, "
        f"{best['events']} events).",
        f"- Variants tried this run: **{n_run}**; total in registry: **{n_registry}**.",
        f"- Variance of trial Sharpes: {sr_var:.4f}.",
        f"- **Deflated Sharpe Ratio (best, corrected for {n_run} trials): {dsr:.0%}**.",
        "",
        "> Verdict: **NOT validated — do not trust this number.** Even though the "
        f"corrected DSR reads {dsr:.0%}, three things inflate it and must be fixed before "
        "any edge claim is credible:",
        "> 1. **Outcome model is a toy.** `_resolve` books every winner at the fixed "
        "+target% and every loser at the (far) invalidation distance; in a *rising* "
        "300-bar sample most longs reach a small +5-6% target regardless of signal "
        "quality, so the per-trade Sharpe mostly measures market drift, not timing.",
        "> 2. **Wrong benchmark.** PSR/DSR here test Sharpe > 0; for a long-biased "
        "strategy in a bull market the right benchmark is **buy-and-hold**, which would "
        "deflate this sharply.",
        "> 3. **Tiny, overlapping samples** (9-47 events) with near-constant outcomes "
        "give artificially low variance (hence high Sharpe).",
        ">",
        "> The machinery (trials registry -> DSR/PSR/CPCV) is correct and wired; the "
        "honest takeaway is that the *current backtest design* cannot certify edge. "
        "Next: realistic exits (triple-barrier), a buy-and-hold benchmark in PSR/DSR, "
        "and far more events.",
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
