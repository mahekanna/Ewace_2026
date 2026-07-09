"""
ewave.rules — Elliott + NeoWave validators over the RuleResult model.
=====================================================================
result.py is the import-graph root (Pivot/Wave/Degree/Status/RuleResult);
topic modules hold the validators; engine.py aggregates; profiles.py selects.
A count is INVALID iff any hard-rule FAIL; guidelines WARN and never
invalidate; REF = human discretion; UNKNOWN = insufficient confirmed data.
"""
from .result import (PHI, INV_PHI, Degree, Pivot, RuleResult, Status, Wave)
from .elliott import (elliott_guidelines, elliott_hard_rules, project_wave5)
from .triangles import (is_neutral_triangle, is_running_triangle,
                        triangle_thrust, x_wave_check)
from .corrections import (classify_complex_correction, classify_correction)
from .diagonals import (diagonal_rules, disambiguate_five,
                        ending_diagonal_rules, is_terminal,
                        leading_diagonal_rules, terminal_retrace_window,
                        terminal_rules)
from .neowave import (CompletionSignal, base_channel_test, confirm_completion,
                      group_polywaves, label_monowaves, line_value,
                      monowave_candidates, retracement_logic,
                      rule_of_proportion, similarity_and_balance,
                      throwover_test, two_four_confirmation, two_four_test)
from .engine import (report, validate_correction, validate_impulse)
from .fib import (blue_box_zone, fib_cluster, fib_extension, fib_retrace,
                  wave_ratio)

__all__ = [
    "PHI", "INV_PHI", "Degree", "Pivot", "RuleResult", "Status", "Wave",
    "elliott_hard_rules", "elliott_guidelines", "project_wave5",
    "triangle_thrust", "is_running_triangle", "is_neutral_triangle",
    "classify_correction", "classify_complex_correction", "x_wave_check",
    "diagonal_rules", "ending_diagonal_rules", "leading_diagonal_rules",
    "disambiguate_five", "is_terminal", "terminal_rules",
    "terminal_retrace_window",
    "similarity_and_balance", "rule_of_proportion", "retracement_logic",
    "line_value", "two_four_test", "two_four_confirmation",
    "CompletionSignal", "confirm_completion", "throwover_test",
    "base_channel_test", "label_monowaves", "monowave_candidates",
    "group_polywaves",
    "validate_impulse", "validate_correction", "report",
    "fib_extension", "fib_retrace", "fib_cluster", "wave_ratio",
    "blue_box_zone",
]
