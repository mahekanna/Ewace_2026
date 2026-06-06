"""
Wave forecasting — project the next wave(s) from the current count.

Run:  python3 -m unittest tests.test_forecast -v
"""
import unittest

from wavelib import Pivot, AnchoredCount, forecast_from_count, forecast_waves
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


if __name__ == "__main__":
    unittest.main()
