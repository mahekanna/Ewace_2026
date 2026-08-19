"""
Wave-3 confirmation entry (wavelib/wave3.py) — synthetic ground-truth tests.

Run:  python3 -m unittest tests.test_wave3 -v
"""
import unittest

from wavelib import wave3_signal, Wave3Signal


def _bars(prices):
    bars, t = [], 0
    for p in prices:
        bars.append((float(t), float(p), float(p) + 0.05, float(p) - 0.05, float(p), 1000.0))
        t += 900
    return bars


def _lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


class TestWave3Long(unittest.TestCase):
    def _setup(self, last2=(119, 121)):
        # lead-in (up 95->110, down 110->100) so the wave-1 origin (100) CONFIRMS as a
        # pivot; then wave1 100->120, wave2 120->110 (50% retr), then break >120.
        prices = ([95] * 15 + _lin(95, 110, 8) + _lin(110, 100, 8) + _lin(100, 120, 12)
                  + _lin(120, 110, 8) + [112, 114, 116, *last2])
        return _bars(prices)

    def test_fires_long_on_break(self):
        sig = wave3_signal(self._setup(), pct=0.02, atr_n=None, use_momentum=False)
        self.assertIsInstance(sig, Wave3Signal)
        self.assertEqual(sig.direction, "long")
        self.assertAlmostEqual(sig.entry, 120, delta=1.0)        # wave-1 high
        self.assertLess(sig.stop, 110)                            # below wave-2 low
        self.assertGreater(sig.targets[0][1], 140)                # 1.618x W1 extension
        self.assertGreater(sig.reward_risk, 1.5)                  # asymmetric by construction

    def test_no_fire_without_break(self):
        # last bar 119 -> never crosses the 120 wave-1 high
        sig = wave3_signal(self._setup(last2=(118, 119)), pct=0.02, atr_n=None, use_momentum=False)
        self.assertIsNone(sig)

    def test_no_fire_when_wave2_exceeds_origin(self):
        # wave 2 retraces past wave-1 origin (100) -> invalid impulse (R1)
        prices = ([95] * 15 + _lin(95, 110, 8) + _lin(110, 100, 8) + _lin(100, 120, 12)
                  + _lin(120, 95, 10) + [100, 110, 121])
        self.assertIsNone(wave3_signal(_bars(prices), pct=0.02, atr_n=None, use_momentum=False))


class TestWave3Short(unittest.TestCase):
    def test_fires_short_on_break(self):
        prices = ([105] * 15 + _lin(105, 90, 8) + _lin(90, 100, 8) + _lin(100, 80, 12)
                  + _lin(80, 90, 8) + [88, 86, 84, 81, 79])
        sig = wave3_signal(_bars(prices), pct=0.02, atr_n=None, use_momentum=False)
        self.assertIsInstance(sig, Wave3Signal)
        self.assertEqual(sig.direction, "short")
        self.assertGreater(sig.stop, 90)                          # above wave-2 high
        self.assertLess(sig.targets[0][1], 60)                    # downside extension
        self.assertGreater(sig.reward_risk, 1.5)


if __name__ == "__main__":
    unittest.main()
