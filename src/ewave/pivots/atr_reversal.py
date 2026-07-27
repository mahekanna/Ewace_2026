"""
pivots.atr_reversal — volatility-adaptive causal reversal pivots.
=================================================================
The percentage-reversal engine in ATR mode, exposed as its own detector (the
uploads' `atr_reversal`): the reversal threshold is `ATR(n) * mult`, an
absolute distance that adapts to volatility instead of a fixed percentage.
"""
from __future__ import annotations

from typing import List

from ..rules.result import Pivot
from .percentage_reversal import causal_atr, zigzag_causal  # noqa: F401 (re-export)


def detect(bars, atr_n: int = 14, mult: float = 3.0) -> List[Pivot]:
    """Causal ATR-reversal pivots: same confirmation semantics as
    `zigzag_causal` (`confirmed_t` stamped at the reversal bar, last pivot
    provisional)."""
    return zigzag_causal(bars, pct=mult, atr_n=atr_n)
