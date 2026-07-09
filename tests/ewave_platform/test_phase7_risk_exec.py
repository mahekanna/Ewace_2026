"""Phase 7 acceptance: risk controls, paper fills, kill switch, live fail-closed."""
import os
import tempfile
import unittest
from unittest import mock

import tests.ewave_platform  # noqa: F401 — src/ path bootstrap

from ewave.backtest.fills import FillModel
from ewave.execution.broker import Order, OrderState, OrderType
from ewave.execution.guard import LiveTradingDisabled, evaluate_gates
from ewave.execution.live import LiveExecutor
from ewave.execution.paper import PaperBroker
from ewave.risk.engine import PortfolioState, RiskEngine
from ewave.signals.models import Signal

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(REPO, "configs")

RISK_CFG = {
    "account_equity": 100000.0, "max_risk_per_trade_pct": 1.0,
    "reduced_risk_pct_below_3_strands": 0.5, "max_daily_loss_pct": 3.0,
    "max_weekly_loss_pct": 6.0, "max_open_positions": 3,
    "max_symbol_exposure_pct": 20.0, "max_portfolio_exposure_pct": 60.0,
    "cooldown_bars_after_loss": 12, "kill_switch_file": "/nonexistent/KILL",
    "live_enabled": False,
}


def _signal(strands=3, entry=100.0, stop=90.0):
    return Signal(symbol="AVGO", timeframe="15m", signal_time=1_750_000_000,
                  pattern_type="wave3_impulse", direction="long",
                  entry_trigger="break", entry_price=entry, stop_price=stop,
                  targets=[("T1", entry + 2 * (entry - stop))],
                  invalidation_level=stop, source_profile="test",
                  confluence_strands=strands)


def _state(**kw):
    base = dict(equity=100000.0)
    base.update(kw)
    return PortfolioState(**base)


class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.risk = RiskEngine(cfg=dict(RISK_CFG))

    def test_approves_and_sizes(self):
        v = self.risk.approve(_signal(strands=3), _state())
        self.assertTrue(v)
        self.assertEqual(v.qty, 100)              # 1% of 100k / $10 risk
        self.assertEqual(v.risk_amount, 1000.0)

    def test_reduced_risk_below_3_strands(self):
        v = self.risk.approve(_signal(strands=0), _state())
        self.assertEqual(v.qty, 50)               # 0.5% instead of 1%

    def test_each_control_blocks(self):
        cases = [
            (_state(day_pnl=-3001.0), "daily loss"),
            (_state(week_pnl=-6001.0), "weekly loss"),
            (_state(open_positions=3), "max open positions"),
            (_state(bars_since_loss=5), "cooldown"),
            (_state(symbol_exposure={"AVGO": 15000.0}), "symbol exposure"),
            (_state(portfolio_exposure=55000.0), "portfolio exposure"),
        ]
        for state, needle in cases:
            v = self.risk.approve(_signal(), state)
            self.assertFalse(v, needle)
            self.assertIn(needle.split()[0], v.reason.lower())

    def test_degenerate_stop_rejected(self):
        v = self.risk.approve(_signal(entry=100.0, stop=100.0), _state())
        self.assertFalse(v)

    def test_kill_switch_blocks_everything(self):
        with tempfile.NamedTemporaryFile() as f:
            risk = RiskEngine(cfg=dict(RISK_CFG, kill_switch_file=f.name))
            v = risk.approve(_signal(), _state())
            self.assertFalse(v)
            self.assertIn("kill switch", v.reason)


class TestPaperBroker(unittest.TestCase):
    def _bar(self, t, o, h, l, c):
        return (t, o, h, l, c, 0)

    def test_market_fills_next_bar_open_with_slippage(self):
        b = PaperBroker(FillModel(slippage_bps=10))
        o = b.submit(Order("O1", "AVGO", "buy", 100, OrderType.MARKET,
                           attach_stop=95.0, attach_target=110.0))
        self.assertEqual(o.state, OrderState.ACCEPTED)
        b.on_bar("AVGO", self._bar(2, 100.0, 101, 99, 100.5))
        self.assertEqual(o.state, OrderState.FILLED)
        self.assertAlmostEqual(o.fill_price, 100.1)   # open + 10bps, never the close
        pos = b.positions()["AVGO"]
        self.assertEqual((pos.stop, pos.target), (95.0, 110.0))

    def test_stop_exit_conservative_and_gap_through(self):
        b = PaperBroker(FillModel())
        b.submit(Order("O1", "AVGO", "buy", 100, OrderType.MARKET,
                       attach_stop=95.0, attach_target=110.0))
        b.on_bar("AVGO", self._bar(2, 100, 101, 99, 100))
        # bar touches BOTH stop and target -> stop wins (conservative)
        ev = b.on_bar("AVGO", self._bar(3, 100, 111, 94, 105))
        self.assertEqual(ev[0]["exit_kind"], "stop")
        self.assertNotIn("AVGO", b.positions())
        # gap-through: open below the stop fills at the open, not the stop
        b.submit(Order("O2", "AVGO", "buy", 100, OrderType.MARKET,
                       attach_stop=95.0))
        b.on_bar("AVGO", self._bar(4, 100, 101, 99, 100))
        ev = b.on_bar("AVGO", self._bar(5, 90.0, 92, 89, 91))
        self.assertAlmostEqual(abs(ev[0]["pnl"]) > 100 * (100 - 95) * 0.99, True)

    def test_target_exit_and_pnl_sign(self):
        b = PaperBroker(FillModel())
        b.submit(Order("O1", "AVGO", "buy", 10, OrderType.MARKET,
                       attach_stop=95.0, attach_target=104.0))
        b.on_bar("AVGO", self._bar(2, 100, 101, 99, 100))
        ev = b.on_bar("AVGO", self._bar(3, 100, 105, 99.9, 104.5))
        self.assertEqual(ev[0]["exit_kind"], "target")
        self.assertAlmostEqual(ev[0]["pnl"], 10 * 4.0, delta=0.5)

    def test_order_minimum_commission_applies_at_order_level(self):
        b = PaperBroker(FillModel(commission_per_share=0.005, commission_minimum=1.0))
        b.submit(Order("O1", "AVGO", "buy", 10, OrderType.MARKET,
                       attach_stop=95.0, attach_target=104.0))
        b.on_bar("AVGO", self._bar(2, 100, 101, 99, 100))
        ev = b.on_bar("AVGO", self._bar(3, 100, 105, 99.9, 104.5))
        # pnl = 40 - round-trip max(0.05, 1.0)*2 = 40 - 2
        self.assertAlmostEqual(ev[0]["pnl"], 38.0, delta=0.01)

    def test_ledgers_append(self):
        with tempfile.TemporaryDirectory() as d:
            b = PaperBroker(FillModel(), ledger_dir=d)
            b.submit(Order("O1", "AVGO", "buy", 10, OrderType.MARKET,
                           attach_stop=95.0))
            b.on_bar("AVGO", self._bar(2, 100, 101, 99, 100))
            self.assertTrue(os.path.exists(os.path.join(d, "orders.jsonl")))
            self.assertTrue(os.path.exists(os.path.join(d, "fills.jsonl")))
            self.assertTrue(os.path.exists(os.path.join(d, "positions.jsonl")))


class TestReplayPaperLoop(unittest.TestCase):
    def _bars(self, sym="avgo", n=3000):
        import json
        with open(os.path.join(REPO, "data", "live", f"{sym}_15m_2026-06.json")) as f:
            return [(b["t"], b["o"], b["h"], b["l"], b["c"], b.get("v", 0) or 0)
                    for b in json.load(f)["bars"]][:n]

    def test_replay_places_orders_only_via_risk(self):
        from ewave.execution.paper import replay_paper
        from ewave.rules.profiles import get_profile
        risk = RiskEngine(cfg=dict(RISK_CFG))
        broker = PaperBroker(FillModel())
        summary = replay_paper({"AVGO": self._bars()}, get_profile("experimental", CFG),
                               risk, broker)
        self.assertGreater(summary["signals_seen"], 0)
        self.assertEqual(summary["orders_placed"] + summary["rejected_by_risk"],
                         summary["signals_seen"])
        self.assertFalse(summary["halted_by_kill_switch"])

    def test_kill_switch_halts_and_flattens_mid_run(self):
        from ewave.execution.paper import replay_paper
        from ewave.rules.profiles import get_profile
        with tempfile.NamedTemporaryFile(delete=False) as f:
            kill = f.name  # exists from the start -> halts on first bar
        try:
            risk = RiskEngine(cfg=dict(RISK_CFG, kill_switch_file=kill))
            broker = PaperBroker(FillModel())
            summary = replay_paper({"AVGO": self._bars(n=1200)},
                                   get_profile("experimental", CFG), risk, broker)
            self.assertTrue(summary["halted_by_kill_switch"])
            self.assertEqual(summary["open_positions"], 0)
            self.assertEqual(summary["orders_placed"], 0)
        finally:
            os.unlink(kill)


class TestLiveFailsClosed(unittest.TestCase):
    GREEN_ENV = {"EWAVE_ENABLE_LIVE": "true"}

    def _green_configs(self, d):
        import json
        with open(os.path.join(d, "execution.json"), "w") as f:
            json.dump({"mode": "live"}, f)
        with open(os.path.join(d, "risk.json"), "w") as f:
            json.dump(dict(RISK_CFG, live_enabled=True,
                           kill_switch_file=os.path.join(d, "KILL")), f)

    def test_default_repo_state_fails_multiple_gates(self):
        failures = evaluate_gates(base_dir=CFG, env={})
        self.assertGreaterEqual(len(failures), 3)
        with self.assertRaises(LiveTradingDisabled):
            LiveExecutor(base_dir=CFG, env={}).start()

    def test_each_missing_gate_fails_alone(self):
        with tempfile.TemporaryDirectory() as d:
            self._green_configs(d)
            report = os.path.join(d, "paper_report.md")
            open(report, "w").write("# report\n")
            glob_pat = os.path.join(d, "*report*.md")
            # all green except the env flag
            f = evaluate_gates(base_dir=d, paper_report_glob=glob_pat, env={})
            self.assertEqual(len(f), 1)
            self.assertIn("EWAVE_ENABLE_LIVE", f[0])
            # all green except the paper report
            os.unlink(report)
            f = evaluate_gates(base_dir=d, paper_report_glob=glob_pat,
                               env=self.GREEN_ENV)
            self.assertEqual(len(f), 1)
            self.assertIn("paper-trading report", f[0])
            open(report, "w").write("# report\n")
            # all green except kill switch present
            open(os.path.join(d, "KILL"), "w").write("")
            f = evaluate_gates(base_dir=d, paper_report_glob=glob_pat,
                               env=self.GREEN_ENV)
            self.assertEqual(len(f), 1)
            self.assertIn("kill switch", f[0])

    def test_all_gates_green_still_refuses_to_trade(self):
        with tempfile.TemporaryDirectory() as d:
            self._green_configs(d)
            open(os.path.join(d, "paper_report.md"), "w").write("# report\n")
            with mock.patch("ewave.execution.live.evaluate_gates", return_value=[]):
                with self.assertRaises(NotImplementedError):
                    LiveExecutor(base_dir=d, env=self.GREEN_ENV).start()


if __name__ == "__main__":
    unittest.main()
