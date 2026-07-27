"""
wavelib.forecast_backtest — LEGACY SHIM over ewave.backtest.engine_forecast
(docs/ARCHITECTURE.md D2). The institution-style forecast backtest moved
verbatim. Reminder: it trades the REF-only next-leg forecast — research
machinery, not the platform's signal path (that is ewave.backtest.engine).
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.backtest.engine_forecast as _fb                      # noqa: E402

globals().update({k: v for k, v in vars(_fb).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _fb
