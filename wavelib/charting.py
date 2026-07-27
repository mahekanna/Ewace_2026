"""
wavelib.charting — LEGACY SHIM over ewave.reporting.charting
(docs/ARCHITECTURE.md D2). The stdlib SVG emitter moved verbatim.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

from ewave.reporting.charting import *                            # noqa: F401,F403,E402
from ewave.reporting.charting import render_chart                 # noqa: F401,E402
