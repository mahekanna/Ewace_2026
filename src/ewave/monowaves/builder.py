"""
monowaves.builder — confirmed pivots → MonoWave table.
======================================================
Uses only pivots visible at `now_t` (docs/NO_LOOKAHEAD_POLICY.md); each
mono-wave's `visible_at` is its end pivot's confirmed_t, so a caller replaying
history can filter `[m for m in build(...) if m.visible_at <= t]` and get
exactly what was knowable at t.
"""
from __future__ import annotations

from typing import List, Optional, Sequence

from ..pivots.models import visible
from ..rules.result import Pivot
from .models import MonoWave


def build(pivots: Sequence[Pivot], now_t: Optional[float] = None,
          bar_seconds: Optional[float] = None) -> List[MonoWave]:
    """Pair consecutive CONFIRMED pivots into mono-waves with objective metrics.

    now_t       : visibility cutoff (default: treat all confirmed pivots as visible)
    bar_seconds : bar interval for time_length_bars/slope; when None it is
                  estimated from the median pivot spacing granularity (callers
                  that know the timeframe should pass it).
    """
    piv = visible(list(pivots), now_t) if now_t is not None else \
        [p for p in pivots if p.confirmed_t is not None]
    out: List[MonoWave] = []
    prev: Optional[MonoWave] = None
    for i in range(len(piv) - 1):
        a, b = piv[i], piv[i + 1]
        secs = b.t - a.t
        n_bars = max(1, round(secs / bar_seconds)) if bar_seconds else 0
        signed = b.price - a.price
        m = MonoWave(
            wave_id=i,
            start=a, end=b,
            visible_at=b.confirmed_t,
            direction="UP" if signed > 0 else "DOWN",
            start_price=a.price, end_price=b.price,
            price_length=abs(signed),
            percent_change=signed / a.price if a.price else float("nan"),
            time_length_secs=secs,
            time_length_bars=n_bars,
            slope=(signed / n_bars) if n_bars else (signed / secs if secs else 0.0),
        )
        if prev is not None and prev.price_length:
            ratio = m.price_length / prev.price_length
            if m.direction != prev.direction:
                m.retracement_of_previous = ratio
            else:
                m.extension_vs_previous = ratio
        out.append(m)
        prev = m
    return out
