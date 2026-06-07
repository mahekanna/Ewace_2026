"""
run_forecast_backtest.py  —  does trading the wave FORECAST beat buy-and-hold?
================================================================================
Trades the engine's forecast the institutional way (confirmation entry, structural
stop, asymmetric R:R, scale-out + breakeven, conviction filter, one position at a
time — see wavelib/forecast_backtest.py) and asks whether it has an edge.

This version tests TWO entry models and TWO timeframes, because the first weekly
break-of-structure run was badly under-powered (147 trades):
  * entry_mode 'bos'  — conservative break-of-structure (few, wide-stop trades)
  * entry_mode 'zone' — EWF reaction-zone pullback (many, tight-stop trades)
  * timeframe 1W (26 instruments, 1987->2026) and 1D (deep semis history)

Every (timeframe x entry_mode x conviction) cell is a trial logged to the registry
so the Deflated Sharpe is honest about how much was tried. Setup geometry is cached
per (timeframe, instrument) so the variants replay cheaply. Writes
reports/FORECAST_BACKTEST_2026-06.md.

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

WINDOW = 300
MIN_HISTORY = 80
MIN_BARS = 250
COST = 0.001
MIN_RR = 1.5
CONF_MINS = (0.15, 0.25)
ENTRY_MODES = ("zone", "bos")
# (timeframe label, file glob tag, bar stride, time-barrier bars)
TIMEFRAMES = (("1W", "1w", 2, 13), ("1D", "1d", 5, 40), ("4H", "4h", 6, 30),
              ("1H", "1h", 10, 48), ("15M", "15m", 10, 48))


def load(path):
    with open(path) as fh:
        d = json.load(fh)
    bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
            for b in d["bars"]]
    return d.get("symbol", os.path.basename(path)), bars


def fdate(t):
    return datetime.datetime.utcfromtimestamp(t).strftime("%Y-%m")


def run_timeframe(tag, stride, max_hold):
    """Return (rows, bench_sr, span, n_instruments) for one timeframe."""
    files = sorted(glob.glob(os.path.join(LIVE, f"*_{tag}_2026-06.json")))
    series = []
    for f in files:
        sym, bars = load(f)
        if len(bars) >= MIN_BARS:
            series.append((bars, wl.compute_setups(bars, window=WINDOW,
                          min_history=MIN_HISTORY, stride=stride)))
    if not series:
        return [], 0.0, ("?", "?"), 0
    bench = []
    for bars, _c in series:
        bench += wl.horizon_returns(bars, horizon=max_hold, bullish=True)
    bench_sr = wl.sharpe_ratio(bench)
    span = (fdate(min(b[0][0] for b, _c in series)),
            fdate(max(b[-1][0] for b, _c in series)))

    # near-free DIRECTION-SKILL check off the same cache: signed return over the
    # horizon, no stop/target/management — isolates whether the forecast even
    # picks the right way (the cleanest test of the predictive claim).
    dpool = []
    for bars, cache in series:
        cl = [b[4] for b in bars]
        nb = len(bars)
        for ti, setup in cache.items():
            if setup is None or ti + max_hold >= nb:
                continue
            dpool.append((cl[ti + max_hold] - cl[ti]) / cl[ti] * setup[0])
    direction = {"n": len(dpool),
                 "mean": (sum(dpool) / len(dpool)) if dpool else 0.0,
                 "sharpe": wl.sharpe_ratio(dpool) if len(dpool) >= 2 else 0.0,
                 "win": (sum(1 for r in dpool if r > 0) / len(dpool)) if dpool else 0.0,
                 "bench_mean": (sum(bench) / len(bench)) if bench else 0.0}

    rows = []
    for mode in ENTRY_MODES:
        for conf in CONF_MINS:
            trades = []
            for bars, cache in series:
                trades += wl.forecast_trades(
                    bars, conf_min=conf, min_rr=MIN_RR, max_hold=max_hold, cost=COST,
                    window=WINDOW, min_history=MIN_HISTORY, stride=stride,
                    entry_mode=mode, setup_cache=cache)
            rets = [tr.pct_return for tr in trades]
            summ = wl.expectancy(trades)
            sr = wl.sharpe_ratio(rets)
            sk, ku = wl.skew_kurt(rets)
            n = len(rets)
            psr_b = wl.probabilistic_sharpe_ratio(sr, bench_sr, n, sk, ku) if n >= 2 else 0.0
            cp = wl.cpcv_profit_factor(rets)
            rows.append({"tf": tag, "mode": mode, "conf": conf, "n": n,
                         "win": summ["win_rate"], "avg_r": summ["avg_r"],
                         "pf": summ["profit_factor"], "sharpe": sr, "skew": sk,
                         "kurt": ku, "psr": psr_b, "cpcv": (cp[0] if cp else None)})
            wl.log_trial({"strategy": "forecast_driven", "tf": tag, "mode": mode,
                          "conf_min": conf, "events": n, "sharpe": sr,
                          "expectancy_r": summ["avg_r"]}, path=REGISTRY)
    return rows, bench_sr, span, len(series), direction


def main():
    all_rows = []
    sections = []
    directions = {}
    for label, tag, stride, max_hold in TIMEFRAMES:
        rows, bench_sr, span, n_inst, direction = run_timeframe(tag, stride, max_hold)
        if not rows:
            continue
        all_rows += rows
        directions[label] = direction
        sec = [f"## {label} — {n_inst} instruments, {span[0]}→{span[1]} "
               f"(buy-and-hold {max_hold}-bar Sharpe **{bench_sr:.3f}**)",
               "| entry | conf≥ | trades | win% | avg R | PF | Sharpe | PSR vs B&H | CPCV PF |",
               "|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            pf = "inf" if r["pf"] == float("inf") else f"{r['pf']:.2f}"
            cp = "n/a" if r["cpcv"] is None else f"{r['cpcv']:.2f}"
            sec.append(f"| {r['mode']} | {r['conf']} | {r['n']} | {r['win']:.0%} | "
                       f"{r['avg_r']:.2f} | {pf} | {r['sharpe']:.3f} | {r['psr']:.0%} | {cp} |")
        # per-timeframe read
        zone = [r for r in rows if r["mode"] == "zone"]
        zpos = zone and all(r["avg_r"] > 0 for r in zone)
        zbig = max((r["n"] for r in zone), default=0)
        sec.append("")
        sec.append(f"- Zone-entry (powered, up to {zbig} trades): expectancy "
                   + ", ".join(f"{r['avg_r']:.2f}R@conf{r['conf']}" for r in zone)
                   + " — " + ("POSITIVE." if zpos else "**not positive** (the powered "
                              "sample shows no edge)."))
        dsk = "BEATS always-long" if direction["mean"] > direction["bench_mean"] else "does NOT beat always-long"
        sec.append(f"- Direction skill (no stop/target, {direction['n']} signals): "
                   f"signed mean {direction['mean'] * 100:+.2f}% vs buy-and-hold "
                   f"{direction['bench_mean'] * 100:+.2f}%, win {direction['win']:.0%}, "
                   f"Sharpe {direction['sharpe']:+.3f} — **{dsk}**.")
        sections.append("\n".join(sec))

    # honest headline: prefer the POWERED zone variants for the verdict
    powered = [r for r in all_rows if r["mode"] == "zone" and r["n"] >= 50]
    zone_pos = powered and all(r["avg_r"] > 0 for r in powered)
    best = max(all_rows, key=lambda r: r["sharpe"]) if all_rows else None
    n_run = len(all_rows)
    n_registry = wl.count_trials(REGISTRY)

    out = ["# Prediction-driven backtest — trading the wave FORECAST",
           "",
           f"_Generated {datetime.date.today().isoformat()} by "
           "`scripts/run_forecast_backtest.py`. Trades the engine's forecast the "
           "institutional way (confirmation entry, structural stop, asymmetric R:R, "
           "scale-out + breakeven, conviction filter, one position at a time). Two "
           "entry models x two timeframes; every cell is a registry-logged trial. "
           f"Net of {COST:.1%} cost. Not investment advice._",
           ""]
    out += sections
    out += [
        "",
        "## Overall verdict",
        f"- Trials this run: **{n_run}** (2 timeframes x {len(ENTRY_MODES)} entry "
        f"models x {len(CONF_MINS)} conviction floors); registry total: **{n_registry}**.",
    ]
    if best:
        out.append(f"- Highest Sharpe cell: {best['tf']}/{best['mode']}/conf{best['conf']} "
                   f"— {best['n']} trades, {best['avg_r']:.2f}R, Sharpe {best['sharpe']:.3f}.")
    out += [
        "",
        (("> Verdict: **No durable edge.** The break-of-structure model looked faintly "
          "positive only because it was tiny/under-powered; once the EWF zone-entry "
          "model produces a properly-powered sample (hundreds of trades), expectancy "
          "is **not positive** — the forecast's reaction zones are not reliably where "
          "price turns. Trading the prediction does not beat buy-and-hold on either "
          "the weekly or the daily timeframe.")
         if not zone_pos else
         ("> Verdict: **A powered, positive signal.** The EWF zone-entry model shows "
          "POSITIVE expectancy across conviction floors on a properly-powered sample "
          "(hundreds of trades) on at least one timeframe — the first result that is "
          "both positive AND not under-powered. Worth genuine out-of-sample / forward "
          "testing before any capital or cycle-layer wiring.")),
        ">",
        "> Reading guide: the **zone** rows are the powered test (many trades); the "
        "**bos** rows are the conservative/under-powered one. Expectancy in R is the "
        "desk metric; PSR-vs-benchmark + CPCV are the multiple-testing-robust gates. "
        "Caveats: overlapping-instrument correlation; per-trade vs fixed-horizon "
        "benchmark Sharpe are not perfectly apples-to-apples; count confidence is "
        "calibrated, not validated. Causal throughout; setup geometry cached per "
        "(timeframe, instrument); timelines strided for runtime.",
    ]
    text = "\n".join(out) + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as fh:
        fh.write(text)
    print(text)
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
