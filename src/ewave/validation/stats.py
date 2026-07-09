"""
validation.stats — institutional statistical validation (PSR/DSR/CPCV/MinTRL).
==============================================================================
Implements the de-facto institutional checks (Bailey & Lopez de Prado) so the
engine can say whether a measured edge is statistically real or just noise from
a short, multiply-tested backtest. Pure stdlib (math + statistics.NormalDist).

See docs/research/deep/08_institutional_validation.md for derivations + sources.
"""
from __future__ import annotations
import itertools
import json
import math
import os
from statistics import NormalDist

_N = NormalDist()
_EULER = 0.5772156649015329


def sharpe_ratio(returns) -> float:
    """Per-observation Sharpe (mean/std of the return series). 0 if degenerate."""
    r = [x for x in returns if x is not None]
    if len(r) < 2:
        return 0.0
    m = sum(r) / len(r)
    var = sum((x - m) ** 2 for x in r) / (len(r) - 1)
    sd = math.sqrt(var)
    return m / sd if sd > 0 else 0.0


def skew_kurt(returns):
    """Sample skewness and (non-excess) kurtosis. Returns (0.0, 3.0) if degenerate."""
    r = [x for x in returns if x is not None]
    n = len(r)
    if n < 3:
        return 0.0, 3.0
    m = sum(r) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / n)
    if sd == 0:
        return 0.0, 3.0
    skew = sum(((x - m) / sd) ** 3 for x in r) / n
    kurt = sum(((x - m) / sd) ** 4 for x in r) / n
    return skew, kurt


def probabilistic_sharpe_ratio(sr, sr_benchmark, n, skew, kurt) -> float:
    """PSR: probability the true Sharpe exceeds `sr_benchmark`, given n obs and
    the return distribution's skew/kurtosis (Bailey & Lopez de Prado)."""
    if n < 2:
        return 0.0
    denom = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * sr * sr
    if denom <= 0:
        return 0.0
    z = (sr - sr_benchmark) * math.sqrt(n - 1) / math.sqrt(denom)
    return _N.cdf(z)


def min_track_record_length(sr, sr_benchmark, skew, kurt, prob=0.95):
    """MinTRL: how many observations are needed for PSR(sr_benchmark) >= prob.
    None if sr <= benchmark (no positive edge to confirm)."""
    if sr <= sr_benchmark:
        return None
    denom = 1.0 - skew * sr + ((kurt - 1.0) / 4.0) * sr * sr
    za = _N.inv_cdf(prob)
    return 1.0 + denom * (za / (sr - sr_benchmark)) ** 2


def expected_max_sharpe(n_trials, sr_variance) -> float:
    """Expected maximum Sharpe from `n_trials` independent backtests with the
    given variance of trial Sharpes — the bar a result must clear to be real."""
    if n_trials < 2 or sr_variance <= 0:
        return 0.0
    a = _N.inv_cdf(1.0 - 1.0 / n_trials)
    b = _N.inv_cdf(1.0 - 1.0 / (n_trials * math.e))
    return math.sqrt(sr_variance) * ((1.0 - _EULER) * a + _EULER * b)


def deflated_sharpe_ratio(sr, n, skew, kurt, n_trials, sr_variance) -> float:
    """DSR: PSR measured against the expected-max Sharpe from n_trials. This is
    the multiple-testing-corrected probability that the edge is real."""
    sr0 = expected_max_sharpe(n_trials, sr_variance)
    return probabilistic_sharpe_ratio(sr, sr0, n, skew, kurt)


def cpcv_splits(n, n_groups=6, n_test=2, embargo=0):
    """Combinatorial purged cross-validation index splits (Lopez de Prado).
    Split [0,n) into n_groups contiguous groups; every combination of n_test
    groups is a test fold, the rest train, with an `embargo` of indices purged
    around each test group to prevent leakage from overlapping-label outcomes.
    Yields (train_idx, test_idx)."""
    bounds = [round(i * n / n_groups) for i in range(n_groups + 1)]
    groups = [list(range(bounds[i], bounds[i + 1])) for i in range(n_groups)]
    for combo in itertools.combinations(range(n_groups), n_test):
        test = sorted(i for g in combo for i in groups[g])
        tset = set(test)
        purged = set()
        for g in combo:                         # embargo around each test group
            lo, hi = bounds[g], bounds[g + 1]
            purged.update(range(max(0, lo - embargo), lo))
            purged.update(range(hi, min(n, hi + embargo)))
        train = [i for i in range(n) if i not in tset and i not in purged]
        yield train, test


def _pf(returns):
    gains = sum(x for x in returns if x > 0)
    losses = sum(-x for x in returns if x < 0)
    if losses > 0:
        return gains / losses
    return float("inf") if gains > 0 else 0.0


def cpcv_profit_factor(returns, n_groups=6, n_test=2, pctile=5):
    """The honest edge verdict (docs/research/deep/08): the lower-percentile
    out-of-sample profit factor across all combinatorial test folds of the
    per-event return series. < 1.0 at the 5th percentile => no provable edge.
    Returns (low_pf, median_pf, n_folds) or None if too few events."""
    r = [x for x in returns if x is not None]
    if len(r) < n_groups:
        return None
    bounds = [round(i * len(r) / n_groups) for i in range(n_groups + 1)]
    groups = [r[bounds[i]:bounds[i + 1]] for i in range(n_groups)]
    pfs = [_pf([x for g in combo for x in groups[g]])
           for combo in itertools.combinations(range(n_groups), n_test)]
    if not pfs:
        return None
    pfs.sort()
    lo_idx = min(len(pfs) - 1, max(0, math.ceil(pctile / 100 * len(pfs)) - 1))
    median = pfs[len(pfs) // 2]
    return pfs[lo_idx], median, len(pfs)


def log_trial(record: dict, path="registry/trials.jsonl") -> None:
    """Append one backtest 'trial' to the registry. DSR needs the TOTAL number of
    variants ever tried (the n_trials problem) — capture it prospectively here."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def count_trials(path="registry/trials.jsonl") -> int:
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())
