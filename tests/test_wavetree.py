"""
Recursive multi-degree wave tree (Stage 1 of the deeper engine).

Synthetic ground-truth: a hand-built 2-level fractal — a 5-wave impulse whose
motive legs are themselves 5-wave impulses and whose corrective legs are 3-wave
zigzags — must compact into a 1 root IMPULSE with 5 children of the right type,
proving recursive sub-structure validation.

Run:  python3 -m unittest tests.test_wavetree -v
"""
import unittest

from wavelib import Pivot
from wavelib.wavetree import build_tree_from_pivots, deepest_degree

DAY = 86400.0


def _pivots(deltas, start=100.0):
    t, price = 0.0, start
    piv = [Pivot(0.0, start, "L")]
    for d in deltas:
        t += DAY
        price += d
        piv.append(Pivot(t, round(price, 4), "H" if d > 0 else "L"))
    return piv


MI = [3, -1, 5, -1, 3]      # sub-impulse up (w3 longest, no overlap)
CD = [-2, 1, -2]            # sub-zigzag down (B retraces 50%)


class TestWaveTree(unittest.TestCase):
    def test_two_level_fractal(self):
        roots = build_tree_from_pivots(_pivots(MI + CD + MI + CD + MI))
        self.assertEqual(len(roots), 1)
        top = roots[0]
        self.assertEqual(top.pattern, "IMPULSE")
        self.assertEqual(top.degree, 2)
        self.assertEqual(len(top.children), 5)
        self.assertEqual([c.pattern for c in top.children],
                         ["IMPULSE", "ZIGZAG", "IMPULSE", "ZIGZAG", "IMPULSE"])
        # sub-structure validated -> high confidence
        self.assertGreaterEqual(top.confidence, 0.8)
        self.assertEqual(deepest_degree(roots), 2)

    def test_single_impulse_monowave_children(self):
        roots = build_tree_from_pivots(_pivots(MI))      # 6 pivots, one impulse
        self.assertEqual(len(roots), 1)
        self.assertEqual(roots[0].pattern, "IMPULSE")
        self.assertEqual(roots[0].degree, 1)
        self.assertTrue(all(c.pattern == "MONOWAVE" for c in roots[0].children))

    def test_corrective_substructure_flagged(self):
        # A 5-leg group whose "motive" sub-waves are corrections is NOT a clean
        # impulse — the top should still resolve but with reduced confidence or
        # not as a single clean impulse. Here: 5 zigzags in a row (no impulse).
        roots = build_tree_from_pivots(_pivots(CD + CD + CD + CD + CD))
        # should not produce a single high-confidence IMPULSE root
        if len(roots) == 1 and roots[0].pattern == "IMPULSE":
            self.assertLess(roots[0].confidence, 0.8)

    def test_too_short(self):
        self.assertEqual(build_tree_from_pivots([Pivot(0, 100, "L")]), [])


if __name__ == "__main__":
    unittest.main()
