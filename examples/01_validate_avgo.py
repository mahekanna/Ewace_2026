"""
Example 01 — Validate AVGO wave structure with the rule engine.
Run from the project root:  python3 -m examples.01_validate_avgo
or:                         cd examples && python3 01_validate_avgo.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from wavelib import (Pivot, Wave, validate_impulse, report,
                     two_four_test, throwover_test, project_wave5)


def P(d, price, kind="H"):
    t = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    return Pivot(t, price, kind)


# --- AVGO wave (III) internal 5 ---
avgo_III = [
    Wave(P("2025-04-07", 138.10, "L"), P("2025-06-09", 265.43, "H")),
    Wave(P("2025-06-09", 265.43, "H"), P("2025-06-23", 241.11, "L")),
    Wave(P("2025-06-23", 241.11, "L"), P("2025-12-08", 414.61, "H")),
    Wave(P("2025-12-08", 414.61, "H"), P("2026-03-30", 289.96, "L")),
    Wave(P("2026-03-30", 289.96, "L"), P("2026-06-03", 495.00, "H")),
]
print(report(validate_impulse(avgo_III), "AVGO wave (III) — 5-wave impulse"))

# --- channeling first ---
print(report([
    two_four_test(P("2025-06-23", 241.11, "L"), P("2026-03-30", 289.96, "L"),
                  P("2026-06-05", 385.74, "L").t, 385.74),
    throwover_test(P("2025-06-09", 265.43), P("2025-12-08", 414.61),
                   495.0, P("2026-06-03", 495.0).t),
], "AVGO — channeling"))

# --- wave 5 projection / truncation ---
print("\nwave (V) projection:",
      project_wave5(w1_len=210.37, w3_len=356.90, w4_end=289.96, prior_high=495.00))
