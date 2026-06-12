"""
wavetree.py  —  Stage 1 of the deeper (recursive, multi-degree) engine.
=======================================================================
The single-degree validators in rules.py answer "is THIS set of 5/3 legs a valid
pattern?". They cannot answer the question that actually matters in Elliott/NeoWave:
"do the legs themselves subdivide correctly?" — i.e. is each motive sub-wave a 5,
each corrective sub-wave a 3, all the way down.

This module builds a **wave tree** bottom-up: monowaves -> compact groups of 3
(corrections) or 5 (impulses/triangles) into parent nodes, repeating up the
degrees. Because each parent is formed from already-classified children, the
parent can verify its sub-structure (motive children are impulses, corrective
children are corrections) — true recursive multi-degree validation, with a
per-node confidence.

CAUSAL: built only from confirmed ZigZag pivots (confirmed_t set). Pure stdlib.
"""
from __future__ import annotations
import bisect
import math
from dataclasses import dataclass, field
from itertools import combinations

from .rules import (Pivot, Wave, Status, RuleResult, Degree, elliott_hard_rules,
                    classify_correction, similarity_and_balance)
from .toolkit import zigzag_causal

_MOTIVE = {"IMPULSE", "DIAGONAL"}
_CORRECTIVE = {"ZIGZAG", "FLAT", "TRIANGLE", "CORRECTION", "COMPLEX", "WXY"}
_FIB = (0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.0, 2.618, 3.618)


def _fib_close(r, sigma: float = 0.2) -> float:
    """Gaussian proximity (0..1) of ratio r to the nearest Fibonacci level — a
    smooth, calibrated kernel (docs/research/deep/07) instead of a linear tent.
    sigma is the relative-distance scale (~20%)."""
    if r != r or r <= 0:
        return 0.0
    d = min(abs(r - t) / t for t in _FIB)
    return math.exp(-(d * d) / (2 * sigma * sigma))


# --------------------------------------------------------------------------- #
# Momentum gate (Elliott Wave Oscillator) — how professionals CONFIRM wave 3.
# Tom Joseph's EWO = SMA(close,5) - SMA(close,35): a real wave 3 carries the
# highest in-trend reading; wave 4 pulls it toward zero; wave 5 diverges.
# (docs/research/practitioner/01 + 02.)
# --------------------------------------------------------------------------- #
def _ewo(closes, fast: int = 5, slow: int = 35):
    def sma(n):
        out = [None] * len(closes)
        run = 0.0
        for i, c in enumerate(closes):
            run += c
            if i >= n:
                run -= closes[i - n]
            if i >= n - 1:
                out[i] = run / n
        return out
    f, s = sma(fast), sma(slow)
    return [(f[i] - s[i]) if (f[i] is not None and s[i] is not None) else None
            for i in range(len(closes))]


def momentum_lookup(bars):
    """Return a causal callable t -> EWO value at the most recent bar <= t (or None
    if EWO not yet defined). Used to gate wave identity in the tree scoring."""
    ts = [b[0] for b in bars]
    ewo = _ewo([b[4] for b in bars])

    def at(t):
        i = bisect.bisect_right(ts, t) - 1
        if i < 0:
            return None
        return ewo[min(i, len(ewo) - 1)]
    return at


def _momentum_multiplier(waves, mom) -> float:
    """Confidence multiplier (≈0.65–1.45) from the EWO momentum profile of a 5-wave
    group. Boosts a momentum-confirmed impulse (W3 strongest, W5 divergent, W4 to
    zero) and penalises one whose 'wave 3' is not the momentum peak — the single
    check professionals say catches most mislabelled impulses."""
    w1, w2, w3, w4, w5 = waves
    e1, e3, e4, e5 = mom(w1.end.t), mom(w3.end.t), mom(w4.end.t), mom(w5.end.t)
    if e1 is None or e3 is None or e5 is None:
        return 1.0
    sgn = 1.0 if w1.up else -1.0                 # orient so + = in trend direction
    a1, a3, a5 = sgn * e1, sgn * e3, sgn * e5
    mult = 1.25 if (a3 >= a1 and a3 >= a5) else 0.7     # W3 must be the momentum peak
    beyond = (w5.end.price > w3.end.price) if w1.up else (w5.end.price < w3.end.price)
    if beyond and a5 < a3:                        # W5 makes new price extreme on weaker momentum
        mult *= 1.12
    if e4 is not None and abs(e4) < abs(e3):      # W4 pulls EWO toward zero
        mult *= 1.05
    return mult


def _impulse_quality(waves) -> float:
    """Fibonacci adherence of an impulse's key ratios (0..1). Ratios are computed
    in LOG magnitude (`log_length`) — the correct measure on large-range
    instruments, where linear price differences make valid proportions invisible
    (docs/research/audit/04). W3 vs W1 is the headline relationship (W3 commonly
    1.618-2.618x W1), so it is weighted double."""
    w1, w2, w3, w4, w5 = waves
    q31 = _fib_close(w3.log_length / w1.log_length if w1.log_length else 0)
    q21 = _fib_close(w2.log_length / w1.log_length if w1.log_length else 0)
    q43 = _fib_close(w4.log_length / w3.log_length if w3.log_length else 0)
    return (2 * q31 + q21 + q43) / 4.0


def _correction_quality(pattern, waves) -> float:
    """Quality of a 3-leg correction (LOG magnitude). Bases are deliberately below
    a clean impulse's quality so a momentum-confirmed 5-wave impulse outranks a
    3-wave parse of the same data (docs/research/audit/01 M1/M7)."""
    A, B, C = waves
    b = B.log_length / A.log_length if A.log_length else 0.0
    cca = C.log_length / A.log_length if A.log_length else 0.0
    if pattern == "ZIGZAG":
        base = 0.65
    elif pattern == "FLAT":
        base = 0.58 if b >= 0.8 else 0.40        # shallow-B "flat" is really ambiguous
    else:
        base = 0.5
    return base * (0.6 + 0.4 * _fib_close(cca))


@dataclass
class WaveNode:
    start: Pivot
    end: Pivot
    degree: int                 # 0 = monowave (leaf); higher = coarser
    role: str                   # "motive" | "corrective" | "leg"
    pattern: str                # IMPULSE/DIAGONAL/ZIGZAG/FLAT/TRIANGLE/MONOWAVE
    children: list = field(default_factory=list)
    results: list = field(default_factory=list)
    confidence: float = 1.0

    @property
    def up(self) -> bool:
        return self.end.price > self.start.price

    @property
    def length(self) -> float:
        return abs(self.end.price - self.start.price)

    def as_wave(self) -> Wave:
        return Wave(self.start, self.end)


def _alternating(waves) -> bool:
    """w1,w3,w5 share a direction; w2,w4 the opposite (a real motive sequence)."""
    d = [w.up for w in waves]
    return d[0] == d[2] == d[4] and d[1] == d[3] and d[1] != d[0]


def _confidence(results, children, motive_idx, corr_idx) -> float:
    conf = 1.0
    conf -= 0.1 * sum(1 for r in results if r.status is Status.WARN)
    for i in motive_idx:                       # motive sub-waves should be 5s
        c = children[i]
        if c.pattern != "MONOWAVE" and c.pattern not in _MOTIVE:
            conf -= 0.2
    for i in corr_idx:                          # corrective sub-waves should be 3s
        c = children[i]
        if c.pattern != "MONOWAVE" and c.pattern not in _CORRECTIVE:
            conf -= 0.2
    return max(0.0, min(1.0, conf))


def _impulse_node(group, degree, momentum=None):
    waves = [n.as_wave() for n in group]
    if not _alternating(waves):
        return None
    hard = elliott_hard_rules(waves)
    if any(h.status is Status.FAIL for h in hard):
        return None                            # not a clean impulse (diagonals: later stage)
    # Real impulse sub-structure (5-3-5-3-5): once the children are themselves
    # classified (degree >= 2), motive legs 1/3/5 must be impulses and corrective
    # legs 2/4 must be corrections. At degree 1 the children are monowaves
    # (sub-structure not yet observable) so this is deferred.
    if degree >= 2:
        if not all(group[i].pattern in _MOTIVE for i in (0, 2, 4)):
            return None
        if not all(group[i].pattern in _CORRECTIVE for i in (1, 3)):
            return None
    results = hard + [similarity_and_balance(waves[1], waves[3], context="w2 vs w4")]
    conf = _confidence(results, group, (0, 2, 4), (1, 3)) * (0.4 + 0.6 * _impulse_quality(waves))
    if momentum is not None:                    # EWO wave-3 confirmation gate
        conf = max(0.0, min(1.0, conf * _momentum_multiplier(waves, momentum)))
    return WaveNode(group[0].start, group[-1].end, degree, "motive", "IMPULSE",
                    list(group), results, conf)


def _triangle_geometry(group):
    """Genuine triangle test on prices: the two boundaries must converge
    (contracting) or diverge (expanding). Returns the kind or None."""
    p = [group[0].start.price] + [n.end.price for n in group]
    up0 = p[1] > p[0]
    peaks = [p[1], p[3], p[5]] if up0 else [p[0], p[2], p[4]]
    troughs = [p[0], p[2], p[4]] if up0 else [p[1], p[3], p[5]]
    if peaks[0] > peaks[1] > peaks[2] and troughs[0] < troughs[1] < troughs[2]:
        return "CONTRACTING"
    if peaks[0] < peaks[1] < peaks[2] and troughs[0] > troughs[1] > troughs[2]:
        return "EXPANDING"
    return None


def _diagonal_node(group, degree):
    """A diagonal is a MOTIVE wedge whose wave 4 overlaps wave 1 (the defining
    trait that disqualifies it as an impulse) and whose legs contract/expand.
    Ending diagonal = 3-3-3-3-3 (all corrective children); leading = 5-3-5-3-5.
    Like triangles, a diagonal's legs are multi-wave, so it only forms at degree>=2."""
    if degree < 2:
        return None
    waves = [n.as_wave() for n in group]
    if not _alternating(waves):
        return None
    w1, w2, w3, w4, w5 = waves
    up = w1.up
    overlap = (w4.end.price < w1.end.price) if up else (w4.end.price > w1.end.price)
    if not overlap:
        return None                            # no overlap -> impulse, not diagonal
    net_dir = (w5.end.price > w1.start.price) if up else (w5.end.price < w1.start.price)
    if not net_dir:
        return None                            # must be net-directional (a wedge, not a triangle)
    contracting = w1.log_length > w3.log_length > w5.log_length
    expanding = w1.log_length < w3.log_length < w5.log_length
    if not (contracting or expanding):
        return None
    hard = elliott_hard_rules(waves)            # R1, R2 must still hold (R3/overlap is expected)
    if hard[0].status is Status.FAIL or hard[1].status is Status.FAIL:
        return None
    subtype = "diagonal"
    if degree >= 2:                             # verify sub-structure once children are classified
        all_corr = all(c.pattern in _CORRECTIVE for c in group)
        leading = (all(group[i].pattern in _MOTIVE for i in (0, 2, 4)) and
                   all(group[i].pattern in _CORRECTIVE for i in (1, 3)))
        if not (all_corr or leading):
            return None
        subtype = "ending diagonal" if all_corr else "leading diagonal"
    shape = "contracting" if contracting else "expanding"
    rr = RuleResult(f"{subtype} ({shape} wedge, w4/w1 overlap)", Status.PASS, f"degree {degree}")
    conf = _confidence([rr], group, (0, 2, 4), (1, 3)) * (0.4 + 0.6 * _impulse_quality(waves)) * 0.9
    return WaveNode(group[0].start, group[-1].end, degree, "motive", "DIAGONAL",
                    list(group), [rr], conf)


def _triangle_node(group, degree):
    # A real triangle's five legs are each CORRECTIVE (3s) and its two boundary
    # trendlines genuinely converge/diverge. Monowave legs cannot be a triangle,
    # so this only forms at degree >= 2 with all-corrective children.
    if degree < 2 or not all(c.pattern in _CORRECTIVE for c in group):
        return None
    geo = _triangle_geometry(group)
    if geo is None:
        return None
    rr = RuleResult(f"triangle: {geo.lower()}, 5 corrective legs, converging lines",
                    Status.PASS, f"degree {degree}")
    conf = _confidence([rr], group, (), (0, 1, 2, 3, 4)) * 0.7
    return WaveNode(group[0].start, group[-1].end, degree, "corrective", "TRIANGLE",
                    list(group), [rr], conf)


def _correction_node(group, degree):
    waves = [n.as_wave() for n in group]
    if waves[0].up == waves[1].up or waves[0].up != waves[2].up:
        return None                            # A,C same direction; B opposite
    rr = classify_correction(waves)
    if rr.status is not Status.PASS:
        return None
    pattern = ("ZIGZAG" if "ZIGZAG" in rr.rule else
               "FLAT" if "FLAT" in rr.rule else "CORRECTION")
    # EWF ABC-vs-WXY discipline (docs/research/deep/09): a true zigzag (ABC, 5-3-5)
    # requires motive A & C; if A/C are themselves corrective (3s) it is a WXY
    # double-three combination, not a zigzag.
    if degree >= 2 and pattern == "ZIGZAG" and not (
            group[0].pattern in _MOTIVE and group[2].pattern in _MOTIVE):
        pattern = "WXY"
    results = [rr, similarity_and_balance(waves[0], waves[2], context="A vs C")]
    # sub-structure expectation: zigzag = 5-3-5 (A,C motive), flat = 3-3-5 (C motive)
    m_idx, c_idx = ((0, 2), (1,)) if pattern == "ZIGZAG" else \
                   ((2,), (0, 1)) if pattern == "FLAT" else ((), (0, 1, 2))
    conf = _confidence(results, group, m_idx, c_idx) * _correction_quality(pattern, waves)
    return WaveNode(group[0].start, group[-1].end, degree, "corrective", pattern,
                    list(group), results, conf)


def _build_level(nodes, degree, momentum=None):
    """One bottom-up compaction pass via dynamic programming: choose the
    segmentation of `nodes` into 5-groups (impulse, else triangle) and 3-groups
    (correction) — plus carried singletons — that MAXIMISES total validated
    confidence. Greedy left-to-right mis-aligns at pattern boundaries; the global
    DP does not."""
    n = len(nodes)

    def seg(i, k):
        grp = nodes[i:i + k]
        if k == 5:
            return (_impulse_node(grp, degree, momentum) or _diagonal_node(grp, degree)
                    or _triangle_node(grp, degree))
        if k == 3:
            return _correction_node(grp, degree)
        return None

    def value(node):
        # reward coverage (children consumed) x quality, with a motive bonus so a
        # clean 5-wave impulse/diagonal outscores splitting it into corrections.
        # Bonus raised (audit 01 M1): a momentum-confirmed impulse must beat two
        # overlapping 3-wave corrections that would otherwise win on node count.
        bonus = 1.5 if node.pattern == "IMPULSE" else 0.8 if node.pattern == "DIAGONAL" else 0.0
        return len(node.children) * node.confidence + bonus

    best = [None] * (n + 1)
    best[n] = (0.0, [])
    for i in range(n - 1, -1, -1):
        carry_score, carry_list = best[i + 1]
        cand = (carry_score, [nodes[i]] + carry_list)          # leave node ungrouped (value 0)
        for k in (5, 3):
            if i + k <= n:
                node = seg(i, k)
                if node is not None:
                    s2, l2 = best[i + k]
                    if value(node) + s2 > cand[0]:
                        cand = (value(node) + s2, [node] + l2)
        best[i] = cand
    new = best[0][1]
    changed = any(nd.degree == degree for nd in new)
    return new, changed


def build_tree_from_pivots(pivots, max_levels: int = 6, momentum=None):
    """Compact a confirmed-pivot list into wave-tree roots (usually 1-3 nodes).
    `momentum` (from `momentum_lookup`) gates impulse confidence by EWO when given."""
    pivots = list(pivots)
    if len(pivots) < 2:
        return []
    nodes = [WaveNode(pivots[i], pivots[i + 1], 0, "leg", "MONOWAVE")
             for i in range(len(pivots) - 1)]
    degree = 1
    while degree <= max_levels:
        nodes, changed = _build_level(nodes, degree, momentum)
        if not changed:
            break
        degree += 1
    return nodes


def build_wave_tree(bars, base_pct: float = 0.03, max_levels: int = 6, use_momentum: bool = True):
    """Causal entry point: ZigZag -> confirmed pivots -> recursive wave tree. By
    default the EWO momentum gate is applied (the professional wave-3 confirmation)."""
    pivots = [p for p in zigzag_causal(bars, pct=base_pct) if p.confirmed_t is not None]
    mom = momentum_lookup(bars) if use_momentum and len(bars) >= 40 else None
    return build_tree_from_pivots(pivots, max_levels, momentum=mom)


def format_tree(nodes, indent: int = 0) -> str:
    """Pretty ASCII rendering of the wave tree."""
    lines = []
    for n in (nodes if isinstance(nodes, list) else [nodes]):
        arrow = "up" if n.up else "dn"
        lines.append("  " * indent + f"[{n.pattern}] d{n.degree} {n.role} {arrow} "
                     f"{n.start.price:.1f}->{n.end.price:.1f} conf={n.confidence:.0%}")
        if n.children:
            lines.append(format_tree(n.children, indent + 1))
    return "\n".join(lines)


def deepest_degree(nodes) -> int:
    return max((n.degree for n in nodes), default=0)


def _span(node) -> float:
    return node.end.t - node.start.t


def tree_confidence(roots) -> float:
    """Honest top-level confidence: the dominant root's own confidence scaled by
    how much of the series it actually covers. A tree that fragments into many
    small roots scores LOW (no single clean count), regardless of leaf quality."""
    if not roots:
        return 0.0
    total = sum(_span(r) for r in roots) or 1.0
    top = max(roots, key=_span)
    return top.confidence * (_span(top) / total)


_LABELS = {
    "IMPULSE": ["1", "2", "3", "4", "5"],
    "DIAGONAL": ["1", "2", "3", "4", "5"],
    "ZIGZAG": ["A", "B", "C"],
    "FLAT": ["A", "B", "C"],
    "CORRECTION": ["A", "B", "C"],
    "WXY": ["W", "X", "Y"],
    "TRIANGLE": ["A", "B", "C", "D", "E"],
}


@dataclass
class AnchoredCount:
    """A single committed wave count: the dominant top structure with its legs
    labelled (1-5 / A-B-C / A-E), a degree, calibrated confidence, and an honest
    note about how settled it is."""
    pattern: str
    degree: int
    labels: list                # list of (label, WaveNode)
    confidence: float
    coverage: float
    degree_label: str           # estimated Elliott degree (Neely complexity window)
    note: str

    def __str__(self):
        head = (f"{self.pattern} @ {self.degree_label} (tree degree {self.degree}) — "
                f"confidence {self.confidence:.0%} (coverage {self.coverage:.0%}); {self.note}")
        legs = "\n".join(f"  wave {lab}: {n.start.price:.2f} -> {n.end.price:.2f} "
                         f"[{n.pattern}]" for lab, n in self.labels)
        return head + ("\n" + legs if legs else "")


def _count_monowaves(node) -> int:
    return 1 if not node.children else sum(_count_monowaves(c) for c in node.children)


_DEGREE_BY_YEARS = [  # (max calendar years, Degree) — Frost & Prechter approx. durations
    (14 / 365, Degree.SUBMINUETTE), (45 / 365, Degree.MINUETTE), (0.30, Degree.MINUTE),
    (1.2, Degree.MINOR), (3.5, Degree.INTERMEDIATE), (9.0, Degree.PRIMARY),
    (27.0, Degree.CYCLE), (80.0, Degree.SUPERCYCLE)]


def anchored_degree(node, series_monowaves: int = None) -> Degree:
    """Estimate Elliott degree from the CALENDAR SPAN of the structure. Previously
    this used monowave complexity, which (a) was measured on the partial node and
    (b) was hard-capped at INTERMEDIATE (audit 02 R4) — and complexity also scales
    with bar count, so an intraday series wrongly reached Supercycle. Degree in EW
    is tied to duration (Grand Supercycle = centuries … Subminuette = minutes), so
    we map the structure's time span to the standard ladder. `series_monowaves` is
    accepted for backward-compatibility and ignored."""
    years = (node.end.t - node.start.t) / (365.25 * 86400.0)
    for hi, deg in _DEGREE_BY_YEARS:
        if years < hi:
            return deg
    return Degree.GRAND_SUPERCYCLE


def _anchored_from(top, confidence, coverage, series_monowaves=None) -> AnchoredCount:
    labs = _LABELS.get(top.pattern, [])
    labels = list(zip(labs, top.children)) if len(top.children) == len(labs) else []
    confidence = max(0.0, min(1.0, confidence))      # confidence is a probability in [0,1]
    note = ("primary count; watch the wave-1/A origin for invalidation" if confidence >= 0.4
            else "LOW confidence — one of several plausible counts; not a committed call")
    deg = anchored_degree(top, series_monowaves)
    return AnchoredCount(top.pattern, top.degree, labels, confidence, coverage,
                         deg.name.replace("_", " ").title(), note)


def _scale_score(roots):
    """(top node, honest_confidence<=1, selection_score). The selection score adds
    a motive bonus / monowave penalty for RANKING only; confidence stays a [0,1]
    probability."""
    top = max(roots, key=_span)
    conf = tree_confidence(roots)
    score = conf * (0.05 if top.pattern == "MONOWAVE"
                    else 1.15 if top.pattern in _MOTIVE else 1.0)
    return top, conf, score


# =========================================================================== #
# TOP-DOWN anchoring — how professionals count (docs/research/practitioner/01).
# Bottom-up compaction cannot turn 3 macro legs into a 5-wave impulse; pros anchor
# the dominant high<->low span and search for the best 5-wave partition of the
# ENTIRE move (full coverage by construction), then drill down. This is the pass
# that lets a secular advance read as a 5-wave IMPULSE rather than an A-B-C.
# =========================================================================== #
def _coarse_pivots(bars, target: int = 15):
    """Confirmed zigzag pivots at a threshold chosen so the full history reduces to
    ~`target` MAJOR swings (the degree the macro count lives at)."""
    best = []
    for pct in (0.05, 0.07, 0.10, 0.14, 0.20, 0.28, 0.40, 0.55):
        piv = [p for p in zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
        if not best or abs(len(piv) - target) < abs(len(best) - target):
            best = piv
        if len(piv) <= target:
            break
    return best


def _impulse_partitions(piv, a, b, mom):
    """All valid 5-wave impulse partitions of piv[a..b] -> (confidence, 'IMPULSE', idx)."""
    out = []
    for i1, i2, i3, i4 in combinations(range(a + 1, b), 4):
        idx = [a, i1, i2, i3, i4, b]
        waves = [Wave(piv[idx[k]], piv[idx[k + 1]]) for k in range(5)]
        if not _alternating(waves):
            continue
        hard = elliott_hard_rules(waves)
        if any(h.status is Status.FAIL for h in hard):
            continue                            # overlap (diagonal) / rule break -> not an impulse
        q = 0.4 + 0.6 * _impulse_quality(waves)
        if mom is not None:
            q *= _momentum_multiplier(waves, mom)
        out.append((max(0.0, min(1.0, q)), "IMPULSE", idx))
    return out


def _correction_partitions(piv, a, b):
    """All valid 3-wave correction partitions of piv[a..b] -> (confidence, pattern, idx)."""
    out = []
    for i1, i2 in combinations(range(a + 1, b), 2):
        idx = [a, i1, i2, b]
        waves = [Wave(piv[idx[k]], piv[idx[k + 1]]) for k in range(3)]
        if waves[0].up == waves[1].up or waves[0].up != waves[2].up:
            continue
        rr = classify_correction(waves)
        if rr.status is not Status.PASS:
            continue
        pattern = ("ZIGZAG" if "ZIGZAG" in rr.rule else
                   "FLAT" if "FLAT" in rr.rule else "CORRECTION")
        out.append((_correction_quality(pattern, waves), pattern, idx))
    return out


def _child_node(piv, a, b, mom):
    """Recursively count the sub-structure of one top-degree leg (piv[a..b])."""
    if b - a <= 1:
        return WaveNode(piv[a], piv[b], 0, "leg", "MONOWAVE")
    roots = build_tree_from_pivots(piv[a:b + 1], momentum=mom)
    if len(roots) == 1:
        return roots[0]
    return WaveNode(piv[a], piv[b], 1, "leg", "CORRECTION", list(roots))


def top_down_count(bars, target: int = 15, momentum=None, max_pivots: int = 22):
    """Anchor the dominant low<->high span and return the best full-range top-degree
    WaveNode (a 5-wave impulse where the structure supports it, else the best
    correction). Full coverage by construction. Returns None if nothing valid."""
    piv = _coarse_pivots(bars, target)
    if len(piv) < 6 or len(piv) > max_pivots:    # too few to be 5 waves / too many to search
        if len(piv) > max_pivots:
            piv = piv[-max_pivots:]              # most recent major swings
        if len(piv) < 4:
            return None
    mom = momentum if momentum is not None else (
        momentum_lookup(bars) if len(bars) >= 40 else None)
    prices = [p.price for p in piv]
    lo_i = min(range(len(piv)), key=lambda i: prices[i])
    hi_i = max(range(len(piv)), key=lambda i: prices[i])
    cands = []
    if lo_i < hi_i and hi_i - lo_i >= 5:         # up impulse: low ... later high
        cands += _impulse_partitions(piv, lo_i, hi_i, mom)
    if hi_i < lo_i and lo_i - hi_i >= 5:         # down impulse: high ... later low
        cands += _impulse_partitions(piv, hi_i, lo_i, mom)
    cands += _correction_partitions(piv, 0, len(piv) - 1)
    if not cands:
        return None
    # prefer a motive (impulse) reading when it is close — the professional bias
    score, pattern, idx = max(cands, key=lambda c: c[0] + (0.2 if c[1] in _MOTIVE else 0.0))
    # HONESTY: we picked the best of many partitions (selection bias) — if many
    # score nearly as high the count is genuinely ambiguous, so haircut confidence.
    # And no Elliott count is ever certain: hard-cap at 0.85.
    same = [c[0] for c in cands if (c[1] in _MOTIVE) == (pattern in _MOTIVE)]
    top_raw = max(same) or 1.0
    n_close = sum(1 for v in same if v >= 0.9 * top_raw)
    decisiveness = 1.0 / (1.0 + 0.25 * (n_close - 1))
    conf = min(0.85, min(1.0, score) * decisiveness)
    children = [_child_node(piv, idx[k], idx[k + 1], mom) for k in range(len(idx) - 1)]
    deg = max((c.degree for c in children), default=0) + 1
    role = "motive" if pattern in _MOTIVE else "corrective"
    return WaveNode(piv[idx[0]], piv[idx[-1]], deg, role, pattern, children, [], conf)


def wave_counts(bars, scales=(0.04, 0.07, 0.12, 0.20), max_alternates: int = 3,
                top_down: bool = True):
    """Return a RANKED list of AnchoredCounts (primary first). A TOP-DOWN full-range
    count (the professional anchoring) is computed first and becomes primary when it
    is a valid structure; bottom-up multi-scale counts supply alternates."""
    out, seen = [], set()
    if top_down:
        td = top_down_count(bars)
        if td is not None and td.confidence >= 0.25:
            mw = _count_monowaves(td)
            ac = _anchored_from(td, td.confidence, 1.0, mw)
            # rank ahead of bottom-up fragments; motive gets the professional bias
            sel = td.confidence * (1.3 if td.pattern in _MOTIVE else 1.0) + 0.4
            out.append((sel, ac))
            seen.add((td.pattern, int(td.start.t), int(td.end.t)))
    for s in scales:
        roots = build_wave_tree(bars, base_pct=s)
        if not roots:
            continue
        total = sum(_span(r) for r in roots) or 1.0
        top, conf, score = _scale_score(roots)
        key = (top.pattern, int(top.start.t), int(top.end.t))
        if key in seen:
            continue
        seen.add(key)
        # degree reflects the FULL series complexity, not just the partial top node
        series_mw = sum(_count_monowaves(r) for r in roots)
        out.append((score, _anchored_from(top, conf, _span(top) / total, series_mw)))
    out.sort(key=lambda x: -x[0])
    return [ac for _, ac in out][:1 + max_alternates]


def anchor_count(bars, scales=(0.04, 0.07, 0.12, 0.20)):
    """Commit to ONE count (the highest-scoring across scales). See wave_counts
    for the primary + alternates list."""
    cs = wave_counts(bars, scales, max_alternates=0)
    return cs[0] if cs else None


def best_count(bars, scales=(0.04, 0.07, 0.12, 0.20)):
    """Pick the single best macro count: build the tree at several ZigZag scales
    and return the one whose dominant top structure best covers the data with the
    highest confidence. Coarser scales yield fewer pivots and a cleaner macro
    count; finer scales show detail. Returns a dict (or None)."""
    best = None
    for s in scales:
        roots = build_wave_tree(bars, base_pct=s)
        if not roots:
            continue
        total = sum(_span(r) for r in roots) or 1.0
        top = max(roots, key=_span)
        # a MONOWAVE top is no count at all (coarse scale found no structure) -> penalize;
        # a motive (impulse/diagonal) top is mildly preferred for a directional move
        score = tree_confidence(roots)
        if top.pattern == "MONOWAVE":
            score *= 0.05
        elif top.pattern in _MOTIVE:
            score *= 1.15
        cand = {"scale": s, "roots": roots, "top": top, "n_roots": len(roots),
                "coverage": _span(top) / total, "confidence": top.confidence,
                "score": score, "depth": deepest_degree(roots)}
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best
