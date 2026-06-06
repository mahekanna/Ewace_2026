# 04 — Automation & Validation
**Workstream: bridging the hand-picked-legs engine to an automated, testable system**

Version 0.1 · Research draft · 2026-06-05

---

## 1. Scope & sources

This document covers five interrelated topics that together constitute the "then start coding" target for the Ewace_2026 engine:

1. Multi-scale ZigZag / pivot detection (percentage vs ATR-adaptive vs fractal pivots) and how multiple pivot streams feed a wave-degree hierarchy.
2. Auto-labeling: segment pivots → enumerate candidate impulse / correction counts at multiple degrees → validate each against the rule engine → score and rank.
3. Auto-degree assignment via Neely's bottom-up monowave → polywave → multiwave construction (the biggest remaining subjectivity).
4. Backtest / hit-rate harness: replay bars causally, score reversals at permitted zones, measure hit-rate of score≥4 zones vs invalidation levels, walk-forward validation.
5. Causal-only discipline: every signal at bar `t` must use only data ≤ `t`; ZigZag confirmation lag; how that binds to the sibling repo `chakra_quant` D-013 requirement.
6. Programmatic charting to replace the hand-built `charts/*.html` SVG files.

Primary audience: a developer starting the automation layer immediately after reading `DOCUMENTATION.md` and `CLAUDE.md`.

Cross-references:
- `docs/research/02_neowave_neely.md` — NeoWave construction rules (authoritative for degree-assignment rationale).
- `wavelib/toolkit.py` — current single-scale `zigzag` implementation.
- `wavelib/rules.py` — `validate_impulse` / `validate_correction` / `report` engines.
- `wavelib/confluence.py` — `score_reversal` and strand definitions.
- `chakra_quant` D-013: causal-only signal law that this repo must satisfy at the seam.

---

## 2. Theory / design

### 2.1 Multi-scale ZigZag and wave-degree pivot hierarchies

The current `zigzag(bars, pct)` in `toolkit.py` produces a single flat list of pivots using a fixed percentage-reversal threshold. This is adequate for manual analysis of one timeframe, but an automated system needs multiple concurrent pivot streams, each corresponding to a distinct wave degree.

**Percentage-reversal vs ATR-adaptive vs fractal pivots**

The oldest and most common approach uses a fixed percentage reversal: a new pivot is registered only when price reverses by at least `pct` of the prior extreme. This is simple but fails in regimes where volatility changes dramatically — a 5% filter that is "right" in quiet markets masks real structure in a high-ATR environment.

ATR-based ZigZag variants replace the fixed `pct` with a dynamic threshold: `threshold = ATR(n) × multiplier`. Because ATR tracks realised volatility, the same multiplier produces structurally comparable swings across volatility regimes. Practical implementations (e.g. the ZigZag ATR library on TradingView/cTrader) confirm that this approach reduces spurious pivots during ranging without suppressing genuine structure during trending phases. The key design choice is the ATR period `n` and the multiplier: smaller multipliers catch Minor-degree swings, larger multipliers capture Intermediate/Primary-degree swings.

Fractal pivots (Bill Williams / traditional N-bar fractals) confirm a high when the center bar's high is the highest of the surrounding `2×N` bars; symmetrically for lows. This is a right-aligned sliding-window test on intrabar extremes. The "Elliott Wave Full Fractal System v2.0" (TradingView, mbedaiwi2) builds and maintains four concurrent pivot streams using ATR-adaptive fractals, each stream scaled to a different degree: Primary (macro), Intermediate (swing-trading), and Minor (intraday) degrees.

**Key principle for degree hierarchy construction**: run three to four independent ZigZag passes over the same OHLC data using increasing ATR multipliers (e.g. 1×, 2×, 4×, 8×). Each pass produces a pivot stream. The slowest stream anchors the largest degree; each faster stream captures the internal structure of the legs produced by the next-slower stream. This is the instrumental bridge between the single-scale `zigzag` and the multi-degree construction Neely's procedure demands.

Sources: [ZigZag ATR — TradingView Library by DeepEntropy](https://www.tradingview.com/script/v8XJuorH-ZigZag-ATR/); [Elliott Wave Full Fractal System v2.0](https://www.tradingview.com/script/KlaTN7AD-Elliott-Wave-Full-Fractal-System-v2-0/); [Zig Zag ATR Indicator — cTrader Store](https://ctrader.com/products/2299).

### 2.2 Auto-labeling: enumerate → validate → score → rank

The "brute-force combinatorial" approach used by the most widely cited open-source Elliott Wave detectors (ElliottWaveAnalyzer by btcorgtfo, python-taew by DrEdwardPCB) reduces to:

1. From the pivot stream at a chosen degree, generate all `C(N, 6)` subsequences of six consecutive pivots (i.e., every possible 5-leg segment).
2. For each 5-leg candidate, run `validate_impulse(waves)` and score the result.
3. For each 3-leg candidate, run `validate_correction(waves)` and score.
4. Rank surviving candidates by hard-rule pass rate, then guideline WARN count, then Fibonacci fidelity.

The ElliottWaveAnalyzer uses a `WaveOptionsGenerator` that produces parameter tuples and removes invalid combinations before validation — effectively a constraint-propagation pruning step that avoids exhaustive enumeration of all logically incompatible combinations. The python-taew library uses an iterative forward-search: find all valid Wave-1 candidates, then for each extend to valid Wave-2, and so on, pruning at each step. Both strategies limit the combinatorial space but do not eliminate it: a dense pivot stream of 50 pivots still produces ~15.8 million 6-tuple candidates, most of which fail Rule-1 immediately.

**Practical pruning rules to implement**:
- Wave-1 must be the initiating directional leg from an identified swing extreme.
- After Wave-1, Wave-2 must not cross Wave-1's origin (hard Rule R1 prune).
- Wave-3 must be longer than Wave-1 times 0.9 (soft pre-filter; avoids R2 failures that are expensive to compute).
- Wave-4 must not overlap Wave-1 territory (hard Rule R3 prune) unless `diagonal=True`.

The combinatorial explosion becomes manageable with these four prunes applied sequentially; the surviving candidate set is typically small (single digits) even on a 40-pivot stream.

**Scoring and ranking**: after validation, each `CandidateCount` carries a tuple `(hard_fail_count, warn_count, fib_score)` — sort ascending on hard fails, ascending on warns, descending on fib_score. The top-ranked candidate becomes the auto-label; the rest are preserved as alternates (important for honest disclosure of ambiguity).

Sources: [ElliottWaveAnalyzer — GitHub (btcorgtfo)](https://github.com/btcorgtfo/ElliottWaveAnalyzer); [python-taew — GitHub (DrEdwardPCB)](https://github.com/DrEdwardPCB/python-taew); [Algorithm for Elliott Waves pattern detection — ACM/IDT](https://dl.acm.org/doi/10.3233/IDT-170319).

### 2.3 Auto-degree assignment via Neely's bottom-up monowave construction

Glenn Neely's NeoWave procedure (from *Mastering Elliott Wave*, ~600 pp) assigns degree by constructing upward from the smallest confirmed price segment, not by imposing a top-down grid. The algorithmic interpretation proceeds in three stages:

**Stage A — Monowave identification**: a monowave is a single undivided directional price segment connecting two consecutive pivot extremes on the most granular pivot stream. Every bar-chart leg between adjacent ZigZag pivots (at the finest ATR multiplier) is a candidate monowave.

**Stage B — Monowave classification via retracement rules**: before combining monowaves into polywaves, each monowave is classified by measuring how far the *subsequent* move retraces it. Neely's retracement depth table maps depth ranges to implied identity labels (`:F3` = corrective three, `:5` = motive five, `:3` = corrective three, etc.). The `retracement_logic()` function in `rules.py` encodes a simplified version of this depth table. A complete implementation would apply all of Neely's "post-conditions" (price rules 1–9 plus time rules) to narrow each monowave's identity before aggregation.

**Stage C — Polywave and multiwave construction**: once adjacent monowaves carry provisional identity labels, groups of 3 or 5 monowaves are tested as polywave patterns (impulse or correction). If validation passes, the polywave is promoted to a single unit at the next degree, and the process repeats. This is precisely the `validate_impulse` / `validate_correction` engine already in `rules.py` — the missing link is the automated bottom-up assembly loop that feeds it progressively larger segments.

The algorithmic formulation is:
```
degree_0_pivots = zigzag(bars, atr_mult=smallest)
for each overlapping window of 3 or 5 consecutive pivots:
    waves = pivots_to_waves(window)
    result = validate_impulse(waves) OR validate_correction(waves)
    if passes hard rules:
        collapse window into a single synthetic Pivot at the appropriate degree
        feed synthetic Pivots into degree_1_pivots stream
repeat for degree_1 → degree_2 → ...
```

The key honesty caveat: Neely's actual procedure involves dozens of cross-referencing conditions (time, complexity, "rule of neutrality") that the simplified depth-table heuristic cannot fully replicate. The system should mark `degree_confidence = HEURISTIC` until a more complete rule set is encoded, matching the `REF` status convention already in `rules.py`.

Sources: [NeoWave basic concepts — ForexTalker](https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/); [Neo Wave Theory explained — LiteFinance](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/); [NW2 — Neo Wave Polywaves — Studocu](https://www.studocu.com/row/document/sri-lanka-institute-of-marketing/digital-marketing/nw2-neo-wave/98941243); [NeoWave Q&A archive — neowave.com](https://www.neowave.com/qow/qow-archive-25.asp).

### 2.4 Backtest / hit-rate harness methodology

The goal is to replay historical bars causally, score reversals at structurally permitted zones, and measure the empirical hit-rate (price subsequently reversed or was invalidated) at score≥4 thresholds.

**Core procedure**:
1. Take a bar series `bars[0..T]`.
2. At each bar `t`, compute the pivot stream and the best auto-label using only `bars[0..t]`.
3. Determine if bar `t` falls inside any previously identified reversal zone (Fibonacci confluence zone from the auto-label at bar `t`).
4. Compute `score_reversal(symbol, bars[t-lookback..t], zone, ...)` — this is the confluence score at bar `t`.
5. Record the entry `(t, score, zone)` whenever `score >= threshold`.
6. Walk forward: check if price subsequently reverses ≥ `min_move` before hitting the invalidation level. Record `outcome ∈ {REVERSAL, INVALIDATED, OPEN}`.
7. Compute `hit_rate = reversals / (reversals + invalidations)`.

**Walk-forward splits**: following Robert Pardo's methodology (first published 1992), the standard approach uses a rolling anchor: optimize threshold parameters (e.g. minimum score, ATR multiplier for ZigZag) on an in-sample window of length `IS`, then measure hit-rate on an out-of-sample window of length `OOS`, then advance the anchor by `step` bars and repeat. The `walk-forward-backtester` Python library (TonyMa1/walk-forward-backtester) implements this rolling window pattern: `train_size` / `test_size` / `step_size` are all independently configurable.

**Performance metrics**: beyond raw hit-rate, the harness should compute: profit factor (sum of winning reversal magnitudes / sum of losing reversal magnitudes to invalidation), Walk-Forward Efficiency (WFE = OOS_return / IS_return), and the multiple-testing correction (since each threshold combination is a separate hypothesis). The StratBase.ai and QuantifiedStrategies analyses of Elliott Wave + Fibonacci structural filters reported improvement of win-rate from 41.5% to 57.4% (profit factor 1.82) versus a baseline momentum signal, with the ZigZag filter providing the incremental edge — but this was in-sample only, and OOS performance was not separately reported, illustrating exactly the validation gap to fill here.

Sources: [Walk-Forward Optimization — QuantInsti](https://blog.quantinsti.com/walk-forward-optimization-introduction/); [Walk-Forward Backtester — GitHub (TonyMa1)](https://github.com/TonyMa1/walk-forward-backtester); [Walk-Forward Optimization — Wikipedia](https://en.wikipedia.org/wiki/Walk_forward_optimization); [Elliott Wave Backtesting — StratBase.ai](https://stratbase.ai/en/blog/elliott-wave-backtesting); [Elliott Wave Backtest Examples — QuantifiedStrategies](https://www.quantifiedstrategies.com/elliott-wave-trading-strategy/).

### 2.5 Causal-only discipline (CRITICAL — D-013 bridge)

This is the most common source of silent invalidation in Elliott Wave backtests, and the most critical design constraint for the chakra_quant integration seam.

**The ZigZag look-ahead problem**: the standard ZigZag implementation — including the current `zigzag()` in `toolkit.py` — assigns a pivot's timestamp to the bar where the *extreme price occurred*, not the bar where the pivot was *confirmed* (i.e., where price had reversed enough to guarantee the pivot would not be updated). In a bar-by-bar replay, this means the algorithm "knows" about a high at bar `t` only at bar `t + N` where `N` is the number of bars needed to push the reversal past the threshold. If the backtest uses the pivot at bar `t` to generate a signal at bar `t` (before confirmation), it has introduced look-ahead bias.

A pandas-ta pull request (PR #874) introduced a `backtest_mode` boolean flag that addresses this exactly: in backtest mode the zigzag runs front-to-back and records each pivot *at the bar of confirmation* rather than back-dating it to the extreme. The confirmation offset is `floor(pct_reversal / typical_bar_range)` bars or, for ATR-based pivots, `ceil(ATR_mult)` bars approximately.

**Concrete rules for this codebase**:
- A pivot is **confirmed** at bar `t_confirm` = first bar `t'` > `t_extreme` at which `price moved >= threshold` in the opposing direction from `extreme_price`. Signal generation must use `t_confirm`, not `t_extreme`.
- All rolling indicators (`rsi`, `ema`, `macd` in `confluence.py`) are already right-aligned (computed from `closes[0..t]` only) — these are compliant.
- `zigzag` must expose a `confirmed_at` timestamp alongside each Pivot. A `Pivot` carrying `t` (extreme bar) must also carry `confirmed_t` (the bar at which it was known to be fixed). Any downstream backtest must use `confirmed_t` for event sequencing.
- `center=True` windows are forbidden (none are currently used, but the guard should be documented in code).
- `df.shift(-N)` with negative N is forbidden (no lookahead shifts).

**Chakra_quant D-013 bridge note**: when the Hurst/FLD cycle signal from chakra_quant is eventually wired into `score_reversal(..., cycle_aligned=True)`, that signal must also be causal — the FLD crossover at bar `t` is known at bar `t` (FLD is a median-displaced forward line, but the *cross detection* uses only data ≤ `t`). The seam is already correct by construction; the only required discipline is that Ewace_2026's own pivot timestamps be similarly honest.

Sources: [ZIGZAG backtest_mode PR — pandas-ta #874](https://github.com/twopirllc/pandas-ta/pull/874); [ZigZag confirmation lag — TradingView scripts](https://www.tradingview.com/scripts/zigzagindicator/); [Look-Ahead Bias in Backtests — InvestingBrokers](https://investingbrokers.com/look-ahead-bias-backtesting/); [Lookahead analysis — Freqtrade docs](https://www.freqtrade.io/en/stable/lookahead-analysis/); [Adaptive Pivot Structure — WillyAlgoTrader](https://www.tradingview.com/script/QhXQwVpN-adaptive-pivot-structure-willyalgotrader/).

### 2.6 Programmatic charting

The current `charts/*.html` files are hand-authored SVG strings assembled by inspection. A `render_chart(waves, projections)` function should replace this with a programmatic SVG emitter, keeping the dependency-free constraint.

**Implementation approach**: pure stdlib SVG emission using Python's `xml.etree.ElementTree` (stdlib) or raw f-string template with coordinate math. The chart requires:
- Coordinate transform: `(unix_t, price)` → `(svg_x, svg_y)` with configurable viewport.
- Wave polyline: connect pivot prices in sequence with coloured stroke.
- Projection fans: thin dashed lines from the last confirmed pivot to each Fibonacci target.
- Labels: wave degree annotations at each pivot, rendered as `<text>` elements.
- Confluence zones: shaded `<rect>` between zone `lo` and `hi`.

Third-party options exist (fsplot for financial SVG, pygal for general SVG graphs) but introducing them violates the stdlib-only core constraint. A helper module `wavelib/charting.py` should produce valid inline HTML or standalone SVG strings that can be written to `charts/` without any external dependency. The `orsinium-labs/svg.py` library offers a typed, zero-dependency approach to SVG generation if the constraint is relaxed to allow a single small vendored file.

Sources: [fsplot — PyPI](https://pypi.org/project/fsplot/); [svg.py — GitHub (orsinium-labs)](https://github.com/orsinium-labs/svg.py); [py-svg-chart — GitHub (alex-rowley)](https://github.com/alex-rowley/py-svg-chart); [pygal — GitHub (Kozea)](https://github.com/Kozea/pygal).

---

## 3. Current wavelib audit

Gap table — current state vs automation requirements.

| Concept | Implemented? (file:func) | Fidelity | Gap note |
|---|---|---|---|
| Single-scale ZigZag pivot detection | `toolkit.py:zigzag` | Full for single scale | Fixed `pct` threshold only; no ATR-adaptive variant; no `confirmed_t` timestamp; end-of-array flush may misplace the terminal pivot |
| Multi-scale / multi-degree pivot streams | Missing | Missing | No ATR-based or fractal variant; no mechanism to run multiple concurrent streams at different multipliers |
| Pivot-to-waves conversion | `toolkit.py:pivots_to_waves` | Full | Works correctly; requires caller to select the right pivot subsequence manually |
| Impulse validation | `rules.py:validate_impulse` | Full | Hard rules + guidelines + S&B + terminal correctly encoded; `diagonal=True` variant present |
| Correction classification | `rules.py:validate_correction` | Full | ZigZag/flat/triangle/complex classified; complex-correction subtypes are heuristic (DOCUMENTATION §9) |
| Channeling tests (2-4 line, 1-3 throwover) | `rules.py:two_four_test`, `throwover_test` | Full | Both present; caller must supply correct pivot arguments manually |
| **`label_and_validate` (auto-labeling engine)** | **Missing** | **Missing** | **No function exists to enumerate candidate counts and rank them; user must hand-pick all legs** |
| Combinatorial pruning | Missing | Missing | No R1/R2/R3 pre-pruning; no `WaveOptionsGenerator` equivalent |
| **Auto-degree assignment (Neely bottom-up)** | **Missing** | **Missing** | **No monowave-classification loop; no polywave assembly; degree is always caller-supplied** |
| Monowave classification (retracement rules) | `rules.py:retracement_logic` | Heuristic stub | Depth-to-identity table present but returns `REF`; no time or complexity conditions; no Neely post-conditions |
| **Backtest harness (bar-by-bar replay)** | **Missing** | **Missing** | **No `backtest_reversals` function; no hit-rate accumulator; no walk-forward splitter** |
| Walk-forward validation | Missing | Missing | No in-sample/out-of-sample splitting; no WFE computation |
| Confluence scoring | `confluence.py:score_reversal` | Full | All 6 strands implemented; 7th strand (cycle) reserved as external boolean |
| RSI / MACD / volume indicators | `confluence.py:rsi,ema,macd` | Full | Causal (right-aligned); needs ≥50-100 bars for divergence to activate |
| **ZigZag confirmation lag / causal pivot timestamps** | **Missing** | **Missing** | **`Pivot.t` is the extreme bar, not the confirmation bar; backtest using `Pivot.t` directly introduces look-ahead bias** |
| **Programmatic charting** | **Missing** | **Missing** | **`charts/*.html` are hand-built SVG strings; no `render_chart` function** |
| Fibonacci projection helpers | `toolkit.py:fib_extension`, `fib_retrace` | Full | Correct; no gap |
| Wave-5 projection | `toolkit.py:project_wave5`, `rules.py:project_wave5` | Full (duplicated) | Two copies exist; should consolidate |
| Terminal retrace window | `toolkit.py:terminal_retrace_projection`, `rules.py:terminal_retrace_window` | Full (duplicated) | Two slightly different signatures; consolidate |
| Similarity & Balance | `rules.py:similarity_and_balance`, `toolkit.py:similarity_and_balance` | Full (duplicated) | Duplicate implementations; resolve canonical location |

**Summary of critical gaps**: `label_and_validate` MISSING; auto-degree MISSING; backtest harness MISSING; `zigzag` is single-scale and lacks `confirmed_t`; charting is hand-built; ZigZag look-ahead / confirmation-lag not handled; several utility functions are duplicated between `toolkit.py` and `rules.py`.

---

## 4. Build roadmap

The items are ordered by dependency: each item can only begin after the previous is solid. Causal-only constraints are acceptance criteria throughout.

---

### Item 1 — `Pivot` causal extension + `zigzag_causal` (prerequisite for everything else)

**Why first**: every downstream component (auto-labeling, backtest, charting) depends on honest pivot timestamps. Without `confirmed_t` the entire backtest would be look-ahead-contaminated.

**Proposed data structure change**:
```python
@dataclass
class Pivot:
    t: float          # unix seconds — bar where price extreme occurred
    confirmed_t: float  # unix seconds — bar where reversal was confirmed (≥ t)
    price: float
    kind: Literal["H", "L"]
    confirmed: bool = True  # False if this is the still-live trailing pivot
```

**Proposed function signature**:
```python
def zigzag_causal(
    bars: list[tuple],          # (t, o, h, l, c)
    pct: float = 0.10,          # percentage reversal threshold
    atr_n: int | None = None,   # if set, use ATR(atr_n) × pct as the dynamic threshold
) -> list[Pivot]:
    """
    Single-pass, front-to-back ZigZag that records confirmed_t on each Pivot.
    The last pivot in the returned list has confirmed=False (still live).
    Causal: at bar t, only pivots with confirmed_t <= t are "known".
    """
```

**Acceptance criteria (tests first)**:
- `test_no_future_pivot`: given bars 0..T, calling `zigzag_causal(bars[:t])` for every `t` in range must not return any pivot with `confirmed_t > t`.
- `test_confirmation_lag`: a pivot at bar `k` (extreme) must have `confirmed_t >= k + 1`.
- `test_live_pivot_unmarked`: the last pivot must always have `confirmed=False`.
- `test_causal_vs_legacy_same_pivots`: the set of `(t, price, kind)` returned by `zigzag_causal` at `T` must match the existing `zigzag` output on the same bars (regression).

**Synthetic test strategy**: generate a step-wave series (deterministic sawtooth) where pivots and confirmation bars are known analytically. Verify `confirmed_t` equals `t_extreme + lag_bars` exactly.

---

### Item 2 — Multi-scale pivot streams

**Proposed function signature**:
```python
def zigzag_multiscale(
    bars: list[tuple],
    scales: list[float] = (0.03, 0.07, 0.15, 0.30),  # pct or ATR mult list
    atr_n: int | None = None,
) -> dict[float, list[Pivot]]:
    """
    Returns one causal Pivot stream per scale.
    Keys are the scale values; values are zigzag_causal outputs.
    Smaller scales = finer degree (Minor); larger scales = coarser degree (Primary).
    """
```

**Degree hierarchy convention**:
```
scales[0] → Minor (Intermediate sub-waves)
scales[1] → Intermediate
scales[2] → Primary
scales[3] → Cycle / higher
```

**Acceptance criteria**:
- Each stream independently satisfies `zigzag_causal` causal tests.
- Pivot count decreases monotonically with scale: `len(streams[0]) >= len(streams[1]) >= ...`
- At any scale `k`, every pivot in `streams[k]` has a corresponding nearest extreme in `streams[k-1]` within `±2` bars (structural containment test).

---

### Item 3 — `label_and_validate`: auto-labeling engine

**Proposed data structure**:
```python
@dataclass
class CandidateCount:
    pivots: list[Pivot]       # the 6 pivots bounding 5 waves
    waves: list[Wave]         # the 5 Wave objects
    count_type: str           # "IMPULSE" | "CORRECTION" | "DIAGONAL"
    results: list[RuleResult] # raw output from validate_impulse/validate_correction
    hard_fails: int           # count of Status.FAIL results
    warns: int                # count of Status.WARN results
    fib_score: float          # 0.0..1.0 — sum of fib-ratio adherence across waves
    degree: int               # 0=Minor, 1=Intermediate, 2=Primary (matches scale index)
    degree_confidence: str    # "COMPUTED" | "HEURISTIC" | "ASSUMED"
```

**Proposed function signature**:
```python
def label_and_validate(
    bars: list[tuple],
    degrees: list[float] = (0.03, 0.07, 0.15),  # scales to run
    atr_n: int | None = None,
    max_candidates: int = 20,
    diagonal: bool = False,
) -> list[CandidateCount]:
    """
    Multi-scale auto-labeling engine.
    Returns candidates sorted ascending by (hard_fails, warns, -fib_score).
    Only pivots with confirmed_t <= bars[-1][0] are used (causal guarantee).
    Combinatorial pruning: R1/R2/R3 pre-checks before full validation.
    """
```

**Algorithm outline**:
```
For each scale in degrees:
    pivots = zigzag_multiscale(bars, [scale])[scale]
    causal_pivots = [p for p in pivots if p.confirmed_t <= bars[-1][0]]
    For each overlapping 6-tuple of causal_pivots:
        waves = pivots_to_waves(6-tuple)
        if R1_prune(waves) fails: skip
        if R2_prune(waves) fails: skip
        if R3_prune(waves) fails and not diagonal: skip
        results_i = validate_impulse(waves, diagonal)
        results_c = validate_correction(waves[:3]) or validate_correction(waves[:5])
        Create CandidateCount for each passing type
Sort all candidates by (hard_fails, warns, -fib_score)
Return top max_candidates
```

**Test plan (synthetic-first per visual-first-validation discipline)**:
- Generate a synthetic 5-wave impulse with textbook ratios on a sawtooth price series. Assert `label_and_validate` returns a candidate with `hard_fails=0` and ranks it first.
- Generate a synthetic A-B-C with known B retrace. Assert correction label is returned with `hard_fails=0`.
- Generate a noisy series with no clean Elliott structure. Assert all candidates have `hard_fails >= 1` (no false clean labels).
- Generate a series with known confirmation lag (ensure pivots near the right edge have `confirmed=False`). Assert those pivots are excluded from candidates.
- Acceptance criterion: **all tests must pass before the function is considered shippable; no widening of tolerances to force a green test.**

---

### Item 4 — Auto-degree assignment (Neely bottom-up loop)

**Proposed function signature**:
```python
def assign_degrees_neely(
    bars: list[tuple],
    base_scale: float = 0.03,
    max_degrees: int = 3,
    atr_n: int | None = None,
) -> list[CandidateCount]:
    """
    Bottom-up Neely-style degree assignment.
    Stage 1: classify all monowaves via retracement_logic.
    Stage 2: assemble groups of 3 or 5 into polywave candidates; validate.
    Stage 3: promote passing polywaves into synthetic Pivots at degree+1.
    Repeat for max_degrees levels.
    Returns all validated CandidateCounts with degree and degree_confidence set.
    degree_confidence="HEURISTIC" for the simplified retracement-only classification.
    """
```

**Data structure**: `Pivot` gains a `synthetic: bool = False` field. Synthetic pivots are assembled polywaves promoted to the next degree; they carry `degree_confidence="HEURISTIC"`.

**Test plan**:
- On the AVGO demo data (hard-coded in `rules.py:_demo()`), assert that the bottom-up loop produces at least one candidate matching the known (III) impulse structure at `degree=1`.
- Assert `degree_confidence="HEURISTIC"` on all results (no false precision claim).
- Assert no synthetic pivot has `confirmed_t` earlier than the latest `confirmed_t` of its constituent monowaves (temporal monotonicity).

---

### Item 5 — `backtest_reversals`: causal bar-by-bar harness

**Proposed data structure**:
```python
@dataclass
class ReversalEvent:
    entry_t: float          # bar index where score >= threshold
    score: int
    zone: tuple[float, float]
    invalidation: float
    entry_price: float

@dataclass
class ReversalOutcome:
    event: ReversalEvent
    outcome: str            # "REVERSAL" | "INVALIDATED" | "OPEN"
    exit_t: float | None
    exit_price: float | None
    move_pct: float | None  # signed % from entry to exit

@dataclass
class BacktestStats:
    n_signals: int
    n_reversals: int
    n_invalidations: int
    n_open: int
    hit_rate: float         # reversals / (reversals + invalidations)
    profit_factor: float
    wfe: float | None       # Walk-Forward Efficiency (OOS / IS return), None if not WFO
    is_period: tuple[float, float] | None
    oos_period: tuple[float, float] | None
```

**Proposed function signature**:
```python
def backtest_reversals(
    bars: list[tuple],              # (t, o, h, l, c, v) — volume required for confluence
    score_threshold: int = 4,       # minimum score to record an event
    min_reversal_pct: float = 0.05, # minimum move to count as confirmed reversal
    degrees: list[float] = (0.03, 0.07),
    wfo_train_size: int | None = None,  # bars for in-sample; None = no WFO
    wfo_test_size: int | None = None,
    wfo_step_size: int | None = None,
    bullish: bool = True,
    cycle_aligned: bool = False,
) -> BacktestStats:
    """
    Bar-by-bar causal replay.
    At each bar t:
      1. Compute label_and_validate(bars[:t+1]) — causal.
      2. Determine active reversal zones from best CandidateCount.
      3. If bars[t] closes inside a zone, call score_reversal using bars[t-50:t+1].
      4. Record ReversalEvent if score >= score_threshold.
      5. Walk forward to determine outcome.
    All signal generation uses only bars[0..t]. No bar[t+1] data used at step t.
    """
```

**Walk-forward split**:
```python
if wfo_train_size is not None:
    for anchor in range(wfo_train_size, len(bars) - wfo_test_size, wfo_step_size):
        is_bars = bars[anchor - wfo_train_size : anchor]
        oos_bars = bars[anchor : anchor + wfo_test_size]
        is_stats = backtest_reversals(is_bars, score_threshold, ...)
        oos_stats = backtest_reversals(oos_bars, score_threshold, ...)
        wfe = oos_stats.profit_factor / is_stats.profit_factor
```

**Acceptance criteria (tests first)**:
- `test_no_future_data`: instrument `label_and_validate` with a call counter; assert it is never called with a bar array whose last `t` exceeds the replay cursor.
- `test_hit_rate_deterministic`: on a synthetic series with four planted reversal events (known outcomes), assert `hit_rate` equals the ground-truth fraction.
- `test_wfo_partition`: assert IS bars and OOS bars do not overlap; assert OOS starts at `anchor` exactly.
- `test_open_events_excluded`: assert OPEN events are not counted in hit_rate denominator.

---

### Item 6 — `render_chart`: programmatic SVG emitter

**Proposed function signature**:
```python
def render_chart(
    waves: list[Wave],
    projections: dict[str, list[float]],  # {"w5": [target1, target2], "retrace": [t1, t2]}
    zones: list[tuple[float, float]] = (),
    title: str = "",
    width: int = 900,
    height: int = 500,
    output_path: str | None = None,       # if None, return SVG string
) -> str:
    """
    Emits a standalone SVG chart string.
    No external dependencies. Uses xml.etree.ElementTree (stdlib).
    Coordinate transform: t→x linear, price→y inverted linear.
    """
```

**Test plan**:
- `test_valid_xml`: assert `xml.etree.ElementTree.fromstring(render_chart(...))` parses without error on the AVGO demo wave set.
- `test_wave_count_polylines`: assert the SVG contains exactly `len(waves)` `<polyline>` elements.
- `test_projection_lines`: assert each projection target produces a `<line>` element.
- `test_zone_rects`: assert each zone produces a `<rect>` element.

---

## 5. Open questions / subjectivity caveats

### 5.1 Combinatorial explosion at high pivot counts

At `N = 60` pivots, the number of 6-tuples is `C(60, 6) ≈ 50 million`. Even with aggressive R1/R2/R3 pruning removing 90–95% of candidates, the remaining search space is large. Mitigation strategies: limit candidates to non-overlapping or minimum-overlap windows (adjacent or skip-one); impose a maximum wave-length ratio pre-filter before any rule validation; cap `max_candidates` and rely on the ranking to surface the best. The ElliottWaveAnalyzer's `skip` parameter (allowing the algorithm to bypass `N` local extrema to find broader trends) is a pragmatic pruning tool worth encoding.

### 5.2 Degree subjectivity — the fundamental open problem

Even with the Neely bottom-up procedure implemented, the resulting degrees are *heuristic inferences*, not ground truth. Two competent analysts routinely assign the same price action to different degrees — the README (§9) and DOCUMENTATION (§9) are explicit about this. The automated degree assignment should never suppress alternates: always return multiple `CandidateCount` objects with different degree assignments and let the caller — or the confluence score — adjudicate. The `degree_confidence` field encodes this epistemic uncertainty.

### 5.3 ZigZag percentage sensitivity and regime dependence

A fixed `pct` threshold of e.g. 5% produces very different pivot counts on AVGO (low-volatility large-cap) vs a crypto asset in a high-volatility period. ATR-adaptive scaling mitigates this but introduces a new parameter (ATR period `atr_n`) that itself can be over-fit. The backtest harness must include `pct` / `atr_mult` in its walk-forward parameter sweep and report how sensitive hit-rate is to small changes (robustness surface). A strategy whose hit-rate collapses at `pct ± 0.01` is not reliable.

### 5.4 Multiple-testing and overfitting risk

Each `(degree, pct, score_threshold)` combination is an independent hypothesis. Running the backtest across a grid of combinations and reporting only the best-performing combination without correction is a textbook multiple-testing error. Mitigations: (a) pre-register the primary hypothesis before backtesting; (b) apply Bonferroni or Benjamini-Hochberg correction to p-values; (c) require Walk-Forward Efficiency > 0.70 on every OOS fold rather than in aggregate; (d) keep the `algorithms.json` registry (borrowed from chakra_quant's ARACHNE framework) and retire failed parameter combinations to `ARCHIVED` so the live hypothesis count `n_trials` is honest.

### 5.5 Elliott Wave's inherent subjectivity resists full automation

Published academic results on automated Elliott Wave detection are sobering: the ACM/IDT paper (Intelligent Decision Technologies, 2018) demonstrates that even rule-based algorithms identify structurally valid patterns that human analysts would label differently at a different degree. The LLM-based ElliottAgents paper (Applied Sciences, Dec 2024) notes that multi-agent consensus reduces label variance but does not eliminate it. The correct framing is not "find the true count" but "enumerate the structurally valid hypotheses, score them by Fibonacci fidelity and confluence, and report the distribution." This is already the design philosophy of `rules.py` (WARN/REF rather than forced PASS/FAIL) and should be preserved throughout the automation layer.

---

## Sources

- [ZigZag ATR — TradingView Library by DeepEntropy](https://www.tradingview.com/script/v8XJuorH-ZigZag-ATR/)
- [Elliott Wave Full Fractal System v2.0 — TradingView by mbedaiwi2](https://www.tradingview.com/script/KlaTN7AD-Elliott-Wave-Full-Fractal-System-v2-0/)
- [Zig Zag ATR Indicator — cTrader Store](https://ctrader.com/products/2299)
- [Elliott Wave Theory: Complete Guide — elliottwavestreet.com](https://elliottwavestreet.com/elliott-wave/elliott-wave-theory-the-complete-guide-to-wave-analysis-and-trading/)
- [Elliott Wave Full Fractal System — IEEE (PDF, arnumber=11520285)](https://ieeexplore.ieee.org/ielx8/6287639/6514899/11520285.pdf?arnumber=11520285&isnumber=6514899)
- [ElliottWaveAnalyzer — GitHub (btcorgtfo)](https://github.com/btcorgtfo/ElliottWaveAnalyzer)
- [python-taew — GitHub (DrEdwardPCB)](https://github.com/DrEdwardPCB/python-taew)
- [elliot-waves-auto — GitHub (ESJavadex)](https://github.com/ESJavadex/elliot-waves-auto)
- [An Algorithm for Elliott Waves Pattern Detection — ACM/IDT (Intelligent Decision Technologies, 2018)](https://dl.acm.org/doi/10.3233/IDT-170319)
- [Elliott Waves Recognition Via Neural Networks — Semantic Scholar / Academia.edu](https://www.semanticscholar.org/paper/Elliott-Waves-Recognition-Via-Neural-Networks-Kotyrba-Voln%C3%A1/0f885f20f24bb2e014c0a8d4a87cb2f8f9709688)
- [Large Language Models and Elliott Wave (ElliottAgents) — Applied Sciences, MDPI, Dec 2024](https://www.mdpi.com/2076-3417/14/24/11897)
- [NeoWave basic concepts — ForexTalker](https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/)
- [NeoWave wave theory (rules 5 & 6) — ForexTalker](https://forextalker.com/neowave-wave-theory-by-glenn-neely-description-of-conditions-b-c-and-d-for-the-sixth-rule/)
- [Neo Wave Theory explained — LiteFinance](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- [NW2 — Neo Wave polywaves & structures — Studocu](https://www.studocu.com/row/document/sri-lanka-institute-of-marketing/digital-marketing/nw2-neo-wave/98941243)
- [NeoWave Q&A: :F3 vs :5 behavior traits — neowave.com](https://www.neowave.com/qow/qow-archive-25.asp)
- [NeoWave wave-2 retracement limits — neowave.com](https://www.neowave.com/qow/qow-archive-1079.asp)
- [Neo Wave rules overview — StockPathShala](https://stockpathshala.com/neo-wave-rules/)
- [Walk-Forward Optimization — QuantInsti](https://blog.quantinsti.com/walk-forward-optimization-introduction/)
- [Walk-Forward Analysis: Gold Standard for Strategy Validation — Quanthop](https://quanthop.com/learn/validation-robustness/walk-forward-analysis)
- [Walk-Forward Optimization — Wikipedia](https://en.wikipedia.org/wiki/Walk_forward_optimization)
- [Walk-Forward Backtester — GitHub (TonyMa1)](https://github.com/TonyMa1/walk-forward-backtester)
- [Elliott Wave Backtesting: Can It Be Tested Systematically? — StratBase.ai](https://stratbase.ai/en/blog/elliott-wave-backtesting)
- [Elliott Wave Trading Strategy — QuantifiedStrategies.com](https://www.quantifiedstrategies.com/elliott-wave-trading-strategy/)
- [PyBacktesting (Elliott Wave + Genetic Algorithms) — GitHub (philippe-ostiguy)](https://github.com/philippe-ostiguy/PyBacktesting)
- [Interpretable Hypothesis-Driven Trading: Walk-Forward Validation — arXiv:2512.12924](https://arxiv.org/pdf/2512.12924)
- [Backtest Overfitting in the Machine Learning Era — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0950705124011110)
- [ZIGZAG backtest_mode boolean flag — pandas-ta PR #874](https://github.com/twopirllc/pandas-ta/pull/874)
- [Zig Zag Indicator: Filtering Noise — LuxAlgo Blog](https://www.luxalgo.com/blog/zig-zag-indicator-filtering-noise-to-highlight-significant-price-swings/)
- [Lookahead Analysis — Freqtrade Documentation](https://www.freqtrade.io/en/stable/lookahead-analysis/)
- [Look-Ahead Bias in Backtests — InvestingBrokers](https://investingbrokers.com/look-ahead-bias-backtesting/)
- [Adaptive Pivot Structure — WillyAlgoTrader (TradingView)](https://www.tradingview.com/script/QhXQwVpN-adaptive-pivot-structure-willyalgotrader/)
- [The Implementation of Automatic Analysis of Elliott Waves — MQL5 Articles](https://www.mql5.com/en/articles/260)
- [Elliott Wave Degrees: Multi-Timeframe Strategy — EWOTrader](https://ewotrader.com/education/elliott-wave-theory/elliott-wave-degrees/)
- [fsplot — PyPI](https://pypi.org/project/fsplot/)
- [svg.py — GitHub (orsinium-labs)](https://github.com/orsinium-labs/svg.py)
- [py-svg-chart — GitHub (alex-rowley)](https://github.com/alex-rowley/py-svg-chart)
- [pygal — GitHub (Kozea)](https://github.com/Kozea/pygal)
- [EW_Dataset (open-source Elliott Wave impulse dataset) — GitHub (A-J-Financial-Solutions)](https://github.com/A-J-Financial-Solutions/EW_Dataset)
- [Elliott Wave Myth Exposed — LiberatedStockTrader](https://www.liberatedstocktrader.com/elliott-wave-theory-principle-examples-stock-market/)
- [Fractal Market Structure and Multiple Time-Frames — Forex Factory](https://www.forexfactory.com/thread/1052387-fractal-market-structure-and-multiple-time-frames)
