"""
rules.corrections — correction classifiers: zigzag/flat family, complex zoo,
x-waves (moved verbatim from wavelib/rules.py §C/§F).
"""
from __future__ import annotations
from typing import Sequence

from .result import RuleResult, Status, Wave, _group_similar, _within
from .triangles import _classify_triangle

# Canonical correction thresholds (Frost & Prechter; docs/research/01_elliott_wave.md §4 Task 1)
ZIGZAG_B_MAX = 0.618    # zigzag: B retraces <= 61.8% of A (sharp)
REG_FLAT_B_MAX = 1.00   # regular flat: B within (0.618, 1.00]; expanded/running: B > 1.00

def classify_correction(w: Sequence[Wave]) -> RuleResult:
    """Identify ZIGZAG / FLAT(regular/expanded/running) / TRIANGLE / (else combo).

    Flat subtype uses a directional ENDPOINT check (does C surpass A's extreme in
    A's direction?) rather than a raw length ratio, and the zigzag/flat split sits
    at the canonical 0.618 (no 0.618-0.90 dead zone). See docs/research/01 §4 Task 1.
    """
    if len(w) == 5:
        return _classify_triangle(w)
    if len(w) != 3:
        return RuleResult("correction", Status.REF,
                          f"{len(w)} legs -> likely COMBINATION (W-X-Y / W-X-Y-X-Z); "
                          "needs sub-structure to resolve")
    A, B, C = w
    b_retr = B.retr(A)                              # how far B retraces A
    c_vs_a = C.length / A.length if A.length else float("nan")
    a_down = A.end.price < A.start.price            # direction of leg A
    # does C's endpoint surpass A's endpoint, in A's direction?
    c_beyond_a_end = (C.end.price < A.end.price) if a_down else (C.end.price > A.end.price)
    # ZIGZAG: sharp, B <= 61.8% of A (boundary inclusive)
    if b_retr <= ZIGZAG_B_MAX + 1e-9:
        return RuleResult("correction = ZIGZAG (5-3-5)", Status.PASS,
                          f"B retraces {b_retr:.0%} of A (<=61.8%); C/A={c_vs_a:.2f}; sharp")
    # FLAT family: B > 61.8% of A (sideways)
    if b_retr <= REG_FLAT_B_MAX:
        note = "" if b_retr >= 0.81 else " (shallow B 0.618-0.81: verify vs combination)"
        return RuleResult("correction = REGULAR FLAT (3-3-5)", Status.PASS,
                          f"B retraces {b_retr:.0%} of A (61.8-100%); C/A={c_vs_a:.2f}{note}")
    # B > 100% of A -> expanded vs running, decided by C's endpoint direction
    if c_beyond_a_end:
        return RuleResult("correction = EXPANDED FLAT (3-3-5)", Status.PASS,
                          f"B {b_retr:.0%} (>100% of A); C surpasses A end -> expanded")
    return RuleResult("correction = RUNNING FLAT (3-3-5)", Status.PASS,
                      f"B {b_retr:.0%} (>100% of A); C falls short of A end -> running")


def classify_complex_correction(legs: Sequence[Wave]) -> RuleResult:
    """
    NeoWave corrective zoo by leg count, gated on time-similarity (S&B):
      3  -> standard (see classify_correction)
      5  -> triangle
      7  -> diametric: diamond (middle leg longest) vs bowtie (middle shortest),
            requiring adjacent-leg time similarity across all 7 legs
      9  -> symmetrical: advancing legs similar to each other, declining legs
            similar to each other
      other -> multi-X complex combination (REF)
    (docs/research/02 §4 Tasks 7, 8.)
    """
    n = len(legs)
    if n == 3:
        return RuleResult("complex?", Status.NA, "3 legs -> standard correction (see classify_correction)")
    if n == 5:
        return _classify_triangle(legs)
    if n == 7:
        lens = [x.length for x in legs]
        times = [x.days for x in legs]
        time_sim = all(_within(times[i], times[i + 1], 1 / 3, 3.0) for i in range(6))
        mid = lens[3]
        if mid == max(lens):
            kind = "DIAMETRIC - diamond (middle leg longest)"
        elif mid == min(lens):
            kind = "DIAMETRIC - bowtie (middle leg shortest)"
        else:
            kind = "DIAMETRIC - irregular middle"
        return RuleResult(f"NeoWave {kind}", Status.PASS if time_sim else Status.WARN,
                          f"7 legs; lens {[round(x, 1) for x in lens]}; adjacent-leg time "
                          f"similarity {'ok' if time_sim else 'violated (verify count)'}")
    if n == 9:
        lens = [x.length for x in legs]
        adv, dec = lens[0::2], lens[1::2]            # advancing vs declining groups
        adv_sim, dec_sim = _group_similar(adv), _group_similar(dec)
        ok = adv_sim and dec_sim
        return RuleResult("NeoWave SYMMETRICAL (9 legs)", Status.PASS if ok else Status.WARN,
                          f"9 legs; advancing-group similar={adv_sim}, declining-group similar={dec_sim}")
    return RuleResult("NeoWave complex combination", Status.REF,
                      f"{n} legs -> multi-X (W-X-Y-X-Z+) / neutral or extracting triangle; "
                      "resolve via sub-degree construction")
