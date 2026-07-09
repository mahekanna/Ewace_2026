"""
wavelib.rules — LEGACY SHIM over ewave.rules (docs/ARCHITECTURE.md D2).
=======================================================================
The rule engine moved to src/ewave/rules/, split by topic:
  result.py      Pivot / Wave / Degree / Status / RuleResult (canonical)
  elliott.py     hard rules R1-R3, guidelines, wave-5 projection
  triangles.py   triangle classifiers, thrust, running/neutral, x-wave
  corrections.py zigzag/flat family, complex-correction zoo
  diagonals.py   leading/ending diagonals, disambiguator, terminals
  neowave.py     S&B, proportion, retracement logic, channeling, completion
                 monitor, monowave constructor (label_monowaves, ...)
  engine.py      validate_impulse / validate_correction / report
  fib.py         Fibonacci helpers

Every historical `from wavelib.rules import X` still resolves — to the SAME
object as the ewave one. The demo below is the historical self-test (CI runs
`python wavelib/rules.py`).
"""
from __future__ import annotations
from datetime import datetime, timezone

try:
    from ewave.rules.result import (PHI, INV_PHI, Degree, Pivot, Wave, Status,
                                    RuleResult, _ok, _within, _group_similar)
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))
    from ewave.rules.result import (PHI, INV_PHI, Degree, Pivot, Wave, Status,
                                    RuleResult, _ok, _within, _group_similar)

from ewave.rules.elliott import (                                 # noqa: F401,E402
    elliott_guidelines, elliott_hard_rules, project_wave5)
from ewave.rules.triangles import (                               # noqa: F401,E402
    BARRIER_FLAT_TOL, _classify_triangle, is_neutral_triangle,
    is_running_triangle, triangle_thrust, x_wave_check)
from ewave.rules.corrections import (                             # noqa: F401,E402
    REG_FLAT_B_MAX, ZIGZAG_B_MAX, classify_complex_correction,
    classify_correction)
from ewave.rules.diagonals import (                               # noqa: F401,E402
    _diagonal_common, diagonal_rules, disambiguate_five,
    ending_diagonal_rules, is_terminal, leading_diagonal_rules,
    terminal_retrace_window, terminal_rules)
from ewave.rules.neowave import (                                 # noqa: F401,E402
    _RETRACE_BREAKS, _retracement_rule, CompletionSignal, base_channel_test,
    confirm_completion, group_polywaves, label_monowaves, line_value,
    monowave_candidates, retracement_logic, rule_of_proportion,
    similarity_and_balance, throwover_test, two_four_confirmation,
    two_four_test)
from ewave.rules.engine import (                                  # noqa: F401,E402
    report, validate_correction, validate_impulse)


# =========================================================================== #
# H. DEMO
# =========================================================================== #
def _P(d, price, kind="H"):
    t = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    return Pivot(t, price, kind)


def _demo():
    # AVGO Primary impulse (I)-(II)-(III) is only 3 waves; demo the wave-(III)
    # internal 5 and the wave-5 terminal.
    # wave (III) internals: ((1))..((5))
    avgo_III = [
        Wave(_P("2025-04-07", 138.10, "L"), _P("2025-06-09", 265.43, "H")),
        Wave(_P("2025-06-09", 265.43, "H"), _P("2025-06-23", 241.11, "L")),
        Wave(_P("2025-06-23", 241.11, "L"), _P("2025-12-08", 414.61, "H")),
        Wave(_P("2025-12-08", 414.61, "H"), _P("2026-03-30", 289.96, "L")),
        Wave(_P("2026-03-30", 289.96, "L"), _P("2026-06-03", 495.00, "H")),
    ]
    print(report(validate_impulse(avgo_III), "AVGO — wave (III) as a 5-wave impulse"))
    print("  wave5 projection:", project_wave5(127.33, 173.50, 289.96, 495.00))
    # CHANNELING FIRST (NeoWave construction order): 2-4 line + wave-5 vs upper channel
    print(report([
        two_four_test(_P("2025-06-23", 241.11, "L"), _P("2026-03-30", 289.96, "L"),
                      _P("2026-06-04", 407, "L").t, 407.0),
        throwover_test(_P("2025-06-09", 265.43), _P("2025-12-08", 414.61),
                       495.0, _P("2026-06-03", 495.0).t),
    ], "AVGO — CHANNELING (apply before trusting the count)"))

    # AVGO terminal (wave ⑤ on 4h) — expect overlap -> terminal/diagonal
    avgo_term = [
        Wave(_P("2026-03-30", 289.96, "L"), _P("2026-04-21", 429.31, "H")),
        Wave(_P("2026-04-21", 429.31, "H"), _P("2026-04-23", 394.66, "L")),
        Wave(_P("2026-04-23", 394.66, "L"), _P("2026-05-14", 442.36, "H")),
        Wave(_P("2026-05-14", 442.36, "H"), _P("2026-05-19", 405.87, "L")),
        Wave(_P("2026-05-19", 405.87, "L"), _P("2026-06-03", 495.00, "H")),
    ]
    print(report(validate_impulse(avgo_term, diagonal=True), "AVGO — wave ⑤ as a terminal/diagonal"))
    build = (avgo_term[-1].end.t - avgo_term[0].start.t) / 86400
    print("  terminal retrace-to-$290 windows:", terminal_retrace_window(build, avgo_term[-1].end.t))

    # MRVL impulse (I)(II)+((1))((2))((3)) — demo (II) retracement logic
    mrvl = [
        Wave(_P("2022-12-30", 33.75, "L"), _P("2025-01-21", 127.48, "H")),   # (I)
        Wave(_P("2025-01-21", 127.48, "H"), _P("2025-04-07", 47.09, "L")),   # (II)
        Wave(_P("2025-04-07", 47.09, "L"), _P("2025-12-04", 102.77, "H")),   # ((1)) of III
        Wave(_P("2025-12-04", 102.77, "H"), _P("2026-02-09", 76.07, "L")),   # ((2))
        Wave(_P("2026-02-09", 76.07, "L"), _P("2026-06-03", 324.20, "H")),   # ((3))
    ]
    print(report([
        retracement_logic(mrvl[1].retr(mrvl[0])),
        similarity_and_balance(mrvl[1], mrvl[3]),
        RuleResult("((3))/((1)) extension", Status.WARN,
                   f"{mrvl[4].length/mrvl[2].length:.1f}× -> extended 3rd, S&B-stretched"),
        throwover_test(_P("2026-04-13", 170.84), _P("2026-05-29", 218.26),
                       324.20, _P("2026-06-03", 324.20).t),
    ], "MRVL — NeoWave audit + channeling"))


if __name__ == "__main__":
    _demo()
