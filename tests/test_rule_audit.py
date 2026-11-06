"""
Rule audit — does the COUNTER obey docs/RULESET.md?
====================================================
One test per rule. Every test exercises the code path that produces a count
(`wavetree` node constructors, the top-down partition search, `wave_counts`,
`forecast_from_count`) — not just the standalone validators — because a rule the
validator knows but the counter ignores is a rule that is not applied.

Synthetic structures are built from pivots with explicit times so both the price
and the time rules can be tested.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wavelib.rules import Pivot, Wave                                     # noqa: E402
from wavelib import wavetree as wt                                       # noqa: E402
from wavelib.forecast import forecast_from_count                         # noqa: E402

DAY = 86400.0


def P(day, price, kind=None):
    return Pivot(day * DAY, float(price), kind or "?")


def path(*pts):
    """pts: (day, price) alternating lows/highs -> Pivot list with kinds inferred."""
    piv = []
    for i, (d, p) in enumerate(pts):
        if i == 0:
            kind = "L" if pts[1][1] > p else "H"
        else:
            kind = "H" if p > pts[i - 1][1] else "L"
        piv.append(P(d, p, kind))
    return piv


def mono(piv):
    """Monowave nodes (degree 0) between consecutive pivots."""
    return [wt.WaveNode(piv[i], piv[i + 1], 0, "leg", "MONOWAVE") for i in range(len(piv) - 1)]


def bars_from_pivots(piv, steps=6):
    """Daily bars that walk linearly between pivots (so ZigZag finds exactly them)."""
    bars = []
    for a, b in zip(piv, piv[1:]):
        n = max(1, int((b.t - a.t) / DAY))
        for k in range(n):
            f0, f1 = k / n, (k + 1) / n
            p0 = a.price + (b.price - a.price) * f0
            p1 = a.price + (b.price - a.price) * f1
            t = a.t + k * DAY
            bars.append((t, p0, max(p0, p1), min(p0, p1), p1, 1000))
    last = piv[-1]
    bars.append((last.t, last.price, last.price, last.price, last.price, 1000))
    return bars


# A clean textbook impulse: W3 extended (>1.618x W1), W2 ~0.5, W4 ~0.3, no overlap,
# S&B fine, nothing inside W5 breaks the 2-4 line.
CLEAN_IMPULSE = path((0, 100), (20, 120), (30, 110), (60, 160), (70, 148), (90, 170))


class A_ImpulseHardRules(unittest.TestCase):
    def test_clean_impulse_is_accepted(self):
        node = wt._impulse_node(mono(CLEAN_IMPULSE), 1)
        self.assertIsNotNone(node)
        self.assertEqual(node.pattern, "IMPULSE")

    def test_R1_wave2_beyond_wave1_origin_rejected(self):
        piv = path((0, 100), (20, 120), (30, 98), (60, 160), (70, 148), (90, 170))
        self.assertIsNone(wt._impulse_node(mono(piv), 1))
        self.assertEqual(wt._impulse_partitions(piv, 0, 5, None), [])

    def test_R2_wave3_shortest_rejected(self):
        piv = path((0, 100), (20, 130), (30, 115), (40, 125), (45, 118), (90, 160))
        self.assertIsNone(wt._impulse_node(mono(piv), 1))
        self.assertEqual(wt._impulse_partitions(piv, 0, 5, None), [])

    def test_R3_wave4_into_wave1_rejected_as_impulse(self):
        piv = path((0, 100), (20, 120), (30, 110), (60, 160), (70, 118), (90, 170))
        self.assertIsNone(wt._impulse_node(mono(piv), 1))
        self.assertEqual(wt._impulse_partitions(piv, 0, 5, None), [])

    def test_N_extension_rule_one_wave_must_be_at_least_1_618x_next_longest(self):
        # 1/3/5 all ~20 points: no extension -> NeoWave says not an impulse
        piv = path((0, 100), (20, 120), (30, 110), (60, 131), (70, 121), (90, 141))
        self.assertIsNone(wt._impulse_node(mono(piv), 1), "no extended wave")
        self.assertEqual(wt._impulse_partitions(piv, 0, 5, None), [])

    def test_N_similarity_and_balance_w2_vs_w4_hard(self):
        # W2: 10 points in 10 days; W4: 2 points in 1 day -> price 5x, time 10x: neither holds
        piv = path((0, 100), (20, 120), (30, 110), (60, 160), (61, 158), (90, 190))
        self.assertIsNone(wt._impulse_node(mono(piv), 1), "S&B: neither price nor time in [1/3,3]")

    def test_N_two_four_line_wave5_must_not_break_it(self):
        # degree-2 impulse whose wave-5 child dips below the 2-4 trendline
        w1 = path((0, 100), (20, 120))
        w2 = path((20, 120), (30, 110))
        w3 = path((30, 110), (60, 160))
        w4 = path((60, 160), (70, 148))
        # 2-4 line through (30,110)-(70,148): slope 0.95/day -> at day 75 = 152.75, day 80 = 157.5
        w5_bad = path((70, 148), (75, 165), (80, 150), (90, 175))   # day 80 @150 < 157.5: breaks line
        w5_ok = path((70, 148), (75, 165), (80, 160), (90, 175))    # 160 > 157.5: holds
        def leg(piv, pattern, role):
            kids = mono(piv)
            return wt.WaveNode(piv[0], piv[-1], 1, role, pattern, kids, [], 0.8) if len(kids) > 1 \
                else wt.WaveNode(piv[0], piv[-1], 1, role, pattern, kids, [], 0.8)
        ok = [leg(w1, "IMPULSE", "motive"), leg(w2, "ZIGZAG", "corrective"), leg(w3, "IMPULSE", "motive"),
              leg(w4, "ZIGZAG", "corrective"), leg(w5_ok, "IMPULSE", "motive")]
        bad = ok[:4] + [leg(w5_bad, "IMPULSE", "motive")]
        self.assertIsNotNone(wt._impulse_node(ok, 2))
        self.assertIsNone(wt._impulse_node(bad, 2), "W5 broke the 2-4 line")


class B_CorrectionRules(unittest.TestCase):
    def test_zigzag_C_must_surpass_A_end(self):
        good = path((0, 100), (10, 80), (15, 90), (30, 70))     # B 50%, C beyond A end
        bad = path((0, 100), (10, 80), (15, 90), (30, 85))      # B 50%, C fails to pass 80
        self.assertEqual(wt._correction_node(mono(good), 1).pattern, "ZIGZAG")
        self.assertIsNone(wt._correction_node(mono(bad), 1), "C must surpass the end of A")
        self.assertEqual(wt._correction_partitions(bad, 0, 3), [])

    def test_regular_flat_needs_C_near_A(self):
        good = path((0, 100), (10, 80), (20, 97), (35, 78))     # B 85%, C ~95% of A, beyond A end
        bad = path((0, 100), (10, 80), (20, 97), (35, 90))      # B 85%, C only 35% of A: double failure
        self.assertEqual(wt._correction_node(mono(good), 1).pattern, "FLAT")
        self.assertIsNone(wt._correction_node(mono(bad), 1), "B<100% and C<<A is no flat at all")

    def test_expanded_and_running_flats(self):
        expanded = path((0, 100), (10, 80), (20, 105), (40, 70))   # B 125%, C beyond A end
        running = path((0, 100), (10, 80), (20, 105), (40, 88))    # B 125%, C short of A end
        self.assertEqual(wt._correction_node(mono(expanded), 1).pattern, "FLAT")
        self.assertEqual(wt._correction_node(mono(running), 1).pattern, "FLAT")

    def test_N_similarity_and_balance_A_vs_C_hard(self):
        # RULESET §E: at least ONE of price/time must be within [1/3, 3x]
        one_holds = path((0, 100), (30, 70), (35, 85), (36, 55))   # price 1.0x ok, time 30x bad
        self.assertIsNotNone(wt._correction_node(mono(one_holds), 1), "price proportion holds")
        bad = path((0, 100), (30, 90), (35, 95), (36, 60))         # price 3.5x AND time 30x
        self.assertIsNone(wt._correction_node(mono(bad), 1), "A vs C: neither price nor time holds")

    def test_triangle_needs_corrective_legs_and_convergence(self):
        piv = path((0, 100), (10, 80), (20, 95), (30, 84), (40, 92), (50, 87))
        kids = [wt.WaveNode(a, b, 1, "corrective", "ZIGZAG", mono([a, b]), [], 0.7)
                for a, b in zip(piv, piv[1:])]
        self.assertIsNotNone(wt._triangle_node(kids, 2))
        self.assertIsNone(wt._triangle_node(mono(piv), 1), "monowave legs cannot be a triangle")
        diverging = path((0, 100), (10, 90), (20, 104), (30, 85), (40, 108), (50, 80))
        kids2 = [wt.WaveNode(a, b, 1, "corrective", "ZIGZAG", mono([a, b]), [], 0.7)
                 for a, b in zip(diverging, diverging[1:])]
        self.assertIsNotNone(wt._triangle_node(kids2, 2))   # expanding is legal
        flat_sides = path((0, 100), (10, 80), (20, 100), (30, 80), (40, 100), (50, 80))
        kids3 = [wt.WaveNode(a, b, 1, "corrective", "ZIGZAG", mono([a, b]), [], 0.7)
                 for a, b in zip(flat_sides, flat_sides[1:])]
        self.assertIsNone(wt._triangle_node(kids3, 2), "parallel sides are not a triangle")


class D_RankingAndCompleteness(unittest.TestCase):
    def test_wave_counts_ranked_by_confidence_times_coverage_without_bonuses(self):
        from data.avgo import DAILY
        for end in (600, 900, 1200, len(DAILY)):
            cs = wt.wave_counts(DAILY[end - 300:end], max_alternates=3)
            # tier 1: counts that end at the window end (the present) come first ...
            flags = [c.ends_now for c in cs]
            self.assertEqual(flags, sorted(flags, reverse=True), f"present-ending first: {flags}")
            # ... and within each tier the order is confidence x coverage, nothing else
            for tier in (True, False):
                keys = [c.confidence * c.coverage for c in cs if c.ends_now == tier]
                self.assertEqual(keys, sorted(keys, reverse=True),
                                 f"ranking must follow confidence x coverage: {keys}")

    def test_in_progress_final_wave_is_expressible(self):
        """Impulse up to a top, then A down, B up (lower high), and price now falling
        below A's low with no confirmed pivot yet: the honest count is a correction
        whose wave C is IN PROGRESS, not a completed structure ending at B."""
        imp = path((0, 100), (20, 130), (30, 115), (60, 190), (75, 170), (100, 230))
        # A breaks below wave 1's top (130), so no impulse can end on the B high (R3),
        # and the only structure reaching the present is the running correction.
        corr = path((100, 230), (125, 120), (140, 150), (170, 100))   # C running, unconfirmed
        piv = imp + corr[1:]
        bars = bars_from_pivots(piv)
        cs = wt.wave_counts(bars, max_alternates=0)
        self.assertTrue(cs)
        c = cs[0]
        self.assertTrue(getattr(c, "in_progress", False), f"got {c.pattern} {c}")
        self.assertIn(c.pattern, ("ZIGZAG", "FLAT", "WXY", "CORRECTION"))
        last_label, last_leg = c.labels[-1]
        self.assertEqual(last_label, "C")
        self.assertAlmostEqual(last_leg.start.price, 150.0, places=0)
        self.assertLess(last_leg.end.price, 120.0)
        self.assertEqual(c.labels[0][1].start.price, 230.0, "the correction starts at the impulse top")


class F_Forecast(unittest.TestCase):
    def _count(self, piv, pattern, in_progress=False):
        kids = mono(piv)
        labs = {"ZIGZAG": "ABC", "FLAT": "ABC", "IMPULSE": "12345"}[pattern]
        node = wt.WaveNode(piv[0], piv[-1], 1, "corrective", pattern, kids, [], 0.6)
        ac = wt._anchored_from(node, 0.6, 1.0)
        ac.labels = list(zip(labs, kids))
        ac.in_progress = in_progress
        return ac

    def test_forecast_anchors_to_the_confirmed_pivot_not_the_current_price(self):
        zz = path((0, 100), (10, 80), (15, 90), (30, 70))       # complete zigzag down -> expect up
        f_near = forecast_from_count(self._count(zz, "ZIGZAG"), 72.0)
        f_far = forecast_from_count(self._count(zz, "ZIGZAG"), 95.0)   # price already ran
        self.assertEqual(f_near.direction, "up")
        self.assertEqual(dict(f_near.targets), dict(f_far.targets),
                         "targets must not move with the current price")
        self.assertEqual(f_near.invalidation, 70.0)

    def test_forecast_for_in_progress_C_projects_C_completion(self):
        piv = path((0, 230), (25, 180), (40, 210), (70, 165))   # C down running (A=50)
        f = forecast_from_count(self._count(piv, "ZIGZAG", in_progress=True), 165.0)
        self.assertEqual(f.direction, "down")
        tg = dict(f.targets)
        self.assertTrue(any(abs(v - 160.0) < 0.5 for v in tg.values()), f"C = A target: {tg}")   # 210-50
        self.assertEqual(f.invalidation, 210.0, "above B's end the running C is void")


if __name__ == "__main__":
    unittest.main()
