"""
automation.py
=============
Auto-labeling and bottom-up degree assignment (docs/research/04 §4 Items 2-4,
docs/research/02 §4 Task 10). Removes the manual pivot-picking step.

CAUSAL-ONLY: every candidate uses only pivots whose reversal is confirmed at or
before the last bar (`confirmed_t <= bars[-1][0]`). Provisional pivots are excluded.

Pure stdlib.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from .rules import (
    Wave, Pivot, Status, RuleResult,
    elliott_hard_rules, validate_impulse, validate_correction,
    label_monowaves, group_polywaves,
)
from .toolkit import zigzag_causal, zigzag_multiscale, pivots_to_waves

_FIB = (0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.0, 2.618, 3.618)


def _closeness(ratio: float, targets=_FIB) -> float:
    """0..1 adherence of `ratio` to the nearest Fibonacci target (1 = exact)."""
    if ratio != ratio:  # NaN
        return 0.0
    d = min(abs(ratio - t) / t for t in targets)
    return max(0.0, 1.0 - min(d, 1.0))


def _fib_score(waves) -> float:
    """Mean Fibonacci adherence of a candidate's key wave ratios (0..1)."""
    if len(waves) >= 5:
        w1, w2, w3, w4, w5 = waves[:5]
        rs = [
            _closeness(w3.length / w1.length if w1.length else float("nan")),
            _closeness(w2.retr(w1)),
            _closeness(w4.retr(w3)),
            _closeness(w5.length / w1.length if w1.length else float("nan")),
        ]
        return sum(rs) / len(rs)
    if len(waves) == 3:
        A, B, C = waves
        return (_closeness(B.retr(A)) +
                _closeness(C.length / A.length if A.length else float("nan"))) / 2
    return 0.0


@dataclass
class CandidateCount:
    pivots: list           # boundary pivots (6 for 5 waves; 4 for 3 waves)
    waves: list            # Wave objects
    count_type: str        # "IMPULSE" | "CORRECTION" | "DIAGONAL"
    results: list          # RuleResult from validate_impulse / validate_correction
    hard_fails: int
    warns: int
    fib_score: float
    degree: int            # scale index: 0=Minor, 1=Intermediate, 2=Primary
    degree_confidence: str = "HEURISTIC"  # COMPUTED | HEURISTIC | ASSUMED

    @property
    def rank_key(self):
        return (self.hard_fails, self.warns, -self.fib_score)


def _make_candidate(pivots, waves, ctype, results, degree) -> CandidateCount:
    hard = sum(1 for r in results if r.status is Status.FAIL)
    warns = sum(1 for r in results if r.status is Status.WARN)
    return CandidateCount(list(pivots), list(waves), ctype, list(results),
                          hard, warns, _fib_score(waves), degree)


def label_and_validate(bars, degrees=(0.03, 0.07, 0.15), atr_n=None,
                       max_candidates: int = 20, diagonal: bool = False):
    """
    Multi-scale auto-labeling engine (docs/research/04 §4 Item 3).

    For each scale: take the causal pivot stream, slide over 6-pivot windows for
    impulse/diagonal candidates and 4-pivot windows for corrections, prune by the
    Elliott hard rules (R1/R2/R3) before full validation, and score each candidate.
    Returns candidates sorted ascending by (hard_fails, warns, -fib_score),
    truncated to `max_candidates`.
    """
    if not bars:
        return []
    last_t = bars[-1][0]
    streams = zigzag_multiscale(bars, scales=tuple(degrees), atr_n=atr_n)
    cands: list[CandidateCount] = []
    for di, scale in enumerate(degrees):
        pivots = [p for p in streams[scale]
                  if p.confirmed_t is not None and p.confirmed_t <= last_t]
        # impulse / diagonal candidates (5 waves)
        for i in range(0, len(pivots) - 5):
            waves = pivots_to_waves(pivots[i:i + 6])
            hard = elliott_hard_rules(waves)
            if not diagonal and any(h.status is Status.FAIL for h in hard):
                continue                       # R1/R2/R3 prune
            results = validate_impulse(waves, diagonal=diagonal)
            cands.append(_make_candidate(pivots[i:i + 6], waves,
                                         "DIAGONAL" if diagonal else "IMPULSE", results, di))
        # correction candidates (3 waves)
        for i in range(0, len(pivots) - 3):
            waves = pivots_to_waves(pivots[i:i + 4])
            results = validate_correction(waves)
            cands.append(_make_candidate(pivots[i:i + 4], waves, "CORRECTION", results, di))
    cands.sort(key=lambda c: c.rank_key)
    return cands[:max_candidates]


def _promote(groups) -> list:
    """Compact non-overlapping validated polywave groups into synthetic boundary
    pivots for the next degree. Each promoted pivot keeps the underlying pivot's
    confirmed_t (>= every constituent monowave's), preserving causal monotonicity."""
    gs = sorted(groups, key=lambda g: g[0][0].start.t)
    syn: list = []
    occupied_until = None
    for g in gs:
        waves = [w for (w, _lab) in g]
        s, e = waves[0].start, waves[-1].end
        if occupied_until is not None and s.t < occupied_until:
            continue                           # overlaps an already-chosen group
        if not syn:
            syn.append(s)
        syn.append(e)
        occupied_until = e.t
    return syn


def assign_degrees_neely(bars, base_scale: float = 0.03, max_degrees: int = 3, atr_n=None):
    """
    Bottom-up Neely-style degree assignment (docs/research/04 §4 Item 4):
    label monowaves -> group polywaves -> validate -> promote to the next degree
    and repeat. Returns validated CandidateCounts with degree + degree_confidence
    ("HEURISTIC" — the simplified retracement-only classification, never a false
    precision claim). CAUSAL: synthetic pivots inherit confirmed_t from their
    constituent monowaves.
    """
    pivots = [p for p in zigzag_causal(bars, pct=base_scale, atr_n=atr_n)
              if p.confirmed_t is not None]
    results: list[CandidateCount] = []
    for degree in range(max_degrees):
        if len(pivots) < 4:
            break
        groups = group_polywaves(label_monowaves(pivots))
        for g in groups:
            waves = [w for (w, _lab) in g]
            if len(waves) == 5:
                res, ctype = validate_impulse(waves), "IMPULSE"
            else:
                res, ctype = validate_correction(waves), "CORRECTION"
            piv = [waves[0].start] + [w.end for w in waves]
            results.append(_make_candidate(piv, waves, ctype, res, degree))
        promoted = _promote(groups)
        if len(promoted) < 4 or len(promoted) >= len(pivots):
            break                              # no further compaction possible
        pivots = promoted
    return results


_MOTIVE_SEQ = {5, 9, 13, 17, 21}
_CORRECTIVE_SEQ = {3, 7, 11, 15, 19}


def swing_sequence(bars=None, pivots=None, pct: float = 0.05):
    """EWF swing-sequence count on confirmed ZigZag pivots (docs/research/deep/09,10).
    Counts alternating swings: motive sequences complete at 5/9/13..., corrective at
    3/7/11...; an in-between count is INCOMPLETE -> the move is expected to extend
    (the actionable signal). Returns a dict with the count, status, and the next
    motive/corrective targets. Causal (confirmed pivots only)."""
    if pivots is None:
        pivots = [p for p in zigzag_causal(bars or [], pct=pct) if p.confirmed_t is not None]
    n = max(0, len(pivots) - 1)
    if n in _MOTIVE_SEQ:
        status = "MOTIVE-COMPLETE"
    elif n in _CORRECTIVE_SEQ:
        status = "CORRECTIVE-COMPLETE"
    else:
        status = "INCOMPLETE"
    return {
        "swings": n,
        "status": status,
        "next_motive": min((m for m in sorted(_MOTIVE_SEQ) if m >= n), default=None),
        "next_corrective": min((c for c in sorted(_CORRECTIVE_SEQ) if c >= n), default=None),
    }
