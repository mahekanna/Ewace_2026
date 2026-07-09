"""
wavelib.forecast — LEGACY SHIM over ewave.signals.trade_plan
(docs/ARCHITECTURE.md D2). The next-leg projection machinery moved verbatim.
REMINDER: the forecast DIRECTION is ghost-forward-disproven (REF-only,
docs/FORWARD_GHOST_TEST_FINDINGS.md); trade_plan's confirmation/confluence/R:R
machinery is the load-bearing part.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.signals.trade_plan as _tp                            # noqa: E402

globals().update({k: v for k, v in vars(_tp).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _tp
