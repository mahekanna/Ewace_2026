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
    diagonal_rules, ending_diagonal_rules, leading_diagonal_rules, disambiguate_five,
    similarity_and_balance, rule_of_proportion, retracement_logic,
    is_terminal, terminal_rules, terminal_retrace_window, is_running_triangle,
    classify_complex_correction, is_neutral_triangle, x_wave_check,
    line_value, two_four_test, two_four_confirmation, throwover_test, base_channel_test,
    confirm_completion, CompletionSignal,
    label_monowaves, monowave_candidates, group_polywaves,
    validate_impulse, validate_correction, report,
)
from .toolkit import (
    zigzag, zigzag_causal, zigzag_multiscale, swing_pivots,
    pivots_to_waves, fib_extension, fib_retrace, wave_ratio, blue_box_zone,
)
from .automation import (
    CandidateCount, label_and_validate, assign_degrees_neely, swing_sequence,
)
from .backtest import (
    backtest_reversals, reversal_returns, horizon_returns,
    ReversalEvent, ReversalOutcome, BacktestStats,
)
from .validation import (
    sharpe_ratio, skew_kurt, probabilistic_sharpe_ratio, min_track_record_length,
    deflated_sharpe_ratio, expected_max_sharpe, log_trial, count_trials,
    cpcv_splits, cpcv_profit_factor,
)
from .charting import render_chart
from .wavetree import (
    WaveNode, build_wave_tree, build_tree_from_pivots, format_tree, deepest_degree,
    best_count, tree_confidence, anchor_count, AnchoredCount,
    wave_counts, anchored_degree,
)
from .confluence import (
    score_reversal, classify_swing_sequence,
    in_zone, momentum_divergence, macd_turn, volume_capitulation,
    choch, channel_break, divergence_at,
    rsi, ema, macd, ConfluenceReport, Strand,
)
from .forecast import (
    WaveForecast, forecast_waves, forecast_from_count, TradePlan, trade_plan,
)
from .forecast_backtest import (
    ForecastTrade, forecast_trades, forecast_returns, expectancy,
)
from .cycle_seam import CycleSignal

__version__ = "0.2.0"
