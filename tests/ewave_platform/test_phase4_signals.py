"""Phase 4 acceptance: Signal model, profile-driven generate(), store freeze, scan."""
import json
import os
import tempfile
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.rules.profiles import get_profile
from ewave.signals import wave3
from ewave.signals.models import Signal, SignalStatus, from_wave3
from ewave.signals.store import SignalStore

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(REPO, "configs")


def _bars(symbol="avgo", tf="15m", n=None):
    with open(os.path.join(REPO, "data", "live", f"{symbol}_{tf}_2026-06.json")) as f:
        d = json.load(f)
    bt = [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
          for b in d["bars"]]
    return bt if n is None else bt[-n:]


class TestSignalModel(unittest.TestCase):
    def _sig(self, **kw):
        base = dict(symbol="AVGO", timeframe="15m", signal_time=1_750_000_000,
                    pattern_type="wave3_impulse", direction="long",
                    entry_trigger="break_close_beyond_w1_extreme",
                    entry_price=100.0, stop_price=95.0,
                    targets=[("1.618x W1", 110.0), ("2.618x W1", 120.0)],
                    invalidation_level=95.0, source_profile="experimental")
        base.update(kw)
        return Signal(**base)

    def test_id_stable_and_content_addressed(self):
        a, b = self._sig(), self._sig()
        self.assertEqual(a.signal_id, b.signal_id)
        c = self._sig(signal_time=1_750_000_900)
        self.assertNotEqual(a.signal_id, c.signal_id)

    def test_defaults_and_roundtrip(self):
        s = self._sig()
        self.assertEqual(s.status, SignalStatus.CONFIRMED)
        self.assertEqual(s.visible_bars_until, s.signal_time)
        self.assertIsNone(s.position_size)   # risk engine's job, not the signal's
        self.assertEqual(s.target_1, 110.0)
        s2 = Signal.from_dict(s.to_dict())
        self.assertEqual(s2, s)


class TestGenerateEquivalence(unittest.TestCase):
    """The profile presets must reproduce the original validated functions
    exactly — signal-for-signal over a real-data replay slice."""

    def _replay(self, fn, bars, roll=400, stride=7):
        hits = []
        for t in range(roll, len(bars), stride):
            sig = fn(bars[t - roll:t + 1])
            if sig:
                hits.append(sig)
        return hits

    def test_experimental_equals_crude_wave3(self):
        bars = _bars(n=2600)
        prof = get_profile("experimental", CFG)
        a = self._replay(lambda w: wave3.wave3_signal(w), bars)
        b = self._replay(lambda w: (wave3.generate(w, prof, "AVGO", "15m") or [None])[0], bars)
        self.assertEqual([(s.entry_t, s.direction, s.entry, s.stop) for s in a],
                         [(s.signal_time, s.direction, s.entry_price, s.stop_price)
                          for s in b])
        self.assertGreater(len(a), 0, "replay slice produced no signals — widen it")

    def test_strict_preset_equals_strict_function(self):
        bars = _bars()
        prof = get_profile("sow_neowave_strict", CFG)
        a = self._replay(lambda w: wave3.wave3_signal_strict(w), bars, stride=13)
        b = self._replay(lambda w: (wave3.generate(w, prof, "AVGO", "15m") or [None])[0],
                         bars, stride=13)
        self.assertEqual([(s.entry_t, s.entry, s.stop) for s in a],
                         [(s.signal_time, s.entry_price, s.stop_price) for s in b])

    def test_strict_defaults_unchanged_by_parameterization(self):
        """The added knobs must not change the historical strict behaviour."""
        bars = _bars(n=3000)
        for t in range(500, len(bars), 11):
            w = bars[t - 400:t + 1]
            self.assertEqual(
                wave3.wave3_signal_strict(w),
                wave3.wave3_signal_strict(w, require_pattern_id=True,
                                          entry_window_w2_mult=2, min_w1_frac=0.01))


class TestForecastIsRefOnly(unittest.TestCase):
    def test_no_signal_module_imports_forecast_direction(self):
        """D6: forecast_from_count's direction must not gate signals — only
        trade_plan machinery is load-bearing. wave3 must not import it."""
        src = os.path.join(REPO, "src", "ewave", "signals", "wave3.py")
        self.assertNotIn("forecast_from_count", open(src).read())
        scan_src = os.path.join(REPO, "src", "ewave", "scanner", "batch.py")
        self.assertNotIn("forecast_from_count", open(scan_src).read())

    def test_trade_plan_module_carries_ref_banner(self):
        src = open(os.path.join(REPO, "src", "ewave", "signals", "trade_plan.py")).read()
        self.assertIn("REF/reference-only", src)


class TestStoreFreeze(unittest.TestCase):
    def test_append_before_latest_and_roundtrip(self):
        s = Signal(symbol="AVGO", timeframe="15m", signal_time=1_750_000_000,
                   pattern_type="wave3_impulse", direction="long",
                   entry_trigger="break", entry_price=100.0, stop_price=95.0,
                   targets=[("T1", 110.0)], invalidation_level=95.0,
                   source_profile="experimental")
        with tempfile.TemporaryDirectory() as d:
            store = SignalStore(d)
            p = store.append([s], day="2026-07-09")
            self.assertTrue(p.exists())
            loaded = store.load("2026-07-09")
            self.assertEqual(loaded, [s])
            store.append([s], day="2026-07-09")     # append-only: grows, no rewrite
            self.assertEqual(len(store.load("2026-07-09")), 2)
            store.write_latest([s])
            self.assertTrue((store.dir / "latest_signals.json").exists())
            self.assertTrue((store.dir / "latest_signals.csv").exists())


class TestScan(unittest.TestCase):
    def test_scan_runs_and_freezes(self):
        from ewave.scanner.batch import scan
        with tempfile.TemporaryDirectory() as d:
            result = scan(["AVGO", "MRVL"], "15m", "experimental",
                          signal_store=SignalStore(d))
            self.assertEqual(result["symbols_scanned"], 2)
            self.assertEqual(result["errors"], [])
            # signals may be 0 on the last cached bar — the artifacts must exist anyway
            self.assertTrue(os.path.exists(os.path.join(d, "latest_signals.json")))

    def test_scan_unknown_symbol_reports_error(self):
        from ewave.scanner.batch import scan
        with tempfile.TemporaryDirectory() as d:
            result = scan(["ZZZZ"], "15m", "experimental",
                          signal_store=SignalStore(d))
            self.assertEqual(len(result["errors"]), 1)


class TestShims(unittest.TestCase):
    def test_wave3_and_forecast_shims_identity(self):
        import wavelib.wave3 as W3
        import wavelib.forecast as F
        from ewave.signals import trade_plan, wave3 as EW3
        self.assertIs(W3.wave3_signal, EW3.wave3_signal)
        self.assertIs(W3.wave3_signal_strict, EW3.wave3_signal_strict)
        self.assertIs(F.trade_plan, trade_plan.trade_plan)
        self.assertIs(F.forecast_from_count, trade_plan.forecast_from_count)
        import wavelib
        self.assertIs(wavelib.CycleSignal.__module__ and wavelib.CycleSignal,
                      __import__("ewave.signals.cycle_seam", fromlist=["CycleSignal"]).CycleSignal)


if __name__ == "__main__":
    unittest.main()
