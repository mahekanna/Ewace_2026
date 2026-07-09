"""
wavelib.wave3 — LEGACY SHIM over ewave.signals.wave3
(docs/ARCHITECTURE.md D2). The validated wave-3 confirmation entry moved
verbatim (strict variant gained optional knobs, defaults unchanged; plus the
new profile-driven generate()). Same objects.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

from ewave.signals.wave3 import (                                 # noqa: F401,E402
    Wave3Signal, generate, wave3_signal, wave3_signal_strict)
