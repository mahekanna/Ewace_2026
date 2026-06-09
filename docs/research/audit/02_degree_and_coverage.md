# 02 — Degree Hierarchy and Automated-Counting Coverage: Audit

**Ewace_2026 / `wavelib` — June 2026**

*Audit only. No code is changed. All citations are file:function:line.*

---

## 1. Theory

### 1.1 The Frost & Prechter Degree Hierarchy

Elliott and Prechter identify **nine degrees** of waves, from largest to smallest
(Frost & Prechter, *Elliott Wave Principle* 10th ed., Ch. 2;
https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf;
Wikipedia https://en.wikipedia.org/wiki/Elliott_wave_principle;
EW Insight https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/):

| Rank | Degree name | Typical duration | Label style |
|------|-------------|-----------------|-------------|
| 9 | Grand Supercycle | Multi-century | (I)...(V) circled Roman |
| 8 | Supercycle | Multi-decade (40–70 yr) | I...V Roman |
| 7 | Cycle | 1 yr – several decades | I...V Roman (context-dependent) |
| 6 | Primary | Months – ~2 years | (1)...(5) circled Arabic |
| 5 | Intermediate | Weeks – months | 1...5 plain Arabic |
| 4 | Minor | Days – weeks | 1...5 plain Arabic, smaller font |
| 3 | Minute | Hours – days | i...v Roman lower |
| 2 | Minuette | Minutes – hours | i...v Roman lower |
| 1 | Subminuette | Sub-minute | (i)...(v) circled lower |

**Key point — degree is relative, not absolute.** Frost & Prechter (Ch. 2, p. 67):
*"The degree of a wave is determined by its size and position relative to component,
adjacent, and encompassing waves."* There is no absolute price or time threshold that
maps a wave to a degree. A Primary-degree wave on a commodity might span 3 months;
on an equity index it might span 3 years. Degree is an *ordinal label within a fractal
hierarchy*, not an absolute timestamp bin.

**Practical corollary:** A multi-year, multi-hundred-percent equity bull run spanning
~16 years (AVGO 2009–2026) is, by any reasonable application of Frost & Prechter's
proportionality principle, at least **Cycle degree** (7), more likely **Supercycle**
(8) or **Grand Supercycle** (9). It is categorically NOT Minuette (2) or Minute (3).
Calling it Minute/Minuette inverts the entire hierarchy.

### 1.2 How Degree Should Be Assigned (Neely Bottom-Up + Proportionality)

Neely (*Mastering Elliott Wave*, 1990; neowave.com Q&A archive
https://www.neowave.com/qow/qow-archive-13.asp) provides the most operational
algorithm. The three interdependent anchors are:

**A — Monowave complexity window.** A complete pattern at a given degree should
subsume **13–55 monowaves** (the ideal window is 21–34) at the degree-0 pivot stream.
Fewer than 13 monowaves → the count is too coarse for that degree label (promote it
one level up). More than 55 → the count is too fine for that degree label (demote one
level down). This is cited in the project's own doc `docs/research/deep/07_auto_labeling_and_anchoring.md` §3.3.

**B — Relative size / proportionality within the parent structure.** When a count
is a sub-wave inside a larger degree, it must be proportionally smaller than its
siblings. A wave-1 at Intermediate degree should be roughly the same magnitude as
its wave-3 and wave-5 siblings; each of those, in turn, is larger than any Minor-
degree sub-wave they contain.

**C — Top-down cross-check.** After a bottom-up assignment, check whether the
resulting primary count fits *inside* an identifiable higher-degree pattern at the
coarser pivot stream. Alignment → `degree_confidence = "CONFIRMED"`. No alignment →
`"HEURISTIC"`.

The canonical inference path for a 16-year bull market with ~100x price appreciation:
1. The series spans vastly more monowaves than the 13–55 Neely window → the single
   pattern seen is at a degree well above Minute.
2. AVGO 1D has 4 234 bars and yields 17 monowaves (full range, per WAVE_COUNTS report).
   Even 17 monowaves exceeds 55 only if those monowaves are themselves degree-1 nodes.
   The full-range Neely sweep at weekly scale (21 monowaves over 879 bars) suggests a
   structure whose correct label is at minimum **Primary** or **Cycle** degree.

### 1.3 What a Sound Full-Range Auto-Labeler Should Do

Per `docs/research/deep/07_auto_labeling_and_anchoring.md` §3.6 (pseudo-Viterbi DP):

1. **Full-range segmentation.** The primary count should be the DP-optimal
   non-overlapping partition that covers the *entire pivot sequence*. Coverage
   close to 100 % is a property of a correct global parse, not a lucky by-product.
2. **Degree from monowave count.** After the full-range cover is found, count the
   degree-0 monowaves it subsumes. The Neely 13–55 window maps this number to a
   degree label. A 16-year series at weekly granularity subsuming >100 monowaves
   is unambiguously above Minute degree.
3. **Proportionality is the primary check.** Degree is assigned *relative* to the
   series being analysed, not via an absolute time or bar-count lookup table.

---

## 2. What the Code Does

### 2.1 Tree-Building: `_build_level` (wavetree.py:223–261)

`build_tree_from_pivots` → `build_wave_tree` runs a greedy bottom-up compaction DP
that at each level tries to merge adjacent nodes into 5-groups (impulse/diagonal/
triangle) and 3-groups (correction). The function iterates from degree 1 up to
`max_levels=6` and stops when no new merges occur.

**The DP only looks locally.** At each index `i`, it tries groups of size 5 or 3
starting at `i`. If neither produces a validated node, the singleton is carried
forward (score 0). The DP thus greedily fills what it can, **but it does not
enforce full coverage**. Any span of pivots that does not fit into a 5-group or
3-group is silently carried as an ungrouped singleton. Singletons do not become
part of the named pattern.

Result: many real price series yield **multiple root nodes** — a dominant validated
pattern covering part of the series plus several ungrouped monowave singletons
on either side.

### 2.2 Coverage Computation: `wave_counts` / `_scale_score` (wavetree.py:387–403, 376–384)

```python
# wavetree.py:396-402
total = sum(_span(r) for r in roots) or 1.0
top, conf, score = _scale_score(roots)
...
out.append((score, _anchored_from(top, conf, _span(top) / total)))
```

`_span(r)` is `r.end.t - r.start.t` — the **time-span** of one root node.
`coverage = _span(top) / total` where `total` is the sum of ALL root nodes' spans,
including ungrouped singletons.

**Critical:** `total` includes only the spans of nodes that the DP *did* produce —
i.e. the union of all root nodes. If the confirmed-pivot stream has a gap at either
end (the first or last pivot is not incorporated into any group), those bars are
**excluded from `total` entirely**. The fraction `_span(top)/total` can therefore
be artificially inflated if uncovered bars are simply absent from `total`, OR it
can be low if the ungrouped singletons together span more time than the top pattern.

For AVGO 1D, the pivot stream starts around 2009 but the best validated pattern
covers only 2013–2018. The bars from 2009–2013 and 2018–2026 appear as ungrouped
monowave singletons. Those singletons do appear in `roots`, their spans do appear
in `total`, so `_span(top)/total ≈ 0.29`. The remaining 71 % is ungrouped.

### 2.3 Selection: `wave_counts` picks the LOCALLY-BEST, not the GLOBALLY-BEST COVER

```python
# wavetree.py:380-383  (_scale_score)
top = max(roots, key=_span)   # ← the single root with the LONGEST time-span
conf = tree_confidence(roots)
score = conf * (bonus for motive patterns)
```

`wave_counts` runs the tree at several ZigZag scales, selects the highest-scoring
`top` across scales, and **returns that top node as the primary count**. It does NOT
ask: "which segmentation covers the full series?" It asks: "which single root node,
across all scales, has the best score?"

If a 29%-coverage ZIGZAG at scale 0.08 has higher `tree_confidence` than a 90%-
coverage fragmented set at scale 0.04, the ZIGZAG wins. Coverage is only an
*implicit* input (via `tree_confidence`, which penalises fragmentation) — it is
never a *hard requirement*.

### 2.4 Degree Assignment: `anchored_degree` (wavetree.py:353–363)

```python
def anchored_degree(node) -> Degree:
    m = _count_monowaves(node)
    if m < 13:
        return Degree.MINUETTE       # value=2
    if m <= 55:
        return Degree.MINUTE         # value=3
    if m <= 144:
        return Degree.MINOR          # value=4
    return Degree.INTERMEDIATE       # value=5
```

This function counts only the monowaves **within the winning `top` node** (the
29%-coverage ZIGZAG for AVGO 1D). It does NOT count monowaves in the entire
series, and it does not count monowaves in the full-range count — only those
inside the locally-best sub-pattern.

**The thresholds are hard-coded absolute counts**, not relative proportionality
checks. A 29%-coverage ZIGZAG over 2013–2018 contains a small number of monowaves
(the ZigZag has 3 children, each containing a handful of sub-monowaves). That
count is virtually guaranteed to fall below 13 (→ MINUETTE) or between 13–55
(→ MINUTE). The 16-year macro story is invisible to this function because it was
never chosen as the `top` node.

Even if a full-range node were chosen, a 16-year series on a daily chart would
subsume hundreds of monowaves — far above the 144-monowave INTERMEDIATE ceiling.
The function has no case for PRIMARY (value=6), CYCLE (value=7), or anything above
INTERMEDIATE. The ceiling is hard-capped at INTERMEDIATE regardless of how large
the move is.

### 2.5 The Degree Enum Mapping (rules.py:47–55)

```python
class Degree(Enum):          # rules.py:38–55
    GRAND_SUPERCYCLE = 9
    SUPERCYCLE = 8
    CYCLE = 7
    PRIMARY = 6
    INTERMEDIATE = 5
    MINOR = 4
    MINUTE = 3
    MINUETTE = 2
    SUBMINUETTE = 1
```

The Degree enum is correctly defined with all nine levels. However, `anchored_degree`
(wavetree.py:353–363) only ever returns MINUETTE, MINUTE, MINOR, or INTERMEDIATE.
CYCLE, PRIMARY, SUPERCYCLE, GRAND_SUPERCYCLE are unreachable from the degree-
assignment path. The top four degrees are dead code for the purposes of labelling.

### 2.6 The `label_and_validate` Path (automation.py:75–109)

`label_and_validate` slides a 6-pivot (5-wave) or 4-pivot (3-wave) window over the
pivot stream and evaluates each sub-sequence independently. It returns a flat ranked
list of `CandidateCount` objects, each covering a **local window** of 3–5 waves.
There is no global segmentation step. The `degree` field on each candidate is the
`di` (scale index: 0=finest, 1=medium, 2=coarsest), **not** an Elliott degree label.

`assign_degrees_neely` (automation.py:131–159) runs a bottom-up promotion loop but
stops when no further compaction is possible or when fewer than 4 promoted pivots
remain. It promotes groups at each degree but **does not enforce that the final
promoted set spans the entire original series**. Gaps at either end of the series
are silently dropped.

---

## 3. Mistake Table

| # | Theory Requirement | Code Behaviour | Verdict | Severity | How It Causes the Symptom |
|---|--------------------|----------------|---------|----------|--------------------------|
| M1 | **Full-range coverage is a hard requirement.** The primary count must be a non-overlapping partition covering the entire confirmed-pivot sequence. A partial cover is an alternate count, not a primary. (Frost & Prechter: the "primary count" is the analyst's *best view of the complete chart*; 07_auto_labeling §3.6 global Viterbi requirement.) | `wave_counts` (wavetree.py:387–403) selects the highest-`score` root across ZigZag scales. Score is `tree_confidence × motive_bonus`. `tree_confidence` (wavetree.py:306–314) is `top.confidence × (_span(top) / total)`, but `total` is only the sum of the spans the DP *did* produce. Coverage is never enforced as a floor or a hard constraint — it is only one implicit factor in an unconstrained maximisation. A 29%-coverage ZIGZAG with high local confidence will beat a 90%-coverage fragmented set with moderate confidence. | WRONG — **coverage is treated as a soft quality signal, not a hard constraint** | **CRITICAL** | Directly causes the 29%/40% coverage failure. The engine selects a high-quality local sub-pattern as the primary count because no constraint forces the winner to cover the full range. |
| M2 | **Degree must reflect absolute scale of the series.** A 16-year ~100x bull run is at minimum Primary (6) / Cycle (7) degree. No absolute monowave-count threshold maps correctly to such a large-scale structure — the threshold must be applied to the *full-range* node, not a partial sub-pattern. (Frost & Prechter Ch. 2; Neely §3.7 in 07_auto_labeling.) | `anchored_degree` (wavetree.py:353–363) counts monowaves *only within the winning partial top node* — a node covering 2013–2018 with ~3–10 sub-monowaves. The count falls below 13 (→ MINUETTE) or 13–55 (→ MINUTE). The 16-year context is invisible because the full-range node was never chosen as `top`. Additionally, the function has no cases for PRIMARY, CYCLE, SUPERCYCLE, GRAND_SUPERCYCLE; the ceiling is hard-capped at INTERMEDIATE even if a full-range node were somehow chosen. | WRONG — **degree is computed on the wrong node AND capped at INTERMEDIATE** | **CRITICAL** | Directly causes the "Minuette/Minute" label on a 16-year move. Two independent bugs: (a) the input node is the wrong (partial) node; (b) the lookup table is truncated at INTERMEDIATE. |
| M3 | **The global DP should segment the entire pivot sequence without gaps.** Per 07_auto_labeling §3.6, the Viterbi DP must cover every pivot with either a validated pattern or an explicit "uncovered" penalty. Pivots not reached by any validated group must contribute to a gap-penalty signal, not silently disappear. | `_build_level` (wavetree.py:223–261) carries ungrouped nodes as singletons (degree unchanged). There is no gap penalty. Singletons after the last validated group, and before the first, are silently retained as degree-0 MONOWAVE roots. `wave_counts` then selects the longest single validated root rather than the best global *cover*. The DP solves "best local pattern" rather than "best complete partition". | WRONG — **DP is not a covering DP; it is a local-best DP** | **HIGH** | Enables M1: because the DP never requires coverage, every scale trial will produce a fragmented root set, and the "best" root by score will always be a local sub-pattern. The full-range count can never be *forced* by the current DP structure. |
| M4 | **Degree lookup must be applied to the full-range count, not the selected sub-pattern.** Even if the partial-coverage count is accepted as primary (which it should not be — see M1), degree should be inferred from the full-range series' monowave density, not from the 29%-coverage node. Per Neely's proportion rule, degree is about the *series context*, not the isolated count. | `_anchored_from` (wavetree.py:366–373) passes `top` (the partial root) directly to `anchored_degree(top)`. There is no step that looks at the full-series monowave count, nor a comparison to the series' total bar span. | WRONG — **degree lookup input is scoped too narrowly** | **HIGH** | Amplifies M2. Even if M2's ceiling were fixed (by adding PRIMARY/CYCLE/etc. cases), the function would still return Minute for a 29%-coverage 5-year sub-structure, which is wrong relative to the 16-year context. |
| M5 | **The ZigZag scales used in `wave_counts` must produce at least one scale coarse enough to resolve the full-range structure.** For AVGO 1D (4 234 bars, $3–$415), a move spanning the full range requires a ZigZag threshold that produces ~5–21 pivots over the full series. | `wave_report.py` passes `scales=(0.04, 0.08, 0.14, 0.22)` for 1D (wave_report.py:28). At 4% the pivot stream is still very dense (many short-term pivots); 22% is the coarsest. The coarsest scale may reduce the pivot count enough to group into a coherent count, but the selection function (`_scale_score`) does not guarantee the full-range count wins if a finer-scale local pattern scores higher. | WRONG/INCOMPLETE — **no scale is explicitly targeted at producing a full-range 5–21 pivot stream; the coarser scales compete unfairly against higher-confidence fine-scale local patterns** | **MEDIUM** | Contributes to coverage failure: even if the 22% scale produces a full-range count, `wave_counts` may still pick a 4–8% scale result with higher local confidence. |
| M6 | **The `Degree` enum upper range (PRIMARY, CYCLE, SUPERCYCLE, GRAND_SUPERCYCLE) must be reachable from `anchored_degree`.** The enum is correctly defined (rules.py:47–55) but the assignment function silently caps at INTERMEDIATE. | `anchored_degree` (wavetree.py:353–363) has no `elif m > 144` branch returning Degree.PRIMARY or higher. It returns `Degree.INTERMEDIATE` for any node with more than 144 sub-monowaves, regardless of whether the series clearly spans Primary or Cycle degree. | WRONG — **dead code / silent cap** | **MEDIUM** | Even for a correctly-chosen full-range node subsuming 300+ monowaves, the label "Intermediate" is returned instead of "Primary" or "Cycle". The enum has 9 levels; the assignment function uses only 4 of the bottom 5. |
| M7 | **`label_and_validate` uses `degree` to mean ZigZag scale index (0/1/2), not Elliott degree.** The `CandidateCount.degree` field is presented externally as if it were an Elliott degree label but is merely the index into the `degrees` tuple argument. | `automation.py:91`, `automation.py:68–72`: `degree=di` where `di` is the loop index 0, 1, or 2. The CandidateCount docstring says "scale index: 0=Minor, 1=Intermediate, 2=Primary" — which is a guess at Elliott degree from scale position, not a computed value. These aliases are incorrect and misleading (scale index 0 could be any degree depending on the data). | WRONG — **semantic conflation of scale index with Elliott degree** | **MEDIUM** | Not a direct cause of the observed coverage/degree symptoms (those are in `wavetree.py`), but it perpetuates degree confusion across the codebase and will mislead any downstream consumer of `label_and_validate` output. |

---

## 4. Concrete Fixes

### Fix F1 — Enforce Full-Range Coverage as a Hard Constraint (addresses M1, M3)

**Target:** `wavetree.py:wave_counts` + `wavetree.py:_build_level`

The current DP selects the best *local* validated root. Replace with a
**covering-DP** that maximises score subject to covering all pivots.

**Step 1 — Modify `_build_level` to track coverage.**

The DP state `best[i]` should represent "the best segmentation of nodes[i:]".
Currently it already does this, but the "carry singleton" branch assigns score 0
for uncovered nodes. Replace score 0 with a **gap penalty** (e.g., −0.1 per
uncovered monowave) so that uncovered spans have an explicit cost:

```python
# wavetree.py:_build_level — proposed change at the carry branch:
GAP_PENALTY = 0.1  # per uncovered node
carry_score, carry_list = best[i + 1]
cand = (carry_score - GAP_PENALTY, [nodes[i]] + carry_list)  # penalise gap
```

This does not force coverage but prices it, making the DP naturally prefer
covers over local optimisations.

**Step 2 — Add a `full_range` pass to `wave_counts`.**

After collecting per-scale results, add a final "full-range forcing" pass:

```python
# In wave_counts, after the per-scale loop:
# Force a full-range pass at the coarsest scale in the caller's scale list
# and include it even if it scores lower than a partial local count.
# This guarantees at least one full-range candidate in the output.
coarsest_scale = max(scales)
roots_coarse = build_wave_tree(bars, base_pct=coarsest_scale)
if roots_coarse:
    total = sum(_span(r) for r in roots_coarse) or 1.0
    # Build a synthetic full-range node spanning ALL roots if no single root covers all
    # ... (see implementation detail below)
```

A simpler equivalent: always include a "full-range MONOWAVE" fallback root
spanning `pivots[0]` to `pivots[-1]` so that `_span(top)/total` always has
a denominator that includes the full series span.

**Step 3 — Add `min_coverage` parameter to `wave_counts`.**

```python
def wave_counts(bars, scales=(0.04, 0.07, 0.12, 0.20),
                max_alternates: int = 3,
                min_coverage: float = 0.0):  # 0.0 = no enforcement (current behaviour)
    ...
    # After collecting all (score, AnchoredCount) pairs:
    # Prefer counts meeting min_coverage; fall back to best available if none do.
    qualifying = [(s, ac) for s, ac in out if ac.coverage >= min_coverage]
    pool = qualifying if qualifying else out
    pool.sort(key=lambda x: -x[0])
    return [ac for _, ac in pool][:1 + max_alternates]
```

Recommended default: `min_coverage=0.75` for production use.

---

### Fix F2 — Assign Degree From the Full-Range Series, Not the Selected Node (addresses M2, M4)

**Target:** `wavetree.py:anchored_degree` + `wavetree.py:_anchored_from`

**Step 1 — Extend `anchored_degree` to cover all nine Degree levels.**

The existing table only returns MINUETTE, MINUTE, MINOR, or INTERMEDIATE.
Add the upper four levels and calibrate the thresholds to Neely's published
window (13–55 = one degree, roughly doubling per degree):

```python
def anchored_degree(node, series_monowave_count: int = None) -> Degree:
    """
    Estimate Elliott degree.
    If series_monowave_count is provided, it is used for proportionality;
    otherwise falls back to counting monowaves within `node` (partial-cover bias).
    """
    m = series_monowave_count if series_monowave_count is not None else _count_monowaves(node)
    # Neely complexity window, extended to all nine degrees.
    # Each tier is ~2x the prior (Neely's fractal proportion rule).
    if m < 13:
        return Degree.SUBMINUETTE   # fewer than 13: below Minuette
    if m <= 34:
        return Degree.MINUETTE
    if m <= 55:
        return Degree.MINUTE
    if m <= 89:
        return Degree.MINOR
    if m <= 144:
        return Degree.INTERMEDIATE
    if m <= 233:
        return Degree.PRIMARY
    if m <= 377:
        return Degree.CYCLE
    if m <= 610:
        return Degree.SUPERCYCLE
    return Degree.GRAND_SUPERCYCLE
```

The Fibonacci sequence (13, 21, 34, 55, 89, 144, 233, 377, 610) is the natural
grid for Neely's complexity window — it is both internally consistent with
Elliott's original fractal observation and matches the published 13–55 range.

**Step 2 — Pass full-series monowave count into `_anchored_from`.**

```python
def _anchored_from(top, confidence, coverage,
                   full_series_monowaves: int = None) -> AnchoredCount:
    ...
    deg = anchored_degree(top, series_monowave_count=full_series_monowaves)
    return AnchoredCount(top.pattern, top.degree, labels, confidence, coverage,
                         deg.name.replace("_", " ").title(), note)
```

And in `wave_counts`, compute the full-series monowave count once:

```python
# Before the scale loop in wave_counts:
# Count degree-0 monowaves in the finest-scale pivot stream
finest_roots = build_wave_tree(bars, base_pct=min(scales))
full_mono = sum(_count_monowaves(r) for r in finest_roots) if finest_roots else None
# Pass full_mono to _anchored_from at every scale
...
_anchored_from(top, conf, _span(top) / total, full_series_monowaves=full_mono)
```

This separates the structural quality of the selected pattern (which might
cover only 29% of the range) from the degree label (which should reflect the
whole series context).

---

### Fix F3 — Fix the Degree-Ceiling Hole in `anchored_degree` (addresses M6)

This is a subset of F2 Step 1. The simplest one-line fix is:

```python
# wavetree.py:anchored_degree — current last line:
    return Degree.INTERMEDIATE   # ← BUG: hard ceiling at INTERMEDIATE

# Replace with a branching ladder that includes PRIMARY, CYCLE, SUPERCYCLE, GSC
# (see full table in Fix F2 Step 1 above).
```

Without F2, this standalone fix still provides partial benefit: at least the
correct degree name will appear in the output if the right node is ever selected.

---

### Fix F4 — Fix the ZigZag Scale Range to Guarantee at Least One Full-Range Pass (addresses M5)

**Target:** `wavelib/wavetree.py:wave_counts` default scales and `scripts/wave_report.py:TFS`

For a series of N bars, the minimum ZigZag threshold that produces a ~5–21 pivot
stream can be estimated as:

```
min_pct ≈ (price_range / reference_price) / (target_pivot_count / 2)
```

For AVGO 1D (range $3–$415, N=4234 bars): `range/ref = 412/415 ≈ 0.993`.
To get ~10 pivots: `min_pct ≈ 0.993 / 5 ≈ 0.20`. The current coarsest scale
(0.22) is about right for AVGO 1D but is not guaranteed to produce a clean
global count because the score function may still prefer a finer-scale local
pattern.

**Recommended change:**

1. Add a `coarse_scale` parameter to `wave_counts` whose value is auto-selected
   as `max(scales) * 1.5` or until fewer than 25 pivots remain.
2. Always run one pass at `coarse_scale` and include the result in the candidate
   pool, even if it scores lower than other candidates (see Fix F1 Step 2).

---

### Fix F5 — Correct `CandidateCount.degree` Semantics in `automation.py` (addresses M7)

**Target:** `automation.py:68–72`, `automation.py:91`, docstring

```python
# automation.py:68 — current:
    return CandidateCount(list(pivots), list(waves), ctype, list(results),
                          hard, warns, _fib_score(waves), degree)   # degree = scale index

# Rename the parameter to clarify:
# Change CandidateCount.degree to CandidateCount.scale_index (int)
# Add CandidateCount.degree_label: Optional[str] = None  # populated after anchoring
```

The docstring comment "0=Minor, 1=Intermediate, 2=Primary" should be removed or
corrected; scale index 0 is the finest scale, not necessarily Minor degree.

---

## 5. Summary

Five lines + top-three mistakes:

1. The engine's primary count is selected by local score-maximisation, not by full-
   range coverage — a 29%-coverage high-quality sub-pattern beats a 90%-coverage
   fragmented global count because coverage is a soft penalty, not a hard constraint.
2. Degree is assigned from the monowave count of the *selected partial node*, not
   the full series; a 29%-coverage ZIGZAG over 2013–2018 naturally has few sub-
   monowaves → MINUETTE/MINUTE.
3. `anchored_degree` hard-caps at INTERMEDIATE; PRIMARY, CYCLE, SUPERCYCLE, and
   GRAND_SUPERCYCLE are unreachable regardless of series size.

---

### TOP 3 MISTAKES (WITH SEVERITY)

**Mistake 1 — No full-range coverage constraint (M1 / M3) — CRITICAL**

`wave_counts` + `_build_level` have no mechanism to force or prefer a count that
spans the entire pivot sequence. The DP maximises per-segment quality, allowing
a 29%-coverage local pattern to win. Fix: (a) gap-penalty in the carry branch of
`_build_level`; (b) `min_coverage` parameter in `wave_counts`; (c) always include
a full-range forcing pass at the coarsest scale. See Fix F1.

**Mistake 2 — Degree computed on the wrong node (M2 / M4) — CRITICAL**

`anchored_degree(top)` (wavetree.py:353) counts only the monowaves inside `top`,
which is the 29%-coverage partial node. The degree of a 16-year series is
determined by the full-series context, not by the count of sub-monowaves inside
a 5-year sub-pattern. Fix: pass `full_series_monowaves` to `anchored_degree` and
compute it once from the finest-scale tree before the scale loop. See Fix F2.

**Mistake 3 — `anchored_degree` ceiling hard-capped at INTERMEDIATE (M6) — MEDIUM**

The function returns `Degree.INTERMEDIATE` for every series subsuming more than
144 monowaves, silently suppressing the PRIMARY, CYCLE, SUPERCYCLE, and
GRAND_SUPERCYCLE tiers. The `Degree` enum (rules.py:47–55) has all nine levels;
`anchored_degree` uses only four of the five lowest. Fix: extend the lookup table
with Fibonacci-spaced thresholds up to GRAND_SUPERCYCLE. See Fix F3.

---

## Sources

- Frost, A.J. & Prechter, R.R. *Elliott Wave Principle*, 10th ed. (2005).
  https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf
- Wikipedia — Elliott Wave Principle:
  https://en.wikipedia.org/wiki/Elliott_wave_principle
- Elliott Wave Insight — Degrees & Labeling:
  https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/
- Neely, G. *Mastering Elliott Wave* (1990). Q&A on degree:
  https://www.neowave.com/qow/qow-archive-13.asp
- Ewace_2026 prior research: `docs/research/deep/07_auto_labeling_and_anchoring.md`
  (§3.3 Neely bottom-up promotion, §3.6 global Viterbi DP, §3.7 degree anchoring)
- Ewace_2026 prior research: `docs/research/01_elliott_wave.md` §2.5 (degree hierarchy)
- Ewace_2026 report: `reports/WAVE_COUNTS_AVGO_MRVL.md` (empirical coverage values)
- Code: `wavelib/wavetree.py:223–261` (`_build_level`)
- Code: `wavelib/wavetree.py:353–363` (`anchored_degree`)
- Code: `wavelib/wavetree.py:376–403` (`_scale_score`, `wave_counts`)
- Code: `wavelib/wavetree.py:298–314` (`deepest_degree`, `tree_confidence`)
- Code: `wavelib/automation.py:68–109` (`label_and_validate`, `_make_candidate`)
- Code: `wavelib/rules.py:38–55` (`Degree` enum)

*Audit written June 2026. Code not modified.*
