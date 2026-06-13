"""
example_naive.py — a trivial baseline forecaster, to show the contract.
=======================================================================
A forecaster is just: forecast(bars) -> Forecast | None, using ONLY the bars given
(causal). This one is an SMA-momentum + ATR-target toy. It is deliberately simple:
expect it to score ~50% next-candle — that is the point of a baseline.

Copy this file into your own project, keep the signature, and put your real model
inside. You may return a `Forecast` (import from gf) OR a plain dict with keys
{direction, target, invalidation[, confidence, kind]} — the harness accepts either,
so your model can stay dependency-free.
"""
from gf import Forecast, sma, atr

FAST, SLOW, LOOKBACK = 10, 40, 60


def forecast(bars):
    if len(bars) < max(SLOW, LOOKBACK):
        return None                              # not enough history → no call
    closes = [b[4] for b in bars]
    price = closes[-1]
    a = atr(bars, 14) or price * 0.01
    fast, slow = sma(closes, FAST), sma(closes, SLOW)
    conf = max(0.0, min(1.0, abs(fast - slow) / a)) if a else 0.5
    if fast >= slow:                             # up-momentum → expect continuation up
        return Forecast("up", price + 1.5 * a, price - 1.0 * a, confidence=conf, kind="sma-momo")
    return Forecast("down", price - 1.5 * a, price + 1.0 * a, confidence=conf, kind="sma-momo")
