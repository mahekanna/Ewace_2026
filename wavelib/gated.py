"""
gated.py — the NeoWave-disciplined entry (RULESET §D/§F, practitioner/03 TR-1/TR-2).

`FORWARD_GHOST_TEST_FINDINGS.md` O7: the disciplined signal was built (`trade_plan`)
and then never tested. Every "no edge" backtest in this repo measured the RAW
projection — fired every bar, no trigger, no confluence, no R:R. `trade_plan` itself
computes the confluence score and the R:R and then returns a plan regardless of what
they say; the gating was left to a caller that never gated.

This module is that caller. A signal is emitted ONLY when every gate passes:

  TR-1 / CC-1  a completed impulse must have reached Stage-1 confirmation — the 2-4
               line broken in LESS time than wave 5 took to build. Before that the
               pattern is a candidate, not a fact. (practitioner/03 CC-1, TR-1)
  A-1          entry only on the CONFIRMATION BREAK of the last confirmed pivot;
               the label alone never trades. (RULESET §F)
  TR-2         two consecutive closes in the trade direction — two closes confirm a
               reversal has begun rather than a spike. (LF-27)
  Table D      >= `conf_min` independent confluence strands. (RULESET §D)
  E-2          reward:risk >= `min_rr` or no trade. (RULESET §E)

Everything is causal: only bars <= the decision bar are ever read.
"""
from dataclasses import dataclass
from typing import Optional

from .confluence import score_reversal
from .forecast import forecast_waves
from .neowave_logic import falsify_count
from .rules import Pivot, Status, Wave, two_four_confirmation
from .toolkit import ATR_SCALES
from .wavetree import _ewo, wave_counts

_MOTIVE = ("IMPULSE", "DIAGONAL")


@dataclass
class GatedSignal:
    t: float
    direction: str            # "long" | "short"
    entry: float
    stop: float
    target: float
    rr: float
    confluence: int
    stage: int                # CC-1 stage reached (0 = n/a for non-impulse setups)
    pattern: str              # the completed structure being traded away from
    reason: str


@dataclass
class GateReject:
    """Why a bar produced NO TRADE — so a run can report where candidates die."""
    t: float
    failed: str


def _last_count(bars, window):
    recent = bars[-window:] if len(bars) > window else bars
    cs = wave_counts(recent, ATR_SCALES[:3], max_alternates=1)
    return (recent, cs[0]) if cs else (recent, None)


def momentum_direction(bars, lookback: int = 60):
    """Direction from MOMENTUM instead of the opposite-last-leg reflex.

    Every professional school gates wave identity on momentum, and the engine never
    did (PRO_APPLICATION_SPEC P1, "the single biggest miss"; ghost-findings O9 —
    momentum gated LABELLING but never the forecast's direction). The rule (EWI
    I4/I5, EWF A8/C6):

        a new price extreme WITHOUT momentum divergence  -> still wave 3, go WITH it
        a new price extreme WITH momentum divergence     -> wave 5, FADE it

    Returns "up" | "down" | None (no fresh extreme to judge).
    """
    closes = [b[4] for b in bars]
    if len(closes) < 80:
        return None
    e = _ewo(closes)
    seg = closes[-lookback:]
    eseg = [x for x in e[-lookback:] if x is not None]
    if len(eseg) < lookback // 2:
        return None
    half = len(seg) // 2
    prior_hi, prior_lo = max(seg[:half]), min(seg[:half])
    now_hi, now_lo = max(seg[half:]), min(seg[half:])
    eh, el = len(eseg) // 2, len(eseg)
    e_prior_hi, e_prior_lo = max(eseg[:eh]), min(eseg[:eh])
    e_now_hi, e_now_lo = max(eseg[eh:el]), min(eseg[eh:el])
    if now_hi > prior_hi:                       # fresh high
        diverging = e_now_hi <= e_prior_hi      # price up, momentum not -> wave 5
        return "down" if diverging else "up"
    if now_lo < prior_lo:                       # fresh low
        diverging = e_now_lo >= e_prior_lo
        return "up" if diverging else "down"
    return None


def plan_from_count(bars, *, window: int = 300, direction_mode: str = "reflex"):
    """The un-gated proposal: direction, entry trigger, structural stop, target.

    Separated from the gates so a backtest can run the SAME proposal through gated
    and un-gated arms and attribute any difference to the discipline alone."""
    recent, count = _last_count(bars, window)
    if count is None or not count.labels:
        return None
    fc = forecast_waves(bars, window=window)
    if fc is None or not fc.targets:
        return None
    legs = [n for _lab, n in count.labels]
    last = legs[-1]
    if direction_mode == "momentum":
        md = momentum_direction(bars)
        if md is None:
            return None
        direction = "long" if md == "up" else "short"
    else:
        direction = "long" if fc.direction == "up" else "short"
    entry = last.end.price
    swing_lo = min(last.start.price, last.end.price)
    swing_hi = max(last.start.price, last.end.price)
    stop = swing_lo if direction == "long" else swing_hi
    target = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
    return dict(recent=recent, count=count, legs=legs, fc=fc, direction=direction,
                entry=entry, stop=stop, target=target, pattern=count.pattern)


def gated_signal(bars, *, symbol: str = "", conf_min: int = 3, min_rr: float = 2.0,
                 require_stage: int = 1, two_bar: bool = True, window: int = 300,
                 explain: bool = False, plan=None, falsify: bool = False):
    """Emit a GatedSignal only if every gate passes, else None (or a GateReject
    naming the first failing gate when `explain=True`).

    `plan` accepts a precomputed `plan_from_count` result so a backtest can run the
    same proposal through gated and un-gated arms without paying for it twice — any
    difference between the arms is then attributable to the gates alone."""
    p = plan if plan is not None else plan_from_count(bars, window=window)
    t = bars[-1][0]
    if p is None:
        return GateReject(t, "no-count") if explain else None
    recent, direction, entry, stop, target = (p["recent"], p["direction"],
                                              p["entry"], p["stop"], p["target"])
    price = bars[-1][4]
    long_ = direction == "long"

    # --- CC-9: behaviour over structure. If what price has ALREADY done since the
    # pattern ended contradicts the label, the count is wrong and there is nothing
    # to trade. This is Neely's error-correction mechanism, and it is the only gate
    # here that can reject the DIRECTION rather than merely the timing.
    if falsify:
        legs = [n.as_wave() for n in p["legs"]]
        if len(legs) >= 3:
            end = legs[-1].end
            post = Wave(end, Pivot(t, price, "H" if price > end.price else "L"))
            up = legs[-1].end.price > legs[0].start.price
            # structural family only: at entry the post-move is by definition
            # unfinished, so CC-3/CC-5 cannot fairly judge it yet
            v = falsify_count(legs, p["pattern"], post=post, uptrend=up,
                              post_complete=False)
            if v.falsified:
                return GateReject(t, f"CC-9 {v.reason[:40]}") if explain else None

    # --- TR-1 / CC-1: a completed impulse must be Stage-1 confirmed -------------
    stage = 0
    if p["pattern"] in _MOTIVE and len(p["legs"]) == 5:
        legs = p["legs"]
        w5 = legs[4].as_wave()
        w2, w4 = legs[1].end, legs[3].end
        uptrend = legs[4].end.price > legs[0].start.price
        s1, s2 = two_four_confirmation(w5, w2, w4, t, price, uptrend=uptrend)
        stage = 2 if s2.status is Status.PASS else (1 if s1.status is Status.PASS else 0)
        if stage < require_stage:
            return GateReject(t, "CC-1 stage") if explain else None

    # --- A-1: confirmation break of the last confirmed pivot -------------------
    broke = price > entry if long_ else price < entry
    if not broke:
        return GateReject(t, "no-break") if explain else None

    # --- TR-2: two consecutive closes in the trade direction -------------------
    if two_bar and len(bars) >= 3:
        c1, c2, c3 = bars[-3][4], bars[-2][4], bars[-1][4]
        if not ((c3 > c2 > c1) if long_ else (c3 < c2 < c1)):
            return GateReject(t, "TR-2 two-bar") if explain else None

    # --- E-2: reward:risk ------------------------------------------------------
    risk = abs(price - stop)
    if risk <= 0:
        return GateReject(t, "no-risk") if explain else None
    rr = abs(target - price) / risk
    if rr < min_rr:
        return GateReject(t, "R:R") if explain else None

    # --- Table D: independent confluence strands -------------------------------
    zone = (min(stop, target), max(stop, target))
    rep = score_reversal(symbol or "x", recent[-250:], zone, bullish=long_)
    if rep.score < conf_min:
        return GateReject(t, "confluence") if explain else None

    return GatedSignal(t, direction, price, stop, target, round(rr, 2), rep.score,
                       stage, p["pattern"],
                       f"{p['pattern']} complete (CC-1 stage {stage}); break of "
                       f"{entry:.2f} confirmed; {rep.score} strands; R:R {rr:.2f}")
