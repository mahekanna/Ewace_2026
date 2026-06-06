"""
Stage 7 — realistic backtest exits (triple-barrier) + buy-and-hold benchmark.

Run:  python3 -m unittest tests.test_backtest_tb -v
"""
import unittest

from wavelib import horizon_returns
from wavelib.backtest import _resolve_tb, ReversalEvent


def _bars(closes, t0=0):
    return [(float(t0 + i), c, c + 0.01, c - 0.01, c, 1000) for i, c in enumerate(closes)]


class TestTripleBarrier(unittest.TestCase):
    EV = ReversalEvent(entry_t=-1.0, score=4, zone=(99, 101), invalidation=90, entry_price=100.0)

    def _bars_hl(self, hl):  # hl = list of (high, low) after entry
        return [(float(i), 100, h, l, (h + l) / 2, 1000) for i, (h, l) in enumerate(hl)]

    def test_take_profit_first(self):
        bars = self._bars_hl([(102, 99), (106, 101)])      # 2nd bar high 106 >= 105 target
        out = _resolve_tb(self.EV, bars, pt=0.05, sl=0.05, max_hold=10, bullish=True)
        self.assertEqual(out.outcome, "REVERSAL")
        self.assertAlmostEqual(out.move_pct, 0.05)

    def test_stop_loss_first(self):
        bars = self._bars_hl([(101, 94)])                  # low 94 <= 95 stop
        out = _resolve_tb(self.EV, bars, pt=0.05, sl=0.05, max_hold=10, bullish=True)
        self.assertEqual(out.outcome, "INVALIDATED")
        self.assertAlmostEqual(out.move_pct, -0.05)

    def test_vertical_barrier_exit(self):
        bars = self._bars_hl([(101, 99), (102, 100), (103, 101)])   # never hits +5%/-5%
        out = _resolve_tb(self.EV, bars, pt=0.05, sl=0.05, max_hold=2, bullish=True)
        self.assertIn(out.outcome, ("REVERSAL", "INVALIDATED"))     # exit at 2nd close
        self.assertLess(abs(out.move_pct), 0.05)                    # bounded by time, not target


class TestHorizonReturns(unittest.TestCase):
    def test_forward_returns(self):
        r = horizon_returns(_bars([100, 110, 121]), horizon=2)      # one 2-bar forward return
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(r[0], 0.21)


if __name__ == "__main__":
    unittest.main()
