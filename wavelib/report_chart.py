"""
wavelib.report_chart — LEGACY SHIM over ewave.reporting.html_report
(docs/ARCHITECTURE.md D2). The HTML report/chart builder moved verbatim.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.reporting.html_report as _rc                         # noqa: E402

globals().update({k: v for k, v in vars(_rc).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _rc
