"""
rules.triangles — triangle classifiers & thrust projection (moved verbatim
from wavelib/rules.py §C/§F).
"""
from __future__ import annotations
from typing import Sequence

from .result import RuleResult, Status, Wave, _within

BARRIER_FLAT_TOL = 0.03  # one triangle boundary "flat" within 3% of its mean price

def _classify_triangle(w: Sequence[Wave]) -> RuleResult:
    """5-leg a-b-c-d-e triangle subtype by FULL leg-length progression.

    Contracting: a>b>c>d>e; expanding: a<b<c<d<e; barrier: one boundary ~flat.
    (docs/research/01 §4 Task 3.) Wave E commonly over/undershoots the a-c line.
    """
    lens = [seg.length for seg in w]
    contracting = all(lens[i] > lens[i + 1] for i in range(4))   # a>b>c>d>e
    expanding = all(lens[i] < lens[i + 1] for i in range(4))     # a<b<c<d<e
    # boundaries: side1 = ends of a,c,e ; side2 = ends of b,d
    side1 = [w[0].end.price, w[2].end.price, w[4].end.price]
    side2 = [w[1].end.price, w[3].end.price]

    def _flat(vals):
        m = sum(vals) / len(vals)
        return bool(m) and (max(vals) - min(vals)) <= BARRIER_FLAT_TOL * abs(m)

    barrier = _flat(side1) or _flat(side2)
    if contracting:
        kind = "CONTRACTING TRIANGLE (most common)"
    elif expanding:
        kind = "EXPANDING TRIANGLE"
    elif barrier:
        kind = "BARRIER/RUNNING TRIANGLE (one boundary flat)"
    else:
        return RuleResult("correction = TRIANGLE? irregular legs (3-3-3-3-3)", Status.WARN,
                          f"leg lengths {[round(x, 1) for x in lens]} not monotonic and no flat "
                          "boundary -> verify count / possible complex correction")
    return RuleResult(f"correction = {kind} (3-3-3-3-3)", Status.PASS,
                      f"leg lengths {[round(x, 1) for x in lens]}; appears in wave-4/B/X, "
                      "precedes the final thrust; wave E may over/undershoot the a-c line (REF)")


def triangle_thrust(widest_leg: float, base: float, direction: int = 1) -> dict:
    """Project the post-triangle thrust: 75%-125% of the widest leg from the
    breakout base. direction=+1 up, -1 down. (docs/research/01 §4 Task 3.)"""
    return {"min": round(base + direction * 0.75 * widest_leg, 2),
            "max": round(base + direction * 1.25 * widest_leg, 2)}



def is_running_triangle(legs: Sequence[Wave]) -> RuleResult:
    """EWF running triangle (docs/research/deep/09): a (usually contracting)
    triangle whose wave B terminates BEYOND the wave-A origin — it makes a new
    extreme that mimics the start of a fresh impulse, so it is the highest
    mislabel-risk pattern. Flag it explicitly. PASS = running; NA = ordinary."""
    if len(legs) != 5:
        return RuleResult("running triangle", Status.NA, f"need 5 legs, got {len(legs)}")
    a, b = legs[0], legs[1]
    origin = a.start.price
    a_down = a.end.price < a.start.price
    b_beyond = (b.end.price > origin) if a_down else (b.end.price < origin)
    return RuleResult("running triangle", Status.PASS if b_beyond else Status.NA,
                      f"wave B {'BREAKS BEYOND' if b_beyond else 'stays within'} the "
                      f"wave-A origin {origin:.2f}" +
                      (" -> looks like a new impulse (mislabel risk)" if b_beyond else ""))


def is_neutral_triangle(legs: Sequence[Wave]) -> RuleResult:
    """NeoWave neutral triangle (docs/research/02 §4 Task 6): 5 legs where leg C
    (index 2) is the longest; legs A and E tend to equality (each >= 38.2% of C);
    C <= ~261.8% of A. Distinct from a contracting/expanding triangle."""
    if len(legs) != 5:
        return RuleResult("neutral triangle arity", Status.NA, f"need 5 legs, got {len(legs)}")
    lens = [x.length for x in legs]
    A, C, E = lens[0], lens[2], lens[4]
    c_longest = C == max(lens)
    a_e_equal = _within(A, E, 0.7, 1.43)             # A ~ E (within ~1.43x)
    a_e_min = (A >= 0.382 * C) and (E >= 0.382 * C)
    c_limit = C <= 2.618 * A + 1e-9
    ok = c_longest and a_e_equal and a_e_min and c_limit
    return RuleResult("NeoWave neutral triangle", Status.PASS if ok else Status.WARN,
                      f"C longest={c_longest}; A~E={a_e_equal}; A,E>=38.2%C={a_e_min}; "
                      f"C<=261.8%A={c_limit}")


def x_wave_check(prior_correction: Wave, x: Wave) -> RuleResult:
    """x-wave connecting two corrections (docs/research/02 §4 Task 9). Rule:
    a small x-wave retraces < 61.8% of the prior correction (PASS); 61.8-100% is a
    large x-wave (WARN); > 100% is not an x-wave -> structural error (FAIL)."""
    rr = x.length / prior_correction.length if prior_correction.length else float("nan")
    if rr < 0.618:
        st, msg = Status.PASS, f"x = {rr:.0%} of prior correction (small x-wave)"
    elif rr <= 1.0:
        st, msg = Status.WARN, f"x = {rr:.0%} of prior correction (large x-wave)"
    elif rr >= 1.618:
        # RULESET SI.3 large-X regime (SOW Day-2 p.8): the "connector" is
        # oversized -> the correction is of a larger degree than assumed
        st, msg = Status.REF, (f"x = {rr:.0%} (>=161.8%) -> LARGE-X regime; "
                               "reassess degree and relabel")
    else:
        st, msg = Status.FAIL, f"x = {rr:.0%} (>100%) -> not an x-wave; structural error"
    return RuleResult("NeoWave x-wave", st, msg)


def triangle_subrules(legs: "Sequence[Wave]") -> "list[RuleResult]":
    """SOW/reference triangle sub-rules (RULESET §I.2): E smallest leg;
    >=3 of the legs retrace >50% of the preceding leg. (The B-D cleanliness
    check lives in neowave.bd_line_test, which owns line geometry.)"""
    if len(legs) != 5:
        return [RuleResult("triangle sub-rules", Status.NA,
                           f"need 5 legs, got {len(legs)}")]
    lens = [x.length for x in legs]
    e_smallest = lens[4] == min(lens)
    out = [RuleResult("triangle: E smallest leg",
                      Status.PASS if e_smallest else Status.WARN,
                      f"leg lengths {[round(x, 2) for x in lens]}")]
    deep = sum(1 for i in range(1, 5)
               if lens[i - 1] and lens[i] / lens[i - 1] > 0.5)
    out.append(RuleResult("triangle: >=3 legs retrace >50% of prior",
                          Status.PASS if deep >= 3 else Status.WARN,
                          f"{deep}/4 legs retrace >50% of the preceding leg"))
    return out


def is_extracting_triangle(legs: "Sequence[Wave]") -> RuleResult:
    """NeoWave extracting triangle (RULESET §I.2; SOW Day-2 p.5): alternating
    contraction/expansion with e < c < a AND d > b. PASS = extracting;
    NA = not this shape."""
    if len(legs) != 5:
        return RuleResult("extracting triangle", Status.NA,
                          f"need 5 legs, got {len(legs)}")
    a, b, c, d, e = (x.length for x in legs)
    ok = e < c < a and d > b
    return RuleResult("extracting triangle",
                      Status.PASS if ok else Status.NA,
                      f"e<c<a={'yes' if e < c < a else 'no'} "
                      f"(e={e:.2f}, c={c:.2f}, a={a:.2f}); "
                      f"d>b={'yes' if d > b else 'no'} (d={d:.2f}, b={b:.2f})"
                      + ("" if ok else " -> not extracting"))
