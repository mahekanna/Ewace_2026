"""
ew_neowave_rules.py
===================
A comprehensive, dependency-free RULE ENGINE for classic Elliott Wave and
NeoWave (Glenn Neely). Encodes the rule sets as machine-checkable validators
plus reference descriptors for the subjective/visual rules.

Sections
  A. Data structures (Pivot, Wave, WaveSet)
  B. Elliott — impulse: 3 hard rules + guidelines
  C. Elliott — corrections: zigzag / flat / triangle / combination classifiers
  D. Elliott — diagonals: leading & ending
  E. NeoWave — Similarity & Balance, Proportion, retracement logic, channeling
  F. NeoWave — terminal impulsions + complex corrections (diametric / symmetrical
     / neutral & extracting triangles) + x-wave logic
  G. validate_impulse() / validate_correction() engines + report
  H. demo (AVGO terminal, MRVL impulse)

Pure stdlib, Python 3.9+. Educational; not investment advice.

HONESTY NOTE: NeoWave's full construction procedure (Neely, ~600 pp) includes
fine micro-thresholds this module approximates. Rules marked REF are descriptive
references requiring discretionary confirmation; rules marked CHECK are computed.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence

# =========================================================================== #
# A. DATA STRUCTURES — canonical home is ewave.rules.result (single owner of
# Pivot/Wave/Degree/Status/RuleResult; docs/ARCHITECTURE.md D7). This module
# re-exports them so every legacy `from wavelib.rules import Pivot` keeps
# working AND is the same class object as the ewave one.
# =========================================================================== #
try:
    from ewave.rules.result import (PHI, INV_PHI, Degree, Pivot, Wave, Status,
                                    RuleResult, _ok)
except ImportError:                      # bare checkout / script execution
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(
        _os.path.abspath(__file__))), "src"))
    from ewave.rules.result import (PHI, INV_PHI, Degree, Pivot, Wave, Status,
                                    RuleResult, _ok)



# =========================================================================== #
# B. ELLIOTT — IMPULSE RULES
# =========================================================================== #
# An impulse has waves [1,2,3,4,5] passed as 5 Wave objects (motive direction).

def elliott_hard_rules(w: Sequence[Wave]) -> list[RuleResult]:
    """The 3 inviolable Elliott rules. Any FAIL => the labeling is wrong."""
    if len(w) != 5:
        return [RuleResult("impulse arity", Status.NA, f"need 5 waves, got {len(w)}")]
    w1, w2, w3, w4, w5 = w
    up = w1.up
    r = []
    # Rule 1: wave 2 never retraces > 100% of wave 1
    c1 = (w2.end.price > w1.start.price) if up else (w2.end.price < w1.start.price)
    r.append(RuleResult("R1 wave2 <100% of wave1", _ok(c1),
                        f"wave2 end {w2.end.price} vs wave1 origin {w1.start.price}"))
    # Rule 2: wave 3 never the shortest of 1,3,5
    c2 = not (w3.length < w1.length and w3.length < w5.length)
    r.append(RuleResult("R2 wave3 not shortest", _ok(c2),
                        f"len 1/3/5 = {w1.length:.1f}/{w3.length:.1f}/{w5.length:.1f}"))
    # Rule 3: wave 4 never enters wave 1 price territory (non-diagonal)
    c3 = (w4.end.price > w1.end.price) if up else (w4.end.price < w1.end.price)
    r.append(RuleResult("R3 wave4/wave1 no overlap", _ok(c3),
                        f"wave4 extreme {w4.end.price} vs wave1 top {w1.end.price}"
                        + ("" if c3 else "  (only legal if DIAGONAL)")))
    return r


def elliott_guidelines(w: Sequence[Wave]) -> list[RuleResult]:
    """Probabilistic guidelines (not inviolable)."""
    if len(w) != 5:
        return [RuleResult("guidelines", Status.NA, "need 5 waves")]
    w1, w2, w3, w4, w5 = w
    r = []
    # Extension: one of 1/3/5 markedly longest
    lens = {1: w1.length, 3: w3.length, 5: w5.length}
    ext = max(lens, key=lens.get)
    second = sorted(lens.values())[-2]
    ext_ratio = lens[ext] / second if second else float("nan")
    if ext_ratio >= 1.618:
        ext_st, ext_msg = Status.PASS, f"wave {ext} extends {ext_ratio:.2f}x (>=1.618 ok)"
    elif ext_ratio >= 1.3:
        ext_st, ext_msg = Status.WARN, f"wave {ext} mildly longer {ext_ratio:.2f}x (1.3-1.618)"
    else:
        ext_st, ext_msg = Status.WARN, f"no clear extension ({ext_ratio:.2f}x; all ~equal)"
    r.append(RuleResult("G extension present", ext_st, ext_msg))
    # Equality: the two non-extended motive waves tend equal
    others = [k for k in lens if k != ext]
    a, b = lens[others[0]], lens[others[1]]
    eqrat = min(a, b) / max(a, b)
    r.append(RuleResult("G equality of non-ext motive", Status.PASS if eqrat > 0.6 else Status.WARN,
                        f"waves {others}: ratio {eqrat:.2f} (≈1.0 or 0.618 ideal)"))
    # Alternation: wave2 vs wave4 depth differs
    d2 = w2.retr(w1); d4 = w4.retr(w3)
    altern = abs(d2 - d4) > 0.15
    r.append(RuleResult("G alternation (2 vs 4 depth)", Status.PASS if altern else Status.WARN,
                        f"wave2 {d2:.0%} of w1 vs wave4 {d4:.0%} of w3 "
                        + ("(alternate ✓)" if altern else "(similar — weak alternation)")))
    # Typical depths
    r.append(RuleResult("G wave2 depth 0.5-0.618", Status.PASS if 0.45 <= d2 <= 0.75 else Status.WARN,
                        f"{d2:.0%} of wave1"))
    r.append(RuleResult("G wave4 depth 0.236-0.382", Status.PASS if 0.18 <= d4 <= 0.45 else Status.WARN,
                        f"{d4:.0%} of wave3"))
    # Wave3 fib to wave1 (canonical 1.618-3.618 band; tiered WARN outside it)
    r3 = w3.length / w1.length if w1.length else float("nan")
    if 1.618 <= r3 <= 3.618:
        r3_st, r3_msg = Status.PASS, f"wave3 = {r3:.2f}x wave1 (1.618-3.618 ok)"
    elif 1.3 <= r3 < 1.618:
        r3_st, r3_msg = Status.WARN, f"wave3 = {r3:.2f}x wave1 (short of 1.618)"
    elif r3 > 3.618:
        r3_st, r3_msg = Status.WARN, f"wave3 = {r3:.2f}x wave1 (>3.618 - check degree shift)"
    else:
        r3_st, r3_msg = Status.WARN, f"wave3 = {r3:.2f}x wave1 (<1.3 - weak third)"
    r.append(RuleResult("G wave3 ~1.618-3.618x wave1", r3_st, r3_msg))
    return r


def project_wave5(w1_len, w3_len, w4_end, prior_high) -> dict:
    """Wave-5 targets: equality (w5=w1), 0.618xw3, extended fifth (1.618xw1),
    and short fifth (0.382xw3). (docs/research/01 §4 Task 5.)"""
    eq = round(w4_end + w1_len, 2)
    ext = round(w4_end + INV_PHI * w3_len, 2)
    ext_w1 = round(w4_end + PHI * w1_len, 2)        # extended fifth
    short = round(w4_end + 0.382 * w3_len, 2)       # short fifth
    trunc = eq < prior_high * 1.03
    return {"w5=w1": eq, "w5=0.618*w3": ext, "w5=1.618*w1": ext_w1,
            "w5=0.382*w3": short, "prior_high": prior_high, "truncation_risk": trunc}


# =========================================================================== #
# C. ELLIOTT — CORRECTION CLASSIFIERS
# =========================================================================== #
# Corrections passed as 3 waves [A,B,C] (zigzag/flat) or 5 [a,b,c,d,e] (triangle).

# Canonical correction thresholds (Frost & Prechter; docs/research/01_elliott_wave.md §4 Task 1)
ZIGZAG_B_MAX = 0.618    # zigzag: B retraces <= 61.8% of A (sharp)
REG_FLAT_B_MAX = 1.00   # regular flat: B within (0.618, 1.00]; expanded/running: B > 1.00
BARRIER_FLAT_TOL = 0.03  # one triangle boundary "flat" within 3% of its mean price


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


# =========================================================================== #
# D. ELLIOTT — DIAGONALS
# =========================================================================== #
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


# =========================================================================== #
# E. NEOWAVE — CORE LOGIC RULES
# =========================================================================== #
def _within(a, b, lo, hi) -> bool:
    r = a / b if b else float("nan")
    return lo <= r <= hi


def _group_similar(vals, lo=1/3, hi=3.0) -> bool:
    return all(_within(vals[i], vals[i + 1], lo, hi) for i in range(len(vals) - 1)) if len(vals) > 1 else True


def similarity_and_balance(a: Wave, b: Wave, lo=1/3, hi=3.0, context: str = "") -> RuleResult:
    """Adjacent corrective waves must relate in price AND time within lo..hi.
    Price is compared in LOG magnitude (correct on large-range instruments)."""
    pr = a.log_length / b.log_length if b.log_length else float("nan")
    tr = a.days / b.days if b.days else float("nan")
    pok, tok = (lo <= pr <= hi), (lo <= tr <= hi)
    st = Status.PASS if (pok and tok) else Status.WARN
    label = "NeoWave Similarity & Balance" + (f" ({context})" if context else "")
    return RuleResult(label, st,
                      f"price {pr:.2f}x (ok={pok}), time {tr:.2f}x (ok={tok})  band [{lo:.2f},{hi:.1f}]")


def rule_of_proportion(parent: Wave, child: Wave, lo=1/3, hi=3.0) -> RuleResult:
    """A subwave should be proportional to its same-degree neighbours / parent context."""
    rr = child.length / parent.length if parent.length else float("nan")
    return RuleResult("NeoWave Proportion", Status.PASS if rr <= 1.0 else Status.WARN,
                      f"child {rr:.2f}× of parent leg")


def retracement_logic(retr: float) -> RuleResult:
    """Depth of the CURRENT move => identity of the PRIOR leg (Neely heuristics)."""
    if retr < 0.382:
        m = "prior=extended 3rd; you're in a 4th"
    elif retr < 0.618:
        m = "prior=1st/5th; current=2nd/4th (normal)"
    elif retr <= 1.0:
        m = "deep: prior=a-wave/1st; current=2nd/B/X (sharp)"
    else:
        m = ">100%: NOT a retracement -> trend change / larger structure"
    return RuleResult("NeoWave retracement logic", Status.REF, f"{retr:.0%} -> {m}")


def line_value(p1: Pivot, p2: Pivot, t_query: float) -> float:
    """Value of the trendline through p1,p2 at time t_query (linear in time)."""
    if (p2.t - p1.t) == 0:
        return float("nan")
    m = (p2.price - p1.price) / (p2.t - p1.t)
    return p1.price + m * (t_query - p1.t)


def two_four_test(w2: Pivot, w4: Pivot, current_t: float, current_price: float,
                  uptrend: bool = True) -> RuleResult:
    """
    NeoWave 2-4 trendline (CHECK, not REF). In an impulse, the motive sequence
    is confirmed COMPLETE only when price decisively breaks the 2-4 line.
    Returns the projected line value and whether it has broken.
    """
    lv = line_value(w2, w4, current_t)
    broken = (current_price < lv) if uptrend else (current_price > lv)
    st = Status.WARN if broken else Status.PASS
    return RuleResult("Channel: 2-4 trendline", st,
                      f"line ~{lv:.1f} now; price {current_price:.1f} "
                      + ("BROKEN -> impulse complete confirmed" if broken
                         else "holding -> impulse not yet confirmed complete"))


def two_four_confirmation(w5: Wave, w2: Pivot, w4: Pivot, current_t: float,
                          current_price: float, uptrend: bool = True) -> list[RuleResult]:
    """
    Two-stage impulse-completion confirmation (docs/research/02 §4 Task 4).

    Stage 1: price has broken the 2-4 line AND did so in LESS time than wave 5 took
             to build (a fast break confirms completion; a slow one is suspect).
    Stage 2: the entire wave-5 price range has been retraced to its origin, within
             <= wave-5 build time.
    CAUSAL: uses only observed data (current_t, current_price).
    """
    lv = line_value(w2, w4, current_t)
    broke = (current_price < lv) if uptrend else (current_price > lv)
    elapsed = (current_t - w5.end.t) / 86400.0
    w5_days = w5.days
    fast = elapsed <= w5_days
    stage1 = RuleResult("2-4 confirmation Stage 1 (break faster than w5)",
                        Status.PASS if (broke and fast) else Status.WARN,
                        f"2-4 line ~{lv:.1f}, price {current_price:.1f}, broken={broke}; "
                        f"elapsed {elapsed:.0f}d vs w5 {w5_days:.0f}d -> fast={fast}")
    w5_origin = w5.start.price
    retraced = (current_price <= w5_origin) if uptrend else (current_price >= w5_origin)
    stage2 = RuleResult("2-4 confirmation Stage 2 (w5 fully retraced)",
                        Status.PASS if (retraced and fast) else Status.WARN,
                        f"w5 origin {w5_origin:.1f}; price {current_price:.1f}; "
                        f"retraced={retraced}; within w5 time={fast}")
    return [stage1, stage2]


@dataclass
class CompletionSignal:
    """Result of the per-bar 2-4 completion monitor (GAP-3).

    stage: 0 = not yet confirmed (pending), 1 = 2-4 line broken faster than wave 5
    built (impulse complete confirmed), 2 = wave 5 ALSO fully retraced within its
    build time (strong confirmation / trend change). `confirmed` is True iff stage 2.
    `at_t`/`bars_elapsed` mark the FIRST bar that reached stage 1.
    """
    confirmed: bool
    stage: int
    at_t: Optional[float]
    bars_elapsed: Optional[int]
    detail: str


def confirm_completion(w5: Wave, w2: Pivot, w4: Pivot,
                       forward_bars: Sequence[tuple],
                       uptrend: bool = True) -> CompletionSignal:
    """Post-constructive, stateful per-bar 2-4 completion monitor (GAP-3, doc 11).

    After an impulse has been CONSTRUCTED, walk `forward_bars` (each
    `(t,o,h,l,c[,v])`, strictly AFTER `w5.end`) one bar at a time and apply the
    two-stage 2-4 confirmation (`two_four_confirmation`) CAUSALLY at each bar's
    own time/close. Returns the FIRST bar that reaches stage 1 (a 2-4 break faster
    than wave 5's build), upgrading to stage 2 if wave 5 is later fully retraced in
    time — or a `pending` signal if neither fires inside the window.

    This is the real-time companion to the static `two_four_confirmation`: the
    constructor proposes a complete impulse, this monitor *waits for the market to
    confirm it* bar by bar without any look-ahead.
    """
    first_break: Optional[tuple] = None
    best_stage = 0
    detail = "pending: 2-4 line not broken faster than wave 5 in this window"
    for i, bar in enumerate(forward_bars):
        t, price = bar[0], bar[4]
        s1, s2 = two_four_confirmation(w5, w2, w4, t, price, uptrend)
        st = 0
        if s1.status is Status.PASS:
            st = 2 if s2.status is Status.PASS else 1
        if st >= 1 and first_break is None:
            first_break = (i, t)
        if st > best_stage:
            best_stage = st
            detail = (f"bar {i} (t={int(t)}): stage {st} -> "
                      + (s2.detail if st == 2 else s1.detail))
        if best_stage == 2:
            break
    if first_break is None:
        return CompletionSignal(False, 0, None, None, detail)
    idx, t0 = first_break
    return CompletionSignal(best_stage == 2, best_stage, t0, idx, detail)


def throwover_test(w1_top: Pivot, w3_top: Pivot, w5_peak: float,
                   peak_t: float, uptrend: bool = True) -> RuleResult:
    """
    Compare the wave-5 peak to the 1-3 upper channel projection.
      peak ABOVE line  -> THROW-OVER (blow-off exhaustion)
      peak SHORT of line-> weak/truncated fifth (also exhaustion, opposite flavour)
    """
    lv = line_value(w1_top, w3_top, peak_t)
    over = (w5_peak > lv) if uptrend else (w5_peak < lv)
    flavour = "THROW-OVER (blow-off)" if over else "FELL SHORT (weak/truncated 5th)"
    return RuleResult("Channel: 1-3 upper / wave-5", Status.REF,
                      f"1-3 line ~{lv:.1f} at peak; wave5 {w5_peak:.1f} -> {flavour}")


def base_channel_test(w0_origin: Pivot, w2_end: Pivot, w1_top: Pivot,
                      current_t: float, current_price: float,
                      uptrend: bool = True) -> RuleResult:
    """
    NeoWave/Elliott base (0-2) channel. Lower line runs through the wave-0 origin
    and the wave-2 end; the upper parallel runs through the wave-1 top. Price
    holding above the lower line during wave 3 confirms the motive count; a break
    below it during wave 4 is an early warning. (docs/research/01 §4 Task 6.)

    CAUSAL: w0/w1/w2 are already complete at the time of the check.
    """
    lv = line_value(w0_origin, w2_end, current_t)
    holding = (current_price >= lv) if uptrend else (current_price <= lv)
    st = Status.PASS if holding else Status.WARN
    return RuleResult("Channel: 0-2 base line", st,
                      f"0-2 line ~{lv:.1f} now; price {current_price:.1f} "
                      + ("holding above (motive intact)" if holding
                         else "broke below (wave-4 warning)"))


# =========================================================================== #
# F. NEOWAVE — TERMINALS & COMPLEX CORRECTIONS
# =========================================================================== #
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
    else:
        st, msg = Status.FAIL, f"x = {rr:.0%} (>100%) -> not an x-wave; structural error"
    return RuleResult("NeoWave x-wave", st, msg)


# =========================================================================== #
# F2. NEOWAVE — BOTTOM-UP CONSTRUCTION (monowave -> polywave)
# =========================================================================== #
# Structure labels (Neely): ':5'/':3' is the load-bearing motive/corrective core
# (docs/research/02 §2.1); refinements (:F3/:c3/:L3/:L5/:s5/:sL3) need higher-
# degree context and are left to future work. This module assigns the :5/:3 core
# plus the retracement-rule number (§2.5), flagging edge monowaves provisional.
_RETRACE_BREAKS = (0.382, 0.618, 1.0, 1.618, 2.618)  # Neely's 7-rule breakpoints


def _retracement_rule(m2_over_m1: float) -> int:
    """Neely retracement-rule number (1..7) for the m2/m1 ratio (docs/research/02 §2.5)."""
    r = m2_over_m1
    if r < 0.382:
        return 1
    if r < 0.618:
        return 2
    if r <= 1.0:
        return 3          # rules 3/4 share the 61.8-100% band (overlap variant)
    if r <= 1.618:
        return 5
    if r <= 2.618:
        return 6
    return 7


def label_monowaves(pivots: Sequence[Pivot]) -> list[tuple[Wave, str]]:
    """
    Assign each monowave (between consecutive pivots) a NeoWave structure label.

    The label combines the :5/:3 core (motive vs corrective, from m1 vs the prior
    monowave m0 in price AND time) with the seven-retracement-rule number (from how
    the next monowave m2 retraces m1). Edge monowaves (no full m0/m2 context) get
    ':?' (provisional). Returns list of (Wave, label). (docs/research/02 §4 Task 1.)

    CAUSAL-ONLY: m1's label uses m0 and m2, both already formed by the time m1 is
    labelled; the final monowave is provisional until its successor confirms.
    """
    pivots = list(pivots)
    waves = [Wave(pivots[i], pivots[i + 1]) for i in range(len(pivots) - 1)]
    out: list[tuple[Wave, str]] = []
    n = len(waves)
    for i, m1 in enumerate(waves):
        m0 = waves[i - 1] if i - 1 >= 0 else None
        m2 = waves[i + 1] if i + 1 < n else None
        if m0 is None or m2 is None:
            out.append((m1, ":?"))           # edge: provisional, no full context
            continue
        # GAP-1: the core label is the PRIMARY candidate from Neely's seven-rule
        # test (with the Rule-3-vs-4 overlap check), not the old retr>1 -> :5
        # heuristic that over-labelled motive. monowave_candidates is causal
        # (uses only m0/m1/m2, all formed by the time m1 is labelled).
        core = monowave_candidates(m0, m1, m2)[0]
        rule = _retracement_rule(m2.length / m1.length if m1.length else float("nan"))
        out.append((m1, f"{core}(R{rule})"))
    return out


def monowave_candidates(m0: "Wave", m1: "Wave", m2: "Wave") -> list[str]:
    """Neely's seven-rule CANDIDATE structure labels for monowave m1 (chained:
    m1.start == m0.end, m2.start == m1.end). Returns a LIST because 30-40% of
    monowaves are genuinely ambiguous; the primary candidate is first.

    Rule 3 vs Rule 4 are separated by whether m2 retraces BACK INTO m0's price
    territory (the overlap test) — without this the 0.618-1.0 band over-labels
    motive (docs/research/deep/11 GAP-1). Condition d uses the m0/m1 ratio."""
    r = m2.length / m1.length if m1.length else float("nan")     # m2 retraces m1
    m0r = m0.length / m1.length if m1.length else float("nan")   # m0 vs m1
    if r != r:
        return [":?"]
    m0lo, m0hi = min(m0.start.price, m0.end.price), max(m0.start.price, m0.end.price)
    overlaps_m0 = m0lo <= m2.end.price <= m0hi                   # Rule 3 vs Rule 4
    if r < 0.382:                       # Rule 1: m1 a strong/extended motive
        cands = [":5"]
    elif r < 0.618:                     # Rule 2: 1st or 5th (motive)
        cands = [":5", ":3"]
    elif r <= 1.0:                      # Rule 3 (no overlap) vs Rule 4 (overlap)
        cands = [":3", ":c3"] if overlaps_m0 else [":3", ":5"]
    elif r <= 1.618:                    # Rule 5: m2 not a retrace -> m1 ended a move
        cands = [":3", ":L5"]
    elif r <= 2.618:                    # Rule 6: strong reversal
        cands = [":3", ":sL3"]
    else:                              # Rule 7: extreme -> last segment / x-wave
        cands = [":sL3", ":x"]
    if m0r > 2.618 and ":sL3" not in cands:     # condition d
        cands.append(":sL3")
    return cands


def group_polywaves(labelled: Sequence[tuple]) -> list[list[tuple]]:
    """
    Slide windows of 3 and 5 over labelled monowaves; keep those that form a valid
    standard correction (3 legs) or pass the impulse hard rules (5 legs) AND clear
    Similarity & Balance on their corrective pair(s). Returns candidate groups
    (overlap allowed). Depends on label_monowaves. (docs/research/02 §4 Task 2.)
    """
    items = list(labelled)
    waves = [w for (w, _lab) in items]
    candidates: list[list[tuple]] = []
    for size in (3, 5):
        for start in range(0, len(waves) - size + 1):
            grp = waves[start:start + size]
            if size == 3:
                rr = classify_correction(grp)
                sb = similarity_and_balance(grp[0], grp[2])           # A vs C
                if rr.status is Status.PASS and sb.status in (Status.PASS, Status.WARN):
                    candidates.append(items[start:start + size])
            else:  # size == 5: a polywave impulse
                hard = elliott_hard_rules(grp)
                if not any(h.status is Status.FAIL for h in hard):
                    candidates.append(items[start:start + size])
    return candidates


# =========================================================================== #
# G. VALIDATION ENGINES
# =========================================================================== #
def validate_impulse(w: Sequence[Wave], diagonal: bool = False) -> list[RuleResult]:
    res = []
    if diagonal:
        res += diagonal_rules(w)
    else:
        res += elliott_hard_rules(w)
    res += elliott_guidelines(w)
    # NeoWave overlays
    if len(w) == 5:
        res.append(similarity_and_balance(w[1], w[3], context="wave2 vs wave4"))
        res.append(is_terminal(w))
    return res


def validate_correction(w: Sequence[Wave]) -> list[RuleResult]:
    res = [classify_correction(w)]
    if len(w) >= 2:
        res.append(retracement_logic(w[1].retr(w[0])))
    if len(w) == 3:
        res.append(similarity_and_balance(w[0], w[2], context="A vs C"))
    if len(w) == 5:
        for i in range(4):                                   # triangle adjacent legs
            res.append(similarity_and_balance(w[i], w[i + 1], context=f"leg{i+1} vs leg{i+2}"))
    if len(w) in (5, 7) or len(w) > 7:
        res.append(classify_complex_correction(w))
    return res


def report(results: list[RuleResult], title="") -> str:
    head = f"\n{'='*64}\n{title}\n{'='*64}" if title else ""
    body = "\n".join(str(x) for x in results)
    fails = sum(1 for x in results if x.status is Status.FAIL)
    verdict = "VALID (no hard-rule failures)" if fails == 0 else f"INVALID — {fails} hard failure(s)"
    return f"{head}\n{body}\n  -> {verdict}"


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
