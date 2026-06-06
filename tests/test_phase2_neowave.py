"""
Phase 2 — NeoWave construction & logic (docs/research/02_neowave_neely.md §4).

Synthetic ground-truth for the bottom-up monowave/polywave constructor, two-stage
impulse confirmation, terminal rules, neutral triangle, the diametric/symmetrical
complex-correction zoo, and x-wave computation.

Run:  python3 -m unittest tests.test_phase2_neowave -v
"""
import unittest

from wavelib import (
    Pivot, Wave, Status,
    label_monowaves, monowave_candidates, group_polywaves,
    two_four_confirmation, confirm_completion, CompletionSignal,
    terminal_rules, is_neutral_triangle,
    classify_complex_correction, x_wave_check,
)

DAY = 86400.0


def P(days, price, kind="H"):
    return Pivot(days * DAY, float(price), kind)


def seg(length, days):
    """A standalone leg with a given price length and duration (direction agnostic)."""
    return Wave(Pivot(0.0, 0.0, "L"), Pivot(days * DAY, float(length), "H"))


def chain(*pivots):
    """Build CHAINED waves (m1.start == m0.end) from consecutive pivots — the
    contract monowave_candidates expects (so the Rule-3-vs-4 overlap test is real)."""
    return [Wave(pivots[i], pivots[i + 1]) for i in range(len(pivots) - 1)]


class TestLabelMonowaves(unittest.TestCase):
    # Chained path: edges (:?), then w1 deep-retraced by w2 (corrective :3),
    # then w2 only shallow-retraced by w3 (motive :5). (GAP-1 candidate core.)
    PIVOTS = [P(0, 100, "L"), P(6, 160, "H"), P(12, 100, "L"),
              P(20, 220, "H"), P(40, 200, "L")]

    def test_edges_provisional_interior_labelled(self):
        labelled = label_monowaves(self.PIVOTS)
        labels = [lab for (_w, lab) in labelled]
        self.assertEqual(labels[0], ":?")          # first monowave: no m0
        self.assertEqual(labels[-1], ":?")         # last monowave: no m2
        self.assertTrue(labels[1].startswith(":3"))  # deeply retraced -> corrective
        self.assertTrue(labels[2].startswith(":5"))  # only shallow-retraced -> motive

    def test_retracement_rule_number_present(self):
        labelled = label_monowaves(self.PIVOTS)
        self.assertIn("(R", labelled[1][1])


class TestMonowaveCandidates(unittest.TestCase):
    def test_motive_when_shallow_retrace(self):
        m0, m1, m2 = seg(10, 1), seg(10, 1), seg(3, 1)        # m2 retraces 30% of m1
        self.assertIn(":5", monowave_candidates(m0, m1, m2))

    def test_ambiguous_deep_retrace(self):
        # 70% retrace that does NOT re-enter m0's range (Rule 3, no overlap) -> the
        # genuinely ambiguous 1st-vs-a-wave case, two candidates :3/:5. Chained so
        # the overlap test is meaningful.
        m0, m1, m2 = chain(P(0, 100, "L"), P(1, 110, "H"), P(2, 60, "L"), P(3, 95, "H"))
        c = monowave_candidates(m0, m1, m2)
        self.assertIn(":5", c)
        self.assertIn(":3", c)                                # genuinely ambiguous -> >1 candidate

    def test_overlap_back_into_m0_flags_c3(self):
        # 80% retrace that DOES re-enter m0's price territory (Rule 4 overlap) ->
        # corrective c-wave candidate, not motive (the GAP-1 fix).
        m0, m1, m2 = chain(P(0, 100, "L"), P(1, 110, "H"), P(2, 100, "L"), P(3, 108, "H"))
        c = monowave_candidates(m0, m1, m2)
        self.assertIn(":c3", c)
        self.assertNotIn(":5", c)

    def test_overshoot_not_a_retrace(self):
        m0, m1, m2 = seg(10, 1), seg(10, 1), seg(20, 1)       # 200% -> reversal/last
        self.assertIn(":3", monowave_candidates(m0, m1, m2))


class TestGroupPolywaves(unittest.TestCase):
    def test_finds_zigzag_polywave(self):
        pivots = [P(0, 100, "H"), P(1, 50, "L"), P(2, 70, "H"),
                  P(3, 30, "L"), P(4, 55, "H"), P(5, 20, "L")]
        groups = group_polywaves(label_monowaves(pivots))
        self.assertTrue(groups)
        for g in groups:
            self.assertIn(len(g), (3, 5))


class TestTwoFourConfirmation(unittest.TestCase):
    # 2-4 line through (0d,100)-(10d,120): value at 20d ~ 140
    W5 = Wave(P(15, 130, "L"), P(18, 160, "H"))

    def test_completed_impulse_both_stages_pass(self):
        res = two_four_confirmation(self.W5, P(0, 100), P(10, 120),
                                    20 * DAY, 125, uptrend=True)
        self.assertTrue(all(r.status is Status.PASS for r in res))

    def test_unbroken_line_stage1_warns(self):
        res = two_four_confirmation(self.W5, P(0, 100), P(10, 120),
                                    20 * DAY, 150, uptrend=True)
        self.assertEqual(res[0].status, Status.WARN)


class TestConfirmCompletion(unittest.TestCase):
    """GAP-3: stateful per-bar 2-4 completion monitor."""
    # 2-4 line through (0d,100)-(10d,120) rises 2/day; W5 builds 130->160 over 3d
    # ending day 18, origin 130.
    W5 = Wave(P(15, 130, "L"), P(18, 160, "H"))
    W2 = P(0, 100, "L")
    W4 = P(10, 120, "L")

    def _bar(self, day, close):
        return (day * DAY, close, close, close, close, 1000)

    def test_first_break_then_full_retrace_confirms_stage2(self):
        fwd = [self._bar(20, 135),   # line ~140 -> broke fast (stage 1)
               self._bar(21, 125)]   # <=130 origin within w5 time (stage 2)
        sig = confirm_completion(self.W5, self.W2, self.W4, fwd, uptrend=True)
        self.assertIsInstance(sig, CompletionSignal)
        self.assertTrue(sig.confirmed)
        self.assertEqual(sig.stage, 2)
        self.assertEqual(sig.bars_elapsed, 0)        # first bar already broke the line
        self.assertEqual(sig.at_t, 20 * DAY)

    def test_line_holds_is_pending(self):
        fwd = [self._bar(20, 145),   # line ~140, price above -> not broken
               self._bar(21, 143)]   # line ~142, still above
        sig = confirm_completion(self.W5, self.W2, self.W4, fwd, uptrend=True)
        self.assertFalse(sig.confirmed)
        self.assertEqual(sig.stage, 0)
        self.assertIsNone(sig.at_t)

    def test_slow_break_does_not_confirm(self):
        # break happens, but only LONG after w5's 3-day build -> not a valid (fast)
        # confirmation per Neely's time gate.
        fwd = [self._bar(30, 110)]   # elapsed 12d >> w5 3d
        sig = confirm_completion(self.W5, self.W2, self.W4, fwd, uptrend=True)
        self.assertFalse(sig.confirmed)
        self.assertEqual(sig.stage, 0)


class TestTerminalRules(unittest.TestCase):
    TERMINAL = [Wave(P(0, 100, "L"), P(2, 130, "H")),
                Wave(P(2, 130, "H"), P(3, 115, "L")),   # w2 retrace 50% of w1
                Wave(P(3, 115, "L"), P(5, 150, "H")),
                Wave(P(5, 150, "H"), P(6, 125, "L")),   # w4 overlaps w1 top (130)
                Wave(P(6, 125, "L"), P(8, 145, "H"))]

    def test_overlap_terminal_passes_basic(self):
        res = terminal_rules(self.TERMINAL)
        self.assertEqual(res[0].status, Status.PASS)            # overlap present
        self.assertFalse(any(r.status is Status.FAIL for r in res))
        w2_rule = [r for r in res if "wave2" in r.rule][0]
        self.assertEqual(w2_rule.status, Status.PASS)           # 50% <= 61.8%

    def test_no_overlap_is_na(self):
        no_overlap = [Wave(P(0, 100, "L"), P(2, 130, "H")),
                      Wave(P(2, 130, "H"), P(3, 120, "L")),
                      Wave(P(3, 120, "L"), P(5, 150, "H")),
                      Wave(P(5, 150, "H"), P(6, 140, "L")),     # stays above w1 top
                      Wave(P(6, 140, "L"), P(8, 160, "H"))]
        res = terminal_rules(no_overlap)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].status, Status.NA)


class TestNeutralTriangle(unittest.TestCase):
    def test_neutral_triangle_pass(self):
        legs = [seg(30, 1), seg(20, 1), seg(50, 1), seg(25, 1), seg(28, 1)]  # C longest, A~E
        self.assertEqual(is_neutral_triangle(legs).status, Status.PASS)

    def test_c_not_longest_warns(self):
        legs = [seg(60, 1), seg(20, 1), seg(50, 1), seg(25, 1), seg(28, 1)]
        self.assertEqual(is_neutral_triangle(legs).status, Status.WARN)


class TestComplexZoo(unittest.TestCase):
    def test_diametric_diamond(self):
        legs = [seg(10, 1), seg(12, 1), seg(14, 1), seg(20, 1),
                seg(14, 1), seg(12, 1), seg(10, 1)]  # middle longest
        r = classify_complex_correction(legs)
        self.assertIn("diamond", r.rule)
        self.assertEqual(r.status, Status.PASS)

    def test_diametric_bowtie(self):
        legs = [seg(20, 1), seg(18, 1), seg(15, 1), seg(8, 1),
                seg(15, 1), seg(18, 1), seg(20, 1)]  # middle shortest
        self.assertIn("bowtie", classify_complex_correction(legs).rule)

    def test_symmetrical_nine_legs(self):
        legs = [seg(10, 1), seg(5, 1), seg(11, 1), seg(5, 1), seg(10, 1),
                seg(5, 1), seg(10, 1), seg(5, 1), seg(11, 1)]
        r = classify_complex_correction(legs)
        self.assertIn("SYMMETRICAL", r.rule)
        self.assertEqual(r.status, Status.PASS)


class TestXWave(unittest.TestCase):
    PRIOR = seg(100, 1)

    def test_small_x_pass(self):
        self.assertEqual(x_wave_check(self.PRIOR, seg(50, 1)).status, Status.PASS)

    def test_large_x_warn(self):
        self.assertEqual(x_wave_check(self.PRIOR, seg(80, 1)).status, Status.WARN)

    def test_oversized_x_fail(self):
        self.assertEqual(x_wave_check(self.PRIOR, seg(120, 1)).status, Status.FAIL)


if __name__ == "__main__":
    unittest.main()
