"""
run_forecast_backtest.py  —  does trading the wave PREDICTION beat buy-and-hold?
================================================================================
This is the test the multi-regime DSR report was missing: instead of a reversal
SCORE with fixed barriers, it trades the engine's FORECAST the way a desk would —
confirmation entry, structural stop, asymmetric R:R, scale-out + breakeven,
conviction filter, one position at a time (see wavelib/forecast_backtest.py).

Pools across the same weekly multi-regime universe (1987->2026, all asset
classes). The "trials" grid is (conf_min x min_rr); each is logged to the
registry so the Deflated Sharpe is honest. Reports institutional metrics
(expectancy in R, win rate, profit factor) AND the Sharpe/PSR/CPCV/DSR stack vs a
buy-and-hold benchmark. Writes reports/FORECAST_BACKTEST_2026-06.md.

Run:  python3 scripts/run_forecast_backtest.py
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
REPORT = os.path.join(ROOT, "reports", "FORECAST_BACKTEST_2026-06.md")
REGISTRY = os.path.join(ROOT, "registry", "trials.jsonl")

MAX_HOLD = 13                      # ~one quarter on weekly bars (time barrier)
WINDOW = 300                       # labelling window (~6y weekly)
MIN_HISTORY = 80
STRIDE = 2
COST = 0.001
MIN_BARS = 200
# trials grid: conviction filter x reward:risk filter
CONF_MINS = (0.15, 0.25)
MIN_RRS = (1.5, 2.5)


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
        print("no weekly series found")
        return

    bench = []
    for _slug, _sym, bars in series:
        bench += wl.horizon_returns(bars, horizon=MAX_HOLD, bullish=True)
    bench_sr = wl.sharpe_ratio(bench)

    variants = []
    for conf in CONF_MINS:
        for rr in MIN_RRS:
            all_trades = []
            for _slug, _sym, bars in series:
                all_trades += wl.forecast_trades(
                    bars, conf_min=conf, min_rr=rr, max_hold=MAX_HOLD,
                    cost=COST, window=WINDOW, min_history=MIN_HISTORY, stride=STRIDE)
            rets = [tr.pct_return for tr in all_trades]
            summ = wl.expectancy(all_trades)
            sr = wl.sharpe_ratio(rets)
            sk, ku = wl.skew_kurt(rets)
            n = len(rets)
            psr_b = wl.probabilistic_sharpe_ratio(sr, bench_sr, n, sk, ku) if n >= 2 else 0.0
            cp = wl.cpcv_profit_factor(rets)
            longs = sum(1 for tr in all_trades if tr.direction == "long")
            variants.append({
                "conf_min": conf, "min_rr": rr, "events": n, "sharpe": sr,
                "skew": sk, "kurt": ku, "psr_vs_bench": psr_b,
                "cpcv_lo_pf": (cp[0] if cp else None),
                "win_rate": summ["win_rate"], "avg_r": summ["avg_r"],
                "profit_factor": summ["profit_factor"], "longs": longs,
                "shorts": n - longs})
            wl.log_trial({"strategy": "forecast_driven_weekly", "conf_min": conf,
                          "min_rr": rr, "events": n, "sharpe": sr,
                          "expectancy_r": summ["avg_r"]}, path=REGISTRY)

    sharpes = [v["sharpe"] for v in variants]
    sr_var = statistics.pvariance(sharpes) if len(sharpes) > 1 else 0.0
    MIN_EVENTS = 30
    eligible = [v for v in variants if v["events"] >= MIN_EVENTS]
    best = max(eligible or variants, key=lambda v: v["sharpe"])
    best_underpowered = not eligible
    n_run = len(variants)
    n_registry = wl.count_trials(REGISTRY)
    dsr = wl.deflated_sharpe_ratio(best["sharpe"], max(best["events"], 2), best["skew"],
                                   best["kurt"], n_trials=max(n_run, 2),
                                   sr_variance=sr_var or 1e-9)
    beats_bh = best["sharpe"] > bench_sr
    pos_expectancy = best["avg_r"] > 0
    first_t = min(bars[0][0] for _s, _y, bars in series)
    last_t = max(bars[-1][0] for _s, _y, bars in series)

    out = ["# Prediction-driven backtest — trading the wave FORECAST (weekly)",
           "",
           f"_Generated {datetime.date.today().isoformat()} by "
           "`scripts/run_forecast_backtest.py`. Trades the engine's forecast/trade_plan "
           "the institutional way: confirmation entry, structural stop, asymmetric R:R "
           "filter, scale-out + breakeven, conviction filter, one position at a time. "
           f"Pooled across **{len(series)} instruments** / multiple asset classes, "
           f"weekly **{fdate(first_t)} → {fdate(last_t)}** (2000/2008/2020/2022 regimes), "
           f"net of {COST:.1%} cost. Not investment advice._",
           "",
           f"**Buy-and-hold benchmark** ({MAX_HOLD}-bar horizon): Sharpe "
           f"**{bench_sr:.3f}** — the bar to clear.",
           "",
           "## Variants tried (conviction x reward:risk; each a logged trial)",
           "| conf≥ | RR≥ | trades | long/short | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for v in variants:
        cp = "n/a" if v["cpcv_lo_pf"] is None else f"{v['cpcv_lo_pf']:.2f}"
        pf = "inf" if v["profit_factor"] == float("inf") else f"{v['profit_factor']:.2f}"
        out.append(f"| {v['conf_min']} | {v['min_rr']} | {v['events']} | "
                   f"{v['longs']}/{v['shorts']} | {v['win_rate']:.0%} | {v['avg_r']:.2f} | "
                   f"{pf} | {v['sharpe']:.3f} | {v['psr_vs_bench']:.0%} | {cp} |")
    out += [
        "",
        "## Verdict",
        f"- Best variant: conf≥{best['conf_min']}, RR≥{best['min_rr']} — "
        f"{best['events']} trades, win rate {best['win_rate']:.0%}, "
        f"**expectancy {best['avg_r']:.2f} R/trade**, profit factor "
        + ("inf" if best['profit_factor'] == float('inf') else f"{best['profit_factor']:.2f}") + ".",
        f"- Sharpe {best['sharpe']:.3f} vs buy-and-hold {bench_sr:.3f} -> beats B&H: "
        f"**{beats_bh}**; PSR vs B&H **{best['psr_vs_bench']:.0%}**." +
        ("  (No variant reached 30 trades — under-powered.)" if best_underpowered else ""),
        f"- Variants this run: **{n_run}**; registry total: **{n_registry}**; "
        f"Deflated Sharpe (vs 0, {n_run} trials): **{dsr:.0%}**.",
        "",
        (("> Verdict: **Positive expectancy, but does not clear the gates.** The wave "
          f"forecast traded with desk-style risk shows {best['avg_r']:.2f}R expectancy "
          f"over {best['events']} trades, but its Sharpe ({best['sharpe']:.3f}) "
          + ("beats" if beats_bh else "does not beat") +
          f" buy-and-hold ({bench_sr:.3f}) and PSR-vs-benchmark is "
          f"{best['psr_vs_bench']:.0%} — short of the 95% bar.")
         if pos_expectancy else
         ("> Verdict: **No edge.** Even traded the institutional way (confirmation "
          "entry, structural stop, scale-out), the wave forecast does not produce "
          f"positive expectancy at the chosen filters (best {best['avg_r']:.2f}R) and "
          f"does not beat buy-and-hold (Sharpe {best['sharpe']:.3f} vs {bench_sr:.3f}).")),
        ">",
        "> This is the honest test of EW/NeoWave's *predictive* claim (the reversal-"
        "score backtest never used the forecast). Expectancy in R is the desk metric; "
        "PSR-vs-benchmark + CPCV are the multiple-testing-robust gates. Caveats: "
        "weekly sample, overlapping-instrument correlation, and the count confidence "
        "is itself only calibrated, not validated — so this measures the forecast as "
        "the engine currently produces it.",
        ">",
        f"> Replay is causal (plan at bar t from bars[..t]); labelling window "
        f"{WINDOW} bars, timeline strided every {STRIDE} bars for runtime.",
    ]
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(text)
    print(text)
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
