"""
backtest.metrics — trade-list statistics + DSR-aware trial logging.
===================================================================
Every backtest run auto-logs a trial to registry/trials.jsonl: the Deflated
Sharpe Ratio needs the TOTAL number of strategy variants ever tried, so silent
re-runs are how a research process lies to itself (docs/research/deep/08).
Selection on the research track goes by DSR + MinTRL, never raw expectancy.
"""
from __future__ import annotations

import statistics
from typing import List, Optional

import json

from ..validation.stats import (count_trials, deflated_sharpe_ratio, log_trial,
                                min_track_record_length,
                                probabilistic_sharpe_ratio, sharpe_ratio,
                                skew_kurt)


def summarize(trades: List, *, symbol: str = "", timeframe: str = "",
              profile: str = "", registry_path: str = "registry/trials.jsonl",
              log: bool = True) -> dict:
    """Metrics for a Wave3Trade list; optionally logs the run as a trial."""
    rs = [t.r for t in trades]
    out = {
        "symbol": symbol, "timeframe": timeframe, "profile": profile,
        "trades": len(rs),
        "expectancy_r": round(statistics.mean(rs), 4) if rs else None,
        "total_r": round(sum(rs), 2) if rs else 0.0,
        "win_rate": round(sum(1 for r in rs if r > 0) / len(rs), 4) if rs else None,
        "profit_factor": None,
        "max_drawdown_r": None,
        "median_planned_rr": round(statistics.median(t.planned_rr for t in trades), 2)
        if trades else None,
        "avg_bars_held": round(statistics.mean(t.bars_held for t in trades), 1)
        if trades else None,
        "sharpe_per_trade": None, "psr": None, "dsr": None, "min_trl": None,
        "n_trials": None,
    }
    if rs:
        gross_w = sum(r for r in rs if r > 0)
        gross_l = -sum(r for r in rs if r < 0)
        out["profit_factor"] = round(gross_w / gross_l, 3) if gross_l else float("inf")
        equity = peak = dd = 0.0
        for r in rs:
            equity += r
            peak = max(peak, equity)
            dd = max(dd, peak - equity)
        out["max_drawdown_r"] = round(dd, 2)
        sr = sharpe_ratio(rs)
        out["sharpe_per_trade"] = round(sr, 4)
        if len(rs) >= 3:
            sk, ku = skew_kurt(rs)
            out["psr"] = round(probabilistic_sharpe_ratio(sr, 0.0, len(rs), sk, ku), 4)
            mtrl = min_track_record_length(sr, 0.0, sk, ku)
            out["min_trl"] = round(mtrl, 1) if mtrl is not None else None
    if log:
        record = {"strategy": f"wave3_{profile}", "symbol": symbol,
                  "timeframe": timeframe, "trades": len(rs),
                  "expectancy_r": out["expectancy_r"],
                  "sharpe": out["sharpe_per_trade"]}
        log_trial(record, path=registry_path)
    n_trials = count_trials(registry_path)
    out["n_trials"] = n_trials
    if rs and len(rs) >= 3 and n_trials >= 2:
        sr = out["sharpe_per_trade"]
        sk, ku = skew_kurt(rs)
        var = _trial_sharpe_variance(registry_path)
        if var > 0:
            out["dsr"] = round(deflated_sharpe_ratio(sr, len(rs), sk, ku,
                                                     n_trials, var), 4)
    return out


def _trial_sharpe_variance(path: str) -> float:
    """Variance of Sharpe across all logged trials (DSR's sr_variance input)."""
    srs = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                s = json.loads(line).get("sharpe")
                if s is not None:
                    srs.append(float(s))
    except FileNotFoundError:
        return 0.0
    if len(srs) < 2:
        return 0.0
    m = sum(srs) / len(srs)
    return sum((x - m) ** 2 for x in srs) / (len(srs) - 1)


def equity_curve(trades: List) -> List[tuple]:
    """[(signal_time, cumulative_R)] for plotting/CSV."""
    eq, out = 0.0, []
    for t in trades:
        eq += t.r
        out.append((t.signal_time, round(eq, 4)))
    return out
