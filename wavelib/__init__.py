"""
wavelib — Elliott Wave / NeoWave rule engine + reversal-confluence scoring.

Quick start
-----------
    from wavelib import zigzag, pivots_to_waves, validate_impulse, report
    pivots = zigzag(bars, pct=0.05)            # bars = (t,o,h,l,c)
    waves  = pivots_to_waves(pivots[-6:])      # last 5 legs
    print(report(validate_impulse(waves)))

Modules
-------
    wavelib.rules       Elliott + NeoWave rule validators, channeling, engines
    wavelib.toolkit     ZigZag, Fibonacci helpers, terminal/wave-5 projection
    wavelib.confluence  Reversal-confidence scoring (momentum/volume/structure)

Note: rules.py and toolkit.py each define a Pivot/Wave dataclass; they are
structurally identical and duck-type-compatible across functions.
"""
from .rules import (
    Pivot, Wave, Degree, Status, RuleResult,
    elliott_hard_rules, elliott_guidelines, project_wave5,
    classify_correction, triangle_thrust,
    diagonal_rules, ending_diagonal_rules, leading_diagonal_rules,
    similarity_and_balance, rule_of_proportion, retracement_logic,
    is_terminal, terminal_retrace_window, classify_complex_correction,
    line_value, two_four_test, throwover_test, base_channel_test,
    validate_impulse, validate_correction, report,
)
from .toolkit import (
    zigzag, zigzag_causal, swing_pivots,
    pivots_to_waves, fib_extension, fib_retrace, wave_ratio,
)
from .confluence import (
    score_reversal, classify_swing_sequence,
    rsi, ema, macd, ConfluenceReport, Strand,
)

__version__ = "0.1.0"
