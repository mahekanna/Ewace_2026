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
from enum import Enum
from typing import Optional, Sequence

PHI = 1.6180339887
INV_PHI = 0.6180339887


# =========================================================================== #
# A. DATA STRUCTURES
# =========================================================================== #
class Degree(Enum):
    """
    Elliott wave degree hierarchy (Frost & Prechter), largest -> smallest.

    Numeric values rank the degrees (higher = larger degree), so degrees compare
    by `.value`. The field is OPTIONAL metadata on Pivot/Wave: `degree is None`
    means "not yet assigned" — the bottom-up Neely constructor (roadmap Phase 2)
    will populate it. See docs/research/01_elliott_wave.md §2.5.
    """
    GRAND_SUPERCYCLE = 9
    SUPERCYCLE = 8
    CYCLE = 7
    PRIMARY = 6
    INTERMEDIATE = 5
    MINOR = 4
    MINUTE = 3
    MINUETTE = 2
    SUBMINUETTE = 1

    @property
    def abbr(self) -> str:
        """Short notation label for the degree."""
        return {
            "GRAND_SUPERCYCLE": "GSC", "SUPERCYCLE": "SC", "CYCLE": "C",
            "PRIMARY": "P", "INTERMEDIATE": "I", "MINOR": "Mn",
            "MINUTE": "mn", "MINUETTE": "mu", "SUBMINUETTE": "smu",
        }[self.name]

    def finer(self) -> Optional["Degree"]:
        """The next-smaller degree, or None at SUBMINUETTE."""
        return Degree(self.value - 1) if self.value > 1 else None

    def coarser(self) -> Optional["Degree"]:
        """The next-larger degree, or None at GRAND_SUPERCYCLE."""
        return Degree(self.value + 1) if self.value < 9 else None


@dataclass
class Pivot:
    t: float
    price: float
    kind: str  # "H" or "L"
    # confirmed_t: bar time at which this pivot's reversal was CONFIRMED (causal
    # discipline — a pivot is only "known" once price reverses past the threshold).
    # None => provisional / still forming (e.g. the final extreme of a series).
    confirmed_t: Optional[float] = None
    degree: Optional["Degree"] = None  # optional wave-degree annotation

    @property
    def date(self) -> str:
        return datetime.fromtimestamp(self.t, tz=timezone.utc).strftime("%Y-%m-%d")

    @property
    def confirmed(self) -> bool:
        return self.confirmed_t is not None


@dataclass
class Wave:
    start: Pivot
    end: Pivot
    label: str = ""
    degree: Optional["Degree"] = None  # optional wave-degree annotation

    @property
    def length(self) -> float: return abs(self.end.price - self.start.price)
    @property
    def signed(self) -> float: return self.end.price - self.start.price
    @property
    def days(self) -> float: return (self.end.t - self.start.t) / 86400.0
    @property
    def up(self) -> bool: return self.end.price > self.start.price

    def retr(self, other: "Wave") -> float:
        return self.length / other.length if other.length else float("nan")
    retrace_of = retr


class Status(Enum):
    PASS = "PASS"; FAIL = "FAIL"; WARN = "WARN"; NA = "N/A"; REF = "REF"


@dataclass
class RuleResult:
    rule: str
    status: Status
    detail: str
    def __str__(self): return f"[{self.status.value:4}] {self.rule}: {self.detail}"


def _ok(c): return Status.PASS if c else Status.FAIL


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
    is_ext = lens[ext] > 1.3 * second
    r.append(RuleResult("G extension present", Status.PASS if is_ext else Status.WARN,
                        f"wave {ext} extends ({lens[ext]:.1f})" if is_ext
                        else "no clear extension (rare: all ~equal)"))
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
    # Wave3 fib to wave1
    r3 = w3.length / w1.length if w1.length else float("nan")
    r.append(RuleResult("G wave3 ≈1.618-2.618×wave1", Status.PASS if 1.3 <= r3 <= 3.0 else Status.WARN,
                        f"wave3 = {r3:.2f}×wave1"))
    return r


def project_wave5(w1_len, w3_len, w4_end, prior_high) -> dict:
    eq = round(w4_end + w1_len, 2)
    ext = round(w4_end + INV_PHI * w3_len, 2)
    trunc = eq < prior_high * 1.03
    return {"w5=w1": eq, "w5=0.618*w3": ext, "prior_high": prior_high,
            "truncation_risk": trunc}


# =========================================================================== #
# C. ELLIOTT — CORRECTION CLASSIFIERS
# =========================================================================== #
# Corrections passed as 3 waves [A,B,C] (zigzag/flat) or 5 [a,b,c,d,e] (triangle).

def classify_correction(w: Sequence[Wave]) -> RuleResult:
    """Identify ZIGZAG / FLAT(regular/expanded/running) / TRIANGLE / (else combo)."""
    if len(w) == 5:
        return _classify_triangle(w)
    if len(w) != 3:
        return RuleResult("correction", Status.REF,
                          f"{len(w)} legs -> likely COMBINATION (W-X-Y / W-X-Y-X-Z); "
                          "needs sub-structure to resolve")
    A, B, C = w
    b_retr = B.retr(A)         # how far B retraces A
    c_vs_a = C.length / A.length if A.length else float("nan")
    # ZIGZAG: sharp, B shallow (<= ~0.618 of A), C extends past A end
    if b_retr <= 0.62:
        return RuleResult("correction = ZIGZAG (5-3-5)", Status.PASS,
                          f"B retraces {b_retr:.0%} of A; C/A={c_vs_a:.2f}; sharp")
    # FLAT family: B deep (>= ~0.9 of A), sideways
    if b_retr >= 0.9:
        bp = (B.end.price - A.start.price)
        if b_retr > 1.0 and c_vs_a > 1.0:
            kind = "EXPANDED FLAT (B>A, C>A)"
        elif b_retr > 1.0 and c_vs_a <= 1.0:
            kind = "RUNNING FLAT (B>A, C truncated)"
        else:
            kind = "REGULAR FLAT (B≈A, C≈A)"
        return RuleResult(f"correction = {kind} (3-3-5)", Status.PASS,
                          f"B retraces {b_retr:.0%} of A; C/A={c_vs_a:.2f}; sideways")
    return RuleResult("correction = intermediate/complex", Status.WARN,
                      f"B retraces {b_retr:.0%} of A (between zigzag & flat) -> "
                      "check for double-three / flat variant")


def _classify_triangle(w: Sequence[Wave]) -> RuleResult:
    """5-leg a-b-c-d-e triangle subtype by extreme progression."""
    highs = [seg.end.price for seg in w]
    # contracting: each swing smaller; expanding: each larger
    lens = [seg.length for seg in w]
    contracting = lens[0] > lens[2] > lens[4]
    expanding = lens[0] < lens[2] < lens[4]
    if contracting:
        kind = "CONTRACTING TRIANGLE (most common)"
    elif expanding:
        kind = "EXPANDING TRIANGLE"
    else:
        kind = "BARRIER/RUNNING TRIANGLE (one boundary flat)"
    return RuleResult(f"correction = {kind} (3-3-3-3-3)", Status.PASS,
                      f"leg lengths {[round(x,1) for x in lens]}; appears in wave-4/B/X, "
                      "precedes the final thrust")


# =========================================================================== #
# D. ELLIOTT — DIAGONALS
# =========================================================================== #
def diagonal_rules(w: Sequence[Wave], position: str = "ending") -> list[RuleResult]:
    """
    Leading (wave 1/A) or ending (wave 5/C) diagonal. 5 legs, wedge.
    Defining trait: wave 4 OVERLAPS wave 1 (legal here, unlike a normal impulse).
    """
    if len(w) != 5:
        return [RuleResult("diagonal arity", Status.NA, f"need 5 legs, got {len(w)}")]
    w1, w2, w3, w4, w5 = w
    up = w1.up
    r = []
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    r.append(RuleResult(f"{position} diagonal: w4/w1 overlap", _ok(overlap),
                        f"wave4 {w4.end.price} vs wave1 {w1.end.price} "
                        + ("(overlap ✓ — diagonal)" if overlap else "(no overlap — not a diagonal)")))
    # diagonals follow wedge-sizing (contracting: w1>w3>w5), not the impulse
    # "wave 3 not shortest" HARD rule -> surface as WARN, not FAIL
    c2 = not (w3.length < w1.length and w3.length < w5.length)
    r.append(RuleResult("diagonal: wave3 vs wedge sizing", Status.PASS if c2 else Status.WARN,
                        f"1/3/5 = {w1.length:.1f}/{w3.length:.1f}/{w5.length:.1f}"
                        + ("" if c2 else "  (w3 shortest -> irregular for a wedge)")))
    # contracting wedge (ending diagonals usually contract)
    contracting = (w5.length < w3.length < w1.length)
    r.append(RuleResult("diagonal: contracting wedge", Status.PASS if contracting else Status.WARN,
                        "legs contract (textbook)" if contracting
                        else "legs expand/irregular (rarer; allowed but non-ideal)"))
    return r


# =========================================================================== #
# E. NEOWAVE — CORE LOGIC RULES
# =========================================================================== #
def similarity_and_balance(a: Wave, b: Wave, lo=1/3, hi=3.0) -> RuleResult:
    """Adjacent corrective waves must relate in price AND time within lo..hi."""
    pr = a.length / b.length if b.length else float("nan")
    tr = a.days / b.days if b.days else float("nan")
    pok, tok = (lo <= pr <= hi), (lo <= tr <= hi)
    st = Status.PASS if (pok and tok) else Status.WARN
    return RuleResult("NeoWave Similarity & Balance", st,
                      f"price {pr:.2f}× (ok={pok}), time {tr:.2f}× (ok={tok})  band [{lo:.2f},{hi:.1f}]")


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


# =========================================================================== #
# F. NEOWAVE — TERMINALS & COMPLEX CORRECTIONS
# =========================================================================== #
def is_terminal(w: Sequence[Wave]) -> RuleResult:
    """Terminal impulsion (NeoWave) / ending diagonal: 5 legs, w4/w1 overlap."""
    if len(w) != 5:
        return RuleResult("terminal", Status.NA, f"need 5 legs, got {len(w)}")
    w1, _, w3, w4, w5 = w
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    if not overlap:
        # NA, not FAIL: absence of a terminal is normal for a directional impulse
        return RuleResult("terminal impulsion", Status.NA,
                          "no wave4/wave1 overlap -> directional impulse (not a terminal)")
    contracting = (w5.length < w3.length < w1.length)
    return RuleResult("terminal impulsion", Status.PASS,
                      "w4/w1 overlap ✓; " + ("contracting (textbook)" if contracting
                      else "expanding/irregular (rarer)") +
                      " -> expect FAST FULL retrace to origin")


def terminal_retrace_window(build_days: float, top_t: float, fracs=(0.25, 0.33, 0.5)) -> dict:
    return {f: datetime.fromtimestamp(top_t + build_days * f * 86400, tz=timezone.utc)
            .strftime("%Y-%m-%d") for f in fracs}


def classify_complex_correction(legs: Sequence[Wave]) -> RuleResult:
    """
    NeoWave corrective zoo by leg count & symmetry:
      3  -> standard (zigzag/flat) — use classify_correction
      5  -> triangle
      7  -> diametric (a-g; symmetrical or bowtie) or symmetrical
      8+ -> multi-X complex combination
    """
    n = len(legs)
    if n == 3:
        return RuleResult("complex?", Status.NA, "3 legs -> standard correction (see classify_correction)")
    if n == 5:
        return _classify_triangle(legs)
    if n == 7:
        lens = [x.length for x in legs]
        mid = lens[3]
        symmetric = max(lens) / min(lens) < 1.6
        # diametric: expands to middle then contracts (bowtie) or vice-versa
        expands_then_contracts = lens[0] < mid > lens[-1]
        if symmetric:
            kind = "SYMMETRICAL (7 legs, similar size)"
        elif expands_then_contracts:
            kind = "DIAMETRIC — bowtie (expand→contract)"
        else:
            kind = "DIAMETRIC — diamond/other (a-b-c-d-e-f-g)"
        return RuleResult(f"NeoWave {kind}", Status.PASS,
                          f"7 corrective legs; lens {[round(x,1) for x in lens]}")
    return RuleResult("NeoWave complex combination", Status.REF,
                      f"{n} legs -> multi-X (W-X-Y-X-Z+) / neutral or extracting triangle; "
                      "resolve via sub-degree construction")


def x_wave_check(p1_end: Wave, x: Wave, p2_start: Wave) -> RuleResult:
    """x-waves join corrective patterns; typically < 61.8% of the prior pattern's depth."""
    return RuleResult("NeoWave x-wave", Status.REF,
                      "x-wave connects two corrections; should be smaller/sharper "
                      "than the patterns it joins")


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
        res.append(similarity_and_balance(w[1], w[3]))  # wave2 vs wave4
        res.append(is_terminal(w))
    return res


def validate_correction(w: Sequence[Wave]) -> list[RuleResult]:
    res = [classify_correction(w)]
    if len(w) >= 2:
        res.append(retracement_logic(w[1].retr(w[0])))
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
