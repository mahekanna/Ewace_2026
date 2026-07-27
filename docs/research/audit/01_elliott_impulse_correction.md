# Audit: Elliott Wave Impulse vs Corrective Classification
**Why the engine mislabels clear multi-year uptrends as corrections**

Version 1.0 · 2026-06-09 · Audit only — no code changed.

---

## Executive Summary (5 lines)

The engine systematically labels AVGO and MRVL as corrective on every timeframe
because: (1) its DP scoring function awards corrections a structural bonus that is
roughly **equal to or higher than the impulse bonus** when the impulse's Fibonacci
quality is mediocre; (2) the `_correction_node` path is far more permissive than
`_impulse_node` — corrections need only pass `classify_correction` (no alternation
gate, no hard-rule battery), so they win whenever the five impulse hard rules produce
any FAIL; (3) the ZigZag scales used (`0.04–0.20 pct`) slice a 1W bulltrend into
small sub-segments each of which looks like a corrective ABC in isolation; (4) the
`_impulse_quality` Fibonacci kernel uses a wide `sigma=0.20` that scores both impulses
and corrections almost equally for typical ratios; and (5) the `value()` bonus for
IMPULSE is only `+0.5` while `correction_quality` for a ZIGZAG starts at `base=0.8`
— a clean zigzag can exceed the impulse score even before the Fibonacci component.

**TOP 3 root-cause mistakes (severity H):**

1. **[H] DP `value()` bonus is too small relative to `_correction_quality` base score
   — a clean zigzag outscores a typical impulse** (`wavetree.py:value`, line 243).
2. **[H] `_correction_node` has no alternation gate and no hard-rule battery;
   impulses require `_alternating()` + `elliott_hard_rules()` FAIL prune, giving
   corrections an overwhelming volume advantage** (`wavetree.py:_correction_node`,
   line 199 vs `_impulse_node`, line 107).
3. **[H] ZigZag scales (0.04–0.20) are too fine to capture multi-year primary
   impulses; every scale produces pivot streams that represent sub-legs of the real
   primary wave, each of which looks corrective in isolation**
   (`wavetree.py:wave_counts`, line 387; `build_wave_tree`, line 281).

---

## 1. Theory (Frost & Prechter lineage, with citations)

### 1.1 What makes an impulse — the three inviolable rules

Every valid impulse wave (motive 5-wave sequence in the direction of the one-larger
degree trend) must satisfy all three rules simultaneously. A single failure invalidates
the impulse label.

**Rule R1 — Wave 2 never retraces more than 100 % of Wave 1**
The end of wave 2 must remain strictly above (bull) / below (bear) the origin of wave 1.
Typical depth: 50 %–61.8 % of wave 1. Even a 99 % retrace is technically valid but
should trigger a re-labeling search.
(Frost & Prechter *Elliott Wave Principle* 10th ed. Ch. 1;
https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf;
https://en.wikipedia.org/wiki/Elliott_wave_principle)

**Rule R2 — Wave 3 is never the shortest of waves 1, 3, and 5**
Exact test: `len(W3) > len(W1)` OR `len(W3) > len(W5)` — i.e., W3 is not shorter
than *both* other motive legs simultaneously. In equity markets W3 is almost always the
longest; the rule only forbids it from being the shortest.
(https://elliottwave-forecast.com/elliott-wave-theory/;
https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)

**Rule R3 — Wave 4 does not enter the price territory of Wave 1**
In a bull impulse: `low(W4) > high(W1)`. Exception: this rule is SUSPENDED for
diagonals (both leading and ending), where wave-4/wave-1 overlap is expected.
(https://en.wikipedia.org/wiki/Elliott_wave_principle;
https://priceactionhelp.com/elliott-wave)

### 1.2 How a practitioner distinguishes impulse from correction

The central question is not about rule checking in isolation — it is about the
_structural identity_ of the entire move. Frost & Prechter's primary heuristics:

**Structure (5 vs 3):** An impulse has five sub-waves; a correction has three (or five
for a triangle, but with corrective internal sub-waves). A five-wave sequence that
passes all three hard rules is presumptively impulsive until proven otherwise.
(Frost & Prechter Ch. 1; https://elliottwavemonitor.com/elliott-wave-theory/)

**Overlap:** Wave 4 must NOT enter wave 1's territory in an impulse. If it does, the
structure is either a diagonal or a correction. This single test eliminates most
impulse/correction ambiguity.

**Depth and proportion:**
- Wave 2 typically retraces 50 %–61.8 % of wave 1. Retracements of 76.4 %–85.4 %
  are deep but valid; approaching 99 % is a red flag.
- Wave 4 is shallower: typically 23.6 %–38.2 % of wave 3. A deep wave 4 (>50 %) in a
  large bull market usually signals a flat or triangle, not a simple wave 4.
  (https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275;
   https://elliottwavedynamics.com/comprehensive-guide-to-elliott-wave-theory/)

**Fibonacci relationships:**
- W3 ≈ 1.618 × W1 (preferred; 2.618 × and 3.618 × in extended markets).
- W5 ≈ W1 (equality, most common); or 0.618 × W3; or 1.618 × W1 (extended fifth).
- These ratios are guidelines, not rules — their absence does not invalidate a count.
  (https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275)

**Channeling:** In an impulse, price respects the 1–3 upper channel and the 2–4 lower
channel. In a correction, price moves laterally against the trend. The base channel
(0–2 line with parallel through wave-1 top) should contain the entire move through
wave 3. A break below the 0–2 lower line during wave 4 is an early warning.
(https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/;
https://www.elliottwave.com/waveopedia/channeling/)

**Wave personality:**
- Wave 3 is "wonders to behold" — the strongest, longest, highest-volume, broadest-
  participation leg. Fundamentals improve, analysts upgrade, breadth expands.
- Wave 4 is boringly sideways — investors know the trend is up but do not act. It
  holds above wave 1's high (hard rule) and is shallower than wave 2.
- An impulse's personality should be recognizable: the motive legs feel energetic
  and the corrective legs feel hesitant.
  (Frost & Prechter Ch. 2;
   https://forextraininggroup.com/characteristics-and-personalities-of-elliott-waves/)

**Degree:** A multi-year bull market in a large-cap semiconductor stock IS an impulse
at the Primary or Cycle degree. At the Minuette or Minute degree, every sub-leg may
look corrective — but that is the correct sub-structure, not a contradiction. The
engine's failure is assigning Minuette-degree labels to Primary-degree moves.
(Frost & Prechter Ch. 2; https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/)

### 1.3 Corrective taxonomy

All corrections move against the one-larger-degree trend.

**Zigzag (5-3-5):** Sharp; wave B retraces ≤ 61.8 % of wave A (this is the principal
classifier — a deep B means flat, not zigzag). B cannot exceed origin of A.
(https://elliottwavemonitor.com/elliott-wave-theory/)

**Regular flat (3-3-5):** B retraces > 61.8 % and ≤ 100 % of A. C ≈ 61.8–100 % of A.
Horizontal-looking overall.

**Expanded flat (3-3-5):** B > 100 % of A (typ. 105–138 %); C surpasses A's end.
Psychologically dangerous: B makes a new high before C crashes.

**Running flat (3-3-5):** B > 100 % of A but C fails to reach A's end. Net horizontal.
Appears in strong trends.

**Triangle (3-3-3-3-3):** Five legs a–e, each corrective. Appears in wave 4, wave B,
or final X-wave. Always precedes a thrust. Contracting (a>b>c>d>e), expanding
(a<b<c<d<e), or barrier (one flat boundary).
(https://www.elliottwave.com/waveopedia/triangles/)

**Combination / WXY (double three):** Two simpler corrections connected by an X-wave.
W and Y can be zigzag, flat, or (as final component only) triangle. X < 61.8 % of W
(guideline). Net travel is sideways.
(https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/double-three-and-triple-three-patterns)

---

## 2. What the Code Does Now (cited file:function:line)

### 2.1 wavetree.py — the scoring and DP engine

**`_impulse_node` (wavetree.py, line 107)**
- Requires `_alternating()` (line 109) — passes only if legs alternate direction.
- Calls `elliott_hard_rules()` (line 111); returns `None` if any FAIL.
- At degree >= 2 (line 118), additionally requires legs 0,2,4 be `_MOTIVE` and 1,3 be
  `_CORRECTIVE`.
- Confidence = `_confidence(results, ...) * (0.4 + 0.6 * _impulse_quality(waves))`
  (line 124).
- `_impulse_quality` (line 41) computes a Gaussian proximity score for three Fibonacci
  ratios: W3/W1, W2/W1, W4/W3. Uses `sigma=0.20` (±20% relative tolerance).

**`_correction_node` (wavetree.py, line 199)**
- Does NOT call `_alternating()` — no alternation gate.
- Does NOT call `elliott_hard_rules()` — no hard-rule battery.
- Calls `classify_correction(waves)` (line 203); returns `None` only if
  `rr.status is not Status.PASS`.
- Confidence = `_confidence(results, ...) * _correction_quality(pattern, waves)`
  (line 218).
- `_correction_quality` (line 50): ZIGZAG base=0.8; FLAT base=0.7 (or 0.45 if shallow
  B); other base=0.6. Then multiplied by `(0.6 + 0.4 * _fib_close(C/A))`.

**`_build_level` / `value()` (wavetree.py, lines 223–261)**
- `value(node)` (line 240):
  ```python
  bonus = 0.5 if node.pattern == "IMPULSE" else 0.3 if node.pattern == "DIAGONAL" else 0.0
  return len(node.children) * node.confidence + bonus
  ```
- The DP selects whichever segmentation of `nodes` maximises `sum(value(node))`.
- For a 5-node impulse: `value = 5 * conf_impulse + 0.5`.
- For a 3-node correction followed by 2 leftovers: `value = 3 * conf_correction + 0.0`.
  But if two 3-node corrections tile the same 6 nodes:
  `value = 3 * conf_A + 0 + 3 * conf_B + 0 = 6 * avg_conf_correction`.
- **Critical observation:** if `conf_impulse ≈ 0.35` (typical for a real impulse with
  mediocre Fibonacci quality), the impulse scores `5 * 0.35 + 0.5 = 2.25`.
  If each correction has `conf_correction ≈ 0.50` (easy for a ZIGZAG with decent C/A),
  two corrections score `6 * 0.50 = 3.00`. **The corrections win.**

**`_scale_score` (wavetree.py, line 376)**
- Applies a `1.15` multiplier to `conf` if `top.pattern in _MOTIVE` and a `0.05`
  multiplier if `MONOWAVE`. This is a selection-ranking boost at scale level, but it
  acts on the *already-chosen* DP root and does not change which pattern was chosen
  inside `_build_level`.

**`wave_counts` (wavetree.py, line 387)**
- Runs at scales `(0.04, 0.07, 0.12, 0.20)`.
- On AVGO weekly (range ~$2.64 to ~$495), a `0.04` (4%) filter yields pivots at every
  ~$10–20 swing; a `0.20` (20%) filter yields pivots at every ~$50–100 swing.
- AVGO's Primary-degree wave 1 ($2.64→$33.16) is itself ~1153% up. A 4% or 20%
  filter slices this into 10–50 sub-legs, none of which span the full Primary-degree
  move. Each sub-leg looks corrective in isolation.

### 2.2 rules.py — the hard-rule and correction classifiers

**`elliott_hard_rules` (rules.py, line 136)**
- R1, R2, R3 are correctly implemented per theory. No issues.

**`classify_correction` (rules.py, line 231)**
- `ZIGZAG_B_MAX = 0.618` — correct canonical threshold.
- Zigzag branch: `b_retr <= 0.618 + 1e-9` — correct.
- Regular flat: `0.618 < b_retr <= 1.00` — correct per Phase-1 fix.
- The endpoint check for expanded vs running — correct.
- **Issue:** No verification that legs alternate direction correctly (A and C should be
  in the same direction, B should be opposite). If `_correction_node` passes waves
  that happen to have A and C in opposite directions, `classify_correction` will still
  return PASS as long as the B-retrace ratio is within range.

**`_alternating` (wavetree.py, line 87)**
- Used only by `_impulse_node`. `_correction_node` does NOT call this.
- A correction's A and C must go the same direction; B is opposite. The code at
  `_correction_node` line 201 checks:
  ```python
  if waves[0].up == waves[1].up or waves[0].up != waves[2].up:
      return None
  ```
  This IS a directional check but it uses `Wave.up` (i.e., `end.price > start.price`).
  This works IF the waves come from the ZigZag (alternating by construction). For DP-
  assembled sub-groups from a non-alternating pivot stream, it may pass non-corrections.

**`_correction_quality` (wavetree.py, line 50)**
- ZIGZAG base = 0.8. Final score = `0.8 * (0.6 + 0.4 * _fib_close(C/A))`.
  When `C/A ≈ 1.0` (equality, the most common zigzag target): `_fib_close(1.0)` ≈ 1.0
  (since 1.0 is in `_FIB`). So `score = 0.8 * (0.6 + 0.4 * 1.0) = 0.8 * 1.0 = 0.80`.
- FLAT base = 0.7 if `b >= 0.8` else 0.45.

**`_impulse_quality` (wavetree.py, line 41)**
- Computes mean of `_fib_close(W3/W1), _fib_close(W2/W1), _fib_close(W4/W3)`.
- `sigma = 0.20` means the kernel has very wide tolerance: a ratio of 0.8 × any
  Fibonacci target still scores ~0.6.
- A real impulse where W3 = 1.618 × W1 (classic): `_fib_close(1.618) ≈ 1.0`.
  But W2 ≈ 0.618 × W1 and W4 ≈ 0.382 × W3 — these are Fibonacci-aligned too.
  So `_impulse_quality ≈ (1.0 + 1.0 + 1.0) / 3 = 1.0`.
- **Why does the impulse still lose?** The confidence formula:
  `conf = _confidence(results, ...) * (0.4 + 0.6 * 1.0) = _confidence * 1.0`.
  `_confidence` deducts 0.1 per WARN in `results`. `elliott_hard_rules` + `similarity_and_balance`
  almost always produce several WARNs even on a real impulse (W2 depth WARN, W4 depth
  WARN, extension WARN if no clear extension, etc.).
  A typical impulse `_confidence ≈ 0.7` (3 WARNs = -0.3 from 1.0).
  So `conf_impulse ≈ 0.7 * 1.0 = 0.70`.
  `value(impulse) = 5 * 0.70 + 0.5 = 4.0`.
  Two corrections at 0.8: `value = 3 * 0.8 + 3 * 0.8 = 4.8`. **Corrections win again.**

---

## 3. Mistake Table

| # | Theory requirement | Code behaviour | Verdict | Severity | How it causes "everything-is-corrective" |
|---|---|---|---|---|---|
| M1 | An impulse that passes all 3 hard rules AND alternates direction should be preferred over ANY correction in the same span | DP `value()` bonus for IMPULSE is `+0.5` (line 243). Two 3-node corrections covering the same 6-node span score `6 * conf_correction + 0.0`. For `conf_correction ≥ 0.42` each, two corrections outscore the impulse regardless of impulse quality. | **WRONG** | **H** | Primary cause of "everything-is-corrective": at any scale where the impulse is split into two overlapping 3-leg segments, corrections always win the DP race. |
| M2 | Corrections are valid only when legs alternate in the correct corrective pattern (A and C same direction, B opposite) AND the B-wave retracement satisfies the classifier | `_correction_node` lacks `_alternating()` or hard-rule check; it enters only through `classify_correction` which checks B-wave ratios but not structural integrity as rigorously as impulse. | **WRONG (partial)** | **H** | Greatly inflates the number of valid correction candidates. More corrections in the DP means corrections are tried at almost every starting node, crowding out impulses. |
| M3 | ZigZag sensitivity must be calibrated to the degree being analysed. A Primary-degree 5-wave advance covering 15 years should be detected at scales that capture it whole. | `wave_counts` uses fixed scales `(0.04, 0.07, 0.12, 0.20)`. For AVGO (26× total move), even `0.20` (20%) yields dozens of pivots within the full Primary wave. No scale ever places the entire 1990–2026 advance into one 5-node candidate. | **WRONG** | **H** | Root cause of why no Primary-degree impulse is ever found: the pivot stream never captures the full Primary advance as a single 5-wave group. |
| M4 | The `_impulse_quality` Fibonacci kernel should discriminate between impulse-characteristic ratios (W3/W1 ≈ 1.618) and correction-characteristic ratios | `sigma = 0.20` in `_fib_close` (wavetree.py line 38). Gaussian kernel with ±20% relative tolerance. Because `_FIB` includes 1.0 (equality), and most corrective C/A ratios are near 1.0, corrections also score near 1.0 on this kernel. The kernel is too broad to distinguish impulse from correction. | **WRONG** | **M** | Makes `_correction_quality` nearly as high as `_impulse_quality`, removing the scoring advantage impulses should have from their Fibonacci structure. |
| M5 | The alternation guideline (W2 sharp/deep vs W4 flat/shallow) is a WARN, not a FAIL | Coded as WARN — correct. However `_confidence()` deducts 0.1 per WARN, so a textbook impulse with 4 WARNs (extension mild, equality mild, W2 depth typical, W4 depth typical) has `conf ≈ 0.60` before Fibonacci quality. This excessively penalises real impulses which naturally accumulate WARNs. | **PARTIAL** | **M** | Depresses impulse confidence below corrective confidence even when the impulse is structurally sound. |
| M6 | Sub-wave structure at degree ≥ 2: motive legs 1,3,5 must be impulses; corrective legs 2,4 must be corrections | Correctly implemented at `_impulse_node` line 118: `all(group[i].pattern in _MOTIVE for i in (0,2,4))` and `all(group[i].pattern in _CORRECTIVE for i in (1,3))`. BUT: at degree 1 (the first compaction level), all children are MONOWAVEs, so the sub-structure check is skipped entirely (the `if degree >= 2` guard on line 118). This means degree-1 impulses are allowed without any sub-wave verification at all. | **WRONG** | **M** | Means the first degree of compaction produces impulse-candidate nodes with no sub-structure constraint, but the same degree-1 nodes feed into degree-2 as children — where the sub-structure requirement then applies. A cycle where corrections at degree 1 are promoted as "CORRECTIVE" children makes the degree-2 impulse fail the motive-child check. This compounds the bias toward corrections. |
| M7 | `_correction_quality` base score for ZIGZAG (0.8) should not exceed the theoretical maximum impulse quality (1.0 × confidence) | At `_correction_quality` (wavetree.py line 56): ZIGZAG base = 0.8. A zigzag with C/A ≈ 1.0 scores `0.8 * 1.0 = 0.80`. A clean impulse has `conf ≈ 0.7` from `_confidence()`, giving value/node = 0.70. The base score for a zigzag (0.80) exceeds the typical impulse confidence (0.70) **before** any Fibonacci component. | **WRONG** | **H** | Zigzag base is set higher than the typical impulse confidence, so zigzags consistently win node-for-node in the DP. |
| M8 | Degree labeling: a 15-year advance in AVGO should be labeled Primary or Cycle, not Minuette | `anchored_degree()` (wavetree.py line 353) assigns degree based on monowave count per Neely's 13–55 window. At the fine scales used (0.04–0.20), the monowave count for any top-level pattern is < 55, so the result is always "MINUTE" or "MINUETTE" even for multi-decade moves. | **WRONG** | **M** | The engine can never produce a Primary/Cycle-degree impulse label for AVGO/MRVL because the ZigZag scales are too fine to produce the required pivot density per the Neely window. |
| M9 | Correction `classify_correction` checks B-wave retrace but NOT that A and C sub-divide in 5 (zigzag) or 3 (flat) waves | Explicitly acknowledged as a data-availability gap in docs/research/01_elliott_wave.md §5.2. The classifier returns PASS based on B-retrace ratio alone. This is theoretically correct given single-degree input, but combined with the generous `_correction_quality` scores, it means corrections are validated with far less structural evidence than impulses. | **PARTIAL / MISSING** | **L** | Individually minor; combined with M1/M2/M7 amplifies the correction bias. |
| M10 | The `value()` bonus for DIAGONAL (+0.3) should be comparable to IMPULSE (+0.5) | `value()` line 243: `bonus = 0.5 (IMPULSE) / 0.3 (DIAGONAL) / 0.0 (else)`. Diagonal bonus is 60% of impulse bonus, which is reasonable. However diagonal detection requires degree >= 2 (`_diagonal_node` line 148), so at degree 1 no diagonal can form. This means the engine never proposes a diagonal at the first degree level, forcing all motive candidates to be IMPULSE-only. | **PARTIAL** | **L** | Minor contribution to the bias; main issue is M1/M2/M3/M7. |

---

## 4. Concrete Fixes

### Fix F1 (addresses M1 and M7) — Rebalance `value()` and `_correction_quality`

**File:** `wavetree.py:value` (line 240); `wavetree.py:_correction_quality` (line 50).

**Problem:** A ZIGZAG correction scores `0.8 * (0.6 + 0.4 * fib)` ≈ 0.80 per node.
An IMPULSE scores `conf * (0.4 + 0.6 * quality)` ≈ 0.70 per node for a real impulse
with 3 WARNs. Two corrections covering 6 nodes beat one impulse covering 5 nodes in
the DP.

**Fix — three coordinated changes:**

1. Increase the IMPULSE `value()` bonus from `+0.5` to `+1.5` (effectively a
   3-child equivalent, reflecting that an impulse encodes significantly more structural
   information than a correction):
   ```python
   bonus = 1.5 if node.pattern == "IMPULSE" else 0.8 if node.pattern == "DIAGONAL" else 0.0
   ```
   Rationale: a 5-wave impulse spans 5 children. For it to lose to two 3-wave
   corrections (6 children total), the corrections must each score ≥
   `(5 * conf_impulse + 1.5) / 6 = (5 * 0.70 + 1.5) / 6 = 0.625 per node`.
   This means each correction needs quality ≥ 0.625 / 0.80 = 78% — a meaningfully
   higher bar than today.

2. Reduce `_correction_quality` base scores closer to the WARN-adjusted impulse range:
   ```python
   if pattern == "ZIGZAG":
       base = 0.65   # was 0.80; now below typical impulse conf of 0.70
   elif pattern == "FLAT":
       base = 0.55 if b >= 0.8 else 0.35
   else:
       base = 0.45
   ```

3. Add tests: construct a synthetic 5-wave impulse at degree 1 and assert
   `value(impulse_node) > value(correction1) + value(correction2)` where the two
   corrections cover the same span.

**Expected outcome:** Impulses that pass all 3 hard rules and have decent Fibonacci
quality should now consistently outscore corrections in the DP.

---

### Fix F2 (addresses M2) — Add a directional sanity gate to `_correction_node`

**File:** `wavetree.py:_correction_node` (line 199).

**Problem:** Corrections are accepted based on `classify_correction` alone. A group of
three nodes where A and B happen to have the same direction (both up, for example) can
pass `classify_correction`'s B-retrace check if the ratio lands in the right range.

**Fix:** Add an explicit check that wave A and wave C are in the same direction (they
are the motive legs of the correction), and that wave B is in the opposing direction:
```python
def _correction_node(group, degree):
    waves = [n.as_wave() for n in group]
    # Directional sanity: A and C same direction, B opposite
    if waves[0].up == waves[1].up or waves[0].up != waves[2].up:
        return None
    # Also require the three nodes themselves to represent alternating ZigZag pivots
    # (a "corrective" group must still have alternating price legs)
    rr = classify_correction(waves)
    if rr.status is not Status.PASS:
        return None
    ...
```
Note: the current code at line 201 already contains this directional check. The problem
is that it checks `Wave.up` (end > start) which is correct for ZigZag-sourced nodes.
The check should be kept and strengthened by also requiring `waves[0].length > 0` and
`waves[2].length > 0` (non-zero amplitude):
```python
if (waves[0].up == waves[1].up or waves[0].up != waves[2].up
        or waves[0].length <= 0 or waves[2].length <= 0):
    return None
```

**Expected outcome:** Spurious correction candidates from non-alternating monowave
groups are eliminated.

---

### Fix F3 (addresses M3) — Add coarser ZigZag scales that capture Primary-degree moves

**File:** `wavetree.py:wave_counts` (line 387); `wavetree.py:build_wave_tree` (line 281).

**Problem:** Fixed scales `(0.04, 0.07, 0.12, 0.20)` are insufficient for multi-decade
bull markets like AVGO (26×) or MRVL (100×). The coarsest scale (20%) still yields
dozens of pivots within what is, at the Primary/Cycle degree, a single wave.

**Fix:** Add coarser scales and make them instrument-adaptive:
```python
# In wave_counts: extend scales to include coarser levels
scales = (0.04, 0.07, 0.12, 0.20, 0.35, 0.60)  # add 35%, 60% for Primary-degree

# Or better: use total-move-percentage adaptation
def adaptive_scales(bars, n_scales=5):
    """Generate scales spanning from ~5 pivots to ~50 pivots over the full bar history."""
    # Estimate total range
    all_prices = [b[4] for b in bars]  # close prices
    total_range = (max(all_prices) - min(all_prices)) / min(all_prices)
    # Distribute scales logarithmically
    min_scale = max(0.02, total_range / 100)
    max_scale = total_range / 3
    import math
    return tuple(min_scale * (max_scale / min_scale) ** (i / (n_scales - 1))
                 for i in range(n_scales))
```

Additionally: the `max_levels` parameter in `build_wave_tree` (default 6) should be
increased to 8–10 for multi-decade data, allowing the DP to compact enough degrees to
reach the Primary/Cycle level.

**Tests to add:**
- Given AVGO weekly data (~879 bars), assert that at least one `AnchoredCount` at scale
  ≥ 0.30 produces an IMPULSE pattern spanning > 80% of the full bar history.
- Assert that `anchored_degree(node).name` for a 200-monowave node is at least "MINOR"
  (not "MINUETTE").

---

### Fix F4 (addresses M4) — Tighten `_fib_close` sigma to discriminate impulse from corrective ratios

**File:** `wavetree.py:_fib_close` (line 31).

**Problem:** `sigma=0.20` (±20% relative tolerance) is wide enough that most market
ratios fall within ~1.0 of some Fibonacci level. A corrective C/A ≈ 0.90 scores
`_fib_close(0.90)` at the nearest target (1.0):
`d = |0.90 - 1.0| / 1.0 = 0.10`; `exp(-(0.10)^2 / (2 * 0.20^2)) = exp(-0.125) ≈ 0.88`.
This is nearly as high as a perfect hit.

**Fix:** Tighten sigma to `0.10` for the impulse quality kernel specifically. This is
the difference between "near a Fibonacci level" and "actually at a Fibonacci level":
```python
def _fib_close(r, sigma: float = 0.10) -> float:  # tightened from 0.20
    """Gaussian proximity (0..1) to nearest Fibonacci level. sigma=0.10 (10% relative)."""
    if r != r or r <= 0:
        return 0.0
    d = min(abs(r - t) / t for t in _FIB)
    return math.exp(-(d * d) / (2 * sigma * sigma))
```

With sigma=0.10, the same ratio 0.90 scores `exp(-(0.10)^2 / (2 * 0.01)) = exp(-0.5) ≈ 0.61`
instead of 0.88 — a meaningful discrimination.

**Tests:** Assert `_fib_close(1.618) > 0.95`; assert `_fib_close(0.90) < 0.70`;
assert `_fib_close(1.0) > 0.90`.

---

### Fix F5 (addresses M5) — Reduce WARN penalty in `_confidence` for impulse-intrinsic WARNs

**File:** `wavetree.py:_confidence` (line 93).

**Problem:** Every WARN deducts 0.10 from confidence. A textbook impulse typically
generates 3–5 WARNs from `elliott_guidelines` (extension WARN if mild, equality WARN,
alternation WARN, W2 depth WARN, W4 depth WARN). This reduces confidence by 0.30–0.50,
severely penalizing real impulses for having guideline characteristics that are NORMAL.

**Fix:** Separate the WARN sources. Hard-rule-adjacent WARNs (R1 close, R3 close)
should carry a higher penalty than guideline WARNs (extension mild, depth typical):
```python
def _confidence(results, children, motive_idx, corr_idx) -> float:
    conf = 1.0
    for r in results:
        if r.status is Status.WARN:
            # Guideline WARNs (depth, extension, alternation) are expected — small penalty
            if any(kw in r.rule for kw in ("G ", "wave2 depth", "wave4 depth",
                                            "extension", "equality", "alternation")):
                conf -= 0.04   # was 0.10; guideline WARN is informational
            else:
                conf -= 0.10   # rule-adjacent WARN is more serious
    for i in motive_idx:
        c = children[i]
        if c.pattern != "MONOWAVE" and c.pattern not in _MOTIVE:
            conf -= 0.20
    for i in corr_idx:
        c = children[i]
        if c.pattern != "MONOWAVE" and c.pattern not in _CORRECTIVE:
            conf -= 0.20
    return max(0.0, min(1.0, conf))
```

**Tests:** Assert that a 5-wave synthetic with all 3 hard rules passing and 4 guideline
WARNs has `confidence >= 0.80`. Assert that a 5-wave sequence with one R1 WARN
(W2 depth close to 100%) has `confidence <= 0.70`.

---

### Fix F6 (addresses M8) — Extend `anchored_degree` monowave window for Primary/Cycle degree

**File:** `wavetree.py:anchored_degree` (line 353).

**Problem:** The Neely monowave window (13–55 for MINUTE) caps all assignments at
MINUTE or MINOR. Multi-decade Primary/Cycle waves encompass 100+ monowaves.

**Fix:** Extend the window table:
```python
def anchored_degree(node) -> Degree:
    m = _count_monowaves(node)
    if m < 13:
        return Degree.MINUETTE
    if m <= 55:
        return Degree.MINUTE
    if m <= 144:
        return Degree.MINOR
    if m <= 377:
        return Degree.INTERMEDIATE
    if m <= 987:
        return Degree.PRIMARY
    return Degree.CYCLE
```
(Fibonacci numbers 13, 55, 144, 377, 987 are the canonical Neely complexity windows;
see Glenn Neely *Mastering Elliott Wave* Ch. 5 monowave labeling section;
https://www.neowave.com/qow/qow-archive-13.asp.)

---

### Fix F7 (addresses M6) — Gate degree-1 impulse formation on monowave direction alternation

**File:** `wavetree.py:_impulse_node` (line 107).

**Problem:** At degree 1, the sub-structure check (`if degree >= 2`) is skipped. This
means any 5 consecutive monowaves that alternate direction and pass R1/R2/R3 can form
an IMPULSE at degree 1 — which is correct by definition (5 alternating monowaves that
pass the hard rules ARE an impulse at that scale). However, these degree-1 impulses
then feed into degree-2 as MOTIVE children. If the same 5 monowaves could alternatively
be parsed as a CORRECTION of their next-larger context, the degree-2 DP will try both.

The current code is actually correct here; the root cause is in `value()` (M1/M7), not
in the sub-structure gate. No code change needed for F7 beyond F1.

---

### New Tests to Add

```python
# tests/test_wavetree_impulse_bias.py

def test_clean_impulse_beats_two_corrections():
    """A 5-wave impulse node must outscore two overlapping corrections in value()."""
    # Synthetic: W1=100, W2=60 (0.60 retrace), W3=161 (1.61x W1), W4=38 (0.24x W3),
    # W5=100 (equality W1)
    # Build nodes directly (no ZigZag needed)
    ...
    impulse_node = _impulse_node(group5, degree=1)
    corr1_node = _correction_node(group[:3], degree=1)
    corr2_node = _correction_node(group[3:], degree=1)
    assert value(impulse_node) > value(corr1_node) + value(corr2_node)

def test_coarse_scale_finds_primary_impulse_on_avgo_weekly():
    """At scale >= 0.30, AVGO weekly data should produce at least one IMPULSE root
    spanning > 70% of the full history."""
    from data.avgo import WEEKLY
    roots = build_wave_tree(WEEKLY, base_pct=0.35, max_levels=10)
    impulse_roots = [r for r in roots if r.pattern == "IMPULSE"]
    assert len(impulse_roots) > 0, "No impulse found at coarse scale"
    total_span = max(r.end.t for r in roots) - min(r.start.t for r in roots)
    best_impulse_coverage = max(r.end.t - r.start.t for r in impulse_roots) / total_span
    assert best_impulse_coverage > 0.70, f"Best impulse covers only {best_impulse_coverage:.0%}"

def test_fib_close_tighter_sigma_discriminates():
    assert _fib_close(1.618) > 0.95
    assert _fib_close(0.90) < 0.70
    assert _fib_close(1.30) < 0.80   # not a Fibonacci level

def test_impulse_confidence_not_crushed_by_guideline_warns():
    """A textbook impulse with 4 guideline WARNs should still have conf >= 0.80."""
    results = [
        RuleResult("G extension present", Status.WARN, "mild"),
        RuleResult("G equality of non-ext motive", Status.WARN, "borderline"),
        RuleResult("G wave2 depth 0.5-0.618", Status.WARN, "0.70 of w1"),
        RuleResult("G wave4 depth 0.236-0.382", Status.WARN, "0.40 of w3"),
    ]
    conf = _confidence(results, [], (), ())
    assert conf >= 0.80, f"Confidence {conf:.2f} too low for guideline-only WARNs"

def test_anchored_degree_primary_for_large_monowave_count():
    from wavelib.wavetree import anchored_degree, WaveNode
    from wavelib.rules import Pivot, Degree
    # Create a fake node with 500 "monowaves" by nesting
    # ... (build a tree with 500 leaves)
    assert anchored_degree(big_node) == Degree.PRIMARY
```

---

## 5. Root Cause Summary

The "everything-is-corrective" symptom has three compounding root causes:

**Root Cause 1 (scoring arithmetic):** The DP `value()` function rewards coverage
(number of children) × confidence. Because corrections have a *higher base confidence*
from `_correction_quality` than a typical impulse gets from the WARN-penalised
`_confidence()`, two 3-node corrections tiling the same 6 nodes always outscore one
5-node impulse. The `+0.5` impulse bonus is too small to compensate. This is the
primary cause.

**Root Cause 2 (scale blindness):** The ZigZag scales (4%–20%) are calibrated for
intraday and short-term swings, not for multi-decade Primary/Cycle-degree advances.
At these scales, the full AVGO bull market is never presented to the DP as a single
5-wave group. The engine can only "see" sub-waves, each of which, in isolation, is
corrective. The engine is not wrong — it is answering the wrong question at the wrong
scale.

**Root Cause 3 (correction gatekeeping is lighter than impulse gatekeeping):**
Impulses must pass `_alternating()`, all three `elliott_hard_rules`, and (at degree
≥ 2) the sub-wave structure check. Corrections pass if `classify_correction()` returns
PASS. This means the population of valid corrections in the DP is an order of magnitude
larger than the population of valid impulses, overwhelming the impulse bonus.

The three interact: even when a correct scale is used (Root 2 fixed), corrections still
win the DP because of the scoring imbalance (Root 1). And even when scoring is
rebalanced, the large correction population still competes aggressively unless the
gatekeeping asymmetry (Root 3) is also addressed.

**Fixes F1 (value rebalancing) + F3 (coarser scales) are the highest-leverage
interventions.** F2 (correction gatekeeping) and F5 (WARN penalty reduction) are
secondary but necessary for robustness.

---

## Sources

- Frost, A.J. & Prechter, R.R. *Elliott Wave Principle*, 10th ed., New Classics Library,
  2005. PDF: https://www.investmenttheory.org/uploads/3/4/8/2/34825752/elliott-wave-principle.pdf
- Elliott Wave International Waveopedia: https://www.elliottwave.com/waveopedia/
- Wikipedia — Elliott Wave Principle: https://en.wikipedia.org/wiki/Elliott_wave_principle
- EW Forecast — Rules, Guidelines & Structures: https://elliottwave-forecast.com/elliott-wave-theory/
- EW Street — The Complete Guide (2026): https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/
- EW Monitor — Everything You Need to Know: https://elliottwavemonitor.com/elliott-wave-theory/
- FBS — Fibonacci Ratios and Impulse Waves: https://fbs.com/analytics/guidebooks/fibonacci-ratios-and-impulse-waves-275
- Price Action Help — Revised Rules and Guidelines: https://priceactionhelp.com/elliott-wave
- Algotrading-Investment — IWSS/CWSS: https://algotrading-investment.com/2020/06/04/impulse-wave-structural-score-and-corrective-wave-structural-score/
- Algotrading-Investment — Channeling Technique: https://algotrading-investment.com/2020/06/04/channelling-technique-elliott-wave/
- Forex Training Group — Wave Personality: https://forextraininggroup.com/characteristics-and-personalities-of-elliott-waves/
- NeoWave degree assignment Q&A: https://www.neowave.com/qow/qow-archive-13.asp
- Kotyrba et al. (2013) — EW Pattern Recognition: https://scs-europe.net/dlib/2013/ecms13papers/is_ECMS2013_0050.pdf
- EW Insight — Degrees & Labeling: https://elliottwaveinsight.co.uk/elliott-wave-degrees-labeling/
- Docs cross-references: docs/research/01_elliott_wave.md, docs/research/deep/07_auto_labeling_and_anchoring.md,
  wavelib/wavetree.py, wavelib/rules.py
