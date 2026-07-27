"""
wavelib.confluence — LEGACY SHIM over ewave.signals.confluence
(docs/ARCHITECTURE.md D2). The 7-strand reversal-confidence scorer moved
verbatim (indicators rsi/ema/macd now live once in ewave.features.indicators).
The full module namespace is mirrored so every historical name — including the
strand internals tests touch — resolves to the same object.
"""
try:
    import ewave  # noqa: F401
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))

import ewave.signals.confluence as _conf                          # noqa: E402

globals().update({k: v for k, v in vars(_conf).items()
                  if not (k.startswith("__") and k.endswith("__"))})
del _conf

if __name__ == "__main__":
    print("Demo: run score_reversal(symbol, bars, zone) on live OHLCV+volume.")
    print("CycleSignal is available from wavelib.cycle_seam for typed 7th-strand input.")
