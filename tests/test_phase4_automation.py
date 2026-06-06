"""
Phase 4 — automation & validation (docs/research/04_automation_validation.md §4).

Synthetic ground-truth for multi-scale labeling, auto-degree, the causal backtest
harness (resolve/aggregate/WFO/no-look-ahead), and the SVG chart emitter.

Run:  python3 -m unittest tests.test_phase4_automation -v
"""
import unittest
import xml.etree.ElementTree as ET

from wavelib import (
    Pivot, Wave,
    zigzag_multiscale, label_and_validate, assign_degrees_neely,
    backtest_reversals, ReversalEvent, render_chart,
)
import wavelib.automation as automation
from wavelib.backtest import _resolve, _aggregate, _wfo_windows, ReversalOutcome


def make_bars(points, per=5, vol=1000):
    """Piecewise-linear flat OHLCV bars through `points` (per bars per leg).
    Flat bars (o=h=l=c) keep intrabar range zero so only the leg turns reverse."""
    bars, t = [], 0
    for a, b in zip(points, points[1:]):
        for k in range(1, per + 1):
            price = float(a + (b - a) * k / per)
            bars.append((float(t), price, price, price, price, vol))
            t += 1
    return bars


# a clean 5-wave impulse: 100->150->120->200->170->230, then a confirming drop
IMPULSE_BARS = make_bars([100, 150, 120, 200, 170, 230, 200])


class TestLabelAndValidate(unittest.TestCase):
    def test_finds_clean_impulse(self):
        cands = label_and_validate(IMPULSE_BARS)
        self.assertTrue(cands)
        self.assertEqual(cands[0].hard_fails, 0)               # best is clean
        self.assertTrue(any(c.count_type == "IMPULSE" for c in cands))

    def test_no_pivots_no_candidates(self):
        straight = make_bars([100, 300], per=20)               # monotonic, no reversal
        self.assertEqual(label_and_validate(straight), [])


class TestMultiscale(unittest.TestCase):
    def test_pivot_count_non_increasing_with_scale(self):
        scales = (0.03, 0.07, 0.15, 0.30)
        streams = zigzag_multiscale(IMPULSE_BARS, scales=scales)
        counts = [len(streams[s]) for s in scales]
        for a, b in zip(counts, counts[1:]):
            self.assertGreaterEqual(a, b)


class TestAutoDegree(unittest.TestCase):
    def test_returns_heuristic_candidates(self):
        res = assign_degrees_neely(IMPULSE_BARS, base_scale=0.03)
        self.assertTrue(res)
        self.assertTrue(all(c.degree_confidence == "HEURISTIC" for c in res))


class TestBacktestResolveAggregate(unittest.TestCase):
    def test_resolve_reversal(self):
        ev = ReversalEvent(entry_t=0.0, score=4, zone=(99, 101), invalidation=90, entry_price=100)
        bars = make_bars([100, 110], per=5)                    # rises to 110 -> hits 105 target
        out = _resolve(ev, bars, min_reversal_pct=0.05, bullish=True)
        self.assertEqual(out.outcome, "REVERSAL")

    def test_resolve_invalidation(self):
        ev = ReversalEvent(entry_t=0.0, score=4, zone=(99, 101), invalidation=90, entry_price=100)
        bars = make_bars([100, 80], per=5)                     # falls through 90 invalidation
        out = _resolve(ev, bars, min_reversal_pct=0.05, bullish=True)
        self.assertEqual(out.outcome, "INVALIDATED")

    def test_aggregate_hit_rate(self):
        ev = ReversalEvent(0.0, 4, (0, 0), 0, 100)
        outs = [
            ReversalOutcome(ev, "REVERSAL", 1, 105, 0.05),
            ReversalOutcome(ev, "REVERSAL", 1, 105, 0.05),
            ReversalOutcome(ev, "INVALIDATED", 1, 90, -0.10),
            ReversalOutcome(ev, "OPEN", None, None, None),
        ]
        stats = _aggregate(outs)
        self.assertAlmostEqual(stats.hit_rate, 2 / 3)          # OPEN excluded from denom
        self.assertEqual(stats.n_open, 1)


class TestWalkForward(unittest.TestCase):
    def test_windows_no_overlap(self):
        wins = _wfo_windows(100, train=40, test=20, step=20)
        self.assertTrue(wins)
        for (is_lo, is_hi), (oos_lo, oos_hi) in wins:
            self.assertEqual(is_hi, oos_lo)                    # OOS starts where IS ends
            self.assertLessEqual(oos_hi, 100)
            self.assertEqual(is_hi - is_lo, 40)
            self.assertEqual(oos_hi - oos_lo, 20)


class TestNoLookAhead(unittest.TestCase):
    def test_label_never_sees_future(self):
        seen = []
        original = automation.label_and_validate

        def recorder(bars, **kw):
            seen.append(bars[-1][0])                           # last bar t handed to labeler
            return []                                          # no events -> fast

        automation.label_and_validate = recorder
        try:
            bars = make_bars([100, 130, 110, 150], per=3)
            backtest_reversals(bars, min_history=2)
            cursor_ts = [bars[t][0] for t in range(2, len(bars))]
            self.assertEqual(seen, cursor_ts)                  # exactly the cursor, never ahead
        finally:
            automation.label_and_validate = original


class TestRenderChart(unittest.TestCase):
    WAVES = [
        Wave(Pivot(0, 100, "L"), Pivot(10, 150, "H")),
        Wave(Pivot(10, 150, "H"), Pivot(20, 120, "L")),
        Wave(Pivot(20, 120, "L"), Pivot(30, 200, "H")),
    ]

    def test_valid_xml(self):
        svg = render_chart(self.WAVES, title="t")
        ET.fromstring(svg)                                     # raises if invalid

    @staticmethod
    def _tag(e):
        return e.tag.split("}")[-1]

    def test_one_polyline_per_wave(self):
        svg = render_chart(self.WAVES)
        root = ET.fromstring(svg)
        polylines = [e for e in root.iter() if self._tag(e) == "polyline"]
        self.assertEqual(len(polylines), len(self.WAVES))

    def test_projection_and_zone_elements(self):
        svg = render_chart(self.WAVES, projections={"w5": [210, 230]}, zones=[(118, 125)])
        root = ET.fromstring(svg)
        lines = [e for e in root.iter() if self._tag(e) == "line"]
        rects = [e for e in root.iter() if self._tag(e) == "rect"]
        self.assertEqual(len(lines), 2)                        # two projection targets
        self.assertEqual(len(rects), 1)                        # one zone


if __name__ == "__main__":
    unittest.main()
