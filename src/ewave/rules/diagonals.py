"""
rules.diagonals — leading/ending diagonals, the 5-leg disambiguator, and
NeoWave terminal impulsions (moved verbatim from wavelib/rules.py §D/§F).
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Sequence

from .elliott import elliott_hard_rules
from .result import RuleResult, Status, Wave

def _diagonal_common(w: Sequence[Wave]) -> tuple[list[RuleResult], bool]:
    """Wedge-sizing checks shared by leading & ending diagonals; returns also the
    w4/w1 overlap flag so each variant can judge overlap per its own expectation."""
    w1, w2, w3, w4, w5 = w
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    # diagonals follow wedge-sizing; "wave 3 not shortest" -> WARN here, not FAIL
    c2 = not (w3.length < w1.length and w3.length < w5.length)
    contracting = (w5.length < w3.length < w1.length)
    r = [
        RuleResult("diagonal: wave3 vs wedge sizing", Status.PASS if c2 else Status.WARN,
                   f"1/3/5 = {w1.length:.1f}/{w3.length:.1f}/{w5.length:.1f}"
                   + ("" if c2 else "  (w3 shortest -> irregular for a wedge)")),
        RuleResult("diagonal: contracting wedge", Status.PASS if contracting else Status.WARN,
                   "legs contract (textbook)" if contracting
                   else "legs expand/irregular (rarer; allowed but non-ideal)"),
    ]
    return r, overlap


def ending_diagonal_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """Ending diagonal (wave 5 / wave C). Sub-structure 3-3-3-3-3; w4/w1 overlap
    EXPECTED (absence -> WARN, not FAIL, since sub-waves aren't machine-checkable
    at this degree). See docs/research/01 §4 Task 2."""
    if len(w) != 5:
        return [RuleResult("ending diagonal arity", Status.NA, f"need 5 legs, got {len(w)}")]
    r, overlap = _diagonal_common(w)
    r.append(RuleResult("ending diagonal: w4/w1 overlap expected",
                        Status.PASS if overlap else Status.WARN,
                        f"overlap {'present (expected)' if overlap else 'absent (atypical for ending)'}"))
    r.append(RuleResult("ending diagonal: sub-structure 3-3-3-3-3", Status.REF,
                        "each leg should subdivide as a three (needs sub-wave data; REF)"))
    return r


def leading_diagonal_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """Leading diagonal (wave 1 / wave A). Sub-structure 5-3-5-3-5; w4/w1 overlap
    COMMON but not required. See docs/research/01 §4 Task 2."""
    if len(w) != 5:
        return [RuleResult("leading diagonal arity", Status.NA, f"need 5 legs, got {len(w)}")]
    r, overlap = _diagonal_common(w)
    r.append(RuleResult("leading diagonal: w4/w1 overlap (informational)", Status.PASS,
                        f"overlap {'present (common)' if overlap else 'absent (acceptable for leading)'}"))
    r.append(RuleResult("leading diagonal: sub-structure 5-3-5-3-5", Status.REF,
                        "motive legs should subdivide 5-3-5-3-5 (needs sub-wave data; REF)"))
    return r


def diagonal_rules(w: Sequence[Wave], position: str = "ending") -> list[RuleResult]:
    """Back-compat dispatcher. Prefer ending_diagonal_rules / leading_diagonal_rules."""
    return leading_diagonal_rules(w) if position == "leading" else ending_diagonal_rules(w)


def disambiguate_five(w: Sequence[Wave]) -> RuleResult:
    """Decide what a 5-leg sequence most likely IS — IMPULSE vs DIAGONAL vs
    TRIANGLE/sideways — using the decision procedure in docs/research/deep/06:
      - must alternate as a motive sequence (w1/w3/w5 one way, w2/w4 the other);
      - no w4/w1 overlap + net-directional + R3 ok  -> IMPULSE;
      - w4/w1 overlap + net-directional (a wedge)    -> DIAGONAL;
      - not net-directional (sideways)               -> TRIANGLE / complex.
    Full ending-vs-leading split needs sub-wave data (see *_diagonal_rules)."""
    if len(w) != 5:
        return RuleResult("disambiguate", Status.NA, f"need 5 legs, got {len(w)}")
    w1, w2, w3, w4, w5 = w
    d = [x.up for x in w]
    if not (d[0] == d[2] == d[4] and d[1] == d[3] and d[1] != d[0]):
        return RuleResult("disambiguate = NOT A 5-SEQUENCE", Status.WARN,
                          "legs do not alternate as a motive 5-wave sequence")
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    net_dir = (w5.end.price > w1.start.price) if up else (w5.end.price < w1.start.price)
    r3_ok = elliott_hard_rules(w)[2].status is Status.PASS
    if not net_dir:
        return RuleResult("disambiguate = TRIANGLE / sideways", Status.WARN,
                          "net move ~0 -> sideways structure (triangle or complex correction)")
    if overlap:
        shape = "contracting" if (w1.length > w3.length > w5.length) else "expanding/irregular"
        return RuleResult("disambiguate = DIAGONAL", Status.PASS,
                          f"w4/w1 overlap + net-directional -> {shape} wedge "
                          "(ending vs leading needs sub-wave structure)")
    if r3_ok:
        return RuleResult("disambiguate = IMPULSE", Status.PASS,
                          "no w4/w1 overlap, net-directional, R3 holds")
    return RuleResult("disambiguate = AMBIGUOUS", Status.REF,
                      "mixed signals; resolve with sub-wave structure")



def is_terminal(w: Sequence[Wave]) -> RuleResult:
    """Terminal impulsion (NeoWave) / ending diagonal: 5 legs, w4/w1 overlap.
    Detail reports the wave-2 retracement vs the 61.8% terminal limit and the
    wedge shape; the fast-full-retrace expectation is a BIAS, not a price/time
    forecast (see terminal_rules + docs/research/02 §2.7)."""
    if len(w) != 5:
        return RuleResult("terminal", Status.NA, f"need 5 legs, got {len(w)}")
    w1, w2, w3, w4, w5 = w
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    if not overlap:
        # NA, not FAIL: absence of a terminal is normal for a directional impulse
        return RuleResult("terminal impulsion", Status.NA,
                          "no wave4/wave1 overlap -> directional impulse (not a terminal)")
    contracting = (w5.length < w3.length < w1.length)
    w2_retr = w2.retr(w1)
    limit_note = "" if w2_retr <= 0.618 + 1e-9 else " (>61.8% - atypical for a terminal)"
    return RuleResult("terminal impulsion", Status.PASS,
                      "w4/w1 overlap; " + ("contracting (textbook)" if contracting
                      else "expanding/irregular (rarer)") +
                      f"; wave2 retraces {w2_retr:.0%} of wave1{limit_note}"
                      " -> bias: fast full retrace toward origin")


def terminal_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """Granular terminal-impulsion checks (docs/research/02 §4 Task 5): overlap,
    wave-2 <= 61.8% retrace limit, wedge shape (contracting/expanding), and a REF
    that each of the 5 legs should be corrective (:3) — checkable once monowave
    structure labels exist (label_monowaves)."""
    if len(w) != 5:
        return [RuleResult("terminal arity", Status.NA, f"need 5 legs, got {len(w)}")]
    w1, w2, w3, w4, w5 = w
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    res = [RuleResult("terminal: w4/w1 overlap", Status.PASS if overlap else Status.NA,
                      "overlap present (terminal/diagonal)" if overlap
                      else "no overlap -> directional impulse, not a terminal")]
    if not overlap:
        return res
    w2_retr = w2.retr(w1)
    res.append(RuleResult("terminal: wave2 <= 61.8% of wave1",
                          Status.PASS if w2_retr <= 0.618 + 1e-9 else Status.WARN,
                          f"wave2 retraces {w2_retr:.0%} of wave1"))
    contracting = (w5.length < w3.length < w1.length)
    expanding = (w5.length > w3.length > w1.length)
    shape = ("contracting (textbook)" if contracting
             else "expanding (rarer)" if expanding else "irregular")
    res.append(RuleResult("terminal: wedge shape",
                          Status.PASS if contracting else Status.WARN, shape))
    res.append(RuleResult("terminal: sub-waves each corrective (:3)", Status.REF,
                          "each of the 5 legs should be a three (verify via monowave labels)"))
    return res


def terminal_retrace_window(build_days: float, top_t: float, fracs=(0.25, 0.33, 0.5)) -> dict:
    return {f: datetime.fromtimestamp(top_t + build_days * f * 86400, tz=timezone.utc)
            .strftime("%Y-%m-%d") for f in fracs}
