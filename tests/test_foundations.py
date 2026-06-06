"""
Phase 0 foundations — synthetic ground-truth tests (visual-first validation).

Covers:
  F1  zigzag_causal + Pivot.confirmed_t   — causal pivot confirmation timing
  F3  Degree enum + optional degree field — wave-degree hierarchy scaffolding
  F4  swing_pivots                        — N-bar confirmed fractal pivots

Pure stdlib (unittest). Run:  python3 -m unittest tests.test_foundations -v
"""
import unittest

from wavelib import (
    Pivot, Wave, Degree,
    zigzag, zigzag_causal, swing_pivots,
)
from data.avgo import H1 as AVGO_H1  # (t,o,h,l,c) bars


class TestDegree(unittest.TestCase):
    def test_ordering_largest_to_smallest(self):
        # Larger degrees compare greater than smaller ones.
        self.assertGreater(Degree.CYCLE.value, Degree.MINOR.value)
        self.assertGreater(Degree.GRAND_SUPERCYCLE.value, Degree.SUBMINUETTE.value)
        self.assertEqual(min(Degree, key=lambda d: d.value), Degree.SUBMINUETTE)

    def test_nine_levels(self):
        self.assertEqual(len(list(Degree)), 9)

    def test_abbr_present(self):
        # Every degree exposes a short notation string.
        for d in Degree:
            self.assertIsInstance(d.abbr, str)
            self.assertTrue(d.abbr)

    def test_optional_field_defaults_none(self):
        p = Pivot(1.0, 100.0, "L")
        w = Wave(p, Pivot(2.0, 110.0, "H"))
        self.assertIsNone(p.degree)
        self.assertIsNone(w.degree)

    def test_degree_assignable(self):
        p = Pivot(1.0, 100.0, "L", degree=Degree.PRIMARY)
        w = Wave(p, Pivot(2.0, 110.0, "H"), degree=Degree.PRIMARY)
        self.assertEqual(p.degree, Degree.PRIMARY)
        self.assertEqual(w.degree, Degree.PRIMARY)


class TestPivotConfirmedField(unittest.TestCase):
    def test_confirmed_t_defaults_none(self):
        p = Pivot(1.0, 100.0, "H")
        self.assertIsNone(p.confirmed_t)
        self.assertFalse(p.confirmed)

    def test_confirmed_property(self):
        p = Pivot(1.0, 100.0, "H", confirmed_t=5.0)
        self.assertTrue(p.confirmed)


class TestZigzagCausal(unittest.TestCase):
    def test_detection_parity_with_zigzag(self):
        # zigzag_causal must detect the SAME pivots as the validated zigzag;
        # it only adds confirmation timing on top.
        base = [(p.t, p.price, p.kind) for p in zigzag(AVGO_H1, pct=0.05)]
        causal = [(p.t, p.price, p.kind) for p in zigzag_causal(AVGO_H1, pct=0.05)]
        self.assertEqual(causal, base)

    def test_confirmed_t_is_causal(self):
        # Every CONFIRMED pivot is confirmed at or after its price extreme —
        # never before (that would be look-ahead).
        bar_times = {b[0] for b in AVGO_H1}
        pivots = zigzag_causal(AVGO_H1, pct=0.05)
        confirmed = [p for p in pivots if p.confirmed_t is not None]
        self.assertTrue(confirmed)  # at least some pivots confirmed
        for p in confirmed:
            self.assertGreaterEqual(p.confirmed_t, p.t)
            self.assertIn(p.confirmed_t, bar_times)

    def test_last_pivot_is_provisional(self):
        # The final extreme has not been confirmed by a reversal yet.
        pivots = zigzag_causal(AVGO_H1, pct=0.05)
        self.assertIsNone(pivots[-1].confirmed_t)
        self.assertFalse(pivots[-1].confirmed)

    def test_synthetic_confirmation_bar(self):
        # Rise 100->150, then a bar whose low pierces 150*(1-0.10)=135 confirms
        # the swing HIGH at the bar that pierced it, not at the $150 extreme.
        bars = [
            (1, 100, 100, 100, 100),
            (2, 110, 110, 110, 110),
            (3, 130, 130, 130, 130),
            (4, 150, 150, 150, 150),   # extreme high
            (5, 145, 145, 140, 142),   # 140 > 135 -> not yet
            (6, 140, 140, 134, 134),   # low 134 < 135 -> CONFIRMS the high here
            (7, 120, 120, 118, 118),
        ]
        pivots = zigzag_causal(bars, pct=0.10)
        highs = [p for p in pivots if p.kind == "H" and p.confirmed_t is not None]
        self.assertTrue(highs)
        h = highs[0]
        self.assertEqual(h.price, 150)
        self.assertEqual(h.t, 4)            # extreme bar
        self.assertEqual(h.confirmed_t, 6)  # confirmation bar


class TestSwingPivots(unittest.TestCase):
    def test_known_local_extrema(self):
        # values: positions 0..8
        #   [5, 7, 9, 7, 5, 8, 10, 6, 4]
        # n_left=n_right=2 -> swing H@pos2(t3), L@pos4(t5), H@pos6(t7)
        series = [(1, 5), (2, 7), (3, 9), (4, 7), (5, 5),
                  (6, 8), (7, 10), (8, 6), (9, 4)]
        piv = swing_pivots(series, n_left=2, n_right=2)
        self.assertEqual([p.kind for p in piv], ["H", "L", "H"])
        self.assertEqual([p.t for p in piv], [3, 5, 7])

    def test_confirmation_lag(self):
        # A swing pivot is only confirmable n_right bars later.
        series = [(1, 5), (2, 7), (3, 9), (4, 7), (5, 5),
                  (6, 8), (7, 10), (8, 6), (9, 4)]
        piv = swing_pivots(series, n_left=2, n_right=2)
        self.assertEqual([p.confirmed_t for p in piv], [5, 7, 9])
        for p in piv:
            self.assertGreater(p.confirmed_t, p.t)

    def test_too_short_returns_empty(self):
        self.assertEqual(swing_pivots([(1, 5), (2, 7)], n_left=2, n_right=2), [])


if __name__ == "__main__":
    unittest.main()
