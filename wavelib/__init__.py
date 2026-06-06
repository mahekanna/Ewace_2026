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
    is_terminal, terminal_rules, terminal_retrace_window,
    classify_complex_correction, is_neutral_triangle, x_wave_check,
    line_value, two_four_test, two_four_confirmation, throwover_test, base_channel_test,
    label_monowaves, group_polywaves,
    validate_impulse, validate_correction, report,
)
from .toolkit import (
    zigzag, zigzag_causal, zigzag_multiscale, swing_pivots,
    pivots_to_waves, fib_extension, fib_retrace, wave_ratio,
)
from .automation import (
    CandidateCount, label_and_validate, assign_degrees_neely,
)
from .backtest import (
    backtest_reversals, ReversalEvent, ReversalOutcome, BacktestStats,
)
from .charting import render_chart
from .confluence import (
    score_reversal, classify_swing_sequence,
    in_zone, momentum_divergence, macd_turn, volume_capitulation,
    choch, channel_break,
    rsi, ema, macd, ConfluenceReport, Strand,
)
from .cycle_seam import CycleSignal

__version__ = "0.2.0"
