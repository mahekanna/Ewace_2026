"""
Wave forecasting — project the next wave(s) from the current count.

Run:  python3 -m unittest tests.test_forecast -v
"""
import unittest

from wavelib import (
    Pivot, AnchoredCount, forecast_from_count, forecast_waves, trade_plan, TradePlan,
)
from wavelib.wavetree import WaveNode


def _node(p0, p1):
    return WaveNode(Pivot(0.0, float(p0), "L" if p1 > p0 else "H"),
                    Pivot(1.0, float(p1), "H" if p1 > p0 else "L"), 1, "x", "X")


def _count(pattern, prices):
    legs = [_node(prices[i], prices[i + 1]) for i in range(len(prices) - 1)]
    labels = list(zip("12345", legs))
    return AnchoredCount(pattern, 2, labels, 0.3, 0.5, "Minute", "test")


def _bars(points, per=6):
    bars, t = [], 0
    for a, b in zip(points, points[1:]):
        for k in range(1, per + 1):
            p = float(a + (b - a) * k / per)
            bars.append((float(t), p, p, p, p, 1000))
            t += 1
    return bars


class TestForecastFromCount(unittest.TestCase):
    def test_completed_impulse_forecasts_correction(self):
        pc = _count("IMPULSE", [100, 150, 130, 200, 180, 240])   # up impulse
        fc = forecast_from_count(pc, price=235)
        self.assertEqual(fc.direction, "down")
        self.assertIn("A-B-C", fc.next_wave)
        self.assertEqual(fc.invalidation, 100.0)                 # wave-1 origin
        self.assertEqual(len(fc.targets), 3)
        # 0.618 retrace of 100->240 is below the 0.382 retrace
        prices = [p for _, p in fc.targets]
        self.assertTrue(prices[0] > prices[-1])                  # 0.382 above 0.618 (down)

    def test_completed_correction_forecasts_impulse(self):
        pc = _count("ZIGZAG", [100, 70, 85, 60])                 # last leg 85->60 down
        fc = forecast_from_count(pc, price=62)
        self.assertEqual(fc.direction, "up")                     # next opposes last (down) leg
        self.assertIn("impulse", fc.next_wave)
        self.assertTrue(all(p > 60 for _, p in fc.targets))      # projected up from the 60 pivot

    def test_triangle_forecasts_thrust(self):
        pc = _count("TRIANGLE", [100, 130, 110, 124, 114, 120])
        fc = forecast_from_count(pc, price=119)
        self.assertIn("thrust", fc.next_wave)
        self.assertEqual(len(fc.targets), 2)


class TestForecastEndToEnd(unittest.TestCase):
    def test_impulse_bars_forecast_down_correction(self):
        fc = forecast_waves(_bars([100, 150, 130, 200, 180, 240, 205]))
        self.assertIsNotNone(fc)
        self.assertEqual(fc.direction, "down")
        self.assertTrue(0.0 <= fc.confidence <= 1.0)             # honest, inherited


class TestPhase4Projection(unittest.TestCase):
    def test_fib_cluster_groups_overlapping_projections(self):
        from wavelib import fib_cluster
        bands = fib_cluster([100, 101, 102, 150])     # 100/101/102 within 2%
        self.assertEqual(bands[0][1], 3)               # top band has 3 overlaps
        self.assertAlmostEqual(bands[0][0], 101.0)

    def test_correction_complete_projects_extensions(self):
        # a completed correction -> next impulse uses EXTENSION targets (>=1.0x),
        # incl. the Blue Box, not retracements
        pc = _count("ZIGZAG", [100, 70, 85, 60])
        fc = forecast_from_count(pc, price=62)
        labels = " ".join(l for l, _ in fc.targets)
        self.assertIn("equal legs", labels)            # 1.0x Blue Box low
        self.assertIn("Blue Box", labels)

    def test_forecast_has_time_window(self):
        from wavelib import Pivot
        from wavelib.wavetree import WaveNode, AnchoredCount
        D = 86400.0

        def nd(t0, p0, t1, p1):
            return WaveNode(Pivot(t0 * D, float(p0), "L"), Pivot(t1 * D, float(p1), "H"),
                            1, "x", "X")
        legs = [nd(0, 100, 10, 150), nd(10, 150, 15, 130), nd(15, 130, 40, 200),
                nd(40, 200, 45, 180), nd(45, 180, 70, 240)]      # last leg = 25 days
        pc = AnchoredCount("IMPULSE", 2, list(zip("12345", legs)), 0.3, 1.0, "Minor", "t")
        fc = forecast_from_count(pc, price=235)
        self.assertGreater(fc.time_hi_days, fc.time_lo_days)      # [N/3, 3N]
        self.assertAlmostEqual(fc.time_lo_days, 25 / 3.0, places=0)
        self.assertIn("time", fc.time_note.lower())
        self.assertIsNotNone(fc.cluster)


class TestTradePlan(unittest.TestCase):
    def test_plan_synthesizes_direction_and_gates(self):
        # completed up-impulse -> forecast a down correction -> plan is SHORT,
        # gated on a break below the last pivot, with a finite confirm window.
        plan = trade_plan(_bars([100, 150, 130, 200, 180, 240, 205]), symbol="TEST")
        self.assertIsInstance(plan, TradePlan)
        self.assertEqual(plan.direction, "short")
        self.assertIn("break BELOW", plan.entry_trigger)
        self.assertGreater(plan.confirm_window_bars, 0)
        self.assertTrue(0.0 <= plan.confidence <= 1.0)
        self.assertTrue(plan.targets)
        # short stop sits above the last swing high
        self.assertGreater(plan.stop_level, plan.entry_level)

    def test_plan_none_on_no_structure(self):
        self.assertIsNone(trade_plan([(float(i), 100, 100, 100, 100, 1) for i in range(5)]))

    def test_plan_carries_phase5_discipline(self):
        # the plan must expose R:R, a confluence target, a confirmation gate count,
        # and an alternate flip-price (the professional trade-management fields)
        plan = trade_plan(_bars([100, 150, 130, 200, 180, 240, 205, 230, 195, 250]),
                          symbol="TEST")
        self.assertIsInstance(plan, TradePlan)
        self.assertGreaterEqual(plan.reward_risk, 0.0)
        self.assertIsInstance(plan.confluence, int)
        self.assertTrue(plan.cluster is None or isinstance(plan.cluster, list))


if __name__ == "__main__":
    unittest.main()
