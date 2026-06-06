"""
backtest.py
===========
Causal bar-by-bar reversal-replay harness (docs/research/04 §4 Item 5).

At each bar t, signals are generated from bars[0..t] ONLY — never bar[t+1] — so
the measured hit-rate is honest. Walk-forward (IS/OOS) splitting is supported.

Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass

from . import automation
from .confluence import score_reversal
from .validation import (sharpe_ratio, skew_kurt, probabilistic_sharpe_ratio,
                         min_track_record_length)


@dataclass
class ReversalEvent:
    entry_t: float
    score: int
    zone: tuple
    invalidation: float
    entry_price: float


@dataclass
class ReversalOutcome:
    event: ReversalEvent
    outcome: str               # "REVERSAL" | "INVALIDATED" | "OPEN"
    exit_t: float | None
    exit_price: float | None
    move_pct: float | None     # signed % from entry to exit


@dataclass
class BacktestStats:
    n_signals: int
    n_reversals: int
    n_invalidations: int
    n_open: int
    hit_rate: float
    profit_factor: float
    sharpe: float = 0.0
    psr: float = 0.0              # P(true Sharpe > 0) given sample size + shape
    min_trl: float | None = None  # observations needed to confirm edge at 95%
    wfe: float | None = None
    is_period: tuple | None = None
    oos_period: tuple | None = None

    @property
    def underpowered(self) -> bool:
        """True if there aren't enough events to confirm the edge (MinTRL > n)."""
        return self.min_trl is not None and self.min_trl > self.n_signals


def _zone_from_candidate(c) -> tuple:
    """Reversal zone = price span of the candidate's last (corrective) leg."""
    w = c.waves[-1]
    return (min(w.start.price, w.end.price), max(w.start.price, w.end.price))


def _invalidation(c, bullish: bool) -> float:
    """Origin of the candidate's first wave — a break past it kills the count."""
    return c.waves[0].start.price


def _resolve(event: ReversalEvent, bars, min_reversal_pct: float, bullish: bool) -> ReversalOutcome:
    """Walk forward from the signal bar to classify the outcome."""
    entry = event.entry_price
    target = entry * (1 + min_reversal_pct) if bullish else entry * (1 - min_reversal_pct)
    after = [b for b in bars if b[0] > event.entry_t]
    for b in after:
        t, h, l, c = b[0], b[2], b[3], b[4]
        # invalidation first (conservative)
        if (bullish and l <= event.invalidation) or (not bullish and h >= event.invalidation):
            move = (event.invalidation - entry) / entry * (1 if bullish else -1)
            return ReversalOutcome(event, "INVALIDATED", t, event.invalidation, move)
        if (bullish and h >= target) or (not bullish and l <= target):
            move = (target - entry) / entry * (1 if bullish else -1)
            return ReversalOutcome(event, "REVERSAL", t, target, move)
    return ReversalOutcome(event, "OPEN", None, None, None)


def _aggregate(outcomes, is_period=None, oos_period=None) -> BacktestStats:
    rev = [o for o in outcomes if o.outcome == "REVERSAL"]
    inv = [o for o in outcomes if o.outcome == "INVALIDATED"]
    opn = [o for o in outcomes if o.outcome == "OPEN"]
    decided = len(rev) + len(inv)
    hit = len(rev) / decided if decided else 0.0
    gains = sum(o.move_pct for o in rev if o.move_pct)
    losses = sum(abs(o.move_pct) for o in inv if o.move_pct)
    pf = (gains / losses) if losses else (float("inf") if gains else 0.0)
    # statistical power of the result (Bailey & Lopez de Prado)
    rets = [o.move_pct for o in outcomes if o.move_pct is not None]
    sr = sharpe_ratio(rets)
    sk, ku = skew_kurt(rets)
    psr = probabilistic_sharpe_ratio(sr, 0.0, len(rets), sk, ku) if len(rets) >= 2 else 0.0
    mtrl = min_track_record_length(sr, 0.0, sk, ku) if len(rets) >= 2 else None
    return BacktestStats(len(outcomes), len(rev), len(inv), len(opn), hit, pf,
                         sharpe=sr, psr=psr, min_trl=mtrl,
                         is_period=is_period, oos_period=oos_period)


def _wfo_windows(n: int, train: int, test: int, step: int):
    """Yield ((is_lo, is_hi), (oos_lo, oos_hi)) index ranges; OOS never overlaps IS."""
    out = []
    anchor = train
    while anchor + test <= n:
        out.append(((anchor - train, anchor), (anchor, anchor + test)))
        anchor += step
    return out


def backtest_reversals(bars, score_threshold: int = 4, min_reversal_pct: float = 0.05,
                       degrees=(0.03, 0.07), wfo_train_size=None, wfo_test_size=None,
                       wfo_step_size=None, bullish: bool = True,
                       cycle_aligned: bool = False, min_history: int = 60) -> BacktestStats:
    """
    Bar-by-bar causal replay (docs/research/04 §4 Item 5). bars = (t,o,h,l,c,v).

    At each bar: auto-label causally, take the best clean candidate, and — if the
    close sits inside its reversal zone — score the reversal on the trailing
    window. Events with score >= threshold are walked forward for their outcome.

    Walk-forward: if wfo_* are set, returns combined OOS stats with `wfe` = mean
    OOS/IS profit-factor ratio across non-overlapping windows.
    """
    if wfo_train_size and wfo_test_size and wfo_step_size:
        ratios, oos_all = [], []
        first_is = last_oos = None
        for (is_lo, is_hi), (oos_lo, oos_hi) in _wfo_windows(
                len(bars), wfo_train_size, wfo_test_size, wfo_step_size):
            is_stats = backtest_reversals(bars[is_lo:is_hi], score_threshold, min_reversal_pct,
                                          degrees, bullish=bullish, cycle_aligned=cycle_aligned,
                                          min_history=min_history)
            oos_stats = backtest_reversals(bars[oos_lo:oos_hi], score_threshold, min_reversal_pct,
                                           degrees, bullish=bullish, cycle_aligned=cycle_aligned,
                                           min_history=min_history)
            if is_stats.profit_factor not in (0.0, float("inf")):
                ratios.append(oos_stats.profit_factor / is_stats.profit_factor)
            first_is = first_is or (bars[is_lo][0], bars[is_hi - 1][0])
            last_oos = (bars[oos_lo][0], bars[oos_hi - 1][0])
        wfe = sum(ratios) / len(ratios) if ratios else None
        agg = BacktestStats(0, 0, 0, 0, 0.0, 0.0, wfe=wfe,
                            is_period=first_is, oos_period=last_oos)
        return agg

    return _aggregate(_replay(bars, score_threshold, min_reversal_pct, degrees,
                              bullish, cycle_aligned, min_history))


def _resolve_tb(event: ReversalEvent, bars, pt: float, sl: float, max_hold: int,
                bullish: bool) -> ReversalOutcome:
    """Triple-barrier exit (Lopez de Prado): take-profit (+pt), stop-loss (-sl), or
    a vertical time barrier at max_hold bars (exit at that close). Returns the
    REALISED return — far more honest than booking every winner at a fixed target."""
    entry = event.entry_price
    if bullish:
        up, dn = entry * (1 + pt), entry * (1 - sl)
    else:
        up, dn = entry * (1 + sl), entry * (1 - pt)   # short: stop above, target below
    after = [b for b in bars if b[0] > event.entry_t][:max_hold]
    for b in after:
        t, h, l, c = b[0], b[2], b[3], b[4]
        if bullish:
            if l <= dn:
                return ReversalOutcome(event, "INVALIDATED", t, dn, -sl)
            if h >= up:
                return ReversalOutcome(event, "REVERSAL", t, up, pt)
        else:
            if h >= up:
                return ReversalOutcome(event, "INVALIDATED", t, up, -sl)
            if l <= dn:
                return ReversalOutcome(event, "REVERSAL", t, dn, pt)
    if after:                                          # vertical barrier: exit at last close
        last = after[-1][4]
        ret = (last - entry) / entry * (1 if bullish else -1)
        return ReversalOutcome(event, "REVERSAL" if ret > 0 else "INVALIDATED",
                               after[-1][0], last, ret)
    return ReversalOutcome(event, "OPEN", None, None, None)


def horizon_returns(bars, horizon: int = 20, bullish: bool = True) -> list:
    """Buy-and-hold baseline: every horizon-forward return in the series. Its
    Sharpe is the benchmark a timing strategy must beat (docs/research/deep/08)."""
    cl = [b[4] for b in bars]
    return [(cl[i + horizon] - cl[i]) / cl[i] * (1 if bullish else -1)
            for i in range(len(cl) - horizon) if cl[i]]


def _replay(bars, score_threshold, min_reversal_pct, degrees, bullish,
            cycle_aligned, min_history, pt=None, sl=None, max_hold=None):
    """Causal bar-by-bar replay -> list[ReversalOutcome]. If pt/sl/max_hold are
    given, exits use the triple-barrier method; else the legacy fixed target."""
    events: list[ReversalEvent] = []
    for t in range(min_history, len(bars)):
        sub = bars[:t + 1]
        cands = automation.label_and_validate(sub, degrees=degrees)
        if not cands or cands[0].hard_fails > 0:
            continue
        zone = _zone_from_candidate(cands[0])
        close = sub[-1][4]
        if not (zone[0] <= close <= zone[1]):
            continue
        window = bars[max(0, t - min_history):t + 1]
        rep = score_reversal("bt", window, zone, bullish=bullish, cycle_aligned=cycle_aligned)
        if rep.score >= score_threshold:
            events.append(ReversalEvent(sub[-1][0], rep.score, zone,
                                        _invalidation(cands[0], bullish), close))
    if pt is not None and sl is not None and max_hold is not None:
        return [_resolve_tb(e, bars, pt, sl, max_hold, bullish) for e in events]
    return [_resolve(e, bars, min_reversal_pct, bullish) for e in events]


def reversal_returns(bars, score_threshold: int = 4, min_reversal_pct: float = 0.05,
                     degrees=(0.03, 0.07), bullish: bool = True,
                     cycle_aligned: bool = False, min_history: int = 60,
                     pt=None, sl=None, max_hold=None) -> list:
    """Per-event signed returns from a causal replay — feed to validation.cpcv_*
    for the honest out-of-sample edge verdict (docs/research/deep/08). Pass
    pt/sl/max_hold to use realistic triple-barrier exits."""
    outs = _replay(bars, score_threshold, min_reversal_pct, degrees, bullish,
                   cycle_aligned, min_history, pt=pt, sl=sl, max_hold=max_hold)
    return [o.move_pct for o in outs if o.move_pct is not None]
