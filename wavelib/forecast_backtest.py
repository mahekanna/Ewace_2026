"""
forecast_backtest.py  —  prediction-driven, institution-style backtest.
========================================================================
The reversal-confluence backtest (`backtest.py`) traded a SCORE with fixed ±%
barriers — it never used the engine's wave PREDICTION. This module does: it trades
the `forecast` / `trade_plan` output the way a desk actually would.

Institutional discipline encoded here:
  1. ENTER ON CONFIRMATION, not on the label. A setup is only taken if price
     breaks the plan's trigger level (the last pivot) in the forecast direction
     WITHIN the Neely time window (the prior leg's build time). No confirmation in
     the window -> the setup expires, no trade (no catching falling knives).
  2. RISK IS DEFINED STRUCTURALLY. The stop sits just beyond the swing that would
     void the count — not an arbitrary %. Risk per trade = |entry - stop|.
  3. ASYMMETRIC R:R FILTER. Skip any setup whose reward-to-risk to the final
     target is below `min_rr`. A desk doesn't take 1:1 trades.
  4. SCALE OUT + BREAKEVEN. Book `partial` at the first Fibonacci target and move
     the stop to breakeven; let the remainder run to the final target (EWF method).
  5. CONVICTION FILTER. Only trade counts whose honest confidence >= `conf_min`.
  6. ONE POSITION AT A TIME. While a trade is open, no new entries (no stacking of
     correlated, overlapping signals).

Everything is CAUSAL: at bar t the plan is built from bars[..t] only and the trade
is then resolved on subsequent bars. Returns are net of round-trip cost.

Metrics are reported the institutional way — expectancy in R-multiples, win rate,
profit factor — alongside the Sharpe/PSR/CPCV/DSR stack so it is directly
comparable to the multi-regime report.

Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .forecast import trade_plan


@dataclass
class ForecastTrade:
    entry_t: float
    entry_price: float
    direction: str               # "long" | "short"
    stop: float
    t1: float
    t2: float
    exit_t: float
    exit_price: float
    pct_return: float            # blended position return, net of cost
    r_multiple: float            # pct_return / initial risk (the desk metric)
    outcome: str                 # "WIN" | "PARTIAL" | "STOP" | "TIME"
    confidence: float
    rr_planned: float            # reward:risk to the final target at entry


def _valid_targets(targets, entry, dirn):
    """Keep only targets on the correct side of entry; return (T1 nearest, T2 far)."""
    good = sorted((p for _lab, p in targets if dirn * (p - entry) > 0),
                  key=lambda p: dirn * (p - entry))
    if not good:
        return None, None
    return good[0], good[-1]


def _manage(bars, i_entry, entry, stop, t1, t2, dirn, partial, max_hold, cost):
    """Walk forward from the entry bar applying scale-out + breakeven + time stop.
    `dirn` = +1 long / -1 short. Returns (exit_t, exit_price, pct_return, outcome)."""
    risk_frac = abs(entry - stop) / entry
    seg = bars[i_entry + 1: i_entry + 1 + max_hold]
    booked = 0.0          # accumulated signed % (weighted by size booked)
    rem = 1.0             # remaining position fraction
    cur_stop = stop
    hit_t1 = False
    for b in seg:
        t, h, l, c = b[0], b[2], b[3], b[4]
        hi_first, lo_first = h, l
        # --- stop check FIRST within the bar (conservative: assume the adverse touch) ---
        stopped = (lo_first <= cur_stop) if dirn == 1 else (hi_first >= cur_stop)
        if stopped:
            booked += rem * dirn * (cur_stop - entry) / entry
            out = "PARTIAL" if hit_t1 else "STOP"
            return t, cur_stop, booked - cost, out
        # --- first target -> book partial, move stop to breakeven ---
        if not hit_t1:
            reached_t1 = (h >= t1) if dirn == 1 else (l <= t1)
            if reached_t1:
                booked += partial * dirn * (t1 - entry) / entry
                rem -= partial
                hit_t1 = True
                cur_stop = entry            # breakeven
        # --- final target -> exit remainder ---
        if hit_t1:
            reached_t2 = (h >= t2) if dirn == 1 else (l <= t2)
            if reached_t2:
                booked += rem * dirn * (t2 - entry) / entry
                return t, t2, booked - cost, "WIN"
    # vertical (time) barrier: exit remainder at last close
    if seg:
        last = seg[-1]
        lc = last[4]
        booked += rem * dirn * (lc - entry) / entry
        return last[0], lc, booked - cost, ("PARTIAL" if hit_t1 else "TIME")
    return None


def forecast_trades(bars, *, conf_min: float = 0.20, min_rr: float = 1.5,
                    max_hold: int = 13, confirm_cap: int = 8, cost: float = 0.001,
                    window: int = 300, min_history: int = 80, stride: int = 1,
                    partial: float = 0.5, min_risk: float = 0.01) -> list:
    """Causal, institution-style replay trading the wave FORECAST. At each bar a
    plan is built from bars[..t]; if it clears the conviction and R:R filters and
    then CONFIRMS (trigger break within the time window), the trade is managed with
    scale-out/breakeven exits. One position at a time. Returns list[ForecastTrade]."""
    trades: list = []
    n = len(bars)
    t = max(min_history, 1)
    while t < n:
        plan = trade_plan(bars[:t + 1], window=window)
        if plan is None or plan.confidence < conf_min:
            t += stride
            continue
        dirn = 1 if plan.direction == "long" else -1
        entry_level = plan.entry_level
        stop = plan.stop_level
        # stop must be on the protective side; risk must be meaningful
        if dirn * (entry_level - stop) <= 0:
            t += stride
            continue
        risk_frac = abs(entry_level - stop) / entry_level
        if risk_frac < min_risk:
            t += stride
            continue
        t1, t2 = _valid_targets(plan.targets, entry_level, dirn)
        if t1 is None:
            t += stride
            continue
        rr = abs(t2 - entry_level) / abs(entry_level - stop)
        if rr < min_rr:
            t += stride
            continue
        # --- wait for CONFIRMATION: trigger break in the forecast direction,
        #     within min(plan window, cap) bars. No break -> setup expires. ---
        cwin = max(1, min(plan.confirm_window_bars, confirm_cap))
        i_entry = None
        for j in range(t + 1, min(t + 1 + cwin, n)):
            hb, lb = bars[j][2], bars[j][3]
            if (dirn == 1 and hb >= entry_level) or (dirn == -1 and lb <= entry_level):
                i_entry = j
                break
        if i_entry is None:
            t += cwin                       # setup expired; jump past the window
            continue
        res = _manage(bars, i_entry, entry_level, stop, t1, t2, dirn,
                      partial, max_hold, cost)
        if res is None:
            t = i_entry + 1
            continue
        exit_t, exit_px, pct, outcome = res
        trades.append(ForecastTrade(
            bars[i_entry][0], entry_level, plan.direction, stop, t1, t2,
            exit_t, exit_px, pct, pct / risk_frac, outcome, plan.confidence, rr))
        # one position at a time: resume AFTER this trade's exit
        nxt = i_entry + 1
        while nxt < n and bars[nxt][0] < exit_t:
            nxt += 1
        t = max(nxt, i_entry + 1)
    return trades


def forecast_returns(bars, **kw) -> list:
    """Per-trade blended % returns (net of cost) — feed to the validation stack."""
    return [tr.pct_return for tr in forecast_trades(bars, **kw)]


def expectancy(trades) -> dict:
    """Institutional trade summary: n, win rate, avg R, expectancy (R), profit
    factor, avg win/loss %. `trades` = list[ForecastTrade]."""
    n = len(trades)
    if not n:
        return {"n": 0, "win_rate": 0.0, "avg_r": 0.0, "expectancy_r": 0.0,
                "profit_factor": 0.0, "avg_win": 0.0, "avg_loss": 0.0}
    wins = [tr for tr in trades if tr.pct_return > 0]
    losses = [tr for tr in trades if tr.pct_return <= 0]
    gross_win = sum(tr.pct_return for tr in wins)
    gross_loss = sum(-tr.pct_return for tr in losses)
    pf = (gross_win / gross_loss) if gross_loss else (float("inf") if gross_win else 0.0)
    avg_r = sum(tr.r_multiple for tr in trades) / n
    return {
        "n": n,
        "win_rate": len(wins) / n,
        "avg_r": avg_r,
        "expectancy_r": avg_r,                       # mean R per trade = expectancy
        "profit_factor": pf,
        "avg_win": (gross_win / len(wins)) if wins else 0.0,
        "avg_loss": (gross_loss / len(losses)) if losses else 0.0,
    }
