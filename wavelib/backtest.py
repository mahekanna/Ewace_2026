"""
wavelib.backtest — LEGACY SHIM over ewave.backtest.replay
(docs/ARCHITECTURE.md D2). The causal reversal-replay harness moved verbatim.
The NEW flagship trade backtest (profile-driven wave-3, reproducing
docs/WAVE3_RESULT.md) lives in ewave.backtest.engine.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.backtest.replay as _bt                               # noqa: E402

globals().update({k: v for k, v in vars(_bt).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _bt
