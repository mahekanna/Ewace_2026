"""
wavelib.validation — LEGACY SHIM over ewave.validation.stats
(docs/ARCHITECTURE.md D2). The Bailey & Lopez de Prado stack moved verbatim.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

from ewave.validation.stats import (                              # noqa: F401,E402
    cpcv_profit_factor, cpcv_splits, count_trials, deflated_sharpe_ratio,
    expected_max_sharpe, log_trial, min_track_record_length,
    probabilistic_sharpe_ratio, sharpe_ratio, skew_kurt)
