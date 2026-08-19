"""
Phase 2 — Neely's predictive layer (CC-3/CC-4/CC-5/FR-3/FR-7/FR-9/CC-9).

These rules are what makes NeoWave claim to be predictive rather than descriptive:
self-defining time limits, and self-confirming post-pattern behaviour that
FALSIFIES a wrong label instead of tolerating it. The 2026-08 audit found them
absent from wavelib, which is why every prior backtest measured a signal with none
of this discipline in it.

Synthetic ground truth, pure stdlib.
Run:  python3 -m unittest tests.test_neowave_logic -v
"""
import unittest

from wavelib import Pivot, Wave, Status
from wavelib.neowave_logic import (
    moves_further_and_faster, preconstructive_filter, post_correction_thrust,
    subwave_time_caps, reverse_logic_rank, falsify_count,
)

DAY = 86400.0


def W(p0, t0, p1, t1):
    """Wave from (price, day) to (price, day)."""
    return Wave(Pivot(t0 * DAY, float(p0), "L"), Pivot(t1 * DAY, float(p1), "H"))


def statuses(rs):
    return [r.status for r in rs]


class TestCC3MovesFurtherAndFaster(unittest.TestCase):
    """The universal confirmation: post-pattern must beat the largest counter-leg
    in BOTH price and time."""

    # up-impulse: 100->150, pull to 120 (the counter leg, 30 days), on to 200
    PATTERN = [W(100, 0, 150, 20), W(150, 20, 120, 50), W(120, 50, 200, 80)]

    def test_confirms_when_further_and_faster(self):
        post = W(200, 80, 130, 95)                 # bigger drop, in 15d < 30d
        r = moves_further_and_faster(self.PATTERN, post, uptrend=True)
        self.assertIs(r.status, Status.PASS)

    def test_fails_when_far_enough_but_too_slow(self):
        post = W(200, 80, 130, 180)                # same size, 100d > 30d
        r = moves_further_and_faster(self.PATTERN, post, uptrend=True)
        self.assertIs(r.status, Status.FAIL)
        self.assertIn("faster=False", r.detail)

    def test_fails_when_fast_enough_but_too_small(self):
        post = W(200, 80, 190, 85)                 # quick but shallow
        r = moves_further_and_faster(self.PATTERN, post, uptrend=True)
        self.assertIs(r.status, Status.FAIL)
        self.assertIn("further=False", r.detail)

    def test_na_without_a_counter_leg(self):
        r = moves_further_and_faster([W(100, 0, 150, 20)], W(150, 20, 100, 30), True)
        self.assertIs(r.status, Status.NA)


class TestCC4PreConstructive(unittest.TestCase):
    """A corrective wave that is FASTER than the wave it corrects is not finished."""

    def test_fast_wave2_falsifies_a_trending_impulse(self):
        w1 = W(100, 0, 150, 40)                    # 40 days up
        w2 = W(150, 40, 130, 50)                   # only 10 days -> not complete
        r = preconstructive_filter(w1, w2)[0]
        self.assertIs(r.status, Status.FAIL)
        self.assertIn("NOT complete", r.detail)

    def test_same_shape_is_only_a_warning_in_a_terminal(self):
        w1 = W(100, 0, 150, 40)
        w2 = W(150, 40, 130, 50)
        r = preconstructive_filter(w1, w2, terminal=True)[0]
        self.assertIs(r.status, Status.WARN)

    def test_wave2_over_3x_is_wrong_degree(self):
        w1 = W(100, 0, 150, 10)
        w2 = W(150, 10, 130, 60)                   # 50d vs 10d = 5x
        r = preconstructive_filter(w1, w2)[0]
        self.assertIs(r.status, Status.FAIL)
        self.assertIn("3x", r.detail)

    def test_normal_proportions_pass(self):
        w1, w2 = W(100, 0, 150, 20), W(150, 20, 130, 50)      # 1.5x
        w3, w4 = W(130, 50, 220, 90), W(220, 90, 195, 150)    # 1.5x
        self.assertEqual(statuses(preconstructive_filter(w1, w2, w3, w4)),
                         [Status.PASS, Status.PASS])


class TestCC5FR3Thrust(unittest.TestCase):
    """A thrust smaller than the correction means the correction is not over."""

    CORR = [W(200, 0, 170, 10), W(170, 10, 190, 20), W(190, 20, 160, 30)]

    def test_adequate_thrust_passes(self):
        size, time_ = post_correction_thrust(self.CORR, W(160, 30, 260, 25 + 30), "ZIGZAG")
        self.assertIs(size.status, Status.PASS)
        self.assertIs(time_.status, Status.PASS)

    def test_undersized_thrust_falsifies_the_correction(self):
        size, _ = post_correction_thrust(self.CORR, W(160, 30, 175, 40), "ZIGZAG")
        self.assertIs(size.status, Status.FAIL)

    def test_complex_correction_demands_more(self):
        """FR-3: after a W-X-Y the next impulse must exceed 161.8%, not merely 100%."""
        thrust = W(160, 30, 205, 45)               # clears 1.0x, not 1.618x
        ok_simple, _ = post_correction_thrust(self.CORR, thrust, "ZIGZAG")
        strict, _ = post_correction_thrust(self.CORR, thrust, "WXY")
        self.assertIs(ok_simple.status, Status.PASS)
        self.assertIs(strict.status, Status.FAIL)


class TestFR7TimeCaps(unittest.TestCase):
    """Self-defining limits: the last leg cannot outlast the legs it follows."""

    def test_zigzag_c_within_a_plus_b_passes(self):
        legs = [W(100, 0, 80, 10), W(80, 10, 92, 25), W(92, 25, 70, 45)]   # 20 <= 25
        self.assertIs(subwave_time_caps(legs, "ZIGZAG")[0].status, Status.PASS)

    def test_zigzag_c_breaching_cap_fails(self):
        legs = [W(100, 0, 80, 5), W(80, 5, 92, 12), W(92, 12, 70, 90)]     # 78 > 12
        r = subwave_time_caps(legs, "ZIGZAG")[0]
        self.assertIs(r.status, Status.FAIL)
        self.assertIn("hidden x-wave", r.detail)

    def test_triangle_e_capped_by_b_c_d(self):
        legs = [W(100, 0, 80, 10), W(80, 10, 95, 20), W(95, 20, 85, 30),
                W(85, 30, 92, 40), W(92, 40, 88, 200)]                     # E huge
        self.assertIs(subwave_time_caps(legs, "TRIANGLE")[0].status, Status.FAIL)

    def test_unknown_pattern_is_na(self):
        self.assertIs(subwave_time_caps([W(1, 0, 2, 1)], "SOMETHING")[0].status, Status.NA)


class TestFR9ReverseLogic(unittest.TestCase):
    def test_prefers_the_least_complete_count(self):
        cands = [("nearly done", 0.9), ("early", 0.2), ("half", 0.5)]
        ranked = reverse_logic_rank(cands, completeness=lambda c: c[1])
        self.assertEqual([c[0] for c in ranked], ["early", "half", "nearly done"])


class TestCC9Falsification(unittest.TestCase):
    """Behaviour over structure — the error-correction mechanism."""

    GOOD = [W(100, 0, 150, 20), W(150, 20, 130, 50), W(130, 50, 220, 80),
            W(220, 80, 195, 130), W(195, 130, 260, 160)]

    def test_clean_impulse_is_not_falsified(self):
        v = falsify_count(self.GOOD, "IMPULSE")
        self.assertFalse(v.falsified, v.reason)
        self.assertIs(v.status, Status.PASS)

    def test_fast_wave2_falsifies(self):
        bad = list(self.GOOD)
        bad[1] = W(150, 20, 130, 23)               # 3-day wave 2 after a 20-day wave 1
        v = falsify_count(bad, "IMPULSE")
        self.assertTrue(v.falsified)
        self.assertIn("CC-4", v.reason)

    def test_weak_post_pattern_move_falsifies(self):
        v = falsify_count(self.GOOD, "IMPULSE",
                          post=W(260, 160, 255, 400), uptrend=True)   # tiny and slow
        self.assertTrue(v.falsified)
        self.assertIn("CC-3", v.reason)

    def test_verdict_lists_every_check_it_ran(self):
        v = falsify_count(self.GOOD, "IMPULSE", post=W(260, 160, 150, 175))
        self.assertGreaterEqual(len(v.results), 3)


if __name__ == "__main__":
    unittest.main()
