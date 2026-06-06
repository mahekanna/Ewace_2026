"""
Stage 6 — EWF (elliottwave-forecast.com) derived features.

Synthetic checks for the Blue Box zone, swing-sequence count, and running-triangle
flag harvested in docs/research/deep/09-10.

Run:  python3 -m unittest tests.test_ewf -v
"""
import unittest

from wavelib import Pivot, Wave, Status, blue_box_zone, swing_sequence, is_running_triangle

DAY = 86400.0


def W(t0, p0, t1, p1):
    return Wave(Pivot(float(t0), float(p0), "L" if p1 > p0 else "H"),
                Pivot(float(t1), float(p1), "H" if p1 > p0 else "L"))


class TestBlueBox(unittest.TestCase):
    def test_zigzag_down_extension_zone(self):
        # A down 100->80 (len 20), B up to 90 -> C zone = 90-100%..161.8% of A, downward
        lo, hi = blue_box_zone(100, 80, 90)
        self.assertAlmostEqual(hi, 70.0)             # 90 - 1.0*20
        self.assertAlmostEqual(lo, 57.64, places=2)  # 90 - 1.618*20

    def test_up_leg_extends_upward(self):
        lo, hi = blue_box_zone(100, 120, 110)        # A up 20, B down to 110
        self.assertAlmostEqual(lo, 130.0)            # 110 + 1.0*20
        self.assertAlmostEqual(hi, 142.36, places=2)  # 110 + 1.618*20


class TestSwingSequence(unittest.TestCase):
    def _piv(self, n):
        return [Pivot(i * DAY, 100 + (i % 2) * 10, "H" if i % 2 else "L") for i in range(n + 1)]

    def test_motive_complete_at_5(self):
        self.assertEqual(swing_sequence(pivots=self._piv(5))["status"], "MOTIVE-COMPLETE")

    def test_corrective_complete_at_3(self):
        self.assertEqual(swing_sequence(pivots=self._piv(3))["status"], "CORRECTIVE-COMPLETE")

    def test_incomplete_between(self):
        s = swing_sequence(pivots=self._piv(4))
        self.assertEqual(s["status"], "INCOMPLETE")
        self.assertEqual(s["next_motive"], 5)


class TestRunningTriangle(unittest.TestCase):
    def test_running_when_b_beyond_origin(self):
        # A down 100->80; B up to 105 (beyond origin 100) -> running
        legs = [W(0, 100, 1, 80), W(1, 80, 2, 105), W(2, 105, 3, 88),
                W(3, 88, 4, 100), W(4, 100, 5, 92)]
        self.assertEqual(is_running_triangle(legs).status, Status.PASS)

    def test_ordinary_triangle_not_running(self):
        legs = [W(0, 100, 1, 80), W(1, 80, 2, 95), W(2, 95, 3, 84),
                W(3, 84, 4, 92), W(4, 92, 5, 87)]
        self.assertEqual(is_running_triangle(legs).status, Status.NA)


if __name__ == "__main__":
    unittest.main()
