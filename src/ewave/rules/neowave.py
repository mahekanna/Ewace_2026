"""
rules.neowave — NeoWave core logic: Similarity & Balance, proportion,
retracement logic, channeling (2-4 / 0-2 / 1-3), the causal per-bar completion
monitor, and the bottom-up monowave constructor (moved verbatim from
wavelib/rules.py §E/§F2).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence

from .corrections import classify_correction
from .elliott import elliott_hard_rules
from .result import Pivot, RuleResult, Status, Wave, _within

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
