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
from dataclasses import dataclass, field

from .rules import (Pivot, Wave, Status, elliott_hard_rules, classify_correction,
                    _classify_triangle, similarity_and_balance)
from .toolkit import zigzag_causal

_MOTIVE = {"IMPULSE", "DIAGONAL"}
_CORRECTIVE = {"ZIGZAG", "FLAT", "TRIANGLE", "CORRECTION", "COMPLEX"}


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


def _impulse_node(group, degree):
    waves = [n.as_wave() for n in group]
    if not _alternating(waves):
        return None
    hard = elliott_hard_rules(waves)
    if any(h.status is Status.FAIL for h in hard):
        return None                            # not a clean impulse (diagonals: later stage)
    results = hard + [similarity_and_balance(waves[1], waves[3], context="w2 vs w4")]
    conf = _confidence(results, group, (0, 2, 4), (1, 3))
    return WaveNode(group[0].start, group[-1].end, degree, "motive", "IMPULSE",
                    list(group), results, conf)


def _triangle_node(group, degree):
    rr = _classify_triangle([n.as_wave() for n in group])
    if rr.status is not Status.PASS:
        return None
    conf = _confidence([rr], group, (), (0, 1, 2, 3, 4))
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
    results = [rr, similarity_and_balance(waves[0], waves[2], context="A vs C")]
    conf = _confidence(results, group, (0, 2), (1,))
    return WaveNode(group[0].start, group[-1].end, degree, "corrective", pattern,
                    list(group), results, conf)


def _build_level(nodes, degree):
    """One bottom-up compaction pass via dynamic programming: choose the
    segmentation of `nodes` into 5-groups (impulse, else triangle) and 3-groups
    (correction) — plus carried singletons — that MAXIMISES total validated
    confidence. Greedy left-to-right mis-aligns at pattern boundaries; the global
    DP does not."""
    n = len(nodes)

    def seg(i, k):
        grp = nodes[i:i + k]
        if k == 5:
            return _impulse_node(grp, degree) or _triangle_node(grp, degree)
        if k == 3:
            return _correction_node(grp, degree)
        return None

    def value(node):
        # reward coverage (children consumed) x quality, with a motive-impulse
        # bonus so a clean 5-wave impulse outscores splitting it into corrections
        bonus = 0.5 if node.pattern == "IMPULSE" else 0.0
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


def build_tree_from_pivots(pivots, max_levels: int = 6):
    """Compact a confirmed-pivot list into wave-tree roots (usually 1-3 nodes)."""
    pivots = list(pivots)
    if len(pivots) < 2:
        return []
    nodes = [WaveNode(pivots[i], pivots[i + 1], 0, "leg", "MONOWAVE")
             for i in range(len(pivots) - 1)]
    degree = 1
    while degree <= max_levels:
        nodes, changed = _build_level(nodes, degree)
        if not changed:
            break
        degree += 1
    return nodes


def build_wave_tree(bars, base_pct: float = 0.03, max_levels: int = 6):
    """Causal entry point: ZigZag -> confirmed pivots -> recursive wave tree."""
    pivots = [p for p in zigzag_causal(bars, pct=base_pct) if p.confirmed_t is not None]
    return build_tree_from_pivots(pivots, max_levels)


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
