"""
cycle_seam.py
=============
Typed interface for the 7th confluence strand (Hurst/FLD cycle timing).

This module defines the CycleSignal dataclass that acts as the seam between
Ewace_2026 (Elliott Wave "where") and chakra_quant (Hurst/FLD cycle "when").

CONTRACT:
  - Ewace_2026 makes NO import of chakra_quant.
  - chakra_quant makes NO import of Ewace_2026.
  - CycleSignal is populated by the CALLER (external integration code).
  - All fields reflect causal data only (data ≤ bar t) — see D-013 in
    chakra_quant's decisions log.

See docs/research/03_confirmation_strands.md §3.5 for the full seam spec.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CycleSignal:
    """
    Causal cycle-timing signal produced by chakra_quant at bar t.

    CONTRACT:
    - `aligned` is derived using ONLY data with timestamp <= t (D-013 causal-only rule).
    - No centered filters, no df.shift(-N) with N > 0, no scipy.signal.filtfilt.
    - The FLD is constructed as: close displaced forward by floor(cycle_period / 2) + 1
      bars (per chakra_quant D-005), so the FLD value at bar t uses close[t - half_period].
    - A bullish alignment: close[t] crossed above the FLD within the last `confirmation_bars`
      bars AND the cycle phase is in the bottom half of its nominal period (phase < pi).
    - A bearish alignment: close[t] crossed below the FLD AND phase > pi.
    - The `source` field encodes the algorithm name so post-hoc audits can verify
      causality (e.g., "goertzel_40bar" vs "batch_fft_40bar").

    Fields
    ------
    aligned           : True = cycle timing supports the reversal direction.
    cycle_period      : Nominal cycle period in bars (e.g. 20, 40, 80). Optional
                        for simple True/False usage.
    phase             : Current cycle phase in radians [0, 2*pi). Optional.
    source            : Algorithm identifier, e.g. "hurst_fld_20bar". Optional.
    fld_value         : The FLD level at bar t (for logging/chart overlay). Optional.
    confirmation_bars : How many bars back the FLD cross was detected (default 3).
    """
    aligned: bool
    cycle_period: Optional[float] = None
    phase: Optional[float] = None
    source: Optional[str] = None
    fld_value: Optional[float] = None
    confirmation_bars: int = 3
