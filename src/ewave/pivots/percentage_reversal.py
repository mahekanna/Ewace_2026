"""
pivots.percentage_reversal — the causal ZigZag (percentage or ATR threshold).
=============================================================================
Moved verbatim from wavelib/toolkit.py (the detector behind every validated
result in docs/WAVE3_RESULT.md). Records, for each pivot, the bar at which its
reversal was CONFIRMED (`Pivot.confirmed_t`); the final extreme is provisional
(`confirmed_t=None`). See docs/NO_LOOKAHEAD_POLICY.md.
"""
from __future__ import annotations

from typing import List, Optional

from ..rules.result import Pivot


def causal_atr(bars, n: int) -> list:
    """Wilder ATR, right-aligned (atr[i] uses bars[:i+1]); None until i+1>=n. Causal."""
    atr = [None] * len(bars)
    prev_c = None
    trs = []
    for i, bar in enumerate(bars):
        h, l, c = bar[2], bar[3], bar[4]
        tr = (h - l) if prev_c is None else max(h - l, abs(h - prev_c), abs(l - prev_c))
        trs.append(tr)
        prev_c = c
        if i + 1 == n:
            atr[i] = sum(trs[:n]) / n
        elif i + 1 > n:
            atr[i] = (atr[i - 1] * (n - 1) + tr) / n
    return atr


_causal_atr = causal_atr  # legacy name (wavelib.toolkit._causal_atr)


def zigzag_causal(bars, pct: float = 0.10, atr_n: Optional[int] = None) -> List[Pivot]:
    """
    Causal ZigZag: detects the SAME pivots as the repainting `zigzag` (in
    percentage mode) but records, for each pivot, the bar at which its reversal
    was CONFIRMED (`Pivot.confirmed_t`).

    A pivot's price extreme (`Pivot.t`) is only *known to be* a pivot once price
    has reversed past it; that later bar is the confirmation. Backtests must use
    `confirmed_t`, never `t`, to avoid look-ahead bias (docs/research/04 §2.5,
    Item 1). The final extreme is still forming -> `confirmed_t` is None.

    pct    : reversal threshold. In percentage mode (atr_n=None) the threshold is
             `ep * pct`; in ATR mode (atr_n set) it is `ATR(atr_n) * pct` — an
             absolute, volatility-adaptive distance. Both are causal.
    """
    bars = list(bars)
    if not bars:
        return []
    atr = causal_atr(bars, atr_n) if atr_n else None
    # provenance stamped on every pivot (ewauto SPEC parity)
    src = "atr" if atr_n else "pct_reversal"
    meta = {"pct": pct, "atr_n": atr_n} if atr_n else {"pct": pct}

    def thr(ep_val, i):
        if atr is not None and atr[i] is not None:
            return atr[i] * pct
        return ep_val * pct

    piv: List[Pivot] = []
    trend = 0                                  # +1 up, -1 down, 0 unseeded
    et, ep = bars[0][0], bars[0][4]            # extreme time / price
    for i, bar in enumerate(bars):
        t, h, l = bar[0], bar[2], bar[3]
        if trend > 0:                          # tracking a high
            if h > ep:
                et, ep = t, h
            if l < ep - thr(ep, i):            # reversal confirmed at THIS bar
                piv.append(Pivot(et, ep, "H", confirmed_t=t, source=src, meta=meta))
                trend, et, ep = -1, t, l
        elif trend < 0:                        # tracking a low
            if l < ep:
                et, ep = t, l
            if h > ep + thr(ep, i):
                piv.append(Pivot(et, ep, "L", confirmed_t=t, source=src, meta=meta))
                trend, et, ep = 1, t, h
        else:                                  # seed (mirror of zigzag)
            if h > ep + thr(ep, i):
                piv.append(Pivot(et, ep, "L", confirmed_t=t, source=src, meta=meta)); trend, et, ep = 1, t, h
            elif l < ep - thr(ep, i):
                piv.append(Pivot(et, ep, "H", confirmed_t=t, source=src, meta=meta)); trend, et, ep = -1, t, l
            else:
                if h > ep: et, ep = t, h
                if l < bars[0][3]: pass
    # final extreme: not yet confirmed by a reversal -> provisional
    piv.append(Pivot(et, ep, "H" if trend > 0 else "L", confirmed_t=None, source=src, meta=meta))
    # collapse consecutive same-kind pivots, keep the more extreme (with its timing)
    out: List[Pivot] = []
    for p in piv:
        if out and out[-1].kind == p.kind:
            if (p.kind == "H" and p.price > out[-1].price) or \
               (p.kind == "L" and p.price < out[-1].price):
                out[-1] = p
        else:
            out.append(p)
    return out


def zigzag_multiscale(bars, scales=(0.03, 0.07, 0.15, 0.30), atr_n=None) -> dict:
    """
    One causal Pivot stream per scale (docs/research/04 §4 Item 2). Smaller scales
    = finer degree (Minor); larger = coarser (Primary+). Keys are the scale values.
    Pivot count is non-increasing as scale grows.
    """
    return {s: zigzag_causal(bars, pct=s, atr_n=atr_n) for s in scales}
