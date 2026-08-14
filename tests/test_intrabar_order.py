"""
Intrabar pivot ordering — regression tests.

OHLC does not record the path price took inside a bar. Both ZigZags used to
process the extreme in the trend's direction first and then test the reversal
threshold against that just-updated extreme, which is only valid when price
actually visited that extreme first. On a bar wide enough to do both, this
minted a low and a high pivot at the same timestamp in reverse chronological
order.

Found live on AVGO 1H, 2026-08-14 13:30 (o 411.93 h 412.36 l 395.13 c 397.07):
the bar opened near its high and sold off, so the path is high-then-low, but
`zigzag_causal(pct=0.04)` emitted `L 395.13` -> `H 412.36` and inverted the
intraday count.

Pure stdlib (unittest). Run:  python3 -m unittest tests.test_intrabar_order -v
"""
import unittest

from wavelib import zigzag, zigzag_causal
from wavelib.toolkit import _intrabar_order


def _bar(t, o, h, l, c):
    return (t, o, h, l, c)


class TestIntrabarOrder(unittest.TestCase):
    def test_down_bar_is_high_first(self):
        self.assertEqual(_intrabar_order(_bar(0, 411.93, 412.36, 395.13, 397.07)),
                         ("H", "L"))

    def test_up_bar_is_low_first(self):
        self.assertEqual(_intrabar_order(_bar(0, 415.70, 424.92, 411.50, 422.98)),
                         ("L", "H"))

    def test_short_bar_returns_none(self):
        # (t,h,l,c) carries no open to infer from -> caller falls back.
        self.assertIsNone(_intrabar_order((0, 100.0, 90.0, 95.0)))


class TestNoReversedSameBarPair(unittest.TestCase):
    """The AVGO 2026-08-14 case, reduced to the bars that matter."""

    # a steady drift down, then the wide high-then-low bar
    BARS = ([_bar(i, 430.0 - i, 431.0 - i, 429.0 - i, 429.5 - i) for i in range(20)]
            + [_bar(20, 411.93, 412.36, 395.13, 397.07),
               _bar(21, 397.06, 399.43, 394.16, 394.29)])

    def _pairs(self, pivots):
        return [(x, y) for x, y in zip(pivots, pivots[1:]) if x.t == y.t]

    def test_causal_does_not_reverse_off_unreached_low(self):
        piv = zigzag_causal(self.BARS, pct=0.04)
        for x, y in self._pairs(piv):
            self.assertEqual((x.kind, y.kind), ("H", "L"),
                             f"same-bar pair {x.kind}->{y.kind} at t={x.t} is reversed")

    def test_last_leg_is_down(self):
        # price ends at its low; the final provisional pivot must be that low,
        # not the high of the wide bar
        piv = zigzag_causal(self.BARS, pct=0.04)
        self.assertEqual(piv[-1].kind, "L")
        self.assertAlmostEqual(piv[-1].price, 394.16, places=2)
        self.assertIsNone(piv[-1].confirmed_t)

    def test_plain_and_causal_agree(self):
        # zigzag_causal's contract: same pivots as zigzag in percentage mode.
        for pct in (0.02, 0.03, 0.04, 0.05, 0.08):
            a = [(p.kind, p.price, p.t) for p in zigzag(self.BARS, pct=pct)]
            b = [(p.kind, p.price, p.t) for p in zigzag_causal(self.BARS, pct=pct)]
            self.assertEqual(a, b, f"streams diverge at pct={pct}")


class TestOrderingInvariantHolds(unittest.TestCase):
    """Any two pivots sharing a bar must match that bar's inferred path."""

    def _check(self, bars, pct):
        seed = bars[0][0]
        by_t = {b[0]: b for b in bars}
        for fn in (zigzag, zigzag_causal):
            piv = fn(bars, pct=pct)
            for x, y in zip(piv, piv[1:]):
                # the seed pivot is priced at bar 0's close, not an extreme —
                # a separate, pre-existing artifact; skip the seed bar
                if x.t != y.t or x.t == seed:
                    continue
                self.assertEqual((x.kind, y.kind), _intrabar_order(by_t[x.t]),
                                 f"{fn.__name__} pct={pct} t={x.t}")

    def test_alternating_wide_bars(self):
        # alternating wide up/down bars: every bar can both extend and reverse
        bars = []
        for i in range(40):
            base = 100.0 + (i % 2) * 5
            if i % 2:                                    # down bar: h then l
                bars.append(_bar(i, base + 8, base + 9, base - 9, base - 8))
            else:                                        # up bar: l then h
                bars.append(_bar(i, base - 8, base + 9, base - 9, base + 8))
        for pct in (0.02, 0.04, 0.06, 0.10):
            self._check(bars, pct)

    def test_causal_confirmations_never_precede_extreme(self):
        bars = [_bar(i, 100 + i, 105 + i, 95 + i, 102 + i) for i in range(30)]
        bars.append(_bar(30, 132.0, 133.0, 100.0, 101.0))   # wide reversal bar
        piv = zigzag_causal(bars, pct=0.05)
        confirms = [p.confirmed_t for p in piv if p.confirmed_t is not None]
        self.assertEqual(confirms, sorted(confirms))
        for p in piv:
            if p.confirmed_t is not None:
                self.assertGreaterEqual(p.confirmed_t, p.t)


if __name__ == "__main__":
    unittest.main()
