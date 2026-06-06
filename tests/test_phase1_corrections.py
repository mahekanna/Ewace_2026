"""
Phase 1 — classifier correctness (docs/research/01_elliott_wave.md §4).

Synthetic ground-truth for the corrected flat/triangle/diagonal classifiers,
firmed-up Fibonacci guidelines, wave-5 projection, and base-channel test.

Run:  python3 -m unittest tests.test_phase1_corrections -v
"""
import unittest

from wavelib import (
    Pivot, Wave, Status,
    classify_correction, triangle_thrust,
    ending_diagonal_rules, leading_diagonal_rules, disambiguate_five,
    elliott_guidelines, project_wave5, base_channel_test,
)


def P(t, price):
    return Pivot(float(t), float(price), "H")


def W(t0, p0, t1, p1):
    k0 = "L" if p1 > p0 else "H"
    k1 = "H" if p1 > p0 else "L"
    return Wave(Pivot(float(t0), float(p0), k0), Pivot(float(t1), float(p1), k1))


class TestFlatVsZigzag(unittest.TestCase):
    def test_zigzag_at_618_boundary(self):
        # A down 100->50 (len50); B up to 80.9 (retr exactly 0.618) -> ZIGZAG
        c = classify_correction([W(1, 100, 2, 50), W(2, 50, 3, 80.9), W(3, 80.9, 4, 30)])
        self.assertEqual(c.status, Status.PASS)
        self.assertIn("ZIGZAG", c.rule)

    def test_regular_flat_in_dead_zone(self):
        # B retraces 75% of A — previously fell into the WARN dead zone.
        c = classify_correction([W(1, 100, 2, 50), W(2, 50, 3, 87.5), W(3, 87.5, 4, 48)])
        self.assertEqual(c.status, Status.PASS)
        self.assertIn("REGULAR FLAT", c.rule)

    def test_expanded_flat_endpoint(self):
        # B>100% (to 110), C surpasses A's end (45 < 50) -> EXPANDED FLAT
        c = classify_correction([W(1, 100, 2, 50), W(2, 50, 3, 110), W(3, 110, 4, 45)])
        self.assertEqual(c.status, Status.PASS)
        self.assertIn("EXPANDED FLAT", c.rule)

    def test_running_flat_endpoint(self):
        # B>100% (to 110), C falls short of A's end (60 > 50) -> RUNNING FLAT
        c = classify_correction([W(1, 100, 2, 50), W(2, 50, 3, 110), W(3, 110, 4, 60)])
        self.assertEqual(c.status, Status.PASS)
        self.assertIn("RUNNING FLAT", c.rule)


class TestTriangle(unittest.TestCase):
    CONTRACTING = [W(1, 100, 2, 50), W(2, 50, 3, 90), W(3, 90, 4, 60),
                   W(4, 60, 5, 80), W(5, 80, 6, 70)]  # lens 50,40,30,20,10

    def test_contracting_all_five_legs(self):
        c = classify_correction(self.CONTRACTING)
        self.assertEqual(c.status, Status.PASS)
        self.assertIn("CONTRACTING", c.rule)

    def test_b_longer_than_a_is_not_contracting(self):
        # lens 40,50,30,20,10 -> not monotonic, no flat boundary -> irregular WARN
        legs = [W(1, 100, 2, 60), W(2, 60, 3, 110), W(3, 110, 4, 80),
                W(4, 80, 5, 100), W(5, 100, 6, 90)]
        c = classify_correction(legs)
        self.assertEqual(c.status, Status.WARN)
        self.assertIn("irregular", c.rule)

    def test_thrust_projection(self):
        t = triangle_thrust(50, 70, direction=-1)
        self.assertEqual(t["min"], 32.5)   # 70 - 0.75*50
        self.assertEqual(t["max"], 7.5)    # 70 - 1.25*50


class TestDiagonalSplit(unittest.TestCase):
    WAVES = [W(1, 100, 2, 130), W(2, 130, 3, 110), W(3, 110, 4, 135),
             W(4, 135, 5, 120), W(5, 120, 6, 138)]

    def test_substructure_notes_differ(self):
        ending = " ".join(r.detail + r.rule for r in ending_diagonal_rules(self.WAVES))
        leading = " ".join(r.detail + r.rule for r in leading_diagonal_rules(self.WAVES))
        self.assertIn("3-3-3-3-3", ending)
        self.assertIn("5-3-5-3-5", leading)
        self.assertNotIn("5-3-5-3-5", ending)

    def test_no_hard_fail_either_way(self):
        for fn in (ending_diagonal_rules, leading_diagonal_rules):
            self.assertFalse(any(r.status is Status.FAIL for r in fn(self.WAVES)))


class TestGuidelinesAndProjection(unittest.TestCase):
    def test_extension_and_wave3_pass_tiers(self):
        impulse = [W(1, 100, 2, 120), W(2, 120, 3, 110), W(3, 110, 4, 150),
                   W(4, 150, 5, 140), W(5, 140, 6, 160)]  # w3=2.0x w1
        res = {r.rule: r for r in elliott_guidelines(impulse)}
        self.assertEqual(res["G extension present"].status, Status.PASS)
        self.assertEqual(res["G wave3 ~1.618-3.618x wave1"].status, Status.PASS)

    def test_project_wave5_has_new_targets(self):
        proj = project_wave5(50, 100, 60, 120)
        self.assertIn("w5=1.618*w1", proj)
        self.assertIn("w5=0.382*w3", proj)


class TestDisambiguateFive(unittest.TestCase):
    def _legs(self, prices):
        return [W(i, prices[i], i + 1, prices[i + 1]) for i in range(5)]

    def test_impulse(self):
        r = disambiguate_five(self._legs([100, 150, 130, 200, 180, 240]))
        self.assertIn("IMPULSE", r.rule)

    def test_diagonal(self):
        r = disambiguate_five(self._legs([100, 130, 118, 138, 128, 140]))  # w4<w1 overlap, net up
        self.assertIn("DIAGONAL", r.rule)

    def test_sideways_triangle(self):
        r = disambiguate_five(self._legs([100, 120, 90, 110, 85, 99]))   # alternates, net not up
        self.assertIn("TRIANGLE", r.rule)


class TestBaseChannel(unittest.TestCase):
    def test_holding_vs_broken(self):
        # lower 0-2 line through (0,100)-(10,120): at t=20 line ~140
        hold = base_channel_test(P(0, 100), P(10, 120), P(5, 140), 20, 150, uptrend=True)
        brk = base_channel_test(P(0, 100), P(10, 120), P(5, 140), 20, 130, uptrend=True)
        self.assertEqual(hold.status, Status.PASS)
        self.assertEqual(brk.status, Status.WARN)


if __name__ == "__main__":
    unittest.main()
