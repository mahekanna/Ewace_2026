"""
pivots.fractal — N-bar confirmed fractal pivots (moved from wavelib/toolkit.py).
================================================================================
"""
from __future__ import annotations

from typing import List

from ..rules.result import Pivot


def swing_pivots(series, n_left: int = 2, n_right: int = 2) -> List[Pivot]:
    """
    N-bar confirmed fractal pivots on a `(t, value)` series.

    Position i is a swing HIGH if `value[i]` is strictly greater than the
    `n_left` values before AND the `n_right` values after it; a swing LOW if
    strictly less. `confirmed_t` is the timestamp `n_right` bars later — the
    earliest bar at which the pivot is knowable (causal confirmation lag).

    Generic over any 1-D series (price highs/lows, RSI, ...), so the same helper
    backs the SMC confirmation strands (03) and the monowave constructor (02).
    Plateaus (ties on either side) are not pivots. Returns pivots in time order.
    """
    s = list(series)
    n = len(s)
    out: List[Pivot] = []
    for i in range(n_left, n - n_right):
        t_i, v_i = s[i][0], s[i][1]
        window = [s[j][1] for j in range(i - n_left, i)] + \
                 [s[j][1] for j in range(i + 1, i + 1 + n_right)]
        conf_t = s[i + n_right][0]
        if all(v_i > x for x in window):
            out.append(Pivot(t_i, v_i, "H", confirmed_t=conf_t))
        elif all(v_i < x for x in window):
            out.append(Pivot(t_i, v_i, "L", confirmed_t=conf_t))
    return out


def detect(bars, n_left: int = 2, n_right: int = 2) -> List[Pivot]:
    """Fractal pivots on OHLC bars: swing highs on the high series, swing lows
    on the low series, merged in time order (uploads' `fractal` detector)."""
    highs = swing_pivots([(b[0], b[2]) for b in bars], n_left, n_right)
    lows = swing_pivots([(b[0], b[3]) for b in bars], n_left, n_right)
    out = [p for p in highs if p.kind == "H"] + [p for p in lows if p.kind == "L"]
    out.sort(key=lambda p: p.t)
    return out
