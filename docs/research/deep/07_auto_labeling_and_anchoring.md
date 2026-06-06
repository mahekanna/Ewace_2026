# 07 — Automatic Single-Count Selection and Degree Anchoring

**Ewace_2026 / `wavelib` deep-research layer — June 2026**

*Audience: developer implementing the automation layer after reading `DOCUMENTATION.md`,
`CLAUDE.md`, and docs 00–04. This document picks up where `04_automation_validation.md`
§2.2–2.3 left off and goes deeper on the hardest open sub-problems.*

---

## 1. Scope and Sources

The engine currently builds a multi-degree candidate tree: given a pivot stream it can
enumerate and validate candidate impulse/correction counts, but it cannot commit to one.
The result is many fragmented roots — counts valid at different anchors and degrees that
the engine cannot rank into a single preferred view.

This document addresses four tightly coupled problems:

1. **The single-count problem** — how to select one count from a forest of valid candidates.
2. **Degree anchoring** — how to assign a consistent, principled degree scale.
3. **Pivot/scale selection** — which ZigZag pass produces the right raw material.
4. **Confidence calibration** — how to turn rule-pass / Fibonacci fidelity into a
   calibrated probability, not an ad-hoc score.

An honest fifth topic closes the document:

5. **Pitfalls and the subjectivity ceiling** — why a unique deterministic answer is
   impossible and how to present alternates honestly.

### Research sources consulted

Academic literature reviewed:

- Kotyrba, Volná et al. (2013), *Methodology for Elliott Waves Pattern Recognition*,
  ECMS 2013 [1], and companion papers [2][3] — multi-classifier neural network approach.
- Vantuch, Zelinka, Vasant (2018), *An Algorithm for Elliott Waves Pattern Detection*,
  Intelligent Decision Technologies 12(1):15–24 [4] — Random Forest / SVM on wave
  sub-sequences, >70 % prediction accuracy.
- Batchelor & Ramyar (2005) via Prechter's rebuttal [5] — empirical test of Fibonacci
  ratio frequency in DJIA; null hypothesis not rejected for raw filtered trends (with
  caveats).
- Grammar of the Wave (2025 arxiv preprint) [6] — neuro-symbolic VLM agent using event
  logic trees for multivariate time series event detection.
- Stochastic Context-Free Grammar (SCFG) / Viterbi parse literature [7] — inside-outside,
  Viterbi for single best parse.
- MDL/MML time-series segmentation (PRESEE algorithm) [8] — parameter-free pivot
  threshold selection.
- Classifier calibration survey [9] — Platt scaling and isotonic regression.
- PyBacktesting (Ostiguy) [10] — genetic algorithm optimization with Sharpe fitness.

Open-source projects studied:

- ElliottWaveAnalyzer (btcorgtfo/drstevendev) [11] — brute-force combinatorial,
  binary pass/fail, no confidence score.
- python-taew (DrEdwardPCB) [12] — iterative forward-search; returns all valid counts.
- elliot-waves-auto (ESJavadex) [13] — ZigZag + Fibonacci projection web app.
- WaveBasis (commercial) [14] — ML + expert-system engine; Similarity Index; degree
  management; bias selector; primary vs alternate count hierarchy.
- MotiveWave (commercial) [15] — auto-decompose to user-chosen degree level.
- Impulse Wave Structural Score / Corrective Wave Structural Score (algotrading-investment)
  [16] — weighted multi-factor scoring formula.
- NeoWave monowave complexity control (Neely, neowave.com) [17] — 13–55 monowave window;
  largest move = extended wave anchor.

---

## 2. Survey of Approaches

### 2.1 Brute-force combinatorial with binary validation (current open-source baseline)

**How it works.** Both ElliottWaveAnalyzer [11] and python-taew [12] share the same
structural pattern:

1. Extract a pivot stream via ZigZag (fixed `pct` or iterative bar search).
2. Generate all sub-sequences of N pivots that could form a 5-wave or 3-wave pattern.
3. Check each sub-sequence against the hard rules (Wave-2 ≤ 100 % of Wave-1, Wave-3 not
   shortest, Wave-4 no overlap except diagonal, etc.) using binary pass/fail lambdas.
4. Return the full list of passing patterns.

**What is missing.** Neither system:

- Ranks survivors by any continuous score.
- Selects a single preferred count.
- Handles degree — the same pattern may appear at three scales simultaneously, and both
  libraries treat each scale independently.
- Provides any probability or confidence output.

**Combinatorial cost.** A 50-pivot stream has C(50,6) ≈ 15.8 million 6-tuples. Hard-rule
early termination reduces this to a tractable set (typically single digits at any one
scale), but across multiple scales and pattern types the total surviving set is O(10–100)
valid candidates — still too many to present to a user as-is.

### 2.2 Neural network classification (Kotyrba-Volná school)

Kotyrba et al. [1][2][3] train two backpropagation networks: the first recognises the
*shape* of a pattern against template patterns in a labelled training set (output is a
similarity consensus 0–1); the second predicts the subsequent trend direction given the
recognised pattern type. Patterns with consensus ≥ 0.90 yielded ~68 % trend prediction
accuracy.

**Advantages.** Produces a continuous "similarity" score. Handles partial (incomplete)
patterns by measuring degree of match.

**Disadvantages for this project.**

- Requires a labelled training set of expert-verified Elliott Wave counts — expensive
  to acquire and inherently subjective.
- The neural network is a black box: it cannot explain *which rules* drove its score.
- The approach does not inherently produce degree assignments or alternates.
- Overfitting risk is high when training data is sparse in terms of count diversity.

### 2.3 Machine learning on wave sub-sequences (Vantuch-Zelinka)

Vantuch et al. [4] extract handcrafted features (ratio of successive wave amplitudes,
time ratios, extension ratios) from candidate 5-wave sequences and classify them using
Random Decision Forest and SVM. Accuracy >70 % on held-out stock data.

**Key insight.** Feature engineering (ratio vectors) is more interpretable than raw
price, and the same features can become scoring dimensions in a rule-based scorer.
The Fibonacci ratios W3/W1, W2-retrace/W1, W4-retrace/W3, W5/W1 are the most
discriminating features in the feature importance analysis.

### 2.4 Grammar-based parsing (the theoretical ideal)

Stochastic Context-Free Grammars (SCFGs) [7] provide a rigorous probabilistic framework
for this problem. The Elliott Wave hierarchy maps naturally to a PCFG:

```
Grand_Supercycle → Supercycle Supercycle Supercycle Supercycle Supercycle Supercycle Supercycle Supercycle
Supercycle        → Cycle Cycle Cycle Cycle Cycle Correction
Cycle             → Impulse Impulse Impulse Impulse Impulse Correction
Impulse           → W1 W2 W3 W4 W5
Correction        → Zigzag | Flat | Triangle | Complex
W1                → monowave | Impulse | DiagTriangle
...
```

Each production rule carries a probability. The **Viterbi parse** — computed by the CYK
dynamic programming algorithm (O(n³ |G|)) — finds the single most probable derivation
of the observed pivot sequence under the grammar [7]. The **inside-outside algorithm**
computes the full posterior over all parse trees, allowing principled computation of the
probability of each complete and partial labeling.

**Why this has not been implemented in the field.** The Elliott Wave grammar is highly
ambiguous (many productions can cover the same span), the terminal symbols (monowaves) do
not have clear probability distributions, and the grammar must be learned from expert-
labeled data that does not exist at scale. The Grammar of the Wave preprint [6] approaches
this for generic multivariate event detection using neuro-symbolic agents (VLMs + event
logic trees) rather than pure SCFGs, but does not directly address Elliott Wave theory.

**Actionable insight.** The PCFG / Viterbi formulation is the theoretically correct
framing. Even without trained probabilities, the *structure* of the Viterbi computation —
bottom-up DP that fills a chart table over spans of the pivot sequence — is the right
algorithmic skeleton for single-count selection. We can substitute rule-based scores for
true probabilities in a pseudo-Viterbi, accepting that the result is MAP-under-proxy-
prior rather than a genuine probability.

### 2.5 Commercial system approaches (WaveBasis, MotiveWave)

WaveBasis [14] uses a hybrid ML + expert-system approach: proprietary statistical and
machine learning algorithms combined with Elliott Wave rule enforcement. It outputs a
**Primary Count** (highest-scoring) plus ordered alternates, each with a **Similarity
Index** (percentage similarity to the primary count). Degree management is automatic:
wave labels further from price are assigned higher degree, using the visual nesting of
patterns as a proxy for degree hierarchy.

MotiveWave [15] uses an "Auto Decompose" tool: the user sets the starting degree and the
system decomposes down to the requested sub-degree level, anchoring to a user-chosen
significant turning point. The extended wave (largest impulse leg) is used to calibrate
which degree slot it occupies.

**Critical limitation of both.** Neither system exposes its scoring function. The
Similarity Index is a black box; the degree assignment heuristics are undocumented.
These commercial systems illustrate what a good user experience looks like but do not
provide an implementable algorithm.

### 2.6 Structural scoring (IWSS/CWSS framework)

The Impulse Wave Structural Score (IWSS) and Corrective Wave Structural Score (CWSS) [16]
are the clearest public formulation of a continuous scoring function:

- Each structural criterion (wave proportions, Fibonacci adherence, alternation,
  momentum characteristics, S&B balance) is scored 0–10.
- Scores are weighted-summed into a total.
- Higher total = stronger structural integrity.

The CWCOUNT framework [from search result context] uses a similar 8-factor binary
confluence score (0 or 1 per factor, 0–8 total), with Fibonacci alignment as a
*confidence modifier*, not a hard gate — a count with good structural proportions but
imperfect Fibonacci ratios is not invalidated, merely scored lower. This distinction is
important: treating Fibonacci guidelines as hard gates over-prunes valid alternates.

### 2.7 MDL/MML for pivot threshold selection

The PRESEE algorithm [8] demonstrates that the Minimum Description Length (MDL) principle
can select the optimal segmentation of a time series *without* a manually chosen
threshold parameter. The idea: the "best" ZigZag threshold is the one that produces a
pivot stream whose description (the segment breakpoints + residuals) is shortest in bits.
Smaller thresholds produce more pivots (longer description of breakpoints) but shorter
residuals; larger thresholds do the reverse. The optimal is at the inflection of the
total description length vs threshold curve.

This is directly applicable to automated ZigZag threshold selection for each degree
level in the Elliott Wave hierarchy, avoiding the arbitrary ATR multiplier choices.

---

## 3. Recommended Algorithm

This section presents a concrete, implementable algorithm for the three coupled problems:
(a) single-count selection, (b) degree anchoring, and (c) calibrated confidence.

### 3.1 Architecture overview

```
OHLCV bars
    │
    ▼
[A] Multi-scale causal pivot streams
    │  (ATR-adaptive ZigZag at k multipliers; confirmed_t timestamps)
    │
    ▼
[B] Bottom-up Neely monowave construction
    │  (stage 0→1→2→... degree promotion)
    │
    ▼
[C] Per-degree candidate enumeration
    │  (5-leg impulse + 3-leg correction; constraint-propagation pruning)
    │
    ▼
[D] Scoring: IWSS/CWSS + Fibonacci adherence
    │
    ▼
[E] Global single-count selection via pseudo-Viterbi DP
    │  (score the joint parse of the entire pivot sequence at each degree)
    │
    ▼
[F] Degree anchoring: extended-wave identification + Neely complexity window
    │
    ▼
[G] Confidence calibration: isotonic regression on held-out validation set
    │
    ▼
Output: {primary_count, alternates[], degree, confidence_pct, notes[]}
```

### 3.2 Step A — Multi-scale causal pivot streams

Run `k=4` independent ATR-ZigZag passes over the same OHLCV data with increasing
multipliers `m ∈ {1.0, 2.0, 4.0, 8.0}`. Multiplier 1× captures Sub-Minute / Minute
degree; 8× captures Primary / Cycle degree.

**Causal pivot confirmation rule (critical, D-013 equivalent):**

```python
class Pivot:
    t_extreme: int       # bar index where price extreme occurred
    t_confirmed: int     # bar index when reversal >= threshold was first observed
    price: float         # price at t_extreme
    direction: int       # +1 = high, -1 = low

def causal_zigzag(bars, atr_mult: float = 2.0, atr_period: int = 14) -> list[Pivot]:
    """
    Right-looking ZigZag: a pivot is ONLY emitted when the opposing move
    has exceeded ATR(atr_period) * atr_mult from the candidate extreme.
    The pivot's t_confirmed = first bar at which this threshold was crossed.
    Never uses future bars. Never backdates t_confirmed.
    """
    atr = compute_atr(bars, atr_period)       # causal, right-aligned
    pivots = []
    candidate_high = bars[0]; candidate_low = bars[0]
    direction = None  # +1 tracking high candidate, -1 tracking low candidate
    for i, bar in enumerate(bars):
        threshold = atr[i] * atr_mult
        if direction != -1:  # tracking or starting high candidate
            if bar.high > candidate_high.high:
                candidate_high = bar
            elif candidate_high.high - bar.low >= threshold:
                pivots.append(Pivot(
                    t_extreme=candidate_high.index,
                    t_confirmed=i,          # <- confirmed NOW, not at extreme
                    price=candidate_high.high,
                    direction=+1
                ))
                candidate_low = bar
                direction = -1
        else:  # tracking low candidate
            if bar.low < candidate_low.low:
                candidate_low = bar
            elif bar.high - candidate_low.low >= threshold:
                pivots.append(Pivot(
                    t_extreme=candidate_low.index,
                    t_confirmed=i,
                    price=candidate_low.low,
                    direction=-1
                ))
                candidate_high = bar
                direction = +1
    return pivots
```

**MDL-informed multiplier tuning.** For each multiplier candidate `m`, compute the
description length `L(m) = n_pivots(m) * log2(T) + sum_residuals(m)`. Select the four
`m` values corresponding to distinct local minima of `L(m)` as a curve of `m` — these
are the "natural" segmentation scales for that instrument's current volatility regime.
This replaces the fixed `{1, 2, 4, 8}` with adaptive choices.

### 3.3 Step B — Neely bottom-up degree promotion

```python
def build_degree_stack(
    bars, atr_period=14, n_degrees=4
) -> list[list[Pivot]]:
    """
    Returns degree_stack[d] = list of Pivots at degree d,
    where degree_stack[0] = finest (confirmed ATR-1x monowaves).
    """
    # Start with finest-scale pivots
    finest_pivots = causal_zigzag(bars, atr_mult=1.0, atr_period=atr_period)
    degree_stack = [finest_pivots]

    for d in range(1, n_degrees):
        prev_pivots = degree_stack[d-1]
        promoted = []
        # Neely complexity window: require 13-55 monowaves per segment
        # Attempt to group consecutive prev_pivots into validated polywave
        i = 0
        while i < len(prev_pivots) - 2:
            # Try 5-wave impulse window
            for window_size in [5, 3]:  # try impulse then correction
                end = i + window_size
                if end >= len(prev_pivots):
                    break
                window = prev_pivots[i:end+1]
                waves = pivots_to_waves(window)
                result = validate_impulse(waves) if window_size == 5 \
                         else validate_correction(waves)
                if result.hard_fail_count == 0:
                    # Collapse to synthetic pivot at next degree
                    synthetic = Pivot(
                        t_extreme=window[0].t_extreme,
                        t_confirmed=window[-1].t_confirmed,
                        price=window[0].price,   # start of pattern
                        direction=window[0].direction,
                        degree=d,
                        sub_pivots=window,
                        score=compute_score(waves, result)
                    )
                    promoted.append(synthetic)
                    i += window_size
                    break
            else:
                i += 1  # no valid grouping; advance one pivot
        degree_stack.append(promoted)
    return degree_stack
```

**Neely's complexity control** maps to constraining the number of `prev_pivots` that are
collapsed into each synthetic pivot: require between 13 and 55 (ideally 21–34) monowaves
per complete macro pattern. If a promotion attempt would produce a degree-d pivot that
subsumes fewer than 13 or more than 55 degree-0 monowaves, reject the grouping [17].

### 3.4 Step C — Per-degree candidate enumeration with constraint propagation

At each degree `d`, produce candidate counts by sliding a window over `degree_stack[d]`:

```python
def enumerate_candidates(
    pivots: list[Pivot],
    pattern_type: str = "both"  # "impulse" | "correction" | "both"
) -> list[CandidateCount]:
    candidates = []
    n = len(pivots)
    for i in range(n - 2):
        for window_size in ([5, 3] if pattern_type == "both" else
                            [5] if pattern_type == "impulse" else [3]):
            if i + window_size >= n:
                continue
            window = pivots[i:i + window_size + 1]
            waves = pivots_to_waves(window)
            # Constraint propagation: fast pre-filter before full validation
            if not _passes_fast_prune(waves, window_size):
                continue
            if window_size == 5:
                result = validate_impulse(waves)
            else:
                result = validate_correction(waves)
            score = compute_score(waves, result)
            candidates.append(CandidateCount(
                start=i, end=i + window_size,
                pivots=window, waves=waves,
                result=result, score=score,
                degree=pivots[0].degree if hasattr(pivots[0], 'degree') else 0
            ))
    return sorted(candidates, key=lambda c: c.score, reverse=True)

def _passes_fast_prune(waves, window_size) -> bool:
    """O(1) hard-rule pre-filter — reject obvious violations before full validate."""
    if window_size == 5:
        W1, W2, W3, W4, W5 = waves
        # R1: W2 cannot retrace >100% of W1
        if W2.retrace_pct(W1) > 1.0:
            return False
        # R2: W3 cannot be shortest of W1, W3, W5 (approximate at pre-filter)
        if W3.size < 0.5 * W1.size:   # very rough pre-filter
            return False
        # R3: W4 no overlap with W1 territory (non-diagonal)
        if waves_overlap(W4, W1):
            return False
    return True
```

### 3.5 Step D — IWSS/CWSS scoring function

Score each candidate with a weighted multi-factor formula. Components map to the
IWSS/CWSS structure [16] plus the CWCOUNT Fibonacci modifier approach [from search context]:

```python
RULE_WEIGHTS = {
    "wave3_not_shortest":      0.20,   # hard structural requirement
    "w2_retrace_in_golden":    0.15,   # W2 retraces 50–78.6% of W1 (ideal)
    "w4_retrace_in_range":     0.10,   # W4 retraces 23.6–50% of W3
    "alternation_w2_w4":       0.10,   # W2 sharp → W4 complex or vice versa
    "w3_extended":             0.10,   # W3 is the longest wave
    "fib_adherence":           0.15,   # how close key ratios are to Fib targets
    "channel_fit":             0.10,   # price stays within 1–2 channel
    "size_balance":            0.05,   # S&B: W1≈W5 in non-extended scenarios
    "time_proportion":         0.05,   # time ratios roughly proportional
}

FIB_TARGETS = {
    "w2_vs_w1":    [0.382, 0.500, 0.618, 0.764],
    "w3_vs_w1":    [1.000, 1.272, 1.618, 2.000, 2.618],
    "w4_vs_w3":    [0.236, 0.382, 0.500],
    "w5_vs_w1":    [0.618, 1.000, 1.618],
}

def compute_score(waves: list[Wave], result: ValidationResult) -> float:
    """
    Returns a score in [0, 1]; higher = more structurally sound.
    Hard fails impose a multiplicative penalty rather than a floor of 0,
    so failed candidates can still be ranked among themselves.
    """
    if len(waves) == 5:
        return _score_impulse(waves, result)
    else:
        return _score_correction(waves, result)

def _score_impulse(waves, result) -> float:
    W1, W2, W3, W4, W5 = waves
    s = 0.0

    # Hard-rule components (from result.rule_outcomes)
    s += RULE_WEIGHTS["wave3_not_shortest"] * (
        1.0 if W3.size >= W1.size and W3.size >= W5.size else 0.0
    )

    # Fibonacci adherence: for each target ratio, measure closeness
    fib_score = _fib_proximity(W2.retrace_pct(W1), FIB_TARGETS["w2_vs_w1"])
    fib_score += _fib_proximity(W3.size / W1.size,  FIB_TARGETS["w3_vs_w1"])
    fib_score += _fib_proximity(W4.retrace_pct(W3), FIB_TARGETS["w4_vs_w3"])
    fib_score += _fib_proximity(W5.size / W1.size,  FIB_TARGETS["w5_vs_w1"])
    s += RULE_WEIGHTS["fib_adherence"] * (fib_score / 4.0)

    # W3 extension bonus
    s += RULE_WEIGHTS["w3_extended"] * (
        1.0 if W3.size >= W1.size * 1.5 and W3.size >= W5.size * 1.5 else 0.3
    )

    # Alternation (W2 vs W4 character)
    s += RULE_WEIGHTS["alternation_w2_w4"] * (
        1.0 if _alternates(W2, W4) else 0.0
    )

    # Guideline penalties: each WARN from result reduces score
    warn_penalty = len(result.warns) * 0.03
    s = max(0.0, s - warn_penalty)

    # Hard-fail multiplicative penalty
    if result.hard_fail_count > 0:
        s *= 0.1 ** result.hard_fail_count   # near-zero but not exactly 0

    return min(1.0, s)

def _fib_proximity(ratio: float, targets: list[float]) -> float:
    """
    Returns 1.0 if ratio is within 2% of any target, decaying to 0
    as distance grows. Uses Gaussian kernel centered at each target.
    sigma = 0.02 * target (2% relative tolerance).
    """
    import math
    best = 0.0
    for t in targets:
        sigma = 0.02 * t if t > 0 else 0.02
        best = max(best, math.exp(-0.5 * ((ratio - t) / sigma) ** 2))
    return best
```

### 3.6 Step E — Global single-count selection via pseudo-Viterbi DP

The key insight: selecting the best *local* count (highest-scoring 5-wave window) can
fail because two locally high-scoring patterns may overlap and contradict each other.
We need a **global** assignment that (a) covers the entire pivot sequence without
contradiction and (b) maximises the sum of local scores.

This is isomorphic to the Viterbi / maximum-weight segmentation problem, solvable in
O(n²) over the pivot sequence:

```python
def global_single_count(
    candidates: list[CandidateCount],
    pivots: list[Pivot]
) -> list[CandidateCount]:
    """
    Viterbi-style DP for non-overlapping, gap-covering segmentation.

    State: dp[i] = (best_total_score, best_path_ending_at_pivot_i)
    Transition: for each candidate c ending at pivot i, dp[i] = max over
                all dp[c.start] + c.score

    Returns the optimal non-overlapping cover of the pivot sequence.
    The primary count is the path that maximises joint score.
    Alternates are the next-best paths (beam of width B=5).
    """
    n = len(pivots)
    INF = float("-inf")

    # dp[i] = (best_score, previous_endpoint, candidate_used)
    dp = [(INF, -1, None)] * n
    dp[0] = (0.0, -1, None)

    # Index candidates by end-pivot index
    from collections import defaultdict
    cands_ending_at = defaultdict(list)
    for c in candidates:
        cands_ending_at[c.end].append(c)

    for i in range(1, n):
        # Option 1: extend from the previous pivot with no candidate (gap penalty)
        prev_score, _, _ = dp[i-1]
        gap_score = prev_score - 0.05   # small gap penalty for uncovered spans
        dp[i] = (gap_score, i-1, None)

        # Option 2: use a candidate ending at i
        for c in cands_ending_at[i]:
            start_score, _, _ = dp[c.start]
            if start_score == INF:
                continue
            total = start_score + c.score
            if total > dp[i][0]:
                dp[i] = (total, c.start, c)

    # Backtrack to recover path
    path = []
    i = n - 1
    while i > 0:
        _, prev_i, c = dp[i]
        if c is not None:
            path.append(c)
            i = c.start
        else:
            i = prev_i
    path.reverse()

    return path  # primary count = this path; store top-B beam for alternates
```

**Beam width for alternates.** Run the DP `B=5` times, each time excluding the
previously selected primary candidate's highest-scoring pattern. The resulting 5 paths
are the alternate counts. Compute their scores as a fraction of the primary score — this
fraction becomes the **relative plausibility** of each alternate.

### 3.7 Step F — Degree anchoring

Degree anchoring answers: *which degree level does the primary count occupy?*

**Rule F1 — Extended wave identification (Neely's "largest violent monowave").**
In the primary count, identify the wave with the largest amplitude divided by its
duration (price velocity, `amplitude / bars`). By Neely's procedure [17], this wave is
the Extended Wave of the MAIN Trend at the degree of the encompassing count. Mark its
degree label as the anchor.

**Rule F2 — Complexity window validation.**
Count the number of degree-0 monowaves subsumed by the entire count. If this number
falls outside [13, 55], the degree assignment is wrong: too few monowaves → count is
one degree too high; too many → one degree too low. Adjust the degree label and
re-annotate accordingly.

**Rule F3 — Top-down cross-check.**
After bottom-up promotion, validate: does the primary count fit *inside* an identifiable
larger-degree pattern in the coarser pivot stream? If the primary count ends at a pivot
that aligns with the start or end of a degree-(d+1) segment, degree is confirmed. If not,
flag `degree_confidence = "HEURISTIC"`.

```python
def anchor_degree(
    primary_count: list[CandidateCount],
    degree_stack: list[list[Pivot]],
    bars_total: int
) -> DegreeAnchor:
    all_subsumed_monowaves = sum(
        count_degree0_monowaves(c) for c in primary_count
    )
    # Neely window test
    if all_subsumed_monowaves < 13:
        degree = primary_count[0].degree + 1   # promote one degree up
        confidence = "HEURISTIC"
    elif all_subsumed_monowaves > 55:
        degree = primary_count[0].degree - 1   # demote one degree
        confidence = "HEURISTIC"
    else:
        degree = primary_count[0].degree
        # Check top-down cross-validation
        fits_parent = _check_parent_alignment(primary_count, degree_stack, degree)
        confidence = "CONFIRMED" if fits_parent else "HEURISTIC"

    return DegreeAnchor(degree=degree, confidence=confidence,
                        monowave_count=all_subsumed_monowaves)
```

**Degree labelling convention** (from Frost & Prechter / Ewace_2026 existing code):
use integer degrees where 0 = Sub-Minuette, 1 = Minuette, 2 = Minute, 3 = Minor,
4 = Intermediate, 5 = Primary, 6 = Cycle, 7 = Supercycle, 8 = Grand Supercycle.

### 3.8 Step G — Confidence calibration

The raw score from Step D is a weighted sum, not a probability. To convert it to a
**calibrated probability** (P(count is structurally correct)):

**Method: isotonic regression calibration [9]**

1. During backtesting, for each candidate count at bar `t` with raw score `s`, record
   the **outcome**: did the implied reversal zone actually produce a reversal before
   invalidation? (`y ∈ {0, 1}`).
2. After collecting `n ≥ 200` outcome pairs `(s, y)`, fit an isotonic regression
   (Pool Adjacent Violators algorithm) mapping raw scores → empirical probabilities.
3. At inference time, map the raw score through the fitted isotonic function to obtain
   `P_calibrated`.

**Why isotonic over Platt scaling.** The score distribution from Step D is unlikely to be
sigmoidal — it is a weighted sum of mixed indicator types. Isotonic regression makes no
distributional assumption, only monotonicity (higher score → higher probability), and is
consistently better-calibrated than Platt scaling when the score is non-sigmoidal [9].

**Until enough backtesting data is available (cold start):**

Use a conservative sigmoid parameterised by empirical ceiling:

```python
import math

def raw_to_confidence(raw_score: float,
                      empirical_ceiling: float = 0.65) -> float:
    """
    Maps raw score in [0,1] to a calibrated probability in [0, empirical_ceiling].
    The ceiling is the known empirical accuracy ceiling for automated EW counting
    (~65-68% from Kotyrba et al., ~70% from Vantuch et al. in-sample).
    This is a temporary monotone transform before isotonic calibration is available.
    """
    # logistic mapping: score=0 → 0.1, score=0.5 → 0.35, score=1.0 → ceiling
    sigmoid = 1.0 / (1.0 + math.exp(-8.0 * (raw_score - 0.5)))
    return 0.10 + (empirical_ceiling - 0.10) * sigmoid
```

**Proper scoring rule for evaluation.** Use Brier score and log-loss (both strictly
proper [9]) to evaluate calibration quality, not accuracy. A model that always outputs
50 % probability has low accuracy but may be better-calibrated than one that outputs
95 % for a 68 %-accurate classification.

### 3.9 Output contract

```python
@dataclass
class SingleCount:
    # Primary count
    primary: list[CandidateCount]      # the DP-optimal non-overlapping cover
    primary_score: float               # joint score of primary path
    degree: int                        # anchored degree integer
    degree_label: str                  # "Minor", "Intermediate", etc.
    degree_confidence: str             # "CONFIRMED" | "HEURISTIC" | "SPECULATIVE"
    confidence_pct: float              # calibrated P(structurally correct) in [0,1]

    # Alternates (for honest disclosure)
    alternates: list[list[CandidateCount]]  # up to 4 alternate paths
    alternate_scores: list[float]           # relative to primary (primary=1.0)

    # Diagnostics
    monowave_count: int                # degree validation: should be 13-55
    hard_fails: int                    # hard-rule violations in primary (should be 0)
    notes: list[str]                   # human-readable caveats
    t_generated: int                   # bar index when this count was generated (causal)
```

---

## 4. Prioritised Implementation Plan

### Phase 1 — Causal pivot infrastructure (prerequisite for everything)

**Priority: Blocking.** All later phases depend on correct causal pivots.

1. Rewrite `toolkit.py:zigzag` to add `confirmed_t` timestamp alongside `t_extreme`.
   Expose a `backtest_mode` boolean (True in all non-live contexts). This fixes the
   single largest source of silent look-ahead in the current engine.
2. Implement `causal_zigzag(bars, atr_mult, atr_period)` as described in §3.2, running
   at four standard multipliers.
3. Add MDL curve computation to auto-select the four "natural" multipliers for a given
   instrument and date range (can use a simple grid search over `m ∈ [0.5, 10.0]` with
   50 logarithmically spaced candidates).
4. Tests: assert that no pivot in the output stream has `t_confirmed <= t_extreme`; assert
   that a known look-ahead-safe replay produces identical pivot streams on two consecutive
   runs (determinism check).

**Estimated effort: 2–3 days.**

### Phase 2 — Scoring function (Step D)

**Priority: High.** Needed before candidate ranking or DP selection.

1. Implement `compute_score(waves, result)` with the IWSS-style weighted formula in §3.5.
2. Add `_fib_proximity(ratio, targets)` using Gaussian kernel (sigma = 2 % relative).
3. Parametrise `RULE_WEIGHTS` in a config dict so weights can be tuned by backtesting.
4. Tests: score a known-good AVGO/MRVL count and assert score ≥ 0.60; score a known
   rule-violating count and assert score ≤ 0.20.

**Estimated effort: 1–2 days.**

### Phase 3 — Global DP single-count selection (Step E)

**Priority: High.** This is the core contribution — replacing the fragmented-roots problem.

1. Implement `global_single_count(candidates, pivots)` with beam width B=5.
2. Store the top-5 paths as alternates.
3. Compute alternate relative scores vs primary.
4. Tests: on a 50-pivot synthetic series with one planted perfect impulse and several
   partial overlapping counts, assert that the DP selects the planted impulse as primary.

**Estimated effort: 2 days.**

### Phase 4 — Neely bottom-up degree promotion (Step B)

**Priority: Medium.** Needed for degree anchoring but the heuristic can be used as a
stopgap initially.

1. Implement `build_degree_stack(bars)` with the promotion loop described in §3.3.
2. Enforce the Neely 13–55 monowave complexity window as a promotion gate.
3. Tests: assert that a known 5-wave Cycle-degree pattern on AVGO weekly data promotes
   correctly to degree 5 (Primary) without error.

**Estimated effort: 3–4 days (complexity of Neely retracement depth table).**

### Phase 5 — Degree anchoring (Step F)

**Priority: Medium.** Depends on Phase 4.

1. Implement `anchor_degree(primary_count, degree_stack)`.
2. Implement extended-wave velocity calculation (amplitude/bars).
3. Implement parent-alignment cross-check against degree+1 pivot stream.
4. Surface `degree_confidence ∈ {"CONFIRMED", "HEURISTIC", "SPECULATIVE"}` in output.

**Estimated effort: 1–2 days.**

### Phase 6 — Confidence calibration (Step G)

**Priority: Lower (requires backtesting data).** Can ship with the cold-start sigmoid
initially and replace with isotonic calibration once 200+ outcomes are recorded.

1. Add `raw_to_confidence(score, empirical_ceiling)` as the cold-start transform.
2. During backtesting harness (`wavelib/backtest.py`), record `(raw_score, outcome)` pairs.
3. After `n >= 200` pairs: fit isotonic regression using `statistics` module or a
   vendored 50-line PAV implementation (no scipy needed, stdlib-only).
4. Evaluate with Brier score at each walk-forward fold.

**Estimated effort: 1 day for cold-start; 2–3 days for full isotonic calibration.**

### Phase 7 — Integration and output contract

1. Wire Phases 1–6 into `wavelib/automation.py:label_and_validate` to replace the
   current multi-root output with a `SingleCount` object.
2. Update `wavelib/confluence.py:score_reversal` to consume `SingleCount.confidence_pct`
   as an additional confluence strand input (the 8th strand, complementing the 7th
   cycle-signal seam).
3. Update `wavelib/charting.py:render_chart` to display primary count + alternates with
   visual confidence encoding (opacity proportional to `alternate_scores`).

**Estimated effort: 2 days.**

---

## 5. Honest Caveats

### 5.1 The subjectivity ceiling

The academic literature is consistent: automated Elliott Wave recognition achieves
60–70 % accuracy on in-sample data [1][2][3][4]. In-sample. Batchelor & Ramyar [5]
found that Fibonacci ratios do not appear in filtered DJIA trends more often than chance,
though Prechter's rebuttal argues the paper tested filtered trends, not actual Elliott
Wave pivots. Neither side has produced a large-scale, independent, out-of-sample
validation. PyBacktesting [10] showed Sharpe > 3 in-sample but -14 out-of-sample in one
fold — a canonical overfitting result.

The subjectivity ceiling exists because:

- Two trained analysts produce different counts for the same chart with meaningful
  frequency. If experts disagree, any algorithm that agrees with one analyst is
  disagreeing with another.
- The rules underdetermine the labeling: Neely's full rule set runs ~600 pages, and even
  then dozens of scenarios are marked "analyst judgment required."
- The Fibonacci guidelines are soft: Batchelor & Ramyar demonstrate they add only weak
  discriminating power over base rates.

**Practical implication.** Set `empirical_ceiling = 0.65` in the cold-start calibration
and never advertise "the" correct count. The output contract always surfaces alternates.
`degree_confidence = "CONFIRMED"` means the count passes internal consistency checks,
not that it is objectively true.

### 5.2 Overfitting via rule tuning

The `RULE_WEIGHTS` dict in §3.5 has 9 free parameters. If those weights are tuned on the
same data used to evaluate confidence calibration, the calibration will be overfit.
Enforce strict train/calibration/test split:

- Train set: tune `RULE_WEIGHTS` on the oldest 60 % of history.
- Calibration set: fit isotonic regression on the next 20 %.
- Test set: evaluate Brier score and log-loss on the final 20 %. Never touch until all
  parameters are frozen.

### 5.3 The single-count is not a prediction

`SingleCount.primary` is the most structurally consistent interpretation of *past* price
as of bar `t`. It is not a prediction of what Wave 5 will do next or whether the current
position within the count is correctly identified. The count will change — possibly
dramatically — as new pivots are confirmed. Downstream code must handle count transitions
without treating a change in primary count as an error.

### 5.4 Degree anchoring is hard even for experts

Neely devotes multiple chapters to degree because it is the single most consequential and
error-prone judgment. The algorithmic anchor in §3.7 (complexity window + parent
alignment) is a necessary heuristic, not a definitive solution. In ambiguous cases the
system should output `degree_confidence = "SPECULATIVE"` and surface both possible degree
assignments as alternates. The user should be told: "This count is consistent with
[Intermediate] degree but could equally be [Minor] degree — the complexity window
({monowave_count} monowaves) is consistent with both."

### 5.5 Scale selection is correlated with the finding

The choice of ATR multiplier determines which pivots are "seen" and therefore which
counts are possible. If the multiplier is tuned to find a specific pattern, any
subsequent confidence estimate is circular. The MDL approach in §3.2 mitigates this by
selecting multipliers without reference to downstream pattern quality — use it.

---

## Sources

[1] Kotyrba, M., Volná, E., et al. (2013). *Methodology for Elliott Waves Pattern
Recognition*. ECMS 2013 Proceedings.
URL: https://scs-europe.net/dlib/2013/ecms13papers/is_ECMS2013_0050.pdf
(also via Semantic Scholar: https://www.semanticscholar.org/paper/Methodology-For-Elliott-Waves-Pattern-Recognition-Kotyrba-Voln%C3%A1/a2c39c0fff06593f92dac055be7456177c0e1aa8)

[2] Kotyrba, M., Volná, E. *Elliott Waves Recognition Via Neural Networks*.
Semantic Scholar: https://www.semanticscholar.org/paper/Elliott-Waves-Recognition-Via-Neural-Networks-Kotyrba-Voln%C3%A1/0f885f20f24cb2f8f9709688

[3] Kotyrba, M. et al. *Multi-classifier based on Elliott wave's recognition*.
ResearchGate: https://www.researchgate.net/publication/257312966_Multi-classifier_based_on_Elliott_wave%27s_recognition

[4] Vantuch, T., Zelinka, I., Vasant, P. (2018). *An Algorithm for Elliott Waves Pattern
Detection*. Intelligent Decision Technologies 12(1):15–24.
DOI: https://dl.acm.org/doi/10.3233/IDT-170319
Also: https://journals.sagepub.com/doi/abs/10.3233/IDT-170319

[5] Prechter, R. (response to Batchelor & Ramyar 2005). *Elliott Waves, Fibonacci and
Statistics*. Socionomics Institute.
URL: http://socionomics.org/pdf/EW_Fibo_Statistics.pdf

[6] *Grammar of the Wave: Towards Explainable Multivariate Time Series Event Detection
via Neuro-Symbolic VLM Agents*. arXiv preprint 2025.
URL: https://arxiv.org/abs/2603.11479

[7] Stochastic Context-Free Grammar / Viterbi parse.
Wikipedia (SCFG): https://web.mit.edu/neboat/tooling/6.863/Stochastic_context-free_grammar.htm
Inside-Outside algorithm: https://arxiv.org/pdf/cmp-lg/9805007

[8] PRESEE: MDL/MML for time-series stream segmentation.
PubMed Central: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3706014/

[9] Classifier Calibration survey (Platt scaling, isotonic regression, Brier score).
Springer Machine Learning: https://link.springer.com/article/10.1007/s10994-023-06336-7
arXiv: https://arxiv.org/pdf/2112.10327

[10] Ostiguy, P. PyBacktesting — genetic algorithm optimization of Elliott Wave strategy.
GitHub: https://github.com/philippe-ostiguy/PyBacktesting

[11] ElliottWaveAnalyzer — brute-force combinatorial EW pattern matcher.
GitHub: https://github.com/btcorgtfo/ElliottWaveAnalyzer

[12] python-taew — iterative forward-search EW labeler.
GitHub: https://github.com/DrEdwardPCB/python-taew

[13] elliot-waves-auto — ZigZag + Fibonacci projection web app.
GitHub: https://github.com/ESJavadex/elliot-waves-auto

[14] WaveBasis — commercial ML + expert-system EW platform.
Automatic Wave Counts docs: https://wavebasis.com/docs/reference-guide/automatic-wave-counts/
How WaveBasis works: https://wavebasis.com/docs/frequently-asked-questions/wavebasis/how-does-wavebasis-work/

[15] MotiveWave — commercial EW platform with Auto Decompose.
Elliott Wave docs: https://docs.motivewave.com/user-guide/elliott-wave
Auto-decompose video: https://www.motivewave.com/support/elliott_wave_auto_wave_decompose.htm

[16] Impulse Wave Structural Score (IWSS) and Corrective Wave Structural Score (CWSS).
algotrading-investment.com: https://algotrading-investment.com/2020/06/04/impulse-wave-structural-score-and-corrective-wave-structural-score/

[17] NeoWave monowave complexity control — Glenn Neely, *Mastering Elliott Wave* (1990).
Q&A (degree assignment): https://www.neowave.com/qow/qow-archive-13.asp
NeoWave basic concepts: https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/
Practical NeoWave: https://www.litefinance.org/blog/for-professionals/neowave-part-27-trading-strategy-based-on-the-neowave-theory-part-1/

[18] ZigZag ATR — TradingView library.
URL: https://www.tradingview.com/script/v8XJuorH-ZigZag-ATR/

[19] A-J Financial Solutions — EW Dataset (open-source labelled dataset).
GitHub: https://github.com/A-J-Financial-Solutions/EW_Dataset

[20] Large Language Models and the Elliott Wave Principle (ElliottAgents multi-agent system).
MDPI Applied Sciences: https://www.mdpi.com/2076-3417/14/24/11897
