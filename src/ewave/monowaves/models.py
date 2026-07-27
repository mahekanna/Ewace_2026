"""
monowaves.models — objective pivot-to-pivot segments.
=====================================================
A MonoWave is measurement, not interpretation: price/time lengths, slope,
direction, retracement/extension vs the previous segment, and — crucially —
`visible_at` = the END pivot's confirmed_t (a segment exists only once its end
pivot is knowable). No Elliott labels here by design (uploads §7); NeoWave
structure labels (:5/:3) attach later via the rules layer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..rules.result import Pivot


@dataclass
class MonoWave:
    wave_id: int                 # index within its build
    start: Pivot
    end: Pivot
    visible_at: float            # end pivot's confirmed_t (causal visibility)
    direction: str               # "UP" | "DOWN"
    start_price: float
    end_price: float
    price_length: float          # abs price change
    percent_change: float        # signed, vs start price
    time_length_secs: float
    time_length_bars: int
    slope: float                 # signed price change per bar
    retracement_of_previous: Optional[float] = None   # this length / prev length
    extension_vs_previous: Optional[float] = None     # signed ratio (same-direction runs)
    structure_label: str = ""    # NeoWave :5/:3 family — attached by rules layer later

    @property
    def up(self) -> bool:
        return self.direction == "UP"
