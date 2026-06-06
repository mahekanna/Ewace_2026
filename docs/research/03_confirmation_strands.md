# 03 — Reversal-Confirmation Strands & Cycle-Seam Specification

**Repository:** `Ewace_2026`  
**Date:** 2026-06-05  
**Scope:** Research-only documentation. No code is created or modified.  
**Relation to `chakra_quant`:** The 7th strand (cycle window) is reserved for external Hurst/FLD input.
This document specifies the seam contract only; no import of `chakra_quant` occurs in this repo.

---

## 1. Scope & sources

This document covers the six price/structure confirmation strands already coded in
`wavelib/confluence.py`, plus the reserved 7th cycle-timing strand. Its purpose is threefold:

1. **Theory** — ground each strand in authoritative sources and articulate the correct
   construction that production-quality indicators use.
2. **Audit** — map every function in `confluence.py` to a fidelity rating and identify gaps.
3. **Seam spec** — define the typed interface the 7th strand expects from `chakra_quant`
   so the contract is explicit before any wiring begins.

Primary sources consulted: Investopedia, StockCharts ChartSchool, AltFins knowledge base,
EBC Financial Group, Trading Setups Review, RSI Divergence Detector (PyPI), Smart Money
Concepts references (DailyPriceAction, FXOpen, TradeThePool), Better Volume / MotiveWave
documentation, Hurst Cycles notes (hurstcycles.com, SentientTrader, ElliottWavePlus),
and the `chakra_quant` CLAUDE.md causal-only rule set (D-013).

---

## 2. Theory

### 2.1 RSI momentum divergence — regular vs hidden

**Correct construction.**
RSI (Wilder, 1978) applies an exponential smoothing with α = 1/14. The seed value for the
first smoothed average is the arithmetic mean of the first 14 up/down closes. Because the
smoothing tails never fully settle, StockCharts uses at minimum 250 historical bars before
the first displayed RSI value to guarantee accuracy [1]. In practice, a warm-up of 50–100
bars after the first 14 is sufficient for divergence work; the code's default 10-bar lookback
window calls `rsi()` on the full `closes` slice, so the effective warm-up is whatever the
caller provides — typically well under 30 bars in the current examples, producing noisy RSI.

Divergence is a **two-pivot comparison on both the price series and the RSI series**:

- *Regular bullish*: price makes a lower low between two confirmed swing lows; RSI makes a
  higher low at those same pivots. This is a reversal signal — momentum is not confirming the
  price extreme [2].
- *Regular bearish*: price higher high / RSI lower high. Reversal signal.
- *Hidden bullish*: price higher low / RSI lower low. Continuation of uptrend signal.
- *Hidden bearish*: price lower high / RSI higher high. Continuation of downtrend signal.

The critical word is **confirmed swing**. A swing low is the bar whose low is lower than the
N bars to its left and right (N ≥ 3, typically 5). Finding the index of `min(seg_lo[:-1])`
(as the code does) does not confirm a swing pivot — it just finds the global minimum of the
window, which may be in the middle of a corrective wiggle rather than a structural low.
Proper pivot detection requires that the candidate bar is a local extremum with at least
`left_bars` lower-high neighbours on both sides before it qualifies [2][3].

**Why >14 bars are needed.**
With only 14 closes, the RSI seed has not stabilised and there is only one pivot pair
possible. In practice, 50–100 bars are needed: roughly 14 bars for seed, 5+ bars for
left-confirmation of the first pivot, 5+ bars between the two pivots for statistical
separation, and 5+ bars for right-confirmation of the second pivot, totalling ≥ 29 bars
minimum with no slack. Industry implementations use 50–250 bars of history [1][3].

**Independence note.** RSI is a function of closes only; it is therefore not independent of
MACD (which also uses closes). They measure overlapping information — RSI through a ratio of
gains/losses, MACD through an EMA spread. Both strands confirming simultaneously adds less
evidence than two truly uncorrelated indicators would.

### 2.2 MACD turn — histogram inflection vs signal cross vs zero-line cross

**Three signals, three speeds [4][5]:**

| Signal | Timing | False-signal rate |
|---|---|---|
| Histogram inflection (3-bar monotone) | Earliest — precedes crossover by 1–3 bars | Highest — fires in every corrective wiggle in ranging markets |
| Signal-line cross (histogram = 0) | Mid-speed | Moderate — the canonical MACD signal |
| Zero-line cross (MACD line = 0) | Latest — lags trend start | Lowest — a confirmation of established trend, not early warning |

The code (`macd_turn`) checks that the last 3 histogram bars are strictly monotone in the
reversal direction (e.g., h[-3] < h[-2] < h[-1] for bullish). This is the histogram
inflection approach — it fires earliest but is also the most fragile:

- In a ranging market where the histogram oscillates in a narrow band, any 3-bar sequence
  will often satisfy the monotone condition by chance.
- A strict 3-bar test has no amplitude gate — a -0.01 → -0.005 → -0.001 histogram counts
  the same as -2.0 → -1.0 → 0.5.
- MACD requires approximately 26 + 9 = 35 bars of input before both the slow EMA and the
  signal EMA have fully warmed up. With the EMA cold-start bias, the first 35 bars of
  histogram values overstate momentum.

**Improvement:** require that the histogram cross zero within the 3-bar window (signal-line
cross), or add a minimum absolute amplitude threshold (e.g., histogram magnitude > 0.1 ×
ATR) to filter noise.

### 2.3 Volume climax and capitulation

**Correct construction [6][7]:**
Volume climax is a spike of 2×–5× the rolling average volume on a single bar, occurring at
or near a price extreme after an extended directional move. Key distinctions:

- **Climax / capitulation**: extreme volume + large range + price at multi-bar extreme.
  Weak holders are exhausted. Typically 3×–5× average [6].
- **High-volume churn**: large volume + *narrow* range (close near open). Institutional
  absorption; not a reversal signal by itself. A narrow-range bar printing 2×–3× average
  can look like a climax spike but indicates distribution or accumulation rather than
  exhaustion [7].
- **Threshold calibration**: the widely cited minimum for institutional participation is
  1.5×–2.0× the 20-day average [7]. The code uses 1.8× over a 10-bar average. The 10-bar
  window is short enough to be vulnerable to intraday intraweek variation; 20 bars is the
  industry standard.
- **Lookback for average**: most volume indicators (IBD, CAN SLIM, Better Volume) use the
  20-bar simple average, not 9 bars. A 10-bar average inflates RVOL after a low-volume
  period and deflates it after a high-volume cluster.

The code's `volume_capitulation` checks `max(vols[-3:]) > avg * 1.8`, which catches the
most recent 3-bar window — acceptable heuristic but does not distinguish climax from churn
because it has no price-range filter.

### 2.4 Market structure: CHoCH and BOS (Smart Money Concepts)

**Precise definitions [8][9]:**

A **swing high** is a bar whose high is strictly greater than the highs of N bars to its
left and right (N = left/right strength, typically 5). A **swing low** is defined
analogously. This confirmation has an inherent lag of N bars — a pivot at bar `t` is
confirmed at bar `t + N`.

- **BOS (Break of Structure)**: price closes beyond the most recent confirmed swing high
  (uptrend) or swing low (downtrend). Confirms trend continuation.
- **CHoCH (Change of Character)**: price closes beyond the swing that produced the *prior
  BOS* — i.e., it breaks the structural level in the *opposite* direction to the prevailing
  trend. This is the first signal that the trend may be reversing.

**Body-close requirement**: SMC practitioners require a full-candle-body close beyond the
structural level, not just a wick penetration, to validate a CHoCH. Wick-only breaks have
high false-positive rates in illiquid or gapped markets [8].

**The code's shortcut**: `choch()` computes `max(h[:-1])` over the last N bars and checks
whether the final bar exceeds it. This is equivalent to asking "does bar −1 make a new
N-bar high?" — which is the definition of a BOS, not a CHoCH. True CHoCH requires (a) a
confirmed swing structure (not a rolling maximum), (b) identification of the trend direction
prior to the break, and (c) that the break is counter-directional to that trend. A rolling
max over 8 bars produces frequent triggers in sideways markets and does not encode any
structural memory of the prior trend.

### 2.5 Counter-trend channel break

**Correct construction [10][11]:**
A counter-trend channel is drawn by anchoring two endpoints at confirmed swing highs (for a
down-channel) or swing lows (for an up-channel), producing a descending resistance line
(bearish channel top). A genuine break requires:

1. At least two confirmed pivots to define the channel line (not just one touch).
2. A bar closing on the other side of the line (close-based, not wick).
3. Optionally, a re-test of the broken line as support/resistance (confirmation).

The code's `channel_break()` checks whether the latest close is above/below an EMA9 of
closes. EMA9 is not a channel line — it is a short-term trend filter. In a smooth decline,
close > EMA9 may confirm a reversal, but in a volatile decline with price oscillating around
EMA9, the condition will fire and reset on consecutive bars. The strand is essentially
measuring short-term mean-reversion, not a structural channel break.

### 2.6 Philosophy of independent confirmation

**The independence requirement [12]:**
The core thesis of multi-strand confluence scoring is that independent evidence sources fail
separately. Two indicators are independent if their false-positive rates are not correlated
— that is, if Indicator A misfires on a particular bar, knowledge of that misfire does not
increase the probability that Indicator B also misfires on the same bar.

In practice, RSI, MACD, and the code's channel break (EMA9) all derive from the same close
series and share systematic biases in ranging markets. When price consolidates after a
decline, all three will simultaneously show "turning up" — not because a reversal is
confirmed, but because the shared input (closes) is slightly rising. This is the "echo
chamber" failure mode: stacking correlated indicators inflates perceived confidence [12].

**Truly independent strands** span different data families:
- Price-derivative: RSI, MACD, channel break (all highly correlated)
- Volume: capitulation, VWAP deviation (partially correlated with price extremes)
- Market structure: CHoCH/BOS (price-derived but encodes structural memory, lower correlation with momentum)
- Time / cycle: Hurst/FLD (not derived from price magnitude at all — derived from cycle phase)

**Score thresholds and false-positive tradeoffs [12]:**
With 7 strands and Bernoulli false-positive rate p per strand, the probability of ≥4 strands
confirming by chance is C(7,4)·p⁴·(1-p)³ + higher terms. At p = 0.3 (typical for any
single momentum indicator in a ranging market), P(score ≥ 4 by chance) ≈ 12%. At p = 0.15
(with filtering), P(score ≥ 4 by chance) ≈ 1.5%. The score threshold of 4 is therefore
appropriate *only if* the strands are meaningfully independent; with the current highly
correlated implementation, 4/7 provides less protection than the number implies.

The current tier labels (≥4: HIGH-CONFIDENCE, 2–3: BUILDING, ≤1: STRUCTURALLY-ALLOWED-ONLY)
are directionally correct but should be treated as *rough* signal tiers, not calibrated
probabilities, until the strands are hardened and independence is verified empirically.

### 2.7 Hurst/FLD cycle timing as a 7th confirmation strand

**Mechanism [13][14]:**
JM Hurst's Future Line of Demarcation (FLD) is the median price (or close) displaced forward
in time by exactly half the cycle's nominal wavelength. When price crosses the FLD upward,
it confirms that a cycle trough has formed — the cycle's "when" is established. This signal
is causal: the FLD at bar `t` uses price data through bar `t − floor(L/2)`, shifted forward,
so no future data is consumed [14].

**Complement to Elliott Wave structure:**
Elliott Wave tells you *where* a reversal is structurally permitted (e.g., a fifth-wave
terminal zone). Hurst cycles tell you *when* a trough or peak is due relative to the nominal
cycle period. The two methods use different measurement families (price ratios vs. time
periodicity) and therefore fail independently — a confirmed FLD cross at a fifth-wave
terminal zone is a genuinely orthogonal confirmation [13].

As `chakra_quant` implements this machinery (see its `src/fld/` package and D-013
causal-only rules), the correct design is a one-way feed: `chakra_quant` computes a boolean
at bar `t` using data ≤ `t` only, and passes it into `score_reversal(..., cycle_aligned=True)`.
This preserves the dependency-free structure of `Ewace_2026` while adding the only truly
time-domain, price-magnitude-independent confirmation strand.

---

## 3. Current wavelib audit

Gap table for every public function in `wavelib/confluence.py`:

| Concept | Implemented? (file:func) | Fidelity | Gap note |
|---|---|---|---|
| RSI calculation | `confluence.py:rsi` | **Heuristic** | Wilder smoothing correct; seed = simple mean of first N bars (standard). No warm-up guard — returns `None` only if `len(closes) <= n`, meaning a 15-bar input silently returns one valid RSI value that is still initialisation noise. |
| EMA | `confluence.py:ema` | **Full** | Standard exponential smoothing with cold-start (first value = first input). Acceptable for MACD; would benefit from a warm-up period flag. |
| MACD | `confluence.py:macd` | **Heuristic** | Correct formula (fast EMA − slow EMA, signal = EMA of MACD). No warm-up guard; first 26–35 bars are biased. |
| Fib/structure zone | `confluence.py:in_zone` | **Full** | Simple price-in-range check. Correct by construction; the quality of the zone itself is the caller's responsibility. |
| Momentum divergence | `confluence.py:momentum_divergence` | **Stub** | Uses `seg_lo.index(min(seg_lo[:-1]))` as the "prior pivot" — this is the global minimum of the window, not a confirmed swing low. Does not detect RSI swing pivots at all. Fails to distinguish regular from hidden divergence. Requires ≥50 bars of closes to produce meaningful RSI; the function returns False ("insufficient RSI history") on the typical 20–30-bar input in `score_reversal`. |
| MACD turn | `confluence.py:macd_turn` | **Heuristic** | 3-bar monotone histogram check is a valid early-warning heuristic but has no amplitude gate, making it noise-sensitive in low-volatility or ranging markets. Does not distinguish histogram inflection from signal-line cross. |
| Volume capitulation | `confluence.py:volume_capitulation` | **Heuristic** | 9-bar average with 1.8× threshold is a workable approximation. Gap 1: 10-bar window is below the industry standard of 20 bars. Gap 2: no price-range filter to distinguish climax (wide range) from churn (narrow range). Gap 3: checks `max(vols[-3:])` — could trigger 3 bars after the climax spike rather than at it. |
| CHoCH (higher-high) | `confluence.py:choch` | **Stub** | `max(h[:-1])` over `lookback` bars is equivalent to detecting a rolling-window high break (BOS), not a CHoCH. Does not define or store prior structural trend. Does not require body close — uses raw high values. No confirmation lag (N bars left/right). In a sideways market this fires on nearly every other bar. |
| Counter-trend channel break | `confluence.py:channel_break` | **Stub** | EMA9 of closes is not a channel line. A two-point anchored resistance/support trendline is the correct construction. The EMA9 test is essentially measuring whether close > recent average close — a mean-reversion signal, not a structural channel break. |
| Swing sequence classifier | `confluence.py:classify_swing_sequence` | **Heuristic** | Counts alternating pivots and classifies 3 = corrective, 5 = impulsive by leg count only. This is the correct heuristic per Elliott Wave conventions but does not validate internal relationships (ratios, overlap). Acceptable as a quick label, not as a validated count. |
| ConfluenceReport aggregator | `confluence.py:ConfluenceReport` | **Full** | Score aggregation, max_score, and string rendering are correct. The `cycle_aligned` boolean seam is in place. Verdict tiers (≥4/2-3/≤1) are directionally appropriate. |
| score_reversal orchestrator | `confluence.py:score_reversal` | **Full** | Correctly unpacks bars, passes sub-slices to each strand, assembles the report. The `cycle_aligned` pass-through is already wired. No guard for minimum bar count — callers may silently get a degraded score. |

**Summary of fidelity distribution:** 2 Full, 4 Heuristic, 3 Stub, 0 Missing. The two
most critical gaps for production use are `momentum_divergence` (needs swing-pivot–based
construction and ≥50 bars) and `choch` (needs proper SMC pivot confirmation, not a rolling
maximum).

---

## 3.5 Cycle-seam spec (chakra_quant bridge — seam only)

**This section documents a future integration interface. No `chakra_quant` code is
imported or wired in this pass.**

### Motivation

The 7th confluence strand is reserved in `score_reversal(..., cycle_aligned: bool = False)`
and in `ConfluenceReport.cycle_aligned`. This is currently an untyped boolean with no
documented contract for what must be true when it is set to `True`. This section specifies
that contract precisely so that when `chakra_quant`'s FLD model is eventually plumbed in,
both sides have a written specification to code against.

### Strand-7 interface — current signature

```python
def score_reversal(
    symbol: str,
    bars: list[tuple],        # (t, o, h, l, c, v)
    zone: tuple[float, float],
    bullish: bool = True,
    cycle_aligned: bool = False,   # ← 7th strand input
) -> ConfluenceReport:
    ...
```

```python
@dataclass
class ConfluenceReport:
    ...
    cycle_aligned: bool = False    # ← stored verbatim, contributes +1 to score
```

### Required enrichment — typed payload

The bare `bool` is insufficient for audit, provenance, and forward-debugging. The seam
should accept (or be constructable from) a typed payload that `chakra_quant` populates:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CycleSignal:
    """
    Causal cycle-timing signal produced by chakra_quant at bar t.

    CONTRACT:
    - `aligned` is derived using ONLY data with timestamp <= t (D-013 causal-only rule).
    - No centered filters, no df.shift(-N) with N > 0, no scipy.signal.filtfilt.
    - The FLD is constructed as: close displaced forward by floor(cycle_period / 2) + 1
      bars (per chakra_quant D-005), so the FLD value at bar t uses close[t - half_period].
    - A bullish alignment: close[t] crossed above the FLD within the last `confirmation_bars`
      bars AND the cycle phase is in the bottom half of its nominal period (phase < pi).
    - A bearish alignment: close[t] crossed below the FLD AND phase > pi.
    """
    aligned: bool                     # True = cycle timing supports the reversal direction
    cycle_period: int                 # Nominal cycle period in bars (e.g. 20, 40, 80)
    phase: float                      # Current cycle phase in radians [0, 2*pi)
    source: str                       # e.g. "hurst_fld_20bar" or "goertzel_40bar"
    fld_value: Optional[float] = None # The FLD level at bar t (for logging/chart overlay)
    confirmation_bars: int = 3        # How many bars back the FLD cross was detected
```

**Proposed updated signature:**

```python
def score_reversal(
    symbol: str,
    bars: list[tuple],
    zone: tuple[float, float],
    bullish: bool = True,
    cycle_aligned: bool = False,          # backward-compatible boolean (legacy)
    cycle_signal: Optional[CycleSignal] = None,  # rich payload (preferred)
) -> ConfluenceReport:
    ...
    effective_aligned = cycle_signal.aligned if cycle_signal is not None else cycle_aligned
    ...
```

`ConfluenceReport` should be extended to carry the `CycleSignal` instance for downstream
logging:

```python
@dataclass
class ConfluenceReport:
    ...
    cycle_aligned: bool = False
    cycle_signal: Optional[CycleSignal] = None
```

### What chakra_quant must supply

To set `CycleSignal.aligned = True` for a bullish reversal at bar `t`, `chakra_quant` must
satisfy ALL of:

1. **FLD construction is causal** (D-013): the FLD at bar `t` is the close displaced by
   `floor(L/2) + 1` bars (D-005). It uses `close[t - half_period]` — only historical data.
2. **Cycle period is calibrated** (D-006): Goertzel scan over Hurst nominal slot ±15%.
   The `cycle_period` field records the winning period for provenance.
3. **Phase is computed causally**: sliding-window FFT or Hilbert homodyne (not batch
   `scipy.signal.hilbert` on the full array — that is forbidden under D-013).
4. **FLD cross is recent**: close[t] just crossed above (bullish) or below (bearish) the
   FLD within `confirmation_bars` bars. A stale cross (> 5 bars ago) should not set
   `aligned = True` for the current bar.
5. **Phase gate**: the cross is more meaningful if the cycle phase is in the bottom half
   (trough region, phase < π) for a bullish cross, or the top half (peak region, phase > π)
   for a bearish cross. The phase gate is recommended but may be omitted if cycle extraction
   is noisy.

### Explicit seam contract (non-negotiable)

- **Ewace_2026 makes no import of `chakra_quant`.** The `CycleSignal` dataclass lives in
  `wavelib/confluence.py` (or a new `wavelib/cycle_seam.py`) and is populated by the caller.
- **`chakra_quant` makes no import of `Ewace_2026`.** It computes a `CycleSignal`-shaped
  dict or object and passes it to `score_reversal` from outside.
- The field names `aligned`, `cycle_period`, `phase`, `source` are the agreed protocol.
  If `chakra_quant` changes its internal names, an adapter layer in the calling code
  translates them — neither library mutates to match the other.
- **Causal-only is non-negotiable** (D-013 in `chakra_quant`'s decisions log). If
  `CycleSignal.aligned` is ever set using future-looking data, the backtest of
  `score_reversal` becomes invalid. The `source` field should encode the algorithm name
  so post-hoc audits can verify causality (e.g., "goertzel_40bar" vs "batch_fft_40bar").

---

## 4. Build roadmap

Tasks are ordered by impact and dependency. Causal-only concerns are flagged with [C].

### Priority 1 — Fix `momentum_divergence` (swing-pivot–based RSI divergence)

**Why first:** RSI divergence is the most theoretically grounded and commonly cited
confirmation of wave-terminal exhaustion. The current implementation silently returns `False`
for most realistic bar counts (<50) and uses a structurally incorrect prior-pivot detection
even when it does run.

**Tasks:**
1a. Add a `zigzag_pivots(series, n_left, n_right)` helper (pure stdlib) that returns
confirmed local extrema with a lag of `n_right` bars — causal by design [C].  
1b. Rewrite `momentum_divergence` to detect paired swing lows/highs on both the price
and RSI series using this helper. Check for regular bullish divergence (price LL / RSI HL)
and regular bearish divergence (price HH / RSI LH).  
1c. Add hidden divergence detection as a separate boolean in the return value.  
1d. Enforce a minimum of `2 * rsi_period + 2 * n_right + pivot_separation` bars (≈ 50+
for n=14, n_right=5) and raise `InsufficientDataError` if not met rather than silently
returning `False`.  
1e. Add amplitude filter: require RSI difference between the two pivots > 3 points to
suppress micro-divergences.

**Causal note [C]:** The `n_right` confirmation lag is inherent to pivot detection. At bar
`t`, the most recently confirmed swing low occurred at bar `t − n_right`. This is causal:
the comparison uses data ≤ `t` only.

### Priority 2 — Fix `choch` (proper SMC swing-pivot structure)

**Why second:** CHoCH is the market-structure strand — it measures whether institutional
order flow has shifted direction. The current rolling-max approach fires in sideways markets
and does not encode structural memory, making it the strand most likely to produce
correlated false positives alongside `channel_break`.

**Tasks:**
2a. Replace `max(h[:-1])` with a call to the `zigzag_pivots` helper from Task 1a.
Store the last confirmed swing high and swing low for the lookback period.  
2b. Track the **prior structural trend**: is the current sequence making higher highs/higher
lows (uptrend) or lower highs/lower lows (downtrend)? A CHoCH occurs when the break is
**counter-directional** to this established trend.  
2c. Add a body-close filter: the breaking bar must close beyond the pivot level, not merely
wick through it. Use `closes[-1]` vs pivot price rather than `highs[-1]`.  
2d. Distinguish BOS (trend-continuation break) from CHoCH (counter-trend break) and expose
both as separate `Strand` values so callers can use either or both.

**Causal note [C]:** Pivot confirmation via `n_right` bars introduces a lag but is causal.
The `choch` function must not look forward — all pivots are confirmed at bar `t − n_right`.

### Priority 3 — Add `CycleSignal` payload type and update `score_reversal` signature

**Why third:** The seam is already coded as a bare `bool`; formalising it as a typed
dataclass costs almost nothing and prevents the 7th strand from being misused (e.g., set
to `True` by a non-causal source). This task should land before any integration work begins
so both repos have an agreed protocol.

**Tasks:**
3a. Add `CycleSignal` dataclass to `wavelib/confluence.py` (or a new `wavelib/cycle_seam.py`).  
3b. Update `score_reversal` signature to accept `cycle_signal: Optional[CycleSignal] = None`
alongside the legacy `cycle_aligned: bool = False`.  
3c. Populate `ConfluenceReport.cycle_signal` from the passed payload.  
3d. Update `__str__` to log `cycle_signal.source`, `cycle_period`, and `phase` when present.  
3e. Write a unit test that passes a mock `CycleSignal(aligned=True, cycle_period=20,
phase=0.8, source="test")` and verifies the score is incremented.

### Priority 4 — Harden `volume_capitulation`

4a. Extend average window from 10 to 20 bars (industry standard).  
4b. Add a price-range filter: a qualifying capitulation bar has range > 1.5 × ATR(20).
This separates climax from churn.  
4c. Change `max(vols[-3:]) > avg * mult` to `vols[-1] > avg * mult` OR document clearly
that the strand fires up to 3 bars after the actual climax. Both choices are defensible but
the semantics differ.  
4d. Consider raising the threshold to 2.0× for high-cap liquid equities (AVGO, MRVL) where
1.8× is easily hit on ordinary institutional rebalancing.

### Priority 5 — Replace `channel_break` with a structural trendline break

5a. Add a `linear_regression_channel(closes, n)` or two-pivot anchored trendline builder.  
5b. Detect the two most recent confirmed swing highs (downtrend) or swing lows (uptrend)
using the `zigzag_pivots` helper.  
5c. Project the channel line to bar `t` and check whether `closes[-1]` has crossed it.  
5d. Add a minimum channel duration filter (e.g., ≥ 10 bars between the two anchoring pivots)
to suppress micro-channel noise.  
**Causal note [C]:** The channel is anchored to confirmed historical pivots only; projection
to bar `t` is causal. Linear extrapolation uses no future data.

### Priority 6 — Minimum bar count guard in `score_reversal`

6a. Add a `_MIN_BARS = 50` constant and raise `ValueError` or return a degraded report
with a warning if `len(bars) < _MIN_BARS`. The current silent failure mode (strands return
`False` without explanation) masks data quality problems.

### Priority 7 — Backtest harness and strand independence verification

7a. Implement `replay_reversals(bars, zones, labels)` that calls `score_reversal` at each
labelled reversal and each non-reversal bar in the same zones.  
7b. Compute a contingency table and pairwise φ coefficient for all strand pairs. Flag any
pair with |φ| > 0.3 as insufficiently independent.  
7c. Calibrate the score threshold empirically: find the score cutoff that maximises
precision at ≥ 60% recall on held-out data (≠ training data used to set zones).

---

## 5. Open questions and subjectivity caveats

**5.1 RSI period choice.** The code uses the Wilder default of 14. For weekly timeframes,
where AVGO and MRVL weekly data is the primary source, 14 weeks is 3.5 months — a reasonable
intermediate-term window. For 4H data, 14 bars = 56 hours ≈ 7 trading days, which may be
too short to capture medium-cycle momentum shifts. The period should arguably scale with
the cycle under analysis.

**5.2 Divergence subjectivity.** Divergence detection on swing pivots requires a judgment
call on what constitutes a "significant" pivot vs. noise. The `n_left` / `n_right`
confirmation window and the ZigZag `pct` parameter are both user-tunable and interact.
There is no universally correct setting; practitioners disagree whether 3-bar or 5-bar
pivot confirmation is more robust.

**5.3 CHoCH vs. MSS (Market Structure Shift).** Some SMC practitioners define CHoCH and
MSS as synonymous; others treat MSS as a higher-timeframe CHoCH. This library does not
currently distinguish timeframes. Adding multi-timeframe confluence would require either a
second data series or a downsampler, both of which increase complexity.

**5.4 FLD phase gate.** The `CycleSignal.phase` gate (only flag `aligned = True` if
phase < π for a bullish cross) is recommended in §3.5 but adds a dependency on cycle
extraction quality. If `chakra_quant`'s Goertzel scan is noisy or the dominant cycle shifts
between calibration windows, the phase may be unreliable. A simpler contract — FLD cross
within N bars, no phase gate — is more robust but less informative.

**5.5 Score threshold calibration.** The current HIGH-CONFIDENCE threshold of 4/7 is
inherited from the session that built the library and has not been backtested. With three
stub-fidelity strands (momentum_divergence, choch, channel_break) often returning `False`
by construction, the effective max score for real data is approximately 4 (zone + MACD +
volume + one structural strand). In practice the system almost never exceeds 4 today —
meaning "HIGH-CONFIDENCE" requires nearly all functioning strands to fire simultaneously.
After the Priority 1–3 tasks above are implemented, the threshold should be recalibrated.

**5.6 Volume data availability.** The `volume_capitulation` strand requires volume in the
bar tuple (t, o, h, l, c, v). AVGO weekly data in `data/avgo.py` is stored as `(t, h, l, c)`
without volume; passing weekly bars to `score_reversal` will raise an IndexError at `b[5]`.
This is a data-quality gap, not a code bug, but it prevents the volume strand from running
on the most structurally relevant (weekly) timeframe.

---

## Sources

1. StockCharts ChartSchool — Relative Strength Index (RSI): RSI warm-up period discussion, 250-bar recommendation:
   https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi

2. EBC Financial Group — RSI Divergence Strategies (regular vs hidden, swing-based pivot detection):
   https://www.ebc.com/forex/rsi-divergence-strategies-timing-the-market-like-a-pro

3. PyPI — rsi-divergence-detector package (pivot detection methodology, prominence/distance parameters):
   https://pypi.org/project/rsi-divergence-detector/

4. AltFins Knowledge Base — MACD Line and Signal Line (histogram inflection vs signal cross vs zero-line cross):
   https://altfins.com/knowledge-base/macd-line-and-macd-signal-line/

5. Mind Math Money — Understanding the MACD Indicator (histogram signal timing comparison):
   https://www.mindmathmoney.com/articles/understanding-the-macd-indicator-macd-line-signal-line-histogram-crossover-and-zero-line

6. FasterCapital — Volume Climax: A Game Changer in Market Analysis (climax 3–5× threshold):
   https://fastercapital.com/content/Volume-climax--A-Game-Changer-in-Market-Analysis.html

7. Trade That Swing — Advanced Guide to Trading Stocks Based on Volume (20-bar average, 1.5–2× institutional threshold, churn distinction):
   https://tradethatswing.com/advanced-guide-to-trading-stocks-based-on-volume-and-volume-analysis/

8. DailyPriceAction — SMC Market Structure: BOS and CHoCH Made Simple (body close requirement, CHoCH vs BOS definition):
   https://dailypriceaction.com/blog/smc-market-structure/

9. GitHub — joshyattridge/smart-money-concepts (Python implementation: swing_length parameter, swing high/low N-bar detection, close_break flag):
   https://github.com/joshyattridge/smart-money-concepts

10. TrendSpider — Breakout Detection (one full candlestick close through trendline requirement):
    https://help.trendspider.com/kb/automated-technical-analysis/breakout-detection

11. QuantifiedStrategies — Trendline Trading Strategy (two-pivot anchor, close-based break):
    https://www.quantifiedstrategies.com/trendline-trading-strategy/

12. Bairman Capital — Confluence in Trading (independence requirement, echo-chamber failure mode):
    https://beirmancapital.com/confluence-in-trading/

13. ElliottWavePlus — How Hurst Cycle Analysis Improves Elliott Wave Counts (FLD complement to Elliott structure, "where" + "when" combination):
    https://elliottwaveplus.com/how-hurst-cycle-analysis-improves-our-elliott-wave-counts/

14. PrescienTrading — The Future Line of Demarcation (FLD construction: price displaced forward by half cycle period, FLD cross confirms trough/peak):
    https://prescientrading.com/kb/the-future-line-of-demarcation-fld/

15. Hurst Cycles Notes — FLDs (FLD crossing as cycle-timing signal):
    https://notes.hurstcycles.com/flds/

16. TradeThePool — Smart Money Concepts Terminology (CHoCH two-candle close confirmation, pivot confirmation lag):
    https://tradethepool.com/technical-skill/smart-money-concepts-terminology/

17. Macroption — RSI Calculation (Wilder smoothing mechanics, seed period):
    https://www.macroption.com/rsi-calculation/
