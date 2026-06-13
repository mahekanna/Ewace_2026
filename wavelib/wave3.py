"""
wave3.py  —  the actual Elliott trade: enter wave 3 on confirmation.
====================================================================
The forecast in `forecast.py` projects the leg AFTER a completed structure — it
never trades waves 3 or 5 (the high-probability legs). This module implements the
professional setup instead:

  1. find an INCOMPLETE impulse: wave 1 (a directional leg) + wave 2 (a 38.2-78.6%
     pullback that does NOT exceed wave 1's origin — Elliott hard rule R1);
  2. ENTRY = the break of the wave-1 extreme (price reclaiming it CONFIRMS wave 3
     has begun — wave 3 must exceed wave 1);
  3. STOP  = just beyond the wave-2 extreme (a structural, count-voiding stop);
  4. TARGETS = Fibonacci EXTENSIONS of wave 1 from the wave-2 extreme
     (1.618x / 2.618x — the canonical wave-3 projections).

Because the stop is ~half of wave 1 and the target is ~1.6x of it, the setup is
naturally asymmetric (R:R ~2+), unlike the next-leg projection (R:R<1). It also
fires SELECTIVELY — only on the confirmation break — not every candle.

Optionally gated by EWO momentum (a real wave 3 expands momentum). CAUSAL: uses
only bars up to the entry candle. Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass

from .toolkit import zigzag_causal
from .wavetree import momentum_lookup


@dataclass
class Wave3Signal:
    direction: str          # "long" | "short"
    entry_t: float
    entry: float            # the wave-1 extreme broken on this candle (fill level)
    stop: float             # just beyond the wave-2 extreme (structural)
    targets: list           # [(label, price), ...] wave-3 Fib extensions of wave 1
    reward_risk: float      # to the first target
    w1: tuple               # (origin_price, wave1_extreme) for context
    w2: float               # wave-2 extreme (the pullback low/high)
    retr: float             # wave-2 retracement fraction of wave 1
    ewo: float              # EWO at entry (momentum into wave 3)
    note: str = ""


def wave3_signal(bars, *, pct: float = 0.02, retr_lo: float = 0.382,
                 retr_hi: float = 0.786, min_w1_frac: float = 0.01,
                 buf: float = 0.001, use_momentum: bool = True):
    """Return a Wave3Signal iff the CURRENT (last) candle confirms a wave-3 entry
    (price just broke the wave-1 extreme out of a valid wave-1/wave-2 structure),
    else None. Causal."""
    if len(bars) < 50:
        return None
    piv = [p for p in zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
    if len(piv) < 3:
        return None
    a, b, c = piv[-3], piv[-2], piv[-1]          # a->b = wave 1, b->c = wave 2
    price = bars[-1][4]
    prev = bars[-2][4]
    t_now = bars[-1][0]
    w1_up = b.price > a.price
    w1_len = abs(b.price - a.price)
    if w1_len <= 0 or w1_len / max(a.price, 1e-9) < min_w1_frac:
        return None
    mom = momentum_lookup(bars) if use_momentum else None
    e = mom(t_now) if mom else None

    # ---- LONG: wave 1 up, wave 2 down (pullback), break ABOVE wave-1 high ----
    if w1_up and c.price < b.price:
        retr = (b.price - c.price) / w1_len
        if not (retr_lo <= retr <= retr_hi):
            return None
        if c.price <= a.price:                   # R1: wave 2 cannot exceed wave-1 origin
            return None
        w1_high, w2_low = b.price, c.price
        if not (prev <= w1_high < price):        # confirmation break happened THIS candle
            return None
        if use_momentum and (e is None or e <= 0):   # momentum must be expanding up
            return None
        entry, stop = w1_high, w2_low * (1 - buf)
        risk = entry - stop
        if risk <= 0:
            return None
        t1, t2 = w2_low + 1.618 * w1_len, w2_low + 2.618 * w1_len
        return Wave3Signal("long", t_now, round(entry, 4), round(stop, 4),
                           [("1.618x W1", round(t1, 2)), ("2.618x W1", round(t2, 2))],
                           round((t1 - entry) / risk, 2), (a.price, b.price), w2_low,
                           round(retr, 3), e if e is not None else 0.0,
                           "wave-3 long: broke wave-1 high after a valid wave-2 pullback")

    # ---- SHORT: wave 1 down, wave 2 up, break BELOW wave-1 low ----
    if (not w1_up) and c.price > b.price:
        retr = (c.price - b.price) / w1_len
        if not (retr_lo <= retr <= retr_hi):
            return None
        if c.price >= a.price:
            return None
        w1_low, w2_high = b.price, c.price
        if not (prev >= w1_low > price):
            return None
        if use_momentum and (e is None or e >= 0):
            return None
        entry, stop = w1_low, w2_high * (1 + buf)
        risk = stop - entry
        if risk <= 0:
            return None
        t1, t2 = w2_high - 1.618 * w1_len, w2_high - 2.618 * w1_len
        return Wave3Signal("short", t_now, round(entry, 4), round(stop, 4),
                           [("1.618x W1", round(t1, 2)), ("2.618x W1", round(t2, 2))],
                           round((entry - t1) / risk, 2), (a.price, b.price), w2_high,
                           round(retr, 3), e if e is not None else 0.0,
                           "wave-3 short: broke wave-1 low after a valid wave-2 pullback")
    return None
