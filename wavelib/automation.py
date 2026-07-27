"""
wavelib.automation — LEGACY SHIM over ewave.patterns.candidates
(docs/ARCHITECTURE.md D2). The multi-scale auto-labeling engine and bottom-up
degree assignment moved verbatim; every historical name resolves to the same
object.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

from ewave.patterns.candidates import (                           # noqa: F401,E402
    CandidateCount, _closeness, _fib_score, _make_candidate, _promote,
    assign_degrees_neely, label_and_validate, swing_sequence)
