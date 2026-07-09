"""Phase 5 acceptance: snapshot freeze, no-lookahead walk, metrics, forecasters."""
import json
import os
import tempfile
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.rules.profiles import get_profile
from ewave.validation.ghost_forward import stability
from ewave.validation.ghost_forward.core import Forecast
from ewave.validation.ghost_forward.forecasters import wave3_forecaster

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(REPO, "configs")


def _flat_bars(n=60, price=100.0):
    return [(1000 + i * 60, price, price + 1, price - 1, price, 10) for i in range(n)]


class TestSnapshotFreeze(unittest.TestCase):
    def test_outcome_pass_refuses_unfrozen(self):
        bars = _flat_bars()
        snaps = stability.snapshot_pass(bars, lambda w: None, roll=10, horizon=5)
        with self.assertRaises(RuntimeError):
            stability.outcome_pass(bars, snaps, roll=10, horizon=5)  # frozen omitted

    def test_run_persists_snapshots_outcomes_metrics(self):
        bars = _flat_bars(100)
        with tempfile.TemporaryDirectory() as d:
            m = stability.run(bars, lambda w: None, roll=10, horizon=5, out_dir=d)
            for name in ("snapshots.jsonl", "outcomes.jsonl", "metrics.json"):
                self.assertTrue(os.path.exists(os.path.join(d, name)), name)
            self.assertEqual(m["forecasts"], 0)
            self.assertEqual(m["steps"], 85)


class TestNoLookaheadWalk(unittest.TestCase):
    def test_forecaster_never_sees_future(self):
        """The monkeypatch proof (NO_LOOKAHEAD_POLICY §4): the last bar of every
        window handed to the forecaster equals the cursor bar exactly."""
        bars = _flat_bars(80)
        seen = []

        def spy(window):
            seen.append(window[-1][0])
            return None
        stability.snapshot_pass(bars, spy, roll=10, horizon=5)
        expected = [b[0] for b in bars[10:len(bars) - 5]]
        self.assertEqual(seen, expected)

    def test_window_never_longer_than_roll(self):
        bars = _flat_bars(80)
        lens = []
        stability.snapshot_pass(bars, lambda w: lens.append(len(w)), roll=12, horizon=5)
        self.assertLessEqual(max(lens), 12)


class TestOutcomeAndMetrics(unittest.TestCase):
    def test_hit_and_mfe_mae(self):
        # price sits at 100; forecast up to 106, invalidation 97; future rises to 107
        bars = _flat_bars(30)
        for i in range(20, 30):
            t, o, h, l, c, v = bars[i]
            bars[i] = (t, 106.0, 107.0, 99.0, 106.5, v)

        def fc(window):
            if window[-1][0] == bars[19][0]:      # fire once at step of bar 19
                return Forecast("up", target=106.0, invalidation=97.0)
            return None
        snaps = stability.snapshot_pass(bars, fc, roll=10, horizon=8)
        outs = stability.outcome_pass(bars, snaps, roll=10, horizon=8, frozen=True)
        fired = [r for s, r in zip(snaps, outs) if s.has_forecast]
        self.assertEqual(len(fired), 1)
        self.assertEqual(fired[0]["outcome"], "HIT")
        # risk = 100-97 = 3; future max high 107 -> MFE = 7/3; min low 99 -> MAE = 1/3
        self.assertAlmostEqual(fired[0]["mfe_r"], 7 / 3, places=2)
        self.assertAlmostEqual(fired[0]["mae_r"], 1 / 3, places=2)
        m = stability.metrics(snaps, outs)
        self.assertEqual(m["target_hit_rate"], 1.0)

    def test_invalidation_first_wins(self):
        bars = _flat_bars(30)
        for i in range(20, 30):
            t, o, h, l, c, v = bars[i]
            bars[i] = (t, 96.0, 107.0, 96.0, 96.5, v)   # low breaches 97 same bar

        def fc(window):
            return Forecast("up", 106.0, 97.0) if window[-1][0] == bars[19][0] else None
        snaps = stability.snapshot_pass(bars, fc, roll=10, horizon=8)
        outs = stability.outcome_pass(bars, snaps, roll=10, horizon=8, frozen=True)
        fired = [r for s, r in zip(snaps, outs) if s.has_forecast]
        self.assertEqual(fired[0]["outcome"], "INVALIDATED")

    def test_episode_stability_and_repaint(self):
        bars = _flat_bars(40)
        # standing call for steps 0-4, vanishes for 5+, reappears revised at 10
        def fc(window):
            t = window[-1][0]
            step = (t - 1000) // 60 - 10
            if 0 <= step <= 4:
                return Forecast("up", 106.0, 97.0, kind="standing")
            if step == 10:
                return Forecast("up", 120.0, 97.0, kind="standing")
            return None
        snaps = stability.snapshot_pass(bars, fc, roll=10, horizon=5)
        eps = stability._episodes(snaps)
        self.assertEqual(len(eps), 2)
        self.assertEqual(eps[0]["length"], 5)
        self.assertEqual(eps[0]["ended_by"], "vanished")
        m = stability.metrics(snaps, stability.outcome_pass(
            bars, snaps, roll=10, horizon=5, frozen=True))
        self.assertEqual(m["repaint_rate"], 1.0)  # both ended episodes vanished


class TestWave3Forecaster(unittest.TestCase):
    def test_real_data_regression_band(self):
        """Crude profile over a real AVGO 15m slice: the fire rate and hit-rate
        must stay in the empirically mapped band (docs/WAVE3_RESULT.md — exact
        trade-level numbers are the Phase 6 backtest anchor; here we check the
        signal-level shape survived the port)."""
        with open(os.path.join(REPO, "data", "live", "avgo_15m_2026-06.json")) as f:
            bars = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
                    for b in json.load(f)["bars"]]
        fc = wave3_forecaster(get_profile("experimental", CFG))
        snaps = stability.snapshot_pass(bars, fc, roll=400, forward=4000, horizon=96)
        outs = stability.outcome_pass(bars, snaps, roll=400, forward=4000,
                                      horizon=96, frozen=True)
        m = stability.metrics(snaps, outs)
        self.assertGreater(m["forecasts"], 20)
        self.assertLess(m["forecasts"], 150)
        self.assertIsNotNone(m["target_hit_rate"])
        self.assertGreater(m["target_hit_rate"], 0.15)
        self.assertLess(m["target_hit_rate"], 0.65)

    def test_forecast_mapping(self):
        prof = get_profile("experimental", CFG)
        fc = wave3_forecaster(prof)
        self.assertIsNone(fc(_flat_bars(60)))    # flat series: no setup


class TestKitShim(unittest.TestCase):
    def test_gf_shim_is_core(self):
        import sys
        sys.path.insert(0, os.path.join(REPO, "ghost_forward_kit"))
        try:
            import gf
            from ewave.validation.ghost_forward import core
            self.assertIs(gf.Forecast, core.Forecast)
            self.assertIs(gf.iter_steps, core.iter_steps)
        finally:
            sys.path.pop(0)


if __name__ == "__main__":
    unittest.main()
