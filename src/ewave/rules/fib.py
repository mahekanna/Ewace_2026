"""
rules.fib — Fibonacci measurement helpers (moved from wavelib/toolkit.py).
==========================================================================
"""
from __future__ import annotations

from .result import PHI, Wave  # noqa: F401 (PHI re-exported)


def fib_extension(w1_len: float, base: float,
                  ratios=(1.0, 1.618, 2.0, 2.618, 3.0, 3.618)) -> dict:
    """Project upward fib extensions of `w1_len` added to `base`."""
    return {r: round(base + r * w1_len, 2) for r in ratios}


def fib_retrace(high: float, low: float,
                ratios=(0.236, 0.382, 0.5, 0.618, 0.786)) -> dict:
    rng = high - low
    return {r: round(high - r * rng, 2) for r in ratios}


def fib_cluster(prices, tol: float = 0.02):
    """Confluence detector: group projection prices into bands where independent
    Fibonacci measurements overlap within `tol` (relative). Returns [(center,
    count)] sorted by count desc — the band with the most overlapping projections
    is the high-confluence target zone. The most-cited institutional-EW edge
    (docs/research/practitioner/04 D-8)."""
    pts = sorted(p for p in prices if p and p > 0)
    if not pts:
        return []
    used = [False] * len(pts)
    bands = []
    for i, p in enumerate(pts):
        if used[i]:
            continue
        grp = [p]
        used[i] = True
        for j in range(i + 1, len(pts)):
            if not used[j] and abs(pts[j] - p) / p <= tol:
                grp.append(pts[j])
                used[j] = True
        bands.append((round(sum(grp) / len(grp), 2), len(grp)))
    bands.sort(key=lambda b: -b[1])
    return bands


def wave_ratio(a: Wave, b: Wave) -> float:
    return a.length / b.length if b.length else float("nan")


def blue_box_zone(a_start: float, a_end: float, b_end: float,
                  lo: float = 1.0, hi: float = 1.618) -> tuple:
    """EWF 'Blue Box' — the Fibonacci-extension reaction zone where the next leg
    (e.g. wave C) is expected to complete. Given swing A (a_start->a_end) and the
    connecting leg's end b_end, project the lo..hi (100%-161.8%) extension of A's
    length from b_end, continuing A's direction. Returns (low_price, high_price);
    the far edge (161.8%) is the hard invalidation. (docs/research/deep/10.)"""
    leg = abs(a_end - a_start)
    direction = -1 if a_end < a_start else 1
    p1 = b_end + direction * lo * leg
    p2 = b_end + direction * hi * leg
    return (min(p1, p2), max(p1, p2))
