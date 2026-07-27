"""
wavelib_adapter.py — example: wrap an EXISTING model into the forecaster contract.
==================================================================================
Shows how to plug a real engine (this repo's Elliott/NeoWave `wavelib.forecast_waves`)
into the generic kit. The pattern is the same for any project: import your model,
call it on the given bars, map its output to a `Forecast`. Running the kit with this
adapter reproduces the project's own forward-test numbers — proof the harness is
faithful and portable.

  python3 ghost_forward.py --data ../data/live/avgo_15m_2026-06.json \
          --forecaster forecasters/wavelib_adapter.py:forecast --roll 400 --resolve 32
"""
import os
import sys

_KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPO = os.path.dirname(_KIT)
sys.path.insert(0, _KIT)          # for gf
sys.path.insert(0, _REPO)         # for wavelib (this repo)

from gf import Forecast
import wavelib as wl


def forecast(bars):
    fc = wl.forecast_waves(bars)            # uses all bars handed in (already roll-windowed)
    if fc is None or not fc.targets:
        return None
    tgt = fc.cluster[0][0] if fc.cluster else fc.targets[0][1]
    kind = fc.next_wave.split("(")[0].strip()   # e.g. "new impulse", "corrective A-B-C"
    return Forecast(direction=fc.direction, target=tgt, invalidation=fc.invalidation,
                    confidence=fc.confidence, kind=kind, note=fc.next_wave)
