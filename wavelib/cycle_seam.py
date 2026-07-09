"""
wavelib.cycle_seam — LEGACY SHIM over ewave.signals.cycle_seam
(docs/ARCHITECTURE.md D2). The typed chakra_quant seam moved VERBATIM —
CycleSignal is the same frozen dataclass object.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

from ewave.signals.cycle_seam import CycleSignal                  # noqa: F401,E402
