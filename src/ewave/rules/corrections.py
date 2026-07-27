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


def diametric_pair_checks(legs: "Sequence[Wave]") -> "list[RuleResult]":
    """Diametric paired-leg relationships (RULESET §I.1 [G]; SOW Fibo sheet):
    G~A (or ~61.8% of A), F~B, E~C — each satisfied by PRICE (ratio in
    [0.5, 1.7], covering 61.8% and equality bands) OR TIME (ratio in [1/3, 3],
    the S&B band). Legs = [a..g]."""
    if len(legs) != 7:
        return [RuleResult("diametric pairs", Status.NA,
                           f"need 7 legs, got {len(legs)}")]
    pairs = ((legs[6], legs[0], "G~A"), (legs[5], legs[1], "F~B"),
             (legs[4], legs[2], "E~C"))
    out = []
    for x, y, name in pairs:
        p_ok = _within(x.length, y.length, 0.5, 1.7)
        t_ok = _within(x.days, y.days, 1 / 3, 3.0)
        pr = x.length / y.length if y.length else float("nan")
        tr = x.days / y.days if y.days else float("nan")
        out.append(RuleResult(f"diametric {name} (price OR time)",
                              Status.PASS if (p_ok or t_ok) else Status.WARN,
                              f"price {pr:.2f}x (ok={p_ok}), time {tr:.2f}x "
                              f"(ok={t_ok})"))
    return out


def zigzag_c_check(w: "Sequence[Wave]") -> RuleResult:
    """Zigzag C-beyond-A gate (RULESET §B / audit G7): C's endpoint should
    surpass A's endpoint in A's direction; a shortfall is a truncated C —
    verify the count (WARN, not FAIL)."""
    if len(w) != 3:
        return RuleResult("zigzag C beyond A", Status.NA,
                          f"need 3 legs, got {len(w)}")
    A, B, C = w
    a_down = A.end.price < A.start.price
    beyond = (C.end.price < A.end.price) if a_down else (C.end.price > A.end.price)
    return RuleResult("zigzag: C surpasses end of A",
                      Status.PASS if beyond else Status.WARN,
                      f"C end {C.end.price:.2f} vs A end {A.end.price:.2f}"
                      + ("" if beyond else " -> truncated C; verify count"))


def correction_time_rules(w: "Sequence[Wave]") -> "list[RuleResult]":
    """SOW corrective time rules (RULESET §I.5 [G]): in zigzag AND flat, B
    should take >= the time of A. Also emits the SOW diagnosis heuristic:
    B faster than A -> triangle/diametric more likely."""
    if len(w) < 2:
        return [RuleResult("correction time rules", Status.NA,
                           f"need >=2 legs, got {len(w)}")]
    A, B = w[0], w[1]
    ok = B.days >= A.days
    out = [RuleResult("correction: B time >= A time",
                      Status.PASS if ok else Status.WARN,
                      f"A {A.days:.1f}d vs B {B.days:.1f}d")]
    if not ok:
        out.append(RuleResult("correction diagnosis (SOW Day-2 p.9)",
                              Status.REF,
                              "B faster than A -> triangle/diametric more "
                              "likely than zigzag/flat"))
    return out


def flat_b_band(A: Wave, B: Wave) -> RuleResult:
    """Flat B-wave strength band (RULESET §I.4 [N]): weak 61.8-80%, normal
    80-100%, strong >100% of A."""
    r = B.retr(A)
    if r != r:
        return RuleResult("flat B band", Status.UNKNOWN, "degenerate A length")
    if r < 0.618:
        return RuleResult("flat B band", Status.NA,
                          f"B {r:.0%} of A (<61.8% -> zigzag territory, not a flat)")
    band = "weak" if r < 0.80 else "normal" if r <= 1.0 else "strong"
    return RuleResult(f"flat B band = {band.upper()}", Status.PASS,
                      f"B retraces {r:.0%} of A "
                      f"(weak 61.8-80 / normal 80-100 / strong >100)")


def max_x_count_check(n_x: int) -> RuleResult:
    """Complex-correction X-count limit (RULESET §I.3 [H]; SOW Day-2 p.7):
    W-X-Y (one X) or W-X-Y-X-Z (two X) — never more."""
    if n_x <= 2:
        return RuleResult("complex: max two X waves", Status.PASS,
                          f"{n_x} X wave(s)")
    return RuleResult("complex: max two X waves", Status.FAIL,
                      f"{n_x} X waves (>2) -> structurally invalid; "
                      "reassess degree/segmentation")
