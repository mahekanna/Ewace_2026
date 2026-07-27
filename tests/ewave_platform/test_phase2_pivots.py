"""Phase 2 acceptance: causal pivots port, visibility, monowaves, F2 shim, quarantine."""
import os
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.data.store import Store
from ewave.monowaves.builder import build as build_monowaves
from ewave.pivots import atr_reversal, fractal, percentage_reversal, repainting
from ewave.pivots.models import pivots_to_waves, provisional_last, visible
from ewave.rules.result import Pivot, Status

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIVE = os.path.join(REPO, "data", "live")


def _avgo_1d(n=500):
    return Store(LIVE).read("AVGO", "1d").tuples()[-n:]


class TestCausalPivots(unittest.TestCase):
    def test_causal_matches_repainting_extremes(self):
        """The causal detector finds the SAME pivots as the repainting one
        (parity guarantee from the original toolkit) — it just also knows WHEN
        each became knowable."""
        bars = _avgo_1d()
        rep = repainting.zigzag(bars, pct=0.05)
        cau = percentage_reversal.zigzag_causal(bars, pct=0.05)
        self.assertEqual([(p.t, p.price, p.kind) for p in rep],
                         [(p.t, p.price, p.kind) for p in cau])

    def test_confirmed_t_is_causal_and_last_provisional(self):
        bars = _avgo_1d()
        piv = percentage_reversal.zigzag_causal(bars, pct=0.05)
        for p in piv[:-1]:
            self.assertIsNotNone(p.confirmed_t)
            # >= : a reversal can confirm on the extreme's own bar (intra-bar)
            self.assertGreaterEqual(p.confirmed_t, p.t)
        self.assertIsNone(piv[-1].confirmed_t)
        self.assertIs(provisional_last(piv), piv[-1])

    def test_visible_gate(self):
        piv = [Pivot(10, 1.0, "L", confirmed_t=15),
               Pivot(20, 2.0, "H", confirmed_t=28),
               Pivot(30, 1.5, "L", confirmed_t=None)]
        self.assertEqual(len(visible(piv, 14)), 0)
        self.assertEqual(len(visible(piv, 15)), 1)
        self.assertEqual(len(visible(piv, 100)), 2)  # provisional never visible

    def test_atr_reversal_detector(self):
        bars = _avgo_1d()
        piv = atr_reversal.detect(bars, atr_n=14, mult=3.0)
        self.assertGreater(len(piv), 3)
        for p in piv[:-1]:
            self.assertIsNotNone(p.confirmed_t)

    def test_fractal_detect_merges_highs_and_lows(self):
        bars = _avgo_1d(100)
        piv = fractal.detect(bars, 2, 2)
        self.assertTrue(any(p.kind == "H" for p in piv))
        self.assertTrue(any(p.kind == "L" for p in piv))
        ts = [p.t for p in piv]
        self.assertEqual(ts, sorted(ts))
        idx = {b[0]: i for i, b in enumerate(bars)}
        for p in piv:
            self.assertEqual(idx[p.confirmed_t] - idx[p.t], 2)  # n_right lag


class TestMonoWaves(unittest.TestCase):
    def test_build_uses_only_confirmed_and_stamps_visible_at(self):
        bars = _avgo_1d()
        piv = percentage_reversal.zigzag_causal(bars, pct=0.05)
        mws = build_monowaves(piv, bar_seconds=86400)
        # provisional last pivot excluded -> one fewer wave than confirmed pairs
        self.assertEqual(len(mws), len([p for p in piv if p.confirmed_t]) - 1)
        for m in mws:
            self.assertEqual(m.visible_at, m.end.confirmed_t)
            self.assertGreaterEqual(m.visible_at, m.end.t)
            self.assertGreater(m.time_length_bars, 0)

    def test_visibility_cutoff_filters(self):
        bars = _avgo_1d()
        piv = percentage_reversal.zigzag_causal(bars, pct=0.05)
        mid_t = bars[len(bars) // 2][0]
        early = build_monowaves(piv, now_t=mid_t, bar_seconds=86400)
        full = build_monowaves(piv, bar_seconds=86400)
        self.assertLess(len(early), len(full))
        for m in early:
            self.assertLessEqual(m.visible_at, mid_t)

    def test_retracement_and_extension_metrics(self):
        p = [Pivot(0, 100, "L", 1), Pivot(10, 110, "H", 11),
             Pivot(20, 105, "L", 21), Pivot(30, 120, "H", 31)]
        mws = build_monowaves(p, bar_seconds=1)
        self.assertEqual(mws[0].direction, "UP")
        self.assertAlmostEqual(mws[1].retracement_of_previous, 0.5)  # 5 vs 10
        self.assertIsNone(mws[1].extension_vs_previous)
        self.assertAlmostEqual(mws[2].retracement_of_previous, 3.0)  # 15 vs 5
        self.assertEqual(mws[0].structure_label, "")  # no labels by default

    def test_no_elliott_labels_assigned(self):
        bars = _avgo_1d()
        piv = percentage_reversal.zigzag_causal(bars, pct=0.05)
        for m in build_monowaves(piv, bar_seconds=86400):
            self.assertEqual(m.structure_label, "")


class TestQuarantine(unittest.TestCase):
    SIGNAL_PATH_PKGS = ("signals", "scanner", "backtest", "patterns",
                        "execution", "monowaves", "risk", "validation")

    def test_no_signal_path_module_imports_repainting(self):
        """docs/NO_LOOKAHEAD_POLICY.md §2: the non-causal zigzag is plotting-only."""
        src = os.path.join(REPO, "src", "ewave")
        offenders = []
        for pkg in self.SIGNAL_PATH_PKGS:
            for root, _dirs, files in os.walk(os.path.join(src, pkg)):
                for fn in files:
                    if not fn.endswith(".py"):
                        continue
                    path = os.path.join(root, fn)
                    text = open(path).read()
                    if "repainting" in text:
                        offenders.append(os.path.relpath(path, src))
        self.assertEqual(offenders, [])


class TestF2ShimAndDedup(unittest.TestCase):
    def test_shim_names_are_the_ewave_objects(self):
        import wavelib
        import wavelib.toolkit as tk
        self.assertIs(tk.zigzag_causal, percentage_reversal.zigzag_causal)
        self.assertIs(tk.swing_pivots, fractal.swing_pivots)
        self.assertIs(tk.zigzag, repainting.zigzag)
        self.assertIs(tk.Pivot, Pivot)
        self.assertIs(wavelib.Pivot, Pivot)
        from ewave.rules.fib import fib_cluster
        self.assertIs(tk.fib_cluster, fib_cluster)

    def test_legacy_duplicates_not_in_ewave(self):
        """F2: the divergent-API NeoWave duplicates live ONLY in the shim."""
        import ewave.rules.fib as fib
        import ewave.pivots.percentage_reversal as pr
        for mod in (fib, pr):
            self.assertFalse(hasattr(mod, "SBResult"))
            self.assertFalse(hasattr(mod, "terminal_retrace_projection"))
        import wavelib.toolkit as tk
        self.assertTrue(hasattr(tk, "SBResult"))  # legacy callers still fine

    def test_status_gained_unknown(self):
        self.assertEqual(Status.UNKNOWN.value, "UNKNOWN")
        import wavelib
        self.assertIs(wavelib.Status.UNKNOWN, Status.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
