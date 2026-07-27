"""
pivots.repainting — the NON-CAUSAL ZigZag. PLOTTING/REFERENCE ONLY.
===================================================================
This detector back-dates every pivot to its price extreme with no confirmation
time — on a chart of the past it looks prophetic, in real time those pivots
were not knowable when drawn. Feeding it into any signal, scan, pattern,
backtest, or execution path is a look-ahead bug by construction
(docs/NO_LOOKAHEAD_POLICY.md §2); an import-graph test enforces that none of
those modules import this one. Use `percentage_reversal.zigzag_causal` instead.

Kept because it is still the right tool for one job: drawing the final wave
skeleton on a completed chart (reporting/charting).
"""
from __future__ import annotations

from typing import List

from ..rules.result import Pivot


def zigzag(bars, pct: float = 0.10) -> List[Pivot]:
    """
    Percentage-reversal ZigZag on intrabar highs/lows. NON-CAUSAL (repaints):
    pivots carry no `confirmed_t` and are placed at their extremes.

    bars : iterable of (t, o, h, l, c[, v])
    pct  : reversal threshold (0.10 = 10%)
    returns alternating H/L pivots (the wave skeleton).
    """
    bars = list(bars)
    if not bars:
        return []
    piv: List[Pivot] = []
    trend = 0                                  # +1 up, -1 down, 0 unseeded
    et, ep = bars[0][0], bars[0][4]            # extreme time / price
    for b in bars:
        t, h, l = b[0], b[2], b[3]
        if trend > 0:                          # tracking a high
            if h > ep:
                et, ep = t, h
            if l < ep * (1 - pct):
                piv.append(Pivot(et, ep, "H"))
                trend, et, ep = -1, t, l
        elif trend < 0:                        # tracking a low
            if l < ep:
                et, ep = t, l
            if h > ep * (1 + pct):
                piv.append(Pivot(et, ep, "L"))
                trend, et, ep = 1, t, h
        else:                                  # seed (avoid dual-branch corruption)
            if h > ep * (1 + pct):
                piv.append(Pivot(et, ep, "L")); trend, et, ep = 1, t, h
            elif l < ep * (1 - pct):
                piv.append(Pivot(et, ep, "H")); trend, et, ep = -1, t, l
            else:
                if h > ep: et, ep = t, h
                if l < bars[0][3]: pass
    piv.append(Pivot(et, ep, "H" if trend > 0 else "L"))
    # collapse consecutive same-kind pivots, keep the more extreme
    out: List[Pivot] = []
    for p in piv:
        if out and out[-1].kind == p.kind:
            if (p.kind == "H" and p.price > out[-1].price) or \
               (p.kind == "L" and p.price < out[-1].price):
                out[-1] = p
        else:
            out.append(p)
    return out
