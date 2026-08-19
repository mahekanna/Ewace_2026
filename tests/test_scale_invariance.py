"""
Phase 0 gate — instrument- and regime-agnostic pivot detection.

A "swing" must mean the same structural thing on EURUSD as on BTC, and in a quiet
regime as in a violent one. Fixed-percentage thresholds do not deliver that: at
pct=0.05 measured pivot density ran 5.5 per 1000 bars on EURUSD and 941 on VIX
(171x), and a 5x volatility shift inside one series changed density by 12-44x.

ATR-relative thresholds (toolkit.ATR_SCALES / DEFAULT_ATR_N) fix this. These tests
pin that property so it cannot silently regress — everything downstream (degree,
counts, signals) inherits the pivots.

Pure stdlib (unittest). Run:  python3 -m unittest tests.test_scale_invariance -v
"""
import math
import random
import unittest

from wavelib import zigzag_causal, adaptive_atr_pivots, ATR_SCALES, DEFAULT_ATR_N


def _walk(n, vol_fn, drift=0.0003, seed=7, px0=100.0, steps=8):
    """Random walk sampled intrabar, so H/L are genuine extremes of the path
    (a flat-range synthetic would hide volatility from ATR and make this test lie)."""
    random.seed(seed)
    px = px0
    bars = []
    for i in range(n):
        vol = vol_fn(i)
        o = px
        path = [px]
        for _ in range(steps):
            px *= math.exp(random.gauss(drift / steps, vol / math.sqrt(steps)))
            path.append(px)
        bars.append((float(i) * 86400.0, o, max(path), min(path), px))
    return bars


def _pivots(bars, **kw):
    return [p for p in zigzag_causal(bars, **kw) if p.confirmed_t is not None]


class TestRegimeInvariance(unittest.TestCase):
    """Same structure, 5x louder: pivot density must not explode."""

    N = 1500

    def setUp(self):
        self.bars = _walk(self.N, lambda i: 0.004 if i < self.N // 2 else 0.020)
        self.half = (self.N // 2) * 86400.0

    def _halves(self, **kw):
        p = _pivots(self.bars, **kw)
        first = sum(1 for x in p if x.t < self.half)
        return first, len(p) - first

    def test_fixed_percent_is_regime_dependent(self):
        # documents the defect the ATR mode exists to fix
        a, b = self._halves(pct=0.05)
        self.assertGreater(b / max(a, 1), 5.0,
                           "fixed-%% used to distort badly; if this now passes the "
                           "synthetic no longer reproduces the problem")

    def test_atr_mode_is_regime_invariant(self):
        for k in (3.0, 5.0):
            a, b = self._halves(pct=k, atr_n=DEFAULT_ATR_N)
            ratio = b / max(a, 1)
            self.assertLess(ratio, 2.0,
                            f"ATR k={k}: density ratio {ratio:.2f}x across a 5x vol shift")


class TestPriceScaleInvariance(unittest.TestCase):
    """A 100x advance at constant log-volatility must not concentrate pivots."""

    def setUp(self):
        n = 2000
        drift = math.log(100) / n
        self.bars = _walk(n, lambda i: 0.012, drift=drift, seed=11, px0=1.0)

    def _deciles(self, **kw):
        p = _pivots(self.bars, **kw)
        dec = [0] * 10
        for x in p:
            dec[min(9, int(x.t / 86400.0 / 200))] += 1
        return dec

    def test_price_range_is_100x(self):
        lo = min(b[3] for b in self.bars)
        hi = max(b[2] for b in self.bars)
        self.assertGreater(hi / lo, 50.0)

    def test_atr_mode_spreads_pivots_evenly(self):
        dec = self._deciles(pct=3.0, atr_n=DEFAULT_ATR_N)
        self.assertTrue(all(d > 0 for d in dec), f"empty decile(s): {dec}")
        self.assertLess(max(dec) / max(min(dec), 1), 3.0, f"uneven: {dec}")


class TestAdaptiveLadderConverges(unittest.TestCase):
    """The old fixed-% ladder topped out at 0.55 and silently truncated history."""

    def test_converges_on_violent_series(self):
        bars = _walk(1200, lambda i: 0.06, seed=3)        # very high volatility
        piv = adaptive_atr_pivots(bars, target=15)
        self.assertLessEqual(len(piv), 25, "ladder failed to coarsen enough")
        self.assertGreaterEqual(len(piv), 4)

    def test_converges_on_quiet_series(self):
        bars = _walk(1200, lambda i: 0.002, seed=4)       # very low volatility
        piv = adaptive_atr_pivots(bars, target=15)
        self.assertGreaterEqual(len(piv), 4, "ladder too coarse for a quiet series")

    def test_ladder_is_monotone_in_scale(self):
        bars = _walk(1200, lambda i: 0.015, seed=5)
        counts = [len(_pivots(bars, pct=k, atr_n=DEFAULT_ATR_N)) for k in ATR_SCALES]
        for a, b in zip(counts, counts[1:]):
            self.assertLessEqual(b, a, f"pivot count must not rise with scale: {counts}")


class TestAtrDefinedFromFirstBar(unittest.TestCase):
    """ATR-mode thresholds are ATR *multiples*; an undefined warm-up would fall back
    to `price * k` — a 500%-of-price threshold — and silently emit no pivots."""

    def test_no_none_warmup(self):
        from wavelib.toolkit import _causal_atr
        bars = _walk(30, lambda i: 0.01, seed=9)
        atr = _causal_atr(bars, DEFAULT_ATR_N)
        self.assertTrue(all(a is not None for a in atr))
        self.assertTrue(all(a > 0 for a in atr))

    def test_short_series_still_produces_pivots(self):
        bars = _walk(40, lambda i: 0.02, seed=10)
        self.assertGreater(len(_pivots(bars, pct=2.0, atr_n=DEFAULT_ATR_N)), 0)


if __name__ == "__main__":
    unittest.main()
