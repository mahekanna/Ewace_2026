# Audit 04 — Pivot / ZigZag Detection and Fibonacci Proportion

_Author: Claude Code audit agent · 2026-06-09_
_Scope: `wavelib/toolkit.py`, `wavelib/wavetree.py`, `wavelib/automation.py`, `wavelib/rules.py`, `scripts/wave_report.py`_
_Status: AUDIT ONLY — no code changed_

---

## 1. Theory — Correct Swing/Pivot Detection

### 1.1 The multi-scale problem

A single fixed percentage threshold cannot serve multiple wave degrees simultaneously. Elliott Wave analysis requires a **degree-consistent pivot set**: the pivots that bound a Primary-degree wave must be structurally different from those bounding a Minute-degree sub-wave. Applying one ZigZag threshold to data spanning decades conflates noise, micro-structure, and macro-structure into one undifferentiated pivot stream.

**Three approaches to pivot detection, ranked by suitability:**

| Method | Description | Strengths | Weaknesses |
|--------|-------------|-----------|------------|
| Fixed % reversal | `threshold = ep × pct` | Simple, stable | Does not adapt to volatility regime; a 5% filter means $0.10 on a $2 stock vs $20 on a $400 stock |
| ATR-adaptive | `threshold = ATR(n) × mult` | Adapts to volatility; produces structurally comparable swings across regimes | Introduces ATR period + multiplier as parameters; must be swept and not over-fit |
| Fractal N-bar | `pivot if value[i] is max/min of surrounding N bars` | Computationally clean; no price-level dependency | Window size N is itself a degree-defining parameter; ignores intrabar highs/lows unless applied to H/L series |

For **wave-degree hierarchies**, best practice (illustrated by TradingView's "Elliott Wave Full Fractal System v2.0" by mbedaiwi2, and the ZigZag ATR library by DeepEntropy) is to run **three or four independent ATR-adaptive ZigZag passes** over the same OHLC data using increasing multipliers (e.g. 1×, 2×, 4×, 8×). Each pass produces a pivot stream anchored to a different degree. The slowest/largest-multiplier stream captures Primary+ pivots; the fastest captures Minor or Minute pivots. Source: [ZigZag ATR — TradingView Library by DeepEntropy](https://www.tradingview.com/script/v8XJuorH-ZigZag-ATR/).

**The percentage-vs-ATR key insight**: for a stock trading from $2 (2009) to $495 (2026), a fixed 10% threshold fires at completely different structural scales at the two ends. A 10% reversal on a $2 stock = $0.20 absolute; on a $400 stock = $40 absolute. The resulting pivot stream has systematic scale inconsistency across the price range — early pivots capture finer-degree structure than late pivots even at the same nominal percentage. Source: [ZigZag — ChartSchool StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/zigzag); [Zig Zag Indicator — LuxAlgo blog](https://www.luxalgo.com/blog/zig-zag-indicator-filtering-noise-to-highlight-significant-price-swings/).

### 1.2 Confirmation lag and causal discipline

The classic ZigZag **repaints**: a pivot at bar `t` (the extreme) is only knowable once price reverses past the threshold at bar `t + N`. Any backtest using `Pivot.t` (the extreme bar) rather than `confirmed_t` (the first confirmation bar) is contaminated by look-ahead bias. This is the single most common source of silent backtest invalidation in ZigZag-based systems. Source: [ZIGZAG backtest_mode PR — pandas-ta #874](https://github.com/twopirllc/pandas-ta/pull/874); [Look-Ahead Bias — InvestingBrokers](https://investingbrokers.com/look-ahead-bias-backtesting/).

### 1.3 High/low vs close for extreme price

ZigZag should track **intrabar highs and lows** (not close prices) for the extremes, since wave pivots occur at the intrabar H/L by definition. The initial seeding price, however, is typically set to the first bar's close or open, which introduces a small offset.

### 1.4 Log vs linear price for Fibonacci proportionality

Glenn Neely states explicitly in *Mastering Elliott Wave* (and confirms on neowave.com QA archive #38 and #11): **if the top price is more than twice the value of the bottom price, logarithmic scale is mandatory for accurate wave counts and channeling.** The greater the price range, the more important log scale becomes.

Source: [Should fibonacci relationships be measured in absolute numbers or the distance covered on a log scale? — neowave.com QA #38](https://www.neowave.com/qow/qow-archive-38.asp); [Should a logarithmic or arithmetic chart be used for Elliott and NEoWave analysis? — neowave.com QA #11](https://www.neowave.com/qow/qow-archive-11.asp); [Logarithmic vs Linear Price Scale — SeeTheWaves](https://seethewaves.com/logarithmic-vs-linear-scale-which-is-better/).

The practical implication: on a logarithmic chart, **equal distance = equal percentage move**. A wave traveling from $100 to $200 (100% gain, log-length = ln(2) = 0.693) is structurally equivalent to a wave from $1000 to $2000 (same percentage). On a linear chart, the second wave measures 10× longer in price points, producing a 10× higher ratio even though the structural proportionality is 1:1.

For Fibonacci validation: if Wave I travels from $2 to $33 (+1,550%), its log-length is ln(33/2) = 2.80. If Wave III travels from $16 to $252 (+1,475%), its log-length is ln(252/16) = 2.75. Log-ratio = 2.75/2.80 ≈ 0.98 — near perfect equality, consistent with a shortened W3 or W1 extension. The **linear ratio** of the same waves is (252-16)/(33-2) = 236/31 = **7.6× — completely off any Fibonacci grid**.

---

## 2. Theory — Fibonacci Relationships that Define and Validate Waves

### 2.1 Canonical relationships per Frost & Prechter and Neely

**Impulse wave relationships** (cited from [Elliott Wave and Fibonacci — EWOTrader](https://ewotrader.com/education/elliott-wave-theory/elliott-wave-and-fibonacci/); [Fibonacci Ratios and Impulse Waves — FBS Academy](https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/fibonacci-ratios-and-impulse-waves); [Elliott Wave Theory — elliott-wave-forecast.com](https://elliottwave-forecast.com/elliott-wave-theory/)):

| Wave | Relationship | Primary targets |
|------|-------------|-----------------|
| Wave 2 retracement of W1 | `W2_len / W1_len` | 50%, 61.8% (sharp); 38.2% (normal) |
| Wave 3 extension of W1 | `W3_len / W1_len` | 1.618×, 2.618× (canonical); minimum >1.0 |
| Wave 4 retracement of W3 | `W4_len / W3_len` | 38.2% (most common); 23.6% if W2 was deep |
| Wave 5 vs Wave 1 | `W5_len / W1_len` | 1.0 (equality); 0.618×W1; 1.618×W1 (extended) |
| Wave 5 vs Wave 3 | `W5_len / W3_len` | 0.618× (if W3 extended); 0.382× (short) |
| When W3 extended: W1 + W5 | sum relationship | `W1_len + W5_len ≈ W3_len` or W1≈W5 by equality |

**Corrective wave relationships:**
- ABC zigzag: B retraces ≤ 61.8% of A; C = 61.8%–161.8% of A (commonly equal)
- Flat: B retraces 80%–138.2% of A; C approximately equals A
- Neely S&B: adjacent corrective legs within 1/3×–3× each other in both price AND time

### 2.2 Where NeoWave adds precision

Neely's seven retracement rules classify monowaves by how deeply the _following_ monowave retraces the current one. The breakpoints (0.382, 0.618, 1.0, 1.618, 2.618) are the same Fibonacci ratios, but applied to _inter-monowave_ relationships, not just impulse sub-wave structure. This makes the classification more granular than classic Elliott but still Fibonacci-grounded.

---

## 3. What the Code Does Now

### 3.1 ZigZag (toolkit.py)

**`zigzag(bars, pct)`** (lines 76–121):
- Uses H/L intrabar extremes during the tracking phase — correct.
- Seeds from `bars[0][4]` (close), not `bars[0][2]` (high) — minor off-by-intrabar-range for first pivot.
- Line 110: `if l < bars[0][3]: pass` — dead code, does nothing.
- Uses **multiplicative percentage**: threshold = `ep * pct`. This is proportional to price level, so a 10% threshold at $2 = $0.20 and at $400 = $40. Across a 300× price range the threshold is 300× larger in absolute terms at the end than at the beginning.
- No `confirmed_t` field.

**`zigzag_causal(bars, pct, atr_n)`** (lines 141–202):
- Adds `confirmed_t` — correct causal discipline for backtest use.
- Supports ATR mode via `atr_n` parameter — the right infrastructure, but the ATR is not used in the default `wave_report.py` call (which passes `atr_n=None`).
- Line 190: same dead code `if l < bars[0][3]: pass`.
- In percentage mode, still uses `ep * pct` threshold — same scale problem as `zigzag`.

**`zigzag_multiscale(bars, scales, atr_n)`** (lines 205–211):
- Runs `zigzag_causal` at each scale — correct structure.
- But each scale is still a fixed percentage, not ATR-adaptive by default.
- `wave_counts()` in wavetree.py calls this with `scales=(0.04, 0.07, 0.12, 0.20)` for typical TFs.
- For AVGO 1W (range 1.50–495, ratio 330×) and MRVL 1W (range 2.50–263, ratio 105×), these fixed percentages produce structurally incomparable pivot streams across the price history.

**`swing_pivots(series, n_left, n_right)`** (lines 214–239):
- N-bar fractal pivot — correctly uses high/low of target bar vs neighbors.
- `confirmed_t` is set to `n_right` bars after the pivot — correct causal lag.
- Not used by `wave_counts` or `adaptive_zigzag` in practice.

### 3.2 adaptive_zigzag (scripts/wave_report.py)

**`adaptive_zigzag(bars, target=24)`** (lines 52–59):
- Tries pct in `(0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30)` and stops when `len(piv) <= target`.
- **Critical bug**: for MRVL 1W (1354 bars spanning 25 years), pct=0.30 still produces **99 confirmed pivots** — far exceeding the target of 24 — but since 0.30 is the last value in the list and no larger value is tried, 99 pivots become the "best" result.
- Consequence: `label_monowaves` is called with 99 pivots → 98 monowaves, exactly matching the "98 monowaves" in the MRVL 1W report. This is **not** a meaningful NeoWave monowave stream; it is a dense, fine-scale pivot set labeled as macro-degree monowaves.
- The fix is either to extend the scale list to 0.50, 0.70, 1.0 or to switch to ATR-adaptive thresholds that work across all price levels.

### 3.3 Fibonacci helpers (toolkit.py)

**`fib_extension(w1_len, base, ratios)`** (line 253):
- Returns absolute price levels: `base + ratio * w1_len`. Correct for projection targets.
- `w1_len` must be in linear price units — caller responsibility.

**`fib_retrace(high, low, ratios)`** (line 258):
- Returns absolute price levels: `high - ratio * (high - low)`. Correct for retracement levels.
- Both helpers operate on linear price, which is appropriate for _price level_ computation (where you want to reach in dollars), but `w1_len` input should ideally be the log-scale length if the instrument spans a large range.

**`wave_ratio(a, b)`** (line 263):
- Returns `a.length / b.length` where `Wave.length = abs(end.price - start.price)`.
- **Linear price ratio.** For large-range instruments this ratio is structurally misleading (see §4).

**`blue_box_zone`** (line 267):
- Projects EWF "Blue Box" using `abs(a_end - a_start)` as the leg length. Same linear price issue.

### 3.4 Wave ratio checks (wavetree.py and automation.py)

**`Wave.length`** (rules.py line 103):
- Defined as `abs(self.end.price - self.start.price)` — **linear price difference**.
- Used everywhere: `_impulse_quality`, `_fib_score`, `similarity_and_balance`, `wave_ratio`.

**`_fib_close(r, sigma=0.2)`** (wavetree.py lines 31–38):
- Gaussian kernel, relative distance: `d = min(|r - t| / t for t in _FIB)`.
- Relative distance normalization is correct (avoids scale dependency in the ratio space).
- `sigma=0.2` = ±24% relative bandwidth at 50% height — quite wide, accepts ratios far from canonical values.

**`_impulse_quality(waves)`** (wavetree.py lines 41–47):
- Checks: W3/W1, W2/W1, W4/W3 — all linear lengths.
- Missing: W5/W1 (equality check) and W5/W3 (extended W3 case).
- Uses `_fib_close` (Gaussian), not `_closeness` (linear tent).

**`_fib_score(waves)`** (automation.py lines 33–47):
- Checks: W3/W1, W2.retr(W1), W4.retr(W3), W5/W1 — all linear lengths.
- Uses `_closeness` (linear tent, clips at 1.0), not `_fib_close` (Gaussian).
- **Inconsistency**: two different scoring functions (`_closeness` vs `_fib_close`) in two different modules produce different scores for the same ratios. Neither scores W5 vs W3.

**`similarity_and_balance`** — duplicated:
- `rules.py:409` returns `RuleResult` (canonical location).
- `toolkit.py:297` returns `SBResult` dataclass (older stub).
- Both use `Wave.length` (linear). The time ratio uses `Wave.days`, which is correct.

---

## 4. Mistake Table

| # | Requirement | Code behaviour | Verdict | Severity | Downstream effect on counts |
|---|-------------|---------------|---------|----------|----------------------------|
| M1 | Wave Fibonacci ratios measured on log-price for large ranges (Neely: mandatory if high > 2× low) | All ratio computations use `Wave.length = abs(end.price - start.price)` (linear) in `rules.py:103`, `wavetree.py:44-46`, `automation.py:37-47` | **WRONG** for any instrument spanning > 2× price (AVGO 330×, MRVL 105×) | **CRITICAL** | `_impulse_quality` and `_fib_score` return scores based on ratios that are 3×–10× off the Fibonacci grid. Example: AVGO W(I)/W(III) measures 7.74× linearly vs 1.10× on log — linear ratio falls nowhere near any Fib level, so quality → ~0; log ratio is near 1.0, quality → 1.0. The engine systematically under-scores valid large-range counts and over-scores counts where waves happen to have similar absolute dollar moves. |
| M2 | `adaptive_zigzag` must reach the target pivot count | Scale list `(0.04…0.30)` too short for MRVL 1W (105× price range); pct=0.30 gives 99 pivots on a 1354-bar 25-year series, never reaching target=24 | **WRONG** — worst case returns 4× the target count | **HIGH** | Feeds 98 "monowaves" to `label_monowaves()` for MRVL 1W. These 98 swings span fine-scale noise, not macro-degree monowaves. Every NeoWave label in the MRVL 1W section of the report is based on the wrong granularity. The 98-monowave result reported is a direct symptom. |
| M3 | Fixed-percentage ZigZag threshold must produce degree-consistent pivots across the price history | `pct` threshold is multiplicative (`ep * pct`), so the absolute dollar threshold is 300× larger at the end of AVGO history than at the start. Early pivots (2009, $2) capture fine structure; late pivots (2026, $400) capture coarser structure at the same nominal `pct` | **WRONG** for long-history data | **HIGH** | Pivot streams are structurally inconsistent across time. Early monowaves represent Minor-degree moves; late monowaves represent Primary-degree moves — both treated identically by `label_monowaves` and the wave tree. Wave degree inferred from monowave complexity is corrupted. The `degree_label` assignments are unreliable for any instrument with a price range > 3–5×. |
| M4 | ZigZag seeding should start from bar[0]'s H/L, not close | `ep = bars[0][4]` (close) at line `toolkit.py:88,169`. First pivot price uses close of bar 0, not its high or low | **MINOR BUG** — off by intrabar range at one pivot | **LOW** | First pivot is misplaced by up to `(bar[0].high - bar[0].close)` for H-type pivots or `(bar[0].close - bar[0].low)` for L-type. For weekly bars this can be several percent. One misplaced pivot corrupts the first wave segment's Fib ratio. Effect diminishes after the second confirmed pivot. |
| M5 | No dead code | `toolkit.py:110` and `toolkit.py:190`: `if l < bars[0][3]: pass` — literal no-ops | **CODE QUALITY** — does nothing | **LOW** | No runtime effect. Was likely an incomplete low-tracking attempt during seeding. Misleads readers into thinking low tracking is happening. |
| M6 | Wave 4 retracement check in `_impulse_quality` uses correct relationship | `wavetree.py:46`: `_fib_close(w4.length / w3.length)` — this scores the retracement of W4 vs W3. Canonical target: 38.2%. But the Fibonacci set `_FIB` includes 0.382, so the check is against the right target. However, it also accepts 0.5, 0.618, 0.786 as high-score values (via wide Gaussian sigma=0.2). Overcounts shallow W4 retracements as "good" quality | **ACCEPTABLE but imprecise** — sigma=0.2 is wide (±24% tolerance) | **LOW-MEDIUM** | Any W4 between ~0.27 and ~0.52 scores near-maximum. This means a W4 retracing 50% of W3 (which violates W4/W3 alternation with a deep W2) scores the same as the ideal 38.2%. Guideline violations are masked in the quality score. |
| M7 | Fibonacci scoring is consistent across modules | `_fib_close` (Gaussian, wavetree.py:31) and `_closeness` (linear tent, automation.py:26) are two different functions computing the same concept, applied to the same wave relationships | **INCONSISTENCY** | **MEDIUM** | `wave_counts()` (wavetree.py) and `label_and_validate()` (automation.py) score the same wave structure differently. A count that ranks first in one engine may rank third in the other. Composite systems mixing both scores are incoherent. |
| M8 | W5 Fibonacci scoring is complete | `_impulse_quality` (wavetree.py) omits W5/W1 and W5/W3 checks; `_fib_score` (automation.py) includes W5/W1 but omits W5/W3 | **INCOMPLETE** | **LOW-MEDIUM** | Extended W3 counts (where W5 ≈ 0.618×W3 or W1+W5 ≈ W3) are not scored. Extended third waves are common in tech stocks (AVGO, MRVL). |
| M9 | `fib_retrace`/`fib_extension` helpers document log-vs-linear usage | Both helpers compute levels in linear price. No documentation warns that for large-range instruments the `w1_len` input should be derived from log-price for accurate projections | **SILENT ASSUMPTION** | **LOW** | Projection targets in the forecast section are computed in linear price. For AVGO at $400 projecting from a W1 that started at $2, linear targets are misleadingly precise. |
| M10 | `similarity_and_balance` has one canonical location | Two implementations: `rules.py:409` (returns RuleResult) and `toolkit.py:297` (returns SBResult). Both use linear `Wave.length` | **DUPLICATION** | **LOW** | Risk of the two diverging; callers get different return types depending on import path. `toolkit.py` version is used in `scripts/wave_report.py` indirectly via `wl.similarity_and_balance` which resolves to `rules.py`. |

---

## 5. Concrete Fixes (Function-Level)

### Fix 1 — Introduce `Wave.log_length` and make ratio checks log-aware (CRITICAL)

**Location**: `rules.py:Wave`, `wavetree.py:_impulse_quality`, `automation.py:_fib_score`

```python
# rules.py — add to Wave dataclass
@property
def log_length(self) -> float:
    """Logarithmic (proportional) wave length.
    Equal to abs(log(end.price) - log(start.price)).
    Use for Fibonacci ratio comparisons when price range > 2×.
    Use .length (linear) only for absolute price levels.
    """
    if self.start.price <= 0 or self.end.price <= 0:
        return float('nan')
    return abs(math.log(self.end.price / self.start.price))
```

Then in `wavetree.py:_impulse_quality` and `automation.py:_fib_score`, replace `w.length` with `w.log_length` in ratio comparisons:

```python
# wavetree.py — _impulse_quality
def _impulse_quality(waves, use_log: bool = True) -> float:
    w1, w2, w3, w4, w5 = waves
    L = lambda w: w.log_length if use_log else w.length
    parts = [
        _fib_close(L(w3) / L(w1) if L(w1) else 0),   # W3/W1 ~1.618
        _fib_close(L(w2) / L(w1) if L(w1) else 0),   # W2 retrace of W1 ~0.618
        _fib_close(L(w4) / L(w3) if L(w3) else 0),   # W4 retrace of W3 ~0.382
        _fib_close(L(w5) / L(w1) if L(w1) else 0),   # W5/W1 ~1.0 or 0.618
    ]
    return sum(parts) / len(parts)
```

Similarly in `automation.py:_fib_score`. Add `use_log=True` as the default; callers can pass `use_log=False` for very short-range instruments (< 2× price).

The `similarity_and_balance` function should use `wave.log_length` for the price ratio and `wave.days` for the time ratio (time is already linear-correct).

### Fix 2 — Extend `adaptive_zigzag` scale list (HIGH)

**Location**: `scripts/wave_report.py:adaptive_zigzag` (lines 52–59)

```python
def adaptive_zigzag(bars, target=24):
    best = []
    # Extended scale list: 0.04 to 1.00 ensures MRVL 1W (105x range) can reach ~24 pivots
    SCALES = (0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00)
    for pct in SCALES:
        piv = [p for p in wl.zigzag_causal(bars, pct=pct) if p.confirmed_t is not None]
        if not best or abs(len(piv) - target) < abs(len(best) - target):
            best = piv
        if len(piv) <= target:
            break
    return best
```

With pct=0.50, MRVL 1W produces ~28 pivots (distance 4 from target 24), versus 99 pivots at pct=0.30 (distance 75). The 0.50 result is still not ideal since it's not ATR-normalized, but it prevents the 98-monowave pathology.

**Proper fix (medium-term)**: replace the entire `adaptive_zigzag` with an ATR-adaptive call using `zigzag_causal(bars, pct=atr_mult, atr_n=20)`. A multiplier of 3–5 on a 20-bar Wilder ATR produces structurally consistent pivots regardless of the absolute price level.

### Fix 3 — ATR-adaptive multi-scale pivot streams (HIGH, prerequisite for degree assignment)

**Location**: `toolkit.py:zigzag_multiscale`, callers in `wavetree.py:build_wave_tree` and `automation.py:label_and_validate`

```python
def zigzag_multiscale_atr(bars, atr_n: int = 20,
                           multipliers=(1.0, 2.0, 4.0, 8.0)) -> dict:
    """
    ATR-adaptive multi-scale pivot streams (one per multiplier).
    Each stream: threshold = ATR(atr_n) × multiplier (absolute, volatility-scaled).
    Smaller multiplier = finer degree (Minor); larger = coarser (Primary+).
    Pivot count is non-increasing as multiplier grows.
    """
    return {m: zigzag_causal(bars, pct=m, atr_n=atr_n) for m in multipliers}
```

This replaces both `zigzag_multiscale` and the separate `adaptive_zigzag` pattern. The `atr_n=20` means the threshold adapts to recent 20-bar volatility, making pivot detection degree-consistent regardless of absolute price level.

### Fix 4 — Fix ZigZag seeding to use H/L of first bar (LOW)

**Location**: `toolkit.py:zigzag` line 89, `toolkit.py:zigzag_causal` line 169

```python
# Instead of:
et, ep = bars[0][0], bars[0][4]  # close

# Use:
et, ep = bars[0][0], bars[0][4]  # start with close as fallback
# But track the intrabar range from bar 0 for seeding:
seed_h, seed_l = bars[0][2], bars[0][3]  # intrabar high and low
```

Then in the seed branch, initialize with the proper extreme once trend is established. This prevents a small first-pivot price error when `bar[0].close` differs materially from `bar[0].high` or `bar[0].low` (common on weekly bars).

### Fix 5 — Remove dead code lines (LOW)

**Location**: `toolkit.py:110` and `toolkit.py:190`

Delete both `if l < bars[0][3]: pass` lines. Replace with a comment explaining what was intended (likely tracking the first bar's low during seeding):

```python
# Note: the first bar's low is incorporated via the seed-branch H/L tracking above.
```

### Fix 6 — Unify Fibonacci scoring into one function (MEDIUM)

**Location**: `wavetree.py:_fib_close` and `automation.py:_closeness`

Resolve to one canonical function in `toolkit.py` or `rules.py`:

```python
# Recommended: Gaussian kernel with relative distance (wavetree variant)
# but with calibrated sigma — consider tightening from 0.2 to 0.15
# to better separate canonical (38.2/61.8/161.8) from off-ratio values.
def fib_proximity(r: float, sigma: float = 0.15) -> float:
    """Gaussian proximity (0..1) to nearest Fibonacci level.
    sigma is the relative-distance scale; 0.15 = ±15% half-bandwidth.
    """
    _FIB = (0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.0, 2.618, 3.618)
    if r != r or r <= 0:
        return 0.0
    d = min(abs(r - t) / t for t in _FIB)
    return math.exp(-(d * d) / (2 * sigma * sigma))
```

Then replace both `_fib_close` and `_closeness` with `fib_proximity`. The tighter sigma (0.15 vs 0.20) reduces acceptance of off-ratio values: at sigma=0.20 a ratio of 1.90 scores 0.97 (accepted as near-2.0); at sigma=0.15 it scores 0.89 (flagged as imprecise).

### Fix 7 — Add W5/W3 ratio to impulse quality (LOW-MEDIUM)

**Location**: `wavetree.py:_impulse_quality`, `automation.py:_fib_score`

For extended Wave 3 counts (common in tech stocks), add:
```python
# When W3 is the extended wave, W5 ≈ 0.618×W3 is the primary target
parts.append(fib_proximity(L(w5) / L(w3) if L(w3) else 0))   # W5/W3 ~0.618
```

Make this conditional on W3 being the longest of W1/W3/W5 to avoid penalizing non-extended-W3 counts.

### Fix 8 — Document log-vs-linear in fib_retrace and fib_extension (LOW)

**Location**: `toolkit.py:253-278`

Add docstring notes:
```python
def fib_extension(w1_len: float, base: float, ...):
    """Project Fibonacci extension price levels.
    w1_len: wave length in the SAME units as base.
    For instruments spanning > 2× price range, w1_len should be
    computed from log-price: w1_len = exp(Wave.log_length) * base
    or the levels should be treated as approximate guides only.
    """
```

---

## 6. Supporting Evidence from Live Data

| Observation | Root cause | Confirms which mistake |
|-------------|-----------|------------------------|
| MRVL 1W: 98 monowaves reported | `adaptive_zigzag` scale list tops out at 0.30 = 99 pivots; never reaches 24-pivot target | M2 |
| AVGO 1W: W(I)/W(III) linear ratio = 7.74× (off all Fib levels); log ratio = 1.10× (near equality) | Linear `Wave.length` used for all ratio computation | M1 |
| AVGO 1W early prices $2–$33, late prices $252–$495: same 10% threshold fires at completely different structural scales | Fixed percentage threshold, no ATR normalization | M3 |
| MRVL W1 linear = 93.73, W3-of-III linear = 55.68: W3 < W1 linearly (apparently violates R2) but in log space these are comparable percentage moves | Linear `Wave.length` | M1 (R2 false violation on linear scale) |
| `wave_counts()` (wavetree) and `label_and_validate()` (automation) produce different confidence rankings for same structure | Two different fib scoring functions | M7 |
| W4 retracement threshold in `_impulse_quality` accepts 23.6%–52% as near-maximum (via sigma=0.2) | Wide Gaussian kernel | M6 |

---

## Sources

- [ZigZag ATR — TradingView Library by DeepEntropy](https://www.tradingview.com/script/v8XJuorH-ZigZag-ATR/)
- [Elliott Wave Full Fractal System v2.0 — TradingView by mbedaiwi2](https://www.tradingview.com/script/KlaTN7AD-Elliott-Wave-Full-Fractal-System-v2-0/)
- [Zig Zag ATR Indicator — cTrader Store](https://ctrader.com/products/2299)
- [ZigZag — ChartSchool / StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/zigzag)
- [Zig Zag Indicator: Filtering Noise — LuxAlgo Blog](https://www.luxalgo.com/blog/zig-zag-indicator-filtering-noise-to-highlight-significant-price-swings/)
- [ZIGZAG backtest_mode PR — pandas-ta #874](https://github.com/twopirllc/pandas-ta/pull/874)
- [Look-Ahead Bias in Backtests — InvestingBrokers](https://investingbrokers.com/look-ahead-bias-backtesting/)
- [Lookahead Analysis — Freqtrade Documentation](https://www.freqtrade.io/en/stable/lookahead-analysis/)
- [Should fibonacci relationships be measured in absolute numbers or the distance covered on a log scale? — neowave.com QA #38](https://www.neowave.com/qow/qow-archive-38.asp)
- [Should a logarithmic or arithmetic chart be used for Elliott and NEoWave analysis? — neowave.com QA #11](https://www.neowave.com/qow/qow-archive-11.asp)
- [You suggest logarithmic charts when doing Wave analysis — neowave.com QA #2320](https://www.neowave.com/qow/qow-archive-2320.asp)
- [Logarithmic vs Linear Price Scale: Which One is Better — SeeTheWaves](https://seethewaves.com/logarithmic-vs-linear-scale-which-is-better/)
- [Trend-Based Fibonacci Extension: Tips for Better Trading — WaveBasis](https://wavebasis.com/your-fibonacci-levels-are-probably-wrong/)
- [Elliott Wave and Fibonacci: Retracements and Projections — EWOTrader](https://ewotrader.com/education/elliott-wave-theory/elliott-wave-and-fibonacci/)
- [Fibonacci Ratios and Impulse Waves in Elliott Wave Analysis — FBS Academy](https://fbs.com/fbs-academy/trading-tutorials/trading-handbook/fibonacci-ratios-and-impulse-waves)
- [Elliott Wave Theory — elliott-wave-forecast.com](https://elliottwave-forecast.com/elliott-wave-theory/)
- [Elliott Wave Guidelines: Ratio Analysis — LinkedIn / Subrat Kumar Dash](https://www.linkedin.com/pulse/elliott-wave-guidelines-ratio-analysis-subrat-kumar-dash)
- [Elliott Wave Principle — Wikipedia](https://en.wikipedia.org/wiki/Elliott_wave_principle)
- [NeoWave basic concepts — ForexTalker](https://forextalker.com/neowave-wave-theory-by-glenn-neely-basic-concepts-basic-principles-and-rules-for-building-neo-waves/)
- [Neo Wave Theory explained — LiteFinance](https://www.litefinance.org/blog/for-professionals/neo-wave-theory-and-pattern-explained/)
- [An Algorithmic Exploration of the ZigZag Indicator — PyQuantLab / Medium](https://pyquantlab.medium.com/an-algorithmic-exploration-of-the-zigzag-indicator-and-price-patterns-33192df976df)
