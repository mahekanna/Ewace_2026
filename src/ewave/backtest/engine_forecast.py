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

from ..signals.trade_plan import forecast_from_count
from ..patterns.tree import wave_counts


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


def _setup_at(bars_upto, window):
    """Build the raw geometry of a forecast setup at the last bar of `bars_upto`
    (causal). Returns (dirn, hi, lo, targets, confidence, confirm_bars) or None,
    where hi/lo are the CORRECTIVE-LEG extremes and `targets` the forecast's
    projected next-wave levels. Entry/stop are derived per entry-model by the
    caller, and the conviction filter is applied by the caller, so this is
    independent of conf/RR/mode and therefore cacheable across variants."""
    recent = bars_upto[-window:] if len(bars_upto) > window else bars_upto
    counts = wave_counts(recent, (0.03, 0.05, 0.08), max_alternates=0)
    if not counts:
        return None
    pc = counts[0]
    fc = forecast_from_count(pc, recent[-1][4])
    if fc is None or not fc.targets:
        return None
    legs = [n for _l, n in pc.labels]
    if not legs:
        return None
    last = legs[-1]
    hi, lo = max(last.start.price, last.end.price), min(last.start.price, last.end.price)
    if hi <= lo:                            # degenerate zero-depth leg -> no risk defined
        return None
    dirn = 1 if fc.direction == "up" else -1
    leg_bars = sum(1 for b in recent if last.start.t <= b[0] <= last.end.t)
    return dirn, hi, lo, list(fc.targets), pc.confidence, max(leg_bars, 1)


def _entry_stop(dirn, hi, lo, entry_mode, zone_frac, buf):
    """Derive (entry, stop) for the chosen entry model.

    bos  — break of structure: long reclaims the leg HIGH (stop below the leg LOW);
           wide stop = full leg depth, low R:R, conservative.
    zone — EWF/NeoWave reaction-zone: long buys a pullback into the lower `zone_frac`
           of the leg (stop just below the leg LOW); short sells a bounce into the
           upper band (stop just above the leg HIGH). Tight stop -> higher R:R, and
           price reaching the zone is a far more frequent trigger than a full break."""
    rng = hi - lo
    if entry_mode == "bos":
        return (hi, lo) if dirn == 1 else (lo, hi)
    # zone
    if dirn == 1:
        return lo + zone_frac * rng, lo * (1 - buf)
    return hi - zone_frac * rng, hi * (1 + buf)


def _confirmed(bar, dirn, entry, entry_mode):
    """Has `bar` triggered the entry? bos = break beyond `entry`; zone = price
    trades INTO the zone (a limit-style touch of `entry`)."""
    h, l = bar[2], bar[3]
    if entry_mode == "bos":
        return (h >= entry) if dirn == 1 else (l <= entry)
    # zone: long fills when price dips down to entry; short fills on a bounce up to it
    return (l <= entry) if dirn == 1 else (h >= entry)


def compute_setups(bars, *, window: int = 300, min_history: int = 80,
                   stride: int = 1) -> dict:
    """Pre-compute the (expensive) per-bar setup geometry on a strided grid, ONCE,
    so the many (entry-mode x conf x R:R) variants can replay cheaply off the cache.
    Returns {bar_index t: setup-or-None}. Causal: setup at t uses bars[:t+1]."""
    return {t: _setup_at(bars[:t + 1], window)
            for t in range(max(min_history, 1), len(bars), max(1, stride))}


_MISS = object()


def forecast_trades(bars, *, conf_min: float = 0.20, min_rr: float = 1.5,
                    max_hold: int = 13, confirm_cap: int = 8, cost: float = 0.001,
                    window: int = 300, min_history: int = 80, stride: int = 1,
                    partial: float = 0.5, min_risk: float = 0.01,
                    entry_mode: str = "zone", zone_frac: float = 0.382,
                    buf: float = 0.005, setup_cache: dict = None) -> list:
    """Causal, institution-style replay trading the wave FORECAST. At each bar a
    risk-defined setup is built from bars[..t]; if it clears the conviction and
    R:R filters and then CONFIRMS within the time window, the trade is managed with
    scale-out/breakeven exits. `entry_mode` selects 'bos' (break-of-structure,
    conservative) or 'zone' (EWF reaction-zone pullback, higher-R:R). One position
    at a time; the SAME setup is never re-traded until the structure changes.
    Pass `setup_cache` (from compute_setups) to avoid recomputing wave counts across
    variants. Returns list[ForecastTrade]."""
    trades: list = []
    n = len(bars)
    t = max(min_history, 1)
    last_setup = None                       # (dirn, entry, stop) of the last setup acted on
    while t < n:
        if setup_cache is not None:
            setup = setup_cache.get(t, _MISS)
            if setup is _MISS:              # off-grid (after a jump) -> compute on demand
                setup = _setup_at(bars[:t + 1], window)
        else:
            setup = _setup_at(bars[:t + 1], window)
        if setup is None:
            t += stride
            continue
        dirn, hi, lo, targets, conf, confirm_bars = setup
        if conf < conf_min:                 # conviction filter (caller-applied)
            t += stride
            continue
        entry, stop = _entry_stop(dirn, hi, lo, entry_mode, zone_frac, buf)
        t1, t2 = _valid_targets(targets, entry, dirn)
        if t1 is None or entry == stop or entry == 0:
            t += stride
            continue
        risk_frac = abs(entry - stop) / entry
        rr = abs(t2 - entry) / abs(entry - stop)
        sig = (dirn, round(entry, 4), round(stop, 4))
        if risk_frac < min_risk or rr < min_rr or sig == last_setup:
            t += stride                     # filtered, or a duplicate of the active setup
            continue
        # --- wait for CONFIRMATION within min(leg-time, cap) bars; else it expires ---
        cwin = max(1, min(confirm_bars, confirm_cap))
        i_entry = None
        for j in range(t + 1, min(t + 1 + cwin, n)):
            if _confirmed(bars[j], dirn, entry, entry_mode):
                i_entry = j
                break
        if i_entry is None:
            last_setup = sig                # remember so we don't re-test it every bar
            t += cwin
            continue
        last_setup = sig
        res = _manage(bars, i_entry, entry, stop, t1, t2, dirn, partial, max_hold, cost)
        if res is None:
            t = i_entry + 1
            continue
        exit_t, exit_px, pct, outcome = res
        trades.append(ForecastTrade(
            bars[i_entry][0], entry, "long" if dirn == 1 else "short", stop, t1, t2,
            exit_t, exit_px, pct, pct / risk_frac, outcome, conf, rr))
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
