"""
gf.py — Ghost Forward-Testing Kit core. CANONICAL COPY MOVED to
src/ewave/validation/ghost_forward/core.py (docs/ARCHITECTURE.md); this file
re-exports it so the kit's CLIs (ghost_forward.py / ghost_diag.py) and any
project that vendored the kit keep working from this directory. To vendor the
kit standalone into another project, copy the ewave core module in place of
this shim.
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))), "src"))

from ewave.validation.ghost_forward.core import (                 # noqa: F401,E402
    Forecast, _norm, atr, in_rth_ny, iter_steps, load_bars, load_forecaster,
    resolve, sma)
