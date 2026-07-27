"""Phase 6 acceptance: WAVE3_RESULT anchors, causal invariants, fills, metrics, trials."""
import json
import os
import statistics
import tempfile
import unittest

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.backtest.engine import Wave3Trade, backtest_wave3
from ewave.backtest.fills import FillModel
from ewave.backtest.metrics import equity_curve, summarize
from ewave.rules.profiles import get_profile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(REPO, "configs")


def _bars(sym):
    with open(os.path.join(REPO, "data", "live", f"{sym}_15m_2026-06.json")) as f:
        return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
                for b in json.load(f)["bars"]]


class TestAnchors(unittest.TestCase):
    """The engine must reproduce the documented year-long forward-test numbers
    (docs/WAVE3_RESULT.md) trade-for-trade — the regression anchor for the
    entire port."""

    def test_avgo_crude_anchor(self):
        trades = backtest_wave3(_bars("avgo"), get_profile("experimental", CFG))
        self.assertEqual(len(trades), 79)
        self.assertAlmostEqual(statistics.mean(t.r for t in trades), 0.167, places=2)

    def test_mrvl_crude_anchor(self):
        trades = backtest_wave3(_bars("mrvl"), get_profile("experimental", CFG))
        self.assertEqual(len(trades), 119)
        self.assertAlmostEqual(statistics.mean(t.r for t in trades), 0.314, places=2)

    def test_strict_fires_rarely_with_higher_quality(self):
        """docs/RULESET.md §H result: strict = few trades, higher per-trade R."""
        trades = backtest_wave3(_bars("avgo"), get_profile("sow_neowave_strict", CFG))
        self.assertLess(len(trades), 15)
        if trades:  # 3 in the documented run
            self.assertGreater(statistics.mean(t.r for t in trades), 0.3)


class TestCausalInvariants(unittest.TestCase):
    def test_entry_never_before_signal(self):
        trades = backtest_wave3(_bars("avgo")[:4000], get_profile("experimental", CFG))
        for t in trades:
            self.assertGreaterEqual(t.entry_time, t.signal_time)

    def test_one_position_at_a_time(self):
        bars = _bars("avgo")
        trades = backtest_wave3(bars, get_profile("experimental", CFG))
        step = {b[0]: i for i, b in enumerate(bars)}
        for a, b in zip(trades, trades[1:]):
            # next signal can only fire after the previous trade released the cursor
            self.assertGreater(step[b.signal_time],
                               step[a.signal_time] + a.bars_held)

    def test_signal_fires_on_cursor_candle(self):
        """The engine asserts sig.entry_t == cursor bar; make one pass to prove
        the assertion path executes on real data without tripping."""
        trades = backtest_wave3(_bars("mrvl")[:3000], get_profile("experimental", CFG))
        self.assertIsInstance(trades, list)


class TestFills(unittest.TestCase):
    def test_cost_reduces_r(self):
        bars = _bars("avgo")[:6000]
        prof = get_profile("experimental", CFG)
        free = backtest_wave3(bars, prof)
        paid = backtest_wave3(bars, prof, fill_model=FillModel(slippage_bps=5))
        self.assertEqual(len(free), len(paid))
        for f, p in zip(free, paid):
            self.assertLess(p.r, f.r)

    def test_cost_r_arithmetic(self):
        fm = FillModel(slippage_bps=10)     # 10 bps/side => 0.2% round trip
        # entry 100, stop 98 -> risk 2; slippage cost 0.2 -> 0.1 R
        self.assertAlmostEqual(fm.cost_r(100.0, 98.0), 0.1, places=6)

    def test_from_config_reads_execution_json(self):
        fm = FillModel.from_config(CFG)
        self.assertEqual(fm.slippage_bps, 2.0)
        self.assertEqual(fm.commission_per_share, 0.005)


class TestMetricsAndTrials(unittest.TestCase):
    def _trades(self):
        return [Wave3Trade(1, 1, "long", 100, 98, 106, 3.0, r, "TARGET", 10)
                for r in (1.0, -1.0, 2.0, 0.5, -1.0)]

    def test_summary_math(self):
        with tempfile.TemporaryDirectory() as d:
            reg = os.path.join(d, "trials.jsonl")
            m = summarize(self._trades(), symbol="X", timeframe="15m",
                          profile="experimental", registry_path=reg)
            self.assertEqual(m["trades"], 5)
            self.assertAlmostEqual(m["expectancy_r"], 0.3)
            self.assertAlmostEqual(m["win_rate"], 0.6)
            self.assertAlmostEqual(m["profit_factor"], 3.5 / 2.0)
            self.assertEqual(m["max_drawdown_r"], 1.0)   # +1 -> 0 dip of 1R
            self.assertEqual(m["n_trials"], 1)           # the run logged itself

    def test_every_run_logs_a_trial(self):
        with tempfile.TemporaryDirectory() as d:
            reg = os.path.join(d, "trials.jsonl")
            summarize(self._trades(), profile="a", registry_path=reg)
            summarize(self._trades(), profile="b", registry_path=reg)
            with open(reg) as f:
                self.assertEqual(len(f.readlines()), 2)

    def test_equity_curve_monotone_time(self):
        ec = equity_curve(self._trades())
        self.assertEqual(len(ec), 5)
        self.assertAlmostEqual(ec[-1][1], 1.5)


class TestShims(unittest.TestCase):
    def test_backtest_shims_identity(self):
        import wavelib.backtest as WB
        import wavelib.forecast_backtest as WFB
        import wavelib.validation as WV
        from ewave.backtest import engine_forecast, replay
        from ewave.validation import stats
        self.assertIs(WB.backtest_reversals, replay.backtest_reversals)
        self.assertIs(WFB.forecast_trades, engine_forecast.forecast_trades)
        self.assertIs(WV.deflated_sharpe_ratio, stats.deflated_sharpe_ratio)


if __name__ == "__main__":
    unittest.main()
