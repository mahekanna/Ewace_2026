"""
backtest.engine — the flagship wave-3 trade backtest (causal entries only).
===========================================================================
Ports scripts/forward_wave3.py — the harness that established the validated
anchors (docs/WAVE3_RESULT.md: AVGO +0.17R/79 trades, MRVL +0.31R/119 trades,
year of 15m bars) — into a profile-driven library engine:

  walk the series candle-by-candle; when the profile's wave-3 entry fires on
  the current candle (causal), ghost-feed the future one bar at a time:
  single-target resolution (stop at wave-2 extreme / T1 at 1.618x W1 / time
  exit) for ungated profiles, or rule-faithful scale-out management (50% off
  at T1, stop->breakeven, rest to T2, S&B time budget = 3x wave-1 duration)
  when profile.scale_out is set. One position at a time; entry >= signal_time
  always (the invariant tests enforce it).

Costs: an optional FillModel nets a round-trip cost in R from every trade
(default 0 so the historical anchors reproduce exactly; configs/execution.json
supplies real values).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..rules.profiles import Profile
from ..signals import wave3
from .fills import FillModel


@dataclass
class Wave3Trade:
    signal_time: float
    entry_time: float          # == signal_time: the fill is at the break level of the trigger candle
    direction: str
    entry: float
    stop: float
    target_1: float
    planned_rr: float
    r: float                   # realized R (cost-netted when a FillModel is given)
    outcome: str               # TARGET | STOP | TIME | WIN | PARTIAL
    bars_held: int
    strands: int = 0


def _resolve_single(sig, future):
    """Single-target ghost-feed (verbatim logic from scripts/forward_wave3.py):
    stop before target within a bar (conservative)."""
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


def _resolve_scaleout(sig, future):
    """Rule-faithful management (C-1/E-5/E-6, verbatim from forward_wave3.py):
    take 50% at T1 (1.618x), stop->breakeven, run the rest to T2 (2.618x);
    S&B TIME BUDGET = 3x wave-1 duration replaces any fixed bar count."""
    entry, stop, t1, t2 = sig.entry, sig.stop, sig.targets[0][1], sig.t2
    long = sig.direction == "long"
    risk = abs(entry - stop)
    if risk <= 0:
        return None
    budget = min(len(future), 3 * max(sig.w1_bars, 1))
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
            rem, hit_t1, cur_stop = 0.5, True, entry
        reach_t2 = (hi >= t2) if long else (lo <= t2)
        if hit_t1 and reach_t2:
            booked += rem * (t2 - entry) / risk * (1 if long else -1)
            return booked, "WIN", i + 1
    if budget:                                               # time-budget exit at close
        last = future[budget - 1][4]
        booked += rem * (last - entry) / risk * (1 if long else -1)
        return booked, ("PARTIAL" if hit_t1 else "TIME"), budget
    return None


def _raw_signal(bars_window, profile: Profile):
    """The profile's Wave3Signal on the current candle (None when quiet)."""
    kw = profile.wave3_kwargs()
    gated = (kw["require_pattern_id"] or kw["conf_min"] > 0 or kw["min_rr"] > 0
             or kw["entry_window_w2_mult"] > 0)
    if gated:
        return wave3.wave3_signal_strict(
            bars_window, conf_min=kw["conf_min"], min_rr=kw["min_rr"],
            retr_lo=kw["retr_lo"], retr_hi=kw["retr_hi"],
            deep_hi=kw["deep_hi"] if kw["deep_hi"] is not None else kw["retr_hi"],
            pct=kw["pct"], buf=kw["buf"], use_momentum=kw["use_momentum"],
            require_pattern_id=kw["require_pattern_id"],
            entry_window_w2_mult=kw["entry_window_w2_mult"],
            min_w1_frac=kw["min_w1_frac"],
            use_ichimoku=kw.get("use_ichimoku", False))
    return wave3.wave3_signal(
        bars_window, pct=kw["pct"], retr_lo=kw["retr_lo"], retr_hi=kw["retr_hi"],
        min_w1_frac=kw["min_w1_frac"], buf=kw["buf"],
        use_momentum=kw["use_momentum"])


def backtest_wave3(bars, profile: Profile, *, max_hold: int = 96, roll: int = 400,
                   start: int = 60, fill_model: Optional[FillModel] = None
                   ) -> List[Wave3Trade]:
    """Causal one-position-at-a-time wave-3 backtest under `profile`."""
    n = len(bars)
    trades: List[Wave3Trade] = []
    t = start
    while t < n - 1:
        sig = _raw_signal(bars[max(0, t - roll):t + 1], profile)
        if sig is None:
            t += 1
            continue
        assert sig.entry_t == bars[t][0], "signal must fire on the cursor candle"
        horizon = max(max_hold, 3 * getattr(sig, "w1_bars", max_hold) + 5)
        future = bars[t + 1:t + 1 + horizon]
        res = (_resolve_scaleout(sig, future) if profile.scale_out
               else _resolve_single(sig, future))
        if res is None:
            t += 1
            continue
        r, outcome, held = res
        if fill_model is not None:
            r -= fill_model.cost_r(sig.entry, sig.stop)
        trades.append(Wave3Trade(
            signal_time=bars[t][0], entry_time=bars[t][0],
            direction=sig.direction, entry=sig.entry, stop=sig.stop,
            target_1=sig.targets[0][1], planned_rr=sig.reward_risk,
            r=round(r, 4), outcome=outcome, bars_held=held,
            strands=getattr(sig, "strands", 0)))
        t += held + 1                            # one position at a time
    return trades
