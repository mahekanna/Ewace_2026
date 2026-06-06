"""
Stage 5 — statistical validation (docs/research/deep/08).

Synthetic checks for the Sharpe / PSR / MinTRL / Deflated-Sharpe math.

Run:  python3 -m unittest tests.test_validation -v
"""
import unittest

from wavelib import (
    sharpe_ratio, skew_kurt, probabilistic_sharpe_ratio, min_track_record_length,
    deflated_sharpe_ratio, expected_max_sharpe,
)


class TestValidationMath(unittest.TestCase):
    def test_sharpe_basic(self):
        self.assertAlmostEqual(sharpe_ratio([0.01, 0.01, 0.01]), 0.0)  # zero variance -> 0
        self.assertGreater(sharpe_ratio([0.02, 0.01, 0.03, 0.015]), 0)

    def test_psr_monotonic_in_sample_size(self):
        # same Sharpe, more observations -> higher confidence it's real
        p_small = probabilistic_sharpe_ratio(0.3, 0.0, 20, 0.0, 3.0)
        p_large = probabilistic_sharpe_ratio(0.3, 0.0, 200, 0.0, 3.0)
        self.assertGreater(p_large, p_small)
        self.assertTrue(0.0 <= p_small <= 1.0 <= 1.0)

    def test_psr_higher_for_higher_sharpe(self):
        self.assertGreater(
            probabilistic_sharpe_ratio(0.5, 0.0, 100, 0.0, 3.0),
            probabilistic_sharpe_ratio(0.1, 0.0, 100, 0.0, 3.0))

    def test_min_trl_positive_and_none_when_no_edge(self):
        self.assertIsNone(min_track_record_length(0.0, 0.0, 0.0, 3.0))
        n = min_track_record_length(0.3, 0.0, 0.0, 3.0)
        self.assertIsNotNone(n)
        self.assertGreater(n, 0)

    def test_deflated_sharpe_below_plain_psr(self):
        # testing many variants raises the bar -> DSR <= PSR(vs 0)
        sr, n, sk, ku = 0.4, 150, 0.0, 3.0
        psr0 = probabilistic_sharpe_ratio(sr, 0.0, n, sk, ku)
        dsr = deflated_sharpe_ratio(sr, n, sk, ku, n_trials=50, sr_variance=0.04)
        self.assertLessEqual(dsr, psr0)

    def test_expected_max_sharpe_grows_with_trials(self):
        self.assertGreater(expected_max_sharpe(100, 0.04), expected_max_sharpe(5, 0.04))


class TestSkewKurt(unittest.TestCase):
    def test_symmetric_near_zero_skew(self):
        sk, ku = skew_kurt([-2, -1, 0, 1, 2, -2, -1, 0, 1, 2])
        self.assertAlmostEqual(sk, 0.0, places=6)
        self.assertGreater(ku, 0)


if __name__ == "__main__":
    unittest.main()
