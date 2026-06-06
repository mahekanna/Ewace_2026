"""
Stage 5 — statistical validation (docs/research/deep/08).

Synthetic checks for the Sharpe / PSR / MinTRL / Deflated-Sharpe math.

Run:  python3 -m unittest tests.test_validation -v
"""
import unittest

from wavelib import (
    sharpe_ratio, skew_kurt, probabilistic_sharpe_ratio, min_track_record_length,
    deflated_sharpe_ratio, expected_max_sharpe, cpcv_splits, cpcv_profit_factor,
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


class TestCPCV(unittest.TestCase):
    def test_splits_train_test_disjoint_and_cover(self):
        for train, test in cpcv_splits(60, n_groups=6, n_test=2, embargo=2):
            self.assertEqual(set(train) & set(test), set())     # disjoint
            self.assertEqual(len(test), 20)                     # 2 of 6 groups
            # purged indices (embargo) belong to neither train nor test
            self.assertLessEqual(len(train) + len(test), 60)

    def test_profit_factor_edge_vs_noise(self):
        winners = [0.05, 0.06, 0.04, 0.05, 0.05, 0.06, 0.04, 0.05] * 3   # consistent edge
        lo, med, k = cpcv_profit_factor(winners, n_groups=6, n_test=2)
        self.assertEqual(lo, float("inf"))                      # no losses -> inf PF (all wins)
        noise = [0.05, -0.05, 0.04, -0.06, 0.05, -0.05, 0.03, -0.04] * 3  # no edge
        lo2, med2, k2 = cpcv_profit_factor(noise, n_groups=6, n_test=2)
        self.assertLess(lo2, 1.5)                               # weak/noise -> low PF

    def test_too_few_events_returns_none(self):
        self.assertIsNone(cpcv_profit_factor([0.01, 0.02], n_groups=6, n_test=2))


class TestTrialsRegistry(unittest.TestCase):
    def test_log_and_count_roundtrip(self):
        import os
        import tempfile
        from wavelib import log_trial, count_trials
        path = os.path.join(tempfile.mkdtemp(), "trials.jsonl")
        self.assertEqual(count_trials(path), 0)
        log_trial({"strategy": "x", "sharpe": 0.5}, path=path)
        log_trial({"strategy": "x", "sharpe": 0.7}, path=path)
        self.assertEqual(count_trials(path), 2)


class TestSkewKurt(unittest.TestCase):
    def test_symmetric_near_zero_skew(self):
        sk, ku = skew_kurt([-2, -1, 0, 1, 2, -2, -1, 0, 1, 2])
        self.assertAlmostEqual(sk, 0.0, places=6)
        self.assertGreater(ku, 0)


if __name__ == "__main__":
    unittest.main()
