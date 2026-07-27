"""
rules.elliott — classic Elliott impulse rules & guidelines (moved verbatim
from wavelib/rules.py §B). Hard rules R1/R2/R3 invalidate; guidelines WARN.
"""
from __future__ import annotations
from typing import Sequence

from .result import (PHI, INV_PHI, RuleResult, Status, Wave, _ok)  # noqa: F401

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
