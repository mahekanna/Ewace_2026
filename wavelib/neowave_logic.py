"""
neowave_logic.py — Neely's *predictive* layer (practitioner/03 CC-/FR- rules).

NeoWave claims to be predictive rather than descriptive because of three pillars
(`practitioner/03_neowave_forecasting.md` §1.3):

  1. LOGIC             a strong correction must yield a powerful move
  2. SELF-DEFINING     a smaller-degree pattern cannot consume more time or price
     LIMITS            than a larger-degree one
  3. SELF-CONFIRMATION strict post-pattern behaviour decides whether the labelling
                       was right; if the market refuses to confirm, the LABEL is
                       wrong — not the rules

Auditing `wavelib` in 2026-08 found pillar 3 entirely unimplemented and pillar 2
only half-built (Similarity & Balance existed; the hard caps did not). Every
backtest that concluded "no edge" therefore tested a signal with none of this in
it. This module supplies the missing rules.

All price comparisons use `Wave.log_length` — linear price makes valid proportions
invisible on any instrument spanning >2x (audit root-cause R1). All checks are
causal: they read the completed pattern plus bars that have already printed.
"""
from dataclasses import dataclass
from typing import Optional, Sequence

from .rules import RuleResult, Status, Wave

__all__ = ["moves_further_and_faster", "preconstructive_filter",
           "post_correction_thrust", "subwave_time_caps", "reverse_logic_rank",
           "falsify_count", "CountVerdict"]


def _largest_counter_leg(waves: Sequence[Wave], uptrend: bool) -> Optional[Wave]:
    """The deepest move against the pattern's own direction — the bar CC-3 sets."""
    counter = [w for w in waves if (w.end.price < w.start.price) == uptrend]
    return max(counter, key=lambda w: w.log_length) if counter else None


# --------------------------------------------------------------------------- #
# CC-3 — the UNIVERSAL confirmation rule
# --------------------------------------------------------------------------- #
def moves_further_and_faster(waves: Sequence[Wave], post: Wave,
                             uptrend: bool) -> RuleResult:
    """CC-3 (HARD). Post-pattern action must move FURTHER and FASTER than the
    largest counter-trend wave inside the pattern just completed.

    This is NeoWave's universal confirmation — the two-stage 2-4 protocol (CC-1) is
    only its specific form for trending/terminal impulses. `post` is the first
    move after the pattern, in the new direction.
    """
    ref = _largest_counter_leg(waves, uptrend)
    if ref is None:
        return RuleResult("CC-3 moves further and faster", Status.NA,
                          "no counter-trend leg inside the pattern to measure against")
    further = post.log_length > ref.log_length
    faster = post.days < ref.days if ref.days > 0 else False
    ok = further and faster
    return RuleResult(
        "CC-3 moves further and faster",
        Status.PASS if ok else Status.FAIL,
        f"post {post.log_length:.4f} over {post.days:.0f}d vs largest counter-leg "
        f"{ref.log_length:.4f} over {ref.days:.0f}d -> further={further} faster={faster}")


# --------------------------------------------------------------------------- #
# CC-4 — pre-constructive filter (a pattern is not STARTED until these hold)
# --------------------------------------------------------------------------- #
def preconstructive_filter(w1: Wave, w2: Wave, w3: Optional[Wave] = None,
                           w4: Optional[Wave] = None,
                           terminal: bool = False) -> list[RuleResult]:
    """CC-4 (HARD). In a TRENDING impulse a corrective wave must consume at least as
    much time as the motive wave it corrects, and no more than 3x it (NW-17).

    A shallow, fast candidate wave 2 is therefore *not finished* — it is still in
    progress, and entering wave 3 off it is premature. In a TERMINAL impulse the
    constraint inverts (corrective sub-waves may be shorter), so `terminal=True`
    downgrades the lower bound to a guideline.
    """
    out: list[RuleResult] = []
    for motive, corr, name in ((w1, w2, "2/1"), (w3, w4, "4/3")):
        if motive is None or corr is None:
            continue
        if motive.days <= 0:
            out.append(RuleResult(f"CC-4 wave-{name} time", Status.NA, "zero-duration motive"))
            continue
        ratio = corr.days / motive.days
        if ratio < 1.0:
            st = Status.WARN if terminal else Status.FAIL
            msg = ("terminal: corrective sub-waves may be shorter" if terminal
                   else "corrective wave is NOT complete (faster than the wave it corrects)")
        elif ratio > 3.0:
            st, msg = Status.FAIL, "exceeds 3x — not a standard impulse at this degree"
        else:
            st, msg = Status.PASS, "within [1x, 3x]"
        out.append(RuleResult(f"CC-4 wave-{name} time ratio",
                              st, f"{ratio:.2f}x ({corr.days:.0f}d vs {motive.days:.0f}d) — {msg}"))
    return out


# --------------------------------------------------------------------------- #
# CC-5 / FR-3 — post-correction thrust
# --------------------------------------------------------------------------- #
_MIN_THRUST = {"ZIGZAG": 1.0, "FLAT": 1.0, "TRIANGLE": 1.0,
               "WXY": 1.618, "COMBINATION": 1.618, "DOUBLE_THREE": 1.618}


def post_correction_thrust(correction: Sequence[Wave], thrust: Wave,
                           kind: str = "ZIGZAG") -> list[RuleResult]:
    """CC-5 + FR-3 (HARD). After a correction, the thrust resuming the prior trend
    must be at least as large as the correction (more, for complex corrections —
    "the post-effect after corrective patterns is usually more powerful"), and
    complete in no more time than the correction took.

    Failure is a post-constructive FAIL: the correction is mislabelled — incomplete,
    or of the wrong type/degree.
    """
    span = Wave(correction[0].start, correction[-1].end)
    need = _MIN_THRUST.get(kind.upper(), 1.0)
    size_ok = thrust.log_length >= need * span.log_length
    time_ok = thrust.days <= span.days if span.days > 0 else True
    return [
        RuleResult("CC-5/FR-3 thrust magnitude",
                   Status.PASS if size_ok else Status.FAIL,
                   f"thrust {thrust.log_length:.4f} vs {need:.3f}x correction "
                   f"{span.log_length:.4f} ({kind})"),
        RuleResult("CC-5 thrust time",
                   Status.PASS if time_ok else Status.WARN,
                   f"thrust {thrust.days:.0f}d vs correction {span.days:.0f}d"),
    ]


# --------------------------------------------------------------------------- #
# FR-7 — hard sub-wave duration caps (pillar 2: self-defining time limits)
# --------------------------------------------------------------------------- #
_CAPS = {"ZIGZAG": (2, (0, 1)), "FLAT": (2, (0, 1)),
         "TRIANGLE": (4, (1, 2, 3)), "DIAMETRIC": (6, (3, 4, 5))}


def subwave_time_caps(waves: Sequence[Wave], pattern: str) -> list[RuleResult]:
    """FR-7 (HARD). The final leg of a pattern cannot outlast the legs it follows:

        flat / zigzag   C <= time(A) + time(B)
        triangle        E <= time(B) + time(C) + time(D)
        diametric       G <= time(D) + time(E) + time(F)

    Breaching the cap means the leg is not that leg — the structure is a higher
    degree, or an x-wave is hiding between them.
    """
    spec = _CAPS.get(pattern.upper())
    if spec is None:
        return [RuleResult("FR-7 sub-wave time cap", Status.NA,
                           f"no published cap for {pattern}")]
    last_i, ref_i = spec
    if len(waves) <= last_i or any(i >= len(waves) for i in ref_i):
        return [RuleResult("FR-7 sub-wave time cap", Status.NA,
                           f"{pattern} needs {last_i + 1} legs, got {len(waves)}")]
    cap = sum(waves[i].days for i in ref_i)
    last = waves[last_i].days
    return [RuleResult(
        f"FR-7 {pattern} final-leg time cap",
        Status.PASS if last <= cap else Status.FAIL,
        f"final leg {last:.0f}d vs cap {cap:.0f}d "
        f"({'within' if last <= cap else 'BREACHED — wrong degree or hidden x-wave'})")]


# --------------------------------------------------------------------------- #
# FR-9 — Rule of Reverse Logic
# --------------------------------------------------------------------------- #
def reverse_logic_rank(candidates, completeness) -> list:
    """FR-9 (HARD). Among counts that are all valid, prefer the LEAST complete.

    Neely's reasoning is asymmetry of cost: assuming a pattern is nearly finished
    invites trading a reversal that never comes, while assuming it has further to
    run keeps the analyst with the trend. `completeness` maps a candidate to a
    0..1 fraction; ties keep the caller's original order (stable sort).
    """
    return sorted(candidates, key=completeness)


# --------------------------------------------------------------------------- #
# CC-9 — behaviour over structure (the falsification engine)
# --------------------------------------------------------------------------- #
@dataclass
class CountVerdict:
    """Outcome of running post-pattern behaviour against a proposed count."""
    falsified: bool
    results: list
    reason: str

    @property
    def status(self) -> Status:
        return Status.FAIL if self.falsified else Status.PASS


def falsify_count(waves: Sequence[Wave], pattern: str, *, post: Optional[Wave] = None,
                  uptrend: bool = True, terminal: bool = False) -> CountVerdict:
    """CC-9 (HARD). "No matter what you think of structure, if post-pattern
    behaviour is inconsistent with your labelling, your wave count is wrong."

    Runs every applicable check and returns a verdict. A FAIL is not "unusual
    behaviour" to be explained away — it means re-label, typically with the final
    pivot moved later (the pattern was not finished).
    """
    res: list[RuleResult] = []
    res += subwave_time_caps(waves, pattern)
    if pattern.upper() in ("IMPULSE", "DIAGONAL") and len(waves) == 5:
        res += preconstructive_filter(waves[0], waves[1], waves[2], waves[3],
                                      terminal=terminal or pattern.upper() == "DIAGONAL")
    if post is not None:
        res.append(moves_further_and_faster(waves, post, uptrend))
        if pattern.upper() in ("ZIGZAG", "FLAT", "TRIANGLE", "WXY"):
            res += post_correction_thrust(waves, post, kind=pattern)
    fails = [r for r in res if r.status is Status.FAIL]
    return CountVerdict(bool(fails), res,
                        "; ".join(r.rule for r in fails) if fails
                        else "no post-pattern behaviour contradicts the label")
