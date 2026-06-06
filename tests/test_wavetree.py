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


class TestStage2Triangles(unittest.TestCase):
    """Stage 2: triangles need real converging/diverging lines AND corrective
    legs — they must NOT form from raw monowaves."""

    def test_geometry_gate(self):
        from wavelib.wavetree import _triangle_geometry, WaveNode

        def grp(prices):
            return [WaveNode(Pivot(i, prices[i], "L"), Pivot(i + 1, prices[i + 1], "H"),
                             0, "leg", "MONOWAVE") for i in range(5)]
        self.assertEqual(_triangle_geometry(grp([100, 120, 105, 116, 108, 113])), "CONTRACTING")
        self.assertEqual(_triangle_geometry(grp([100, 120, 98, 128, 90, 135])), "EXPANDING")
        self.assertIsNone(_triangle_geometry(grp([100, 110, 120, 130, 140, 150])))

    def test_no_triangle_from_monowaves(self):
        # a contracting-looking 5-monowave set must NOT be labelled a TRIANGLE
        roots = build_tree_from_pivots(_pivots([10, -7, 5, -3, 1]))
        patterns = []

        def walk(n):
            patterns.append(n.pattern)
            for c in n.children:
                walk(c)
        for r in roots:
            walk(r)
        self.assertNotIn("TRIANGLE", patterns)


class TestStage3Confidence(unittest.TestCase):
    """Stage 3: honest confidence + shallow-flat penalty + fragmentation scoring."""

    @staticmethod
    def _mono(t0, p0, t1, p1):
        from wavelib.wavetree import WaveNode
        return WaveNode(Pivot(t0, p0, "L" if p1 > p0 else "H"),
                        Pivot(t1, p1, "H" if p1 > p0 else "L"), 0, "leg", "MONOWAVE")

    def test_shallow_flat_scores_below_zigzag(self):
        from wavelib.wavetree import _correction_node
        zz = [self._mono(0, 100, 1, 120), self._mono(1, 120, 2, 112), self._mono(2, 112, 3, 130)]
        fl = [self._mono(0, 100, 1, 120), self._mono(1, 120, 2, 105), self._mono(2, 105, 3, 125)]
        z, f = _correction_node(zz, 1), _correction_node(fl, 1)
        self.assertIsNotNone(z)
        self.assertIsNotNone(f)
        self.assertGreater(z.confidence, f.confidence)

    def test_fragmentation_lowers_confidence(self):
        from wavelib.wavetree import WaveNode, tree_confidence
        big = WaveNode(Pivot(0, 100, "L"), Pivot(100 * DAY, 200, "H"), 2, "motive",
                       "IMPULSE", confidence=0.9)
        small = WaveNode(Pivot(100 * DAY, 200, "H"), Pivot(108 * DAY, 190, "L"), 1,
                         "corrective", "ZIGZAG", confidence=0.9)
        self.assertAlmostEqual(tree_confidence([big]), 0.9)        # one dominant root
        self.assertLess(tree_confidence([big, small]), 0.9)        # fragmented -> honest drop

    def test_best_count_returns_dominant(self):
        roots = build_tree_from_pivots(_pivots(MI + CD + MI + CD + MI))
        # the clean fractal: single root covering everything
        from wavelib.wavetree import tree_confidence
        self.assertEqual(len(roots), 1)
        self.assertGreaterEqual(tree_confidence(roots), 0.8)


if __name__ == "__main__":
    unittest.main()
