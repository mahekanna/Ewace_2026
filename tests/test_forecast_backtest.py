"""
Prediction-driven, institution-style backtest (wavelib/forecast_backtest.py).

Deterministic synthetic ground-truth for the trade-management state machine
(scale-out, breakeven, structural stop, time barrier), the expectancy summary,
and an end-to-end smoke run.

Run:  python3 -m unittest tests.test_forecast_backtest -v
"""
import unittest

from wavelib import forecast_trades, forecast_returns, expectancy, ForecastTrade
from wavelib.forecast_backtest import _manage, _valid_targets


def bar(t, h, l, c):
    return (float(t), float(c), float(h), float(l), float(c), 1000.0)


class TestManageLong(unittest.TestCase):
    # entry bar at index 0; forward bars from index 1
    ENTRY, STOP, T1, T2 = 100.0, 95.0, 110.0, 120.0   # risk 5%, RR to T2 = 4:1

    def test_full_target_run_is_win(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 111, 105, 109),   # hits T1 -> book 0.5 @110, stop->BE
                bar(2, 121, 110, 120)]   # hits T2 -> book 0.5 @120
        exit_t, px, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                           self.T1, self.T2, 1, 0.5, 10, 0.0)
        self.assertEqual(outcome, "WIN")
        self.assertAlmostEqual(pct, 0.5 * 0.10 + 0.5 * 0.20)   # 0.15
        self.assertAlmostEqual(px, 120.0)

    def test_stop_before_target_is_full_loss(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 101, 94, 96)]     # low pierces stop 95 first
        exit_t, px, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                           self.T1, self.T2, 1, 0.5, 10, 0.0)
        self.assertEqual(outcome, "STOP")
        self.assertAlmostEqual(pct, -0.05)                     # -1R
        self.assertAlmostEqual(pct / (5 / 100), -1.0)

    def test_breakeven_after_partial(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 111, 105, 109),   # T1 -> book 0.5 @110, stop->100
                bar(2, 108, 99, 100)]    # low hits breakeven stop 100
        exit_t, px, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                           self.T1, self.T2, 1, 0.5, 10, 0.0)
        self.assertEqual(outcome, "PARTIAL")
        self.assertAlmostEqual(pct, 0.5 * 0.10)                # +0.5R locked, rem flat
        self.assertAlmostEqual(px, 100.0)

    def test_time_barrier_exit_at_close(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 104, 99, 103),    # no T1 (110), no stop (95)
                bar(2, 105, 100, 103)]
        exit_t, px, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                           self.T1, self.T2, 1, 0.5, 2, 0.0)
        self.assertEqual(outcome, "TIME")
        self.assertAlmostEqual(pct, 0.03)                      # exit whole at 103
        self.assertAlmostEqual(px, 103.0)

    def test_cost_is_subtracted(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 111, 105, 109),
                bar(2, 121, 110, 120)]
        _, _, pct, _ = _manage(bars, 0, self.ENTRY, self.STOP,
                               self.T1, self.T2, 1, 0.5, 10, 0.002)
        self.assertAlmostEqual(pct, 0.15 - 0.002)


class TestManageShort(unittest.TestCase):
    ENTRY, STOP, T1, T2 = 100.0, 105.0, 90.0, 80.0    # short: stop above, targets below

    def test_short_full_run_is_win(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 95, 89, 91),      # hits T1 90 -> book 0.5, stop->BE
                bar(2, 90, 79, 80)]      # hits T2 80
        _, px, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                      self.T1, self.T2, -1, 0.5, 10, 0.0)
        self.assertEqual(outcome, "WIN")
        self.assertAlmostEqual(pct, 0.5 * 0.10 + 0.5 * 0.20)
        self.assertAlmostEqual(px, 80.0)

    def test_short_stop_is_loss(self):
        bars = [bar(0, 100, 100, 100),
                bar(1, 106, 99, 104)]    # high pierces stop 105
        _, _, pct, outcome = _manage(bars, 0, self.ENTRY, self.STOP,
                                     self.T1, self.T2, -1, 0.5, 10, 0.0)
        self.assertEqual(outcome, "STOP")
        self.assertAlmostEqual(pct, -0.05)


class TestValidTargets(unittest.TestCase):
    def test_keeps_correct_side_long(self):
        t1, t2 = _valid_targets([("a", 95), ("b", 110), ("c", 120)], 100, 1)
        self.assertEqual((t1, t2), (110, 120))            # 95 dropped (below entry)

    def test_none_when_no_valid(self):
        t1, t2 = _valid_targets([("a", 95), ("b", 90)], 100, 1)
        self.assertIsNone(t1)


class TestExpectancy(unittest.TestCase):
    def _t(self, pct, r):
        return ForecastTrade(0, 100, "long", 95, 110, 120, 1, 100 + pct * 100,
                             pct, r, "WIN" if pct > 0 else "STOP", 0.3, 4.0)

    def test_summary_math(self):
        trades = [self._t(0.15, 3.0), self._t(-0.05, -1.0), self._t(0.10, 2.0)]
        s = expectancy(trades)
        self.assertEqual(s["n"], 3)
        self.assertAlmostEqual(s["win_rate"], 2 / 3)
        self.assertAlmostEqual(s["avg_r"], (3.0 - 1.0 + 2.0) / 3)
        self.assertAlmostEqual(s["profit_factor"], (0.15 + 0.10) / 0.05)

    def test_empty(self):
        s = expectancy([])
        self.assertEqual(s["n"], 0)
        self.assertEqual(s["profit_factor"], 0.0)


class TestEndToEnd(unittest.TestCase):
    def _wave(self, pts, per=8):
        bars, t = [], 0
        for a, b in zip(pts, pts[1:]):
            for k in range(1, per + 1):
                p = a + (b - a) * k / per
                h, l = p * 1.01, p * 0.99
                bars.append((float(t), float(p), float(h), float(l), float(p), 1000.0))
                t += 1
        return bars

    def test_runs_and_invariants_hold(self):
        # a multi-leg zig-zag that produces some counts/forecasts
        bars = self._wave([100, 150, 125, 190, 165, 220, 185, 240, 210, 260])
        trades = forecast_trades(bars, conf_min=0.0, min_rr=1.0, max_hold=20,
                                 window=200, min_history=40, stride=2)
        self.assertIsInstance(trades, list)
        for tr in trades:
            # r-multiple sign matches the % return sign (consistency)
            self.assertEqual(tr.pct_return > 0, tr.r_multiple > 0)
            self.assertIn(tr.outcome, {"WIN", "PARTIAL", "STOP", "TIME"})
            self.assertGreaterEqual(tr.rr_planned, 1.0)        # passed the R:R filter
        # returns helper agrees with trade list
        self.assertEqual(len(forecast_returns(bars, conf_min=0.0, min_rr=1.0,
                                              max_hold=20, window=200,
                                              min_history=40, stride=2)), len(trades))


if __name__ == "__main__":
    unittest.main()
