"""
Phase 1+2 rebuild — log measurement, calendar degree, and the EWO momentum gate
(docs/research/practitioner/00_PRO_APPLICATION_SPEC.md; docs/research/audit/).

Deterministic, synthetic-ground-truth tests for the professional-application layer.

Run:  python3 -m unittest tests.test_logmomentum -v
"""
import math
import unittest

from wavelib import Pivot, Wave
from wavelib.wavetree import (_momentum_multiplier, anchored_degree, _impulse_quality,
                              WaveNode, momentum_lookup, top_down_count, wave_counts)

DAY = 86400.0
YEAR = 365.25 * DAY


def W(d0, p0, d1, p1):
    return Wave(Pivot(d0 * DAY, float(p0), "L"), Pivot(d1 * DAY, float(p1), "H"))


class TestLogLength(unittest.TestCase):
    def test_log_length_is_log_ratio(self):
        self.assertAlmostEqual(W(0, 100, 1, 200).log_length, math.log(2))
        self.assertAlmostEqual(W(0, 100, 1, 50).log_length, math.log(2))  # symmetric

    def test_log_reveals_large_range_impulse_proportion(self):
        # AVGO-like legs: W3/W1 = 7.74x on a LINEAR scale (matches no Fib, ~0) but
        # ~1.10x on a LOG scale (near equality) — log measurement must see it.
        w1, w2 = W(0, 2.64, 2, 33.16), W(2, 33.16, 3, 15.57)
        w3, w4 = W(3, 15.57, 6, 251.88), W(6, 251.88, 7, 128.5)
        w5 = W(7, 128.5, 9, 414.61)
        # linear ratio would be off the Fib grid; log ratio is ~1.10 -> decent quality
        self.assertGreater(w3.length / w1.length, 5.0)                 # linear: absurd
        self.assertLess(abs(w3.log_length / w1.log_length - 1.10), 0.1)  # log: ~equality
        self.assertGreater(_impulse_quality([w1, w2, w3, w4, w5]), 0.4)


class TestCalendarDegree(unittest.TestCase):
    def _node(self, years):
        return WaveNode(Pivot(0.0, 100, "L"), Pivot(years * YEAR, 200, "H"),
                        1, "motive", "IMPULSE")

    def test_span_maps_to_degree(self):
        self.assertEqual(anchored_degree(self._node(0.01)).name, "SUBMINUETTE")
        self.assertEqual(anchored_degree(self._node(0.75)).name, "MINOR")
        self.assertEqual(anchored_degree(self._node(3.0)).name, "INTERMEDIATE")
        self.assertEqual(anchored_degree(self._node(5.0)).name, "PRIMARY")
        self.assertEqual(anchored_degree(self._node(16.0)).name, "CYCLE")  # 16-yr move

    def test_high_degrees_reachable(self):
        # Primary/Cycle/Supercycle/Grand-Supercycle were dead code before (audit R4)
        self.assertEqual(anchored_degree(self._node(40.0)).name, "SUPERCYCLE")
        self.assertEqual(anchored_degree(self._node(120.0)).name, "GRAND_SUPERCYCLE")


class TestMomentumGate(unittest.TestCase):
    # an up-impulse: w1 up, w2 down, w3 up, w4 down, w5 up
    W1, W2 = W(0, 100, 2, 120), W(2, 120, 3, 110)
    W3, W4 = W(3, 110, 6, 160), W(6, 160, 7, 145)
    W5 = W(7, 145, 9, 180)
    WAVES = [W1, W2, W3, W4, W5]

    def _mom(self, e1, e3, e4, e5):
        d = {2 * DAY: e1, 6 * DAY: e3, 7 * DAY: e4, 9 * DAY: e5}
        return lambda t: d.get(t, 0.0)

    def test_confirmed_impulse_is_boosted(self):
        # EWO peaks at wave 3, wave 5 diverges (lower), wave 4 near zero
        mult = _momentum_multiplier(self.WAVES, self._mom(1.0, 3.0, 0.2, 2.0))
        self.assertGreater(mult, 1.2)

    def test_unconfirmed_wave3_is_penalised(self):
        # 'wave 3' is NOT the momentum peak (wave 5 is) -> not really wave 3
        mult = _momentum_multiplier(self.WAVES, self._mom(1.0, 1.5, 0.2, 3.0))
        self.assertLess(mult, 1.0)

    def test_missing_momentum_is_neutral(self):
        self.assertEqual(_momentum_multiplier(self.WAVES, lambda t: None), 1.0)


class TestMomentumLookup(unittest.TestCase):
    def test_causal_and_defined(self):
        bars = [(float(i) * DAY, 100, 101, 99, 100.0 + i, 1000) for i in range(60)]
        at = momentum_lookup(bars)
        self.assertIsNone(at(-1.0))                    # before first bar
        self.assertIsNotNone(at(50 * DAY))             # EWO defined after warmup
        # uses the most recent bar <= t (causal)
        self.assertEqual(at(50 * DAY), at(50 * DAY + 3600))


class TestTopDownImpulse(unittest.TestCase):
    def _impulse_bars(self):
        # a clean 5-wave impulse with deep (zigzag-detectable) corrections + a
        # trailing leg so the wave-5 high confirms as a pivot; wave 3 is biggest.
        # lead-in (120->100 confirms the impulse low), then 1-2-3-4-5, then a trail
        pts = [120, 100, 140, 116, 190, 150, 210, 180]
        bars, t = [], 0
        for a, b in zip(pts, pts[1:]):
            for k in range(1, 41):                 # 40 bars/leg -> EWO warms up
                p = a + (b - a) * k / 40
                bars.append((float(t), p, p * 1.003, p * 0.997, float(p), 1000.0))
                t += 1
        return bars

    def test_top_down_finds_full_range_impulse(self):
        td = top_down_count(self._impulse_bars(), target=8)
        self.assertIsNotNone(td)
        self.assertEqual(td.pattern, "IMPULSE")
        self.assertEqual(len(td.children), 5)
        self.assertTrue(0.0 < td.confidence <= 0.85)     # honest, never certain

    def test_confidence_is_capped_and_honest(self):
        cs = wave_counts(self._impulse_bars(), scales=(0.05, 0.10), max_alternates=1)
        self.assertTrue(cs)
        self.assertLessEqual(cs[0].confidence, 0.85)      # no 100% counts


if __name__ == "__main__":
    unittest.main()
