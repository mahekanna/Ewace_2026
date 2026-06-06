# 08 — Institutional-Grade Backtest Validation

**Ewace_2026 / `wavelib`** — Validation methodology for the Elliott Wave / NeoWave
reversal engine. June 2026.

> **Purpose.** The current `backtest_reversals` harness in `wavelib/backtest.py`
> measures hit-rate and profit-factor over a single in-sample period or a simple
> rolling walk-forward split. That is *necessary* but not *sufficient* to claim
> genuine edge. This document specifies the full institutional-grade validation
> stack — the same framework professional quant funds use — adapted to the specific
> structure of this engine (sparse causal reversal events, overlapping outcome labels,
> small event count). Every method includes exact formulas and pure-Python / NumPy
> pseudo-code so the harness can be built without external ML libraries.

---

## 1. Scope & sources

### 1.1 What this document covers

Six interconnected validation layers:

1. Walk-forward analysis (WFA) — the temporal robustness backbone.
2. Probabilistic Sharpe Ratio (PSR) and Deflated Sharpe Ratio (DSR) — correcting for
   non-normality and multiple testing at the single-strategy level.
3. Probability of Backtest Overfitting (PBO) via Combinatorially Symmetric
   Cross-Validation (CSCV) — detecting whether the best parameter set was found by
   luck across the strategy universe.
4. Combinatorial Purged Cross-Validation (CPCV) — preventing look-ahead leakage from
   overlapping event labels specific to event-based reversal signals.
5. Multiple-testing deflation — adjusting for the inflation caused by testing N
   variants of the same strategy idea.
6. Event-based backtest hygiene — triple-barrier labeling, meta-labeling, and the
   specific look-ahead risks in ZigZag / pivot-confirmation strategies.

### 1.2 Why the current harness is not sufficient

The existing `backtest_reversals` computes:

```
hit_rate = n_reversals / (n_reversals + n_invalidations)
profit_factor = sum(gains) / sum(losses)
wfe = mean(oos_pf / is_pf)   # across rolling windows
```

This is honest and causal, but it lacks:

- Any correction for the non-normality of return distributions (fat tails, negative
  skew are common in reversal strategies).
- Any adjustment for the number of parameter combinations tried (score_threshold,
  min_reversal_pct, ATR multiplier, degree scales, etc.).
- A statistically valid significance test for whether hit_rate > 0.5 given a small
  event count (~20–80 reversals per symbol/period).
- Protection against label-leakage when outcomes span multiple bars after entry.
- A distribution of OOS performance paths (not just one WFA slice).

### 1.3 Primary sources (inline citations throughout)

- Bailey, D. H. & Lopez de Prado, M. (2012). "The Sharpe Ratio Efficient Frontier."
  *Journal of Risk*, 15(2). [PSR derivation]
- Bailey, D. H. & Lopez de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting
  for Selection Bias, Backtest Overfitting and Non-Normality." *Journal of Portfolio
  Management*, 40(5), pp. 94–107. [DSR, MinBTL]
- Bailey, D. H., Borwein, J., Lopez de Prado, M., & Zhu, Q. J. (2016). "The
  Probability of Backtest Overfitting." *Journal of Computational Finance*, 20(4).
  [CSCV / PBO]
- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.
  [CPCV, purging/embargo, triple-barrier, meta-labeling — Chapters 7, 12, 14]
- Hansen, P. R. (2005). "A Test for Superior Predictive Ability." *Journal of Business
  & Economic Statistics*, 23(4). [SPA test]
- White, H. (2000). "A Reality Check for Data Snooping." *Econometrica*, 68(5). [RC]
- Nikolopoulos, S. D. (2026, April). "Spurious Predictability in Financial Machine
  Learning." arXiv:2604.15531. [latest evidence on inflation under martingale nulls]
- Benjamini, Y. & Hochberg, Y. (1995). "Controlling the False Discovery Rate."
  *Journal of the Royal Statistical Society*, 57(1). [BH correction]

---

## 2. Walk-Forward Analysis (WFA)

### 2.1 Concept

Walk-forward analysis divides the full history into a sequence of non-overlapping
In-Sample (IS) windows used for parameter fitting and Out-of-Sample (OOS) windows
used for performance measurement. The OOS segments are concatenated to form a
composite performance record that was never touched during optimisation.

Two regimes exist:

**Anchored (expanding IS window)**
```
Iteration 1:  [─────IS₁─────][OOS₁]
Iteration 2:  [────────IS₂────────][OOS₂]
Iteration 3:  [────────────IS₃────────────][OOS₃]
```
The IS start date is fixed; the IS end date advances. Use when you believe earlier
data is permanently informative (structural market regime is stable).

**Rolling (fixed IS window)**
```
Iteration 1:  [──IS──][OOS₁]
Iteration 2:     [──IS──][OOS₂]
Iteration 3:        [──IS──][OOS₃]
```
Both IS boundaries slide forward together. Use when older data is stale (regime
drift) — relevant for Elliott Wave counts, where market character shifts across
secular cycles.

### 2.2 Window sizing

Recommended for a weekly/4H event-based strategy:

| Parameter         | Minimum                | Preferred               |
|-------------------|------------------------|-------------------------|
| IS window         | 200 bars               | 400–600 bars            |
| OOS window        | 50 bars                | 100–150 bars            |
| Step size         | = OOS window           | = OOS window            |
| IS:OOS ratio      | 4:1                    | 4:1 to 6:1              |
| Total data needed | IS + 5 × OOS ≥ 800 bars | IS + 8 × OOS ≥ 1200 bars |

The IS:OOS ratio of 4:1 is the most widely cited heuristic (QuantInsti 2026). An
80:20 split avoids the optimism from large IS and the noise from small OOS.

### 2.3 Walk-Forward Efficiency (WFE)

The WFE quantifies how much IS performance survives into OOS:

```
WFE = OOS_metric / IS_metric
```

Where `metric` can be Sharpe ratio, profit factor, or annualised return. For each
WFA window `i`:

```
WFE_i = OOS_PF_i / IS_PF_i
```

Aggregate across K windows:

```
mean_WFE = (1/K) Σ WFE_i
```

**Thresholds** (Kiploks Robustness Engine, 2026; Quanthop 2026):

| WFE range      | Interpretation                          |
|----------------|-----------------------------------------|
| ≥ 0.70         | Robust — OOS tracks IS closely          |
| 0.50 – 0.70    | Acceptable — moderate decay             |
| 0.30 – 0.50    | Suspect — significant overfit           |
| < 0.30         | Reject — IS performance does not generalise |

A Sharpe decay ratio below 0.5 (i.e., OOS Sharpe < 0.5 × IS Sharpe) is a hard
warning sign regardless of absolute levels.

**Consistency ratio**: the fraction of WFA windows where OOS_PF > 1.0:

```
consistency = count(OOS_PF_i > 1.0) / K
```

Target ≥ 0.60 (the strategy should be profitable in 3 of every 5 OOS windows).

### 2.4 Pure-Python pseudo-code

```python
from itertools import product
from statistics import mean

def walk_forward(bars, scorer, is_size, oos_size, step, mode="rolling"):
    """
    bars     : list of (t, o, h, l, c, v) tuples, already sorted ascending
    scorer   : callable(bars) -> float  (returns a scalar metric, e.g. profit_factor)
    is_size  : int, number of IS bars
    oos_size : int, number of OOS bars
    step     : int, advance per iteration (usually = oos_size)
    mode     : "rolling" | "anchored"
    Returns  : dict with wfe_per_window, mean_wfe, consistency
    """
    n = len(bars)
    results = []
    start = 0
    while True:
        is_end = start + is_size
        oos_end = is_end + oos_size
        if oos_end > n:
            break
        if mode == "rolling":
            is_slice = bars[start:is_end]
        else:  # anchored: IS always begins at bar 0
            is_slice = bars[0:is_end]
        oos_slice = bars[is_end:oos_end]

        is_metric  = scorer(is_slice)
        oos_metric = scorer(oos_slice)

        wfe_i = (oos_metric / is_metric) if is_metric and is_metric != 0 else None
        results.append({
            "is_range":  (bars[0 if mode=="anchored" else start][0], bars[is_end-1][0]),
            "oos_range": (bars[is_end][0], bars[oos_end-1][0]),
            "is_metric":  is_metric,
            "oos_metric": oos_metric,
            "wfe":        wfe_i,
        })
        start += step

    valid_wfe = [r["wfe"] for r in results if r["wfe"] is not None]
    mean_wfe  = mean(valid_wfe) if valid_wfe else None
    consistency = (sum(1 for r in results if r["oos_metric"] and r["oos_metric"] > 1.0)
                   / len(results)) if results else None
    return {"windows": results, "mean_wfe": mean_wfe, "consistency": consistency}
```

---

## 3. Probabilistic Sharpe Ratio (PSR) and Deflated Sharpe Ratio (DSR)

### 3.1 The problem with raw Sharpe ratio

A raw Sharpe ratio estimate from a short backtest is unreliable for two reasons:

1. **Non-normality**: reversal strategies have negatively skewed, fat-tailed return
   distributions. The standard Sharpe confidence interval assumes normality and will
   understate the true variance of the estimate.
2. **Selection bias**: if you tested N parameter variants and report the best, the
   reported Sharpe is upward-biased by an amount proportional to √(log N).

The PSR and DSR correct for both.

### 3.2 Probabilistic Sharpe Ratio (PSR)

*Source: Bailey & Lopez de Prado (2012)*

**Intuition**: PSR is the probability that the *true* underlying Sharpe exceeds some
benchmark SR*, given the sample statistics including higher moments.

**Standard error of the estimated SR** (accounts for non-normality):

```
                  1 - γ₃·SR̂ + ((γ₄ - 1)/4)·SR̂²
σ̂²(SR̂) =  ─────────────────────────────────────────
                              T - 1
```

Where:
- `SR̂` = sample Sharpe ratio (annualised, computed from trade-level P&L)
- `T` = number of independent observations (number of resolved trades)
- `γ₃` = sample skewness of trade returns
- `γ₄` = sample excess kurtosis + 3 (i.e., fourth standardised moment)

**PSR formula**:

```
PSR(SR*) = Φ( (SR̂ - SR*) · √(T - 1) / σ̂(SR̂) )
```

Where `Φ` is the standard normal CDF.

**Interpretation**: PSR > 0.95 means there is a 95% probability the true Sharpe
exceeds the benchmark SR*. For a fresh signal with no prior track record, SR* = 0
is the natural null (i.e., "does the strategy have any edge?").

**Minimum Track Record Length (MinTRL)**

Solving PSR ≥ α for T gives the minimum number of observations needed to reject
the null at confidence α:

```
T_min = 1 + (1 - γ₃·SR* + ((γ₄-1)/4)·SR*²) · (Φ⁻¹(α) / (SR̂ - SR*))²
```

For a target of SR̂ = 0.5 annualised, SR* = 0, α = 0.95:
- Normally distributed returns (γ₃=0, γ₄=3): T_min ≈ 17 years of daily trades
- Negatively skewed returns (γ₃=-1, γ₄=5): T_min increases substantially

**This has a direct implication for Ewace_2026**: with ~20–80 reversal events per
symbol, PSR will be low even for profitable strategies. MinTRL must be computed
explicitly to know whether the available event count is sufficient.

### 3.3 Deflated Sharpe Ratio (DSR)

*Source: Bailey & Lopez de Prado (2014)*

**Intuition**: DSR = PSR evaluated at a benchmark SR* that accounts for the expected
maximum Sharpe from running N independent trials.

**Expected maximum SR from N independent trials** (using the expected maximum of N
standard normals corrected by the variance of individual SRs):

```
SR₀ = √V̂ · ((1 - γ) · Φ⁻¹(1 - 1/N) + γ · Φ⁻¹(1 - 1/(N·e)))
```

Where:
- `V̂` = sample variance of Sharpe ratios across the N trials
  `V̂ = (1/N) Σᵢ (SR̂ᵢ - mean(SR̂))²`
- `γ ≈ 0.5772` = Euler-Mascheroni constant
- `N` = number of independent parameter variants tested
- `e ≈ 2.7183` = Euler's number
- `Φ⁻¹` = inverse standard normal CDF (quantile function)

If all N trials share the same covariance structure (most conservative assumption):

```
V̂ = (1/N) Σᵢ (SR̂ᵢ - SR̄)²
```

**DSR formula**:

```
DSR = PSR(SR₀) = Φ( (SR̂_best - SR₀) · √(T-1) / σ̂(SR̂_best) )
```

Where `SR̂_best` is the Sharpe of the strategy selected as the winner.

**Threshold**: DSR > 0.95 (two-sided 5% significance) is the standard gate.
Lopez de Prado (2018) and the `chakra_quant` ARACHNE_CORE spec both cite DSR ≥ 0.95
as the minimum evidence threshold. DSR ≤ 0.5 means the winner was more likely
selected by chance than by genuine edge.

**Key sensitivity**: DSR falls rapidly with N. If you test 20 parameter combinations
(score_threshold ∈ {3,4,5}, min_reversal_pct ∈ {0.03,0.05,0.07,0.10},
ATR_multiplier ∈ {1,2}): N=24, and the required SR₀ may exceed 1.0 even if
individual SRs cluster around 0.6.

### 3.4 Pure-Python / NumPy implementation

```python
import math

def _phi(x):
    """Standard normal CDF via error function (stdlib only)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def _phi_inv(p, tol=1e-9):
    """Inverse normal CDF via Newton-Raphson (accurate to ~1e-9 for 0.001<p<0.999)."""
    # Initial approximation using rational minimax
    if p <= 0 or p >= 1:
        raise ValueError("p must be in (0, 1)")
    if p < 0.5:
        sign, q = -1, p
    else:
        sign, q = 1, 1 - p
    t = math.sqrt(-2 * math.log(q))
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]
    x = sign * (t - (c[0] + c[1]*t + c[2]*t**2) / (1 + d[0]*t + d[1]*t**2 + d[2]*t**3))
    # Newton refinement
    for _ in range(5):
        fx = _phi(x) - p
        x -= fx / math.exp(-0.5 * x**2) * math.sqrt(2 * math.pi)
    return x

def psr(sr_hat, sr_star, T, skew, kurt):
    """
    Probabilistic Sharpe Ratio.

    sr_hat  : float, sample annualised Sharpe ratio
    sr_star : float, benchmark Sharpe (0.0 for H₀: no edge)
    T       : int, number of independent observations (resolved trades)
    skew    : float, sample skewness of trade returns
    kurt    : float, sample EXCESS kurtosis of trade returns (normal=0)

    Returns PSR as a probability in [0, 1].
    """
    gamma4 = kurt + 3  # convert excess kurtosis to raw fourth moment
    var_sr = (1 - skew * sr_hat + ((gamma4 - 1) / 4) * sr_hat**2) / (T - 1)
    sigma_sr = math.sqrt(max(var_sr, 1e-12))
    z = (sr_hat - sr_star) * math.sqrt(T - 1) / sigma_sr
    return _phi(z)

def min_trl(sr_hat, sr_star, skew, kurt, alpha=0.95):
    """
    Minimum Track Record Length: minimum T such that PSR >= alpha.

    Returns integer number of observations needed.
    """
    gamma4 = kurt + 3
    z_alpha = _phi_inv(alpha)
    factor = 1 - skew * sr_star + ((gamma4 - 1) / 4) * sr_star**2
    if sr_hat <= sr_star:
        return float('inf')
    T_min = 1 + factor * (z_alpha / (sr_hat - sr_star))**2
    return math.ceil(T_min)

def sr_benchmark(sr_estimates, N=None):
    """
    Expected maximum SR from N independent trials (for DSR benchmark).

    sr_estimates : list[float], SR estimates from all tested variants
    N            : int or None; if None uses len(sr_estimates)

    Returns SR₀ scalar.
    """
    EULER_MASCHERONI = 0.5772156649
    E = math.e
    if N is None:
        N = len(sr_estimates)
    if N < 2:
        return 0.0
    mean_sr = sum(sr_estimates) / N
    var_sr = sum((s - mean_sr)**2 for s in sr_estimates) / N
    V = math.sqrt(max(var_sr, 1e-12))
    term1 = (1 - EULER_MASCHERONI) * _phi_inv(1 - 1/N)
    term2 = EULER_MASCHERONI * _phi_inv(1 - 1/(N * E))
    return V * (term1 + term2)

def dsr(sr_best, sr_estimates, T, skew, kurt, N=None):
    """
    Deflated Sharpe Ratio.

    sr_best      : float, sample SR of the selected strategy
    sr_estimates : list[float], SR from ALL tested variants (including best)
    T            : int, observations used for sr_best
    skew, kurt   : float, moments of best strategy's trade returns

    Returns DSR in [0, 1]. Target: DSR > 0.95 to pass.
    """
    sr0 = sr_benchmark(sr_estimates, N)
    return psr(sr_best, sr0, T, skew, kurt)
```

**Usage note**: for event-based strategies, `T` = number of *resolved* trades
(REVERSAL or INVALIDATED), not number of bars. Open events must be excluded from
moment calculations.

---

## 4. Probability of Backtest Overfitting (PBO) via CSCV

### 4.1 The CSCV algorithm

*Source: Bailey, Borwein, Lopez de Prado & Zhu (2016)*

**Problem**: given N strategy variants tested on the same historical data, and the
best-performing one selected, what is the probability that the "best" variant was
selected by luck rather than genuine edge?

**Algorithm — Combinatorially Symmetric Cross-Validation**:

Step 1 — Build performance matrix M of size (T × N):
- T rows = time sub-periods (partition the history into S equal sub-periods)
- N columns = strategy variants (parameter combinations)
- M[i, j] = performance metric (e.g., Sharpe ratio) of variant j in sub-period i

Step 2 — Choose S = 2·K where K ≥ 4 (S must be even; S=16 is standard):
- Partition the performance matrix rows into S equal blocks

Step 3 — Enumerate all C(S, S/2) combinations of blocks:
- For each combination `c`:
  - IS set  = the S/2 chosen blocks → compute IS Sharpe for each of N variants
  - OOS set = the remaining S/2 blocks → compute OOS Sharpe for each variant
  - Find `n*(c)` = argmax of IS Sharpe across N variants (the "winner")
  - Record the OOS Sharpe of that winner: `oos_perf[c] = OOS_SR[n*(c)]`
  - Record the rank of n*(c) in the OOS ranking: `oos_rank[c]`

Step 4 — Compute logit of relative rank:
```
λ(c) = log( oos_rank[c] / (N + 1 - oos_rank[c]) )
```
`λ < 0` means the IS winner ranked below median OOS → evidence of overfitting.

Step 5 — PBO = fraction of combinations where IS winner underperforms OOS median:
```
PBO = count(λ(c) < 0) / C(S, S/2)
```

**Interpretation**:
- PBO = 0.0: IS winner always outperforms OOS median → no overfitting evidence
- PBO = 0.5: pure chance — IS rank is uncorrelated with OOS rank
- PBO > 0.5: IS winner systematically underperforms OOS → overfitting
- Target: PBO < 0.1 for high confidence; PBO < 0.25 acceptable

### 4.2 Probabilistic loss distribution

As a diagnostic supplement, plot the distribution of `λ(c)` values. A strategy with
genuine edge shows a distribution skewed right (more positive logit values). A
data-mined strategy shows a symmetric or left-skewed distribution. The median λ and
the fraction below zero jointly characterise overfitting severity.

### 4.3 Pure-Python implementation

```python
import math
from itertools import combinations

def _sharpe(returns):
    """Annualised Sharpe from a list of period returns. Returns None if <2 obs."""
    n = len(returns)
    if n < 2:
        return None
    mean = sum(returns) / n
    var  = sum((r - mean)**2 for r in returns) / (n - 1)
    std  = math.sqrt(var) if var > 0 else 1e-12
    return mean / std  # not annualised here; consistent across variants

def compute_pbo(perf_matrix, S=16):
    """
    perf_matrix : list[list[float]] — shape (T, N)
                  T rows = time-ordered observations (trade P&L)
                  N cols = strategy variants
    S           : int, must be even; number of blocks (use 16)

    Returns dict with 'pbo', 'lambdas', 'n_combos'.
    """
    T = len(perf_matrix)
    N = len(perf_matrix[0])
    if T < S:
        raise ValueError(f"Need at least {S} observations, got {T}")
    if S % 2 != 0:
        raise ValueError("S must be even")

    # Step 1: partition T rows into S blocks
    block_size = T // S
    blocks = []
    for i in range(S):
        lo = i * block_size
        hi = lo + block_size if i < S - 1 else T
        blocks.append(list(range(lo, hi)))

    # Precompute per-block, per-strategy Sharpe
    # block_sharpe[i][j] = Sharpe of variant j in block i
    block_sharpe = []
    for blk in blocks:
        row = []
        for j in range(N):
            rets = [perf_matrix[t][j] for t in blk]
            row.append(_sharpe(rets) or 0.0)
        block_sharpe.append(row)

    # Step 3–4: enumerate all C(S, S/2) IS/OOS combinations
    K = S // 2
    all_is_indices = list(combinations(range(S), K))
    lambdas = []

    for is_idx in all_is_indices:
        oos_idx = [i for i in range(S) if i not in is_idx]

        # IS Sharpe for each variant
        is_sr = []
        for j in range(N):
            vals = [block_sharpe[i][j] for i in is_idx]
            is_sr.append(sum(vals) / len(vals))

        # OOS Sharpe for each variant
        oos_sr = []
        for j in range(N):
            vals = [block_sharpe[i][j] for i in oos_idx]
            oos_sr.append(sum(vals) / len(vals))

        # IS winner
        n_star = is_sr.index(max(is_sr))

        # OOS rank of IS winner (1 = best, N = worst)
        oos_winner = oos_sr[n_star]
        oos_rank = sum(1 for s in oos_sr if s >= oos_winner)  # rank by descending SR

        # Logit
        lam = math.log(oos_rank / (N + 1 - oos_rank)) if 0 < oos_rank < N else 0.0
        lambdas.append(lam)

    pbo = sum(1 for l in lambdas if l < 0) / len(lambdas)
    return {"pbo": pbo, "lambdas": lambdas, "n_combos": len(lambdas)}
```

**For Ewace_2026**: the performance matrix rows are individual *trade outcomes*
(not bars). Each column is a parameter variant. With only 20–50 resolved trades,
S=8 is more appropriate than S=16 (requires T ≥ S).

---

## 5. Combinatorial Purged Cross-Validation (CPCV)

### 5.1 The leakage problem specific to reversal events

In the Ewace_2026 engine, a `ReversalEvent` at bar `t_entry` has an outcome
resolved at bar `t_exit`. The label for that event (REVERSAL / INVALIDATED) spans
the interval `[t_entry, t_exit]`. This is an **overlapping label**.

Standard K-fold cross-validation places `t_entry` in training and `t_exit` in
testing (or vice versa), creating leakage: the model trained on the full forward
trajectory of early events "knows" information that is only revealed later. Even
though `backtest_reversals` is causal at *entry* (it only uses bars[0..t] to detect
the event), the outcome window contaminates any cross-validation scheme that ignores
this span.

CPCV (Lopez de Prado 2018, Ch. 12) solves this by:
1. **Purging** training observations whose outcome span overlaps the test fold.
2. **Embargoing** a buffer zone after each test fold to prevent autocorrelation leakage.
3. **Combining** multiple test folds simultaneously (p > 1) to generate many OOS
   paths with enough data remaining in each training set.

### 5.2 Purging rule

Given an event `i` with label span `[t₀ᵢ, t₁ᵢ]` and a test fold spanning `[τ₀, τ₁]`:

**Purge event i from training if**:
```
t₀ᵢ < τ₁  AND  t₁ᵢ > τ₀
```
i.e., the event's outcome window overlaps the test fold at all. This is the most
conservative rule and the one Lopez de Prado recommends.

For the Ewace_2026 engine:
- `t₀ᵢ` = `event.entry_t` (bar where entry signal is confirmed)
- `t₁ᵢ` = `outcome.exit_t` (bar where outcome is resolved), or `T` if still OPEN

### 5.3 Embargo rule

After test fold ends at `τ₁`, remove from training any events whose *feature
computation window* overlaps `[τ₁, τ₁ + h]`:

```
embargo_bars = h ≈ 0.01 · T   (Lopez de Prado's recommendation)
```

For a history of 500 bars: embargo ≈ 5 bars. For the Ewace engine where features
span up to `min_history` bars (default 60), a safer embargo is:

```
h = max(min_history, ceil(0.01 · T))
```

### 5.4 CPCV split construction

**Setup**: k total folds, p test folds per combination (standard: k=6, p=2).

**Number of test paths** (the key CPCV property):
```
n_paths = C(k, p) · p / k
```

For k=6, p=2: C(6,2) = 15 combinations, n_paths = 15 × 2/6 = 5 paths.
Each path covers the full timeline without gaps.

**Algorithm**:

```
1. Sort events chronologically by t_entry.
2. Divide into k equal folds: F₁, F₂, ..., Fₖ (each fold = consecutive events).
3. For each combination c = choose(k, p) test folds:
   a. test_folds  = union of p chosen folds
   b. train_folds = remaining k-p folds
   c. Purge from train_folds any event overlapping test_folds (by span rule §5.2)
   d. Embargo: also remove events in [max(τ₁) to max(τ₁) + h] from train_folds
   e. Fit the model/select parameters on train_folds
   f. Evaluate on test_folds; record metric (e.g., profit_factor_oos_c)
4. Assemble OOS paths: each bar appears in exactly C(k-1, p-1) test sets.
   Concatenate OOS evaluations in chronological order to form one full-history
   OOS path per backtest path.
5. Compute distribution of OOS metrics across all C(k,p) combinations.
   Report: mean, std, 5th-percentile of OOS Sharpe across paths.
```

### 5.5 Pure-Python implementation

```python
from itertools import combinations as _combs
import math

def cpcv_splits(events, k=6, p=2, embargo_bars=5):
    """
    events       : list of dicts with keys 'entry_t', 'exit_t' (unix seconds or bar index)
    k            : int, number of folds
    p            : int, number of test folds per combination (p < k)
    embargo_bars : int, number of bars to embargo after each test fold end

    Yields dicts: {'train_idx': [...], 'test_idx': [...], 'combo': tuple}
    where indices refer to positions in the sorted events list.
    """
    events = sorted(events, key=lambda e: e['entry_t'])
    n = len(events)
    if n < k:
        raise ValueError(f"Need at least {k} events, got {n}")
    fold_size = n // k
    folds = []
    for i in range(k):
        lo = i * fold_size
        hi = lo + fold_size if i < k - 1 else n
        folds.append(list(range(lo, hi)))

    for combo in _combs(range(k), p):
        test_idx  = []
        for fi in combo:
            test_idx.extend(folds[fi])
        train_idx_raw = []
        for fi in range(k):
            if fi not in combo:
                train_idx_raw.extend(folds[fi])

        # Determine test fold time span
        test_t0 = min(events[i]['entry_t'] for i in test_idx)
        test_t1 = max(events[i]['exit_t']  for i in test_idx)

        # Purge: remove training events whose outcome overlaps test window
        # Embargo: remove training events within embargo_bars of test_t1
        # (using bar-index distance as proxy for bars between events)
        def _is_purged(idx):
            ev = events[idx]
            overlap = ev['entry_t'] < test_t1 and ev['exit_t'] > test_t0
            embargo = abs(idx - max(test_idx)) <= embargo_bars
            return overlap or embargo

        train_idx = [i for i in train_idx_raw if not _is_purged(i)]
        yield {'train_idx': train_idx, 'test_idx': test_idx, 'combo': combo}

def run_cpcv(events, metric_fn, k=6, p=2, embargo_bars=5):
    """
    events     : list of event dicts
    metric_fn  : callable(events_subset) -> float
                 given a list of events (with outcomes), returns a scalar metric

    Returns list of OOS metrics, one per C(k,p) combination.
    """
    oos_metrics = []
    for split in cpcv_splits(events, k, p, embargo_bars):
        test_events  = [events[i] for i in split['test_idx']]
        metric_oos   = metric_fn(test_events)
        oos_metrics.append(metric_oos)
    return oos_metrics
```

**Output interpretation**: compute the distribution of `oos_metrics`. A genuine edge
shows:
- Mean OOS metric > threshold (e.g., PF > 1.0, Sharpe > 0.5)
- 5th-percentile OOS metric > 0 (edge persists even in bad splits)
- Standard deviation is small relative to mean (stable edge)

---

## 6. Multiple-Testing Deflation

### 6.1 The n_trials problem

Every time a researcher runs a backtest with a different parameter combination,
confluence score threshold, or structural label variant, they perform an implicit
hypothesis test. If N such tests are run and only the best is reported, the family-
wise error rate (FWER) inflates.

**The inflation formula** (Nikolopoulos 2026, arXiv:2604.15531): under a martingale-
difference null, the optimised IS winner's test statistic grows as:

```
E[max_statistic] ∝ √(log Keff)
```

Where `Keff` = effective number of independent strategies (accounting for correlation
between variants). For 20 variants with pairwise correlation 0.7: `Keff ≈ 6`, so the
inflation factor is √(log 6) ≈ 1.3. For 100 variants: `Keff ≈ 30`, inflation ≈ 1.7.

This is exactly the quantity captured by the DSR benchmark SR₀ in §3.3. The three
corrections below are complementary approaches.

### 6.2 Bonferroni correction (FWER control)

Most conservative. Controls the probability of *any* false discovery.

```
α_adjusted = α / N
```

For α = 0.05, N = 20: α_adjusted = 0.0025. Reject H₀ only if p < 0.0025.

**Problem**: overly conservative when strategies are correlated. With N=20 correlated
variants, Bonferroni rejects almost nothing. Use only as a floor.

### 6.3 Benjamini-Hochberg correction (FDR control)

Less conservative. Controls the *expected fraction* of false discoveries among
rejections (False Discovery Rate).

**Algorithm**:
1. Run N hypothesis tests; collect p-values p₁ ≤ p₂ ≤ ... ≤ pₙ (sorted ascending).
2. For each rank i, compute threshold: `t_i = (i/N) · α`
3. Find largest i such that `pᵢ ≤ t_i`. Call it `i*`.
4. Reject all H₀ for i = 1, ..., i* (not just i*).

**Pseudo-code**:

```python
def benjamini_hochberg(p_values, alpha=0.05):
    """
    p_values : list of floats, one per tested strategy variant
    alpha    : target FDR level

    Returns list of booleans: True = reject H₀ (strategy has edge)
    """
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    # Threshold for each rank
    thresholds = [(rank + 1) / n * alpha for rank in range(n)]
    # Find largest rank where p <= threshold
    i_star = -1
    for rank, (orig_idx, pv) in enumerate(indexed):
        if pv <= thresholds[rank]:
            i_star = rank
    # Reject all up to i_star
    rejected = set()
    for rank, (orig_idx, pv) in enumerate(indexed):
        if rank <= i_star:
            rejected.add(orig_idx)
    return [i in rejected for i in range(n)]
```

### 6.4 White's Reality Check and Hansen's SPA test

*Sources: White (2000); Hansen (2005)*

These are bootstrap tests that ask: "Is the *best* performing strategy significantly
better than a benchmark, after accounting for the fact that it was selected from N
candidates?"

**White's Reality Check (RC)**:

Let `f_j,t` = performance of strategy j at time t minus the benchmark performance
(excess returns). The null is H₀: max_j E[f_j] ≤ 0.

Statistic:
```
V_T = max_j { (1/T) Σ_t f_j,t }
```

Bootstrap procedure:
1. Resample `f_j,t` via stationary block bootstrap (block length l = √T).
2. In each bootstrap draw b:
   `V*_T,b = max_j { (1/T) Σ_t f*_j,t,b - (1/T) Σ_t f_j,t }`
   (the re-centering removes IS bias)
3. RC p-value = fraction of bootstrap draws where V*_T,b ≥ V_T

**Hansen's SPA improvement**: SPA re-centres the bootstrap distribution using a
sample-dependent correction that removes poorly-performing strategies from the
studentised statistic, increasing power (fewer false rejections of good strategies,
fewer false acceptances of bad ones).

**Practical note**: both tests are implemented in Python via the `arch` library
(`arch.bootstrap.SPA`), which provides the stationary bootstrap with block-length
optimisation. For a pure-stdlib version, implement the circular block bootstrap:

```python
def block_bootstrap_max_sr(perf_matrix, n_boot=1000, block_len=None):
    """
    perf_matrix : list[list[float]], shape (T, N)
                  rows = time, cols = strategy variants
                  each entry = excess return vs benchmark
    block_len   : int or None (defaults to sqrt(T))

    Returns float: RC p-value for H₀: max strategy E[f] ≤ 0.
    """
    import math, random
    T = len(perf_matrix)
    N = len(perf_matrix[0])
    if block_len is None:
        block_len = max(1, int(math.sqrt(T)))

    # Observed statistic
    col_means = [sum(perf_matrix[t][j] for t in range(T)) / T for j in range(N)]
    V_T = max(col_means)

    # Bootstrap distribution
    boot_stats = []
    for _ in range(n_boot):
        # Circular block bootstrap
        start = random.randint(0, T - 1)
        boot_idx = [(start + i) % T for i in range(T)]
        # Only need block boundaries
        indices = []
        while len(indices) < T:
            b_start = random.randint(0, T - 1)
            for i in range(block_len):
                if len(indices) < T:
                    indices.append((b_start + i) % T)
        boot_col_means = [
            sum(perf_matrix[indices[t]][j] for t in range(T)) / T
            for j in range(N)
        ]
        # Re-centre: subtract observed mean (White's RC centering)
        boot_excess = max(boot_col_means[j] - col_means[j] for j in range(N))
        boot_stats.append(boot_excess)

    p_value = sum(1 for b in boot_stats if b >= V_T) / n_boot
    return p_value
```

**Threshold**: p-value < 0.05 (after bootstrapping with n_boot ≥ 1000) indicates
the best strategy genuinely outperforms the benchmark, adjusted for selection from N
candidates.

### 6.5 Tracking n_trials: the registry obligation

**Every parameter variant tested must be counted**. This is the hardest discipline
to maintain in practice. Researchers who iteratively try variants, forget to count
them, then later report their "final" result understate N and therefore overstate DSR.

For Ewace_2026, maintain a `registry/trials.jsonl` file with one record per run:

```json
{"run_id": "2026-06-06T10:00", "params": {"score_threshold": 4, "min_pct": 0.05}, "is_sr": 0.72, "oos_sr": 0.55}
{"run_id": "2026-06-06T10:05", "params": {"score_threshold": 3, "min_pct": 0.05}, "is_sr": 0.63, "oos_sr": 0.41}
```

N for DSR = total rows in `trials.jsonl`. Retire failed variants (mark as ARCHIVED)
but keep them in the count for DSR purposes; they inflate the multiple-testing
universe even if not deployed.

---

## 7. Event-Based Backtest Hygiene

### 7.1 The ZigZag / pivot look-ahead problem

This is the most critical issue for Ewace_2026 and is already partially addressed
(Phase 0 F1 — `zigzag_causal`). The problem: a ZigZag pivot extreme (e.g., the high
of a wave-5 terminal) is only *confirmed* when price reverses by `threshold` in the
opposite direction. At the bar of the actual extreme, you do not yet know it was an
extreme. There are two failure modes:

1. **Entry dating**: dating the entry signal to the bar of the pivot extreme rather
   than the bar of confirmation. This uses future information (the reversal that
   confirms the pivot) to place a trade at a price that was not known to be a turning
   point. `zigzag_causal` fixes this by recording `confirmed_t` ≥ `extreme_t`.

2. **Wave count validation**: running `label_and_validate` on a pivot stream where
   the *most recent* pivot is provisional (it can still be extended by subsequent
   price action). This inflates apparent pattern clarity. The fix is to only use
   pivots whose confirmation bars are ≤ current bar t in the causal replay loop.

**Current status**: `zigzag_causal` is implemented (Phase 0 F1 ✅). The `backtest_reversals`
causal replay (Phase 4 A4 ✅) runs `label_and_validate` on `bars[0..t]`. The
remaining risk is that `label_and_validate` may use the last provisional swing point
from the most recent ZigZag run on `bars[0..t]`. Verify that the ZigZag used inside
`automation.label_and_validate` returns only confirmed pivots.

### 7.2 Triple-barrier labeling

*Source: Lopez de Prado (2018), Ch. 3*

Triple-barrier labeling replaces the simple hit-target-or-stop binary with a richer
label that mirrors actual trade execution.

**Setup**: for each entry event at time `t₀` and price `p₀`:
- Upper barrier: `p₀ × (1 + pt)` where `pt` = profit target (e.g., 2× ATR / entry)
- Lower barrier: `p₀ × (1 - sl)` where `sl` = stop loss (e.g., 1× ATR / entry)
- Vertical barrier: `t₀ + max_hold` (time limit in bars)

**Label assignment**:
```
label = +1  if upper barrier hit first
label = -1  if lower barrier hit first
label =  0  if vertical barrier hit first (timeout — no strong signal)
```

**Advantages over the current engine**:
- Explicitly models stop-loss (the current engine uses the invalidation level as a
  binary switch, which is conceptually correct but not ATR-calibrated).
- The vertical barrier exposes time-decaying signals: a reversal that takes 100 bars
  to play out may not be actionable.
- Enables meta-labeling (§7.3).

**ATR-based barrier sizing** (recommended for Ewace_2026):

```python
def atr(bars, period=14):
    """True Range ATR, causal (right-aligned window)."""
    tr_list = []
    for i in range(1, len(bars)):
        _, _, h, l, c = bars[i][:5]
        prev_c = bars[i-1][4]
        tr = max(h - l, abs(h - prev_c), abs(l - prev_c))
        tr_list.append(tr)
    atr_vals = []
    for i in range(len(tr_list)):
        window = tr_list[max(0, i - period + 1):i + 1]
        atr_vals.append(sum(window) / len(window))
    return atr_vals

def triple_barrier_label(bars, entry_bar_idx, pt_atr_mult=2.0, sl_atr_mult=1.0,
                          max_hold=50, bullish=True):
    """
    bars          : list of (t,o,h,l,c,...) tuples
    entry_bar_idx : int, index of entry bar in bars
    pt_atr_mult   : profit target = pt_atr_mult × ATR
    sl_atr_mult   : stop loss    = sl_atr_mult × ATR
    max_hold      : int, maximum bars to hold

    Returns: {'label': +1/-1/0, 'exit_bar': int, 'exit_price': float}
    """
    atr_vals = atr(bars)
    entry_price = bars[entry_bar_idx][4]  # close
    # ATR at entry (use ATR up to entry bar)
    entry_atr = atr_vals[entry_bar_idx - 1] if entry_bar_idx > 0 else atr_vals[0]

    if bullish:
        upper = entry_price + pt_atr_mult * entry_atr
        lower = entry_price - sl_atr_mult * entry_atr
    else:
        upper = entry_price + sl_atr_mult * entry_atr  # stop for short
        lower = entry_price - pt_atr_mult * entry_atr  # target for short

    for i in range(entry_bar_idx + 1, min(entry_bar_idx + max_hold + 1, len(bars))):
        _, _, h, l, c = bars[i][:5]
        if bullish:
            if l <= lower:  # stop first (conservative — check stop before target)
                return {'label': -1, 'exit_bar': i, 'exit_price': lower}
            if h >= upper:
                return {'label': +1, 'exit_bar': i, 'exit_price': upper}
        else:
            if h >= upper:  # stop for short
                return {'label': -1, 'exit_bar': i, 'exit_price': upper}
            if l <= lower:
                return {'label': +1, 'exit_bar': i, 'exit_price': lower}

    # Vertical barrier hit
    exit_bar = min(entry_bar_idx + max_hold, len(bars) - 1)
    return {'label': 0, 'exit_bar': exit_bar, 'exit_price': bars[exit_bar][4]}
```

### 7.3 Meta-labeling

*Source: Lopez de Prado (2018), Ch. 3*

Meta-labeling decouples the question of *direction* (the primary model) from the
question of *whether to trade at all* (the secondary meta-model).

In Ewace_2026:
- **Primary model**: `label_and_validate` + `score_reversal` → generates a signal
  with a direction (bullish/bearish) and a score.
- **Meta-model**: given a primary signal, predict whether the triple-barrier label
  will be +1 (trade it) or 0/-1 (skip). Features: confluence score, ATR regime,
  degree confidence, number of hard fails.

**Why this matters**: it separates precision (do we have structural edge?) from
recall (does the structural edge translate to tradeable profit after slippage?). The
meta-model can be as simple as a score threshold or as complex as a logistic
regression on the confluence components.

**Causal requirement**: the meta-model must be trained on events from the IS window
only and applied to OOS events — precisely the CPCV framework. This closes the loop
between §5 and §7.

### 7.4 Preventing confirmation-lag look-ahead in reversal scoring

The critical timing chain in `backtest_reversals`:

```
bar t:   bars[0..t] → label_and_validate → cands[0] → zone check
         if close_t ∈ zone: → score_reversal(window=bars[t-60..t]) → event
bar t+1: _resolve(event, bars[t+1..], target, invalidation)
```

Potential leakage points:
1. If `label_and_validate` uses the ATR or momentum value at bar t+1 to confirm
   a pivot — check that all internal ZigZag calls use right-aligned windows.
2. If `score_reversal` uses RSI divergence between swing pivots where the more
   recent pivot's confirmation bar > t — check that `swing_pivots` only uses
   `confirmed_t ≤ t`.
3. The `max_hold` parameter in `_resolve` implies future bars are observed from
   bar t. This is correct (it simulates entering at close_t and watching forward).
   But the *target* and *invalidation* must be set at bar t, not retrospectively.

**Audit checklist for causal integrity**:
- [ ] `automation.label_and_validate(bars[:t+1])` — all ZigZag calls right-aligned?
- [ ] `toolkit.swing_pivots` — returns only pivots with `confirmed_t ≤ bars[-1][0]`?
- [ ] `confluence.score_reversal` — RSI values computed on `bars[max(0,t-60):t+1]`?
- [ ] `ReversalEvent.invalidation` set to wave origin price at bar t (not future low)?
- [ ] Triple-barrier `upper`/`lower` set from `atr(bars[:t+1])` at bar t?

---

## 8. Concrete Validation Harness Design for Ewace_2026

### 8.1 End-to-end pipeline

```
STEP 1: COLLECT EVENTS (causal)
─────────────────────────────────
bars[0..T] (AVGO weekly / H4, ~5–10 years)
   ↓
backtest_reversals (causal replay, current implementation)
   ↓
ReversalEvent list with confirmed entry_t, zone, invalidation
   ↓
Triple-barrier outcome labeling (§7.2)
   → ReversalOutcome: label ∈ {+1, -1, 0}, exit_t, exit_price, move_pct

STEP 2: CPCV EVALUATION (§5)
─────────────────────────────
events sorted by entry_t
   ↓
CPCV splits (k=6, p=2, embargo=max_hold bars)
   ↓ (for each of C(6,2)=15 combinations)
train/test split → purge overlapping outcomes → metric_fn(test_events)
   → OOS metrics: [PF_1, PF_2, ..., PF_15]
   → Distribution: mean_OOS_PF, std, 5th-percentile

STEP 3: PSR / DSR (§3)
───────────────────────
For the "winner" parameter set (best IS metric):
   → compute trade-level returns: r_i = move_pct_i for each resolved event
   → SR̂ = mean(r) / std(r)
   → skew, kurt from r
   → PSR(SR* = 0.0): is there any edge at all?
   → DSR using sr_estimates from all N parameter variants: is the winner due to luck?

STEP 4: PBO (§4)
─────────────────
Build perf_matrix (resolved trades × N variants)
   ↓
CSCV with S = min(8, n_events // 5)
   ↓
PBO: fraction of combinations where IS winner underperforms OOS median

STEP 5: MULTIPLE-TESTING CORRECTION (§6)
──────────────────────────────────────────
p-values from PSR for each of N variants
   ↓
Benjamini-Hochberg at α = 0.05
   ↓
Surviving strategies: genuine edge (FDR controlled)

STEP 6: WALK-FORWARD (§2, outer wrapper)
──────────────────────────────────────────
All of STEPS 1–5 inside each WFA window
   ↓
WFE distribution across rolling IS/OOS splits
   ↓
Final verdict table (§8.3)
```

### 8.2 Minimum evidence thresholds (gate table)

| Gate | Metric            | Minimum to advance | Strong evidence |
|------|-------------------|--------------------|-----------------|
| G1   | n_resolved_events | ≥ 30               | ≥ 80            |
| G2   | PSR(SR*=0)        | ≥ 0.80             | ≥ 0.95          |
| G3   | DSR               | ≥ 0.65             | ≥ 0.95          |
| G4   | PBO               | ≤ 0.35             | ≤ 0.10          |
| G5   | Mean CPCV OOS PF  | ≥ 1.10             | ≥ 1.30          |
| G6   | 5th-pct CPCV PF   | ≥ 0.90             | ≥ 1.05          |
| G7   | WFE (mean)        | ≥ 0.50             | ≥ 0.70          |
| G8   | WFA consistency   | ≥ 0.55             | ≥ 0.70          |
| G9   | BH-corrected p    | ≥ 1 significant    | ≥ 3 significant |

**Pass rule**: must clear G1 + at least 5 of G2–G9. A strategy that passes G1
but fails G2 and G4 is DATA-MINED (cherry-picked parameters on noise). A strategy
that passes G2 but fails G7 is CURVE-FITTED (works IS, not OOS).

### 8.3 Verdict reporting skeleton

```python
def validation_report(events, bars, all_param_variants, winning_params):
    """
    events           : list of ReversalOutcome from backtest_reversals
    bars             : full OHLC bar list
    all_param_variants : list[dict] of all parameter dicts tried
    winning_params   : dict, the selected "best" params

    Prints a structured validation verdict.
    """
    resolved = [e for e in events if e.outcome != "OPEN"]
    n = len(resolved)
    returns = [e.move_pct for e in resolved if e.move_pct is not None]

    # Moments
    mean_r = sum(returns) / n if n else 0
    std_r  = (sum((r - mean_r)**2 for r in returns) / (n-1))**0.5 if n > 1 else 1e-6
    sr_hat = mean_r / std_r if std_r else 0
    skew   = sum(((r - mean_r)/std_r)**3 for r in returns) / n if n else 0
    kurt_excess = sum(((r - mean_r)/std_r)**4 for r in returns)/n - 3 if n else 0

    # PSR
    psr_val = psr(sr_hat, 0.0, n, skew, kurt_excess)

    # DSR (requires SR estimates from all N variants)
    N = len(all_param_variants)
    sr_estimates = [v.get('oos_sr', 0.0) for v in all_param_variants]
    dsr_val = dsr(sr_hat, sr_estimates, n, skew, kurt_excess, N)

    # MinTRL
    mtrl = min_trl(sr_hat, 0.0, skew, kurt_excess, alpha=0.95)

    print(f"=== VALIDATION REPORT ===")
    print(f"Resolved events : {n}")
    print(f"Hit rate        : {sum(1 for e in resolved if e.outcome=='REVERSAL')/n:.2%}")
    print(f"Profit factor   : {sum(r for r in returns if r>0)/abs(sum(r for r in returns if r<0)+1e-9):.2f}")
    print(f"Sample SR       : {sr_hat:.3f}")
    print(f"Skew / ExKurt   : {skew:.2f} / {kurt_excess:.2f}")
    print(f"PSR(SR*=0)      : {psr_val:.3f}  {'PASS' if psr_val>=0.95 else 'MARGINAL' if psr_val>=0.80 else 'FAIL'}")
    print(f"DSR (N={N})     : {dsr_val:.3f}  {'PASS' if dsr_val>=0.95 else 'MARGINAL' if dsr_val>=0.65 else 'FAIL'}")
    print(f"MinTRL (α=0.95) : {mtrl} trades needed for significance")
    print(f"Current n       : {n}  ({'' if n>=mtrl else 'INSUFFICIENT — '}{n/mtrl*100:.0f}% of required)")
```

---

## 9. Prioritised Implementation Plan

Listed by impact vs complexity. All items are pure-Python / NumPy, no external ML
libraries required.

### Priority 1 — Immediate (fixes silent errors in current harness)

**P1.1 — Causal ZigZag audit** (2 hours)
Trace `label_and_validate` → `zigzag_causal` → confirm that all pivot timestamps
used for wave-count validation satisfy `pivot.confirmed_t ≤ current_bar_t`. Add
an assertion to `backtest_reversals` that fires if any event's wave origin bar
index > its entry bar index.

**P1.2 — Moments-aware PSR for current hit-rate test** (1 hour)
Replace the implicit binomial z-test (hit_rate vs 0.5) with `psr(sr_hat, 0.0, n,
skew, kurt_excess)`. Report PSR alongside hit-rate. Output MinTRL so the user knows
how many more events are needed.

**P1.3 — n_trials registry** (1 hour)
Create `registry/trials.jsonl`. Log every backtest run with its parameters and IS/OOS
metrics. This is required for DSR computation and is zero-cost to implement now; very
expensive to reconstruct later.

### Priority 2 — High value (adds statistical rigour to existing WFA)

**P2.1 — DSR alongside WFE** (3 hours)
After a WFA run, collect SR estimates from all parameter variants in the WFA loop.
Call `dsr(best_sr, all_sr_estimates, n, skew, kurt)` and report alongside WFE.
Flag DSR < 0.65 as a hard warning.

**P2.2 — Triple-barrier outcome labeling** (4 hours)
Add `label_triple_barrier(bars, event, pt_mult, sl_mult, max_hold)` to
`wavelib/backtest.py`. Run alongside the existing `_resolve` to generate a richer
label set. ATR barriers expose time-decaying signals the current binary doesn't catch.

**P2.3 — BH correction on parameter sweep** (2 hours)
When running `backtest_reversals` across a grid of parameters, collect per-variant
PSR p-values = `1 - psr(...)`. Apply `benjamini_hochberg` at α=0.05. Report which
variants survive FDR correction.

### Priority 3 — Structural (needed before claiming publishable results)

**P3.1 — CPCV harness** (1 day)
Implement `cpcv_splits` and `run_cpcv` as in §5.5. Wire into a new function
`validate_cpcv(bars, params, k=6, p=2)` that returns the full distribution of OOS
profit-factors. This is the primary falsification gate for the engine.

**P3.2 — PBO via CSCV** (1 day)
Implement `compute_pbo` as in §4.3. Requires collecting per-variant, per-sub-period
performance. Use S=8 for the current small event count.

**P3.3 — Walk-forward RC / SPA bootstrap** (1 day)
Implement `block_bootstrap_max_sr` as in §6.4 to formally test whether any variant
genuinely beats the market after selection from N candidates.

### Priority 4 — Research grade (needed for journal-quality evidence)

**P4.1 — Multi-symbol replication** (ongoing)
The best statistical defence against overfitting is replication on independent symbols
in the same structural class. Run the full CPCV/DSR harness on NVDA, AMD, TSMC in
addition to AVGO/MRVL. If the signal holds across all five, the evidence base is
substantially stronger.

**P4.2 — Synthetic null baseline** (2 days)
Generate 1000 synthetic bar series with the same volatility / autocorrelation as
AVGO (bootstrap the actual returns). Run the engine on each. The empirical distribution
of hit-rates under the null quantifies how often random data produces a passing score.
A true positive should exceed the 95th percentile of this null distribution.

**P4.3 — Meta-labeling model** (2 days)
Train a logistic meta-model (IS) to predict triple-barrier label from confluence
score components. Evaluate OOS within CPCV. If the meta-model improves precision
vs the raw score ≥ 4 threshold, the feature set has discriminative power.

---

## 10. Caveats and Honest Limitations

### 10.1 Small sample problem

The entire validation stack above performs poorly with fewer than 30 resolved events.
With 20 events, PSR is imprecise (wide confidence interval), CSCV with S=8 produces
only C(8,4)=70 combinations (acceptable), CPCV with k=6 folds of 3 events each
leaves ~15 training events per IS window (marginal). The MinTRL formula should be
computed first: if it exceeds available events, gather more history before claiming
statistical significance.

**Practical ceiling for AVGO weekly data (2015–2026 = ~550 bars)**: the engine
might fire 30–60 reversal events. DSR will be marginal at best unless the raw SR is
very high (> 1.0). This is an honest limitation of low-frequency structural analysis.

### 10.2 Regime dependence

Elliott Wave / NeoWave patterns are most reliably labelled in trending markets. The
hit-rate measured in the IS period may reflect a specific trending regime (e.g., the
2016–2021 bull market) that does not persist into a ranging or bear regime OOS. CPCV
partially addresses this by testing across multiple time subsets, but it cannot
protect against a single structural break. Report the regime context (trending vs.
ranging via simple 200-bar moving average slope) for each WFA window.

### 10.3 Degree subjectivity

The auto-degree assignment (`assign_degrees_neely`) remains HEURISTIC confidence.
Different degree assignments produce different wave counts, different reversal zones,
and therefore different event sets — effectively a hidden hyperparameter. If degree
is treated as another dimension of the parameter grid, N increases substantially and
DSR degrades further.

### 10.4 Label ambiguity at degree boundaries

When the auto-labeler returns multiple candidate counts with similar scores (e.g.,
impulse vs. ABC correction at the same degree), the engine picks the top-ranked. But
the second candidate may generate a contradicting signal. Reporting only the top
candidate understates ambiguity and potentially inflates apparent hit-rate.

### 10.5 Sparse events and the clustered-events problem

Reversal events tend to cluster at market turning points (by construction — the
engine fires when structure is clear). Clustered events violate the independence
assumption underlying PSR and CSCV. The embargo in CPCV mitigates but does not
eliminate this: two reversal events at bars t=100 and t=105 (which may share most of
their feature computation windows) will receive the same purge/embargo treatment as
events 60 bars apart, but their returns will be highly correlated. Report the
autocorrelation of the event return series as a diagnostic.

### 10.6 The multiplicity gap vs. live N

The N in DSR should reflect ALL hypotheses entertained by the researcher during
development — including informal "I tried this and it didn't work" experiments that
were never logged. In practice this number is unknowable but is certainly larger than
the logged runs. The trials registry (P1.3) mitigates this prospectively but cannot
correct for prior experimentation. Treat DSR as a lower bound on the true multiple-
testing penalty.

---

## Sources

- [Bailey & Lopez de Prado (2014) — The Deflated Sharpe Ratio (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)
- [Bailey & Lopez de Prado (2014) — The Deflated Sharpe Ratio (davidhbailey.com)](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
- [Bailey, Borwein, Lopez de Prado & Zhu (2016) — Probability of Backtest Overfitting (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)
- [Bailey et al. — Backtest Overfitting full paper (davidhbailey.com)](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)
- [Deflated Sharpe Ratio — Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- [CRAN pbo package — Probability of Backtest Overfitting vignette](https://cran.r-project.org/web/packages/pbo/vignettes/pbo.html)
- [pypbo — Python PBO implementation (GitHub)](https://github.com/esvhd/pypbo)
- [Purged cross-validation — Wikipedia](https://en.wikipedia.org/wiki/Purged_cross-validation)
- [Cross Validation: Purging, Embargoing, Combinatorial — QuantInsti](https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial/)
- [skfolio CombinatorialPurgedCV documentation](https://skfolio.org/generated/skfolio.model_selection.CombinatorialPurgedCV.html)
- [CPCV explained — paperswithbacktest.com](https://paperswithbacktest.com/course/combinatorial-purged-cross-validation-cpcv)
- [CPCV with code — Quant Beckman](https://www.quantbeckman.com/p/with-code-combinatorial-purged-cross)
- [The Combinatorial Purged CV method — Towards AI](https://towardsai.net/p/l/the-combinatorial-purged-cross-validation-method)
- [mlfinlab backtest statistics documentation](https://random-docs.readthedocs.io/en/latest/implementations/backtest_statistics.html)
- [Hansen (2005) — SPA test (arch library)](https://arch.readthedocs.io/en/latest/multiple-comparison/generated/arch.bootstrap.SPA.html)
- [White (2000) — Reality Check — ResearchGate](https://www.researchgate.net/publication/4896389_A_Reality_Check_for_Data_Snooping)
- [Walk-Forward Efficiency (WFE) explained — Kiploks](https://kiploks.com/research/walk-forward-efficiency-wfe-explained-what-it-means-and-how-to-read-it)
- [Walk-Forward Analysis — Quanthop](https://quanthop.com/learn/validation-robustness/walk-forward-analysis)
- [Walk-Forward Validation: Anchored vs Rolling — QuanterLab](https://quanterlab.com/articles/foundations-walk-forward)
- [Triple-barrier labeling algorithm — williamsantos.me](https://williamsantos.me/posts/2022/triple-barrier-labelling-algorithm/)
- [Triple-barrier labeling — mlfinpy documentation](https://mlfinpy.readthedocs.io/en/latest/Labelling.html)
- [Triple-barrier method — Hudson & Thames meta-labeling](https://hudsonthames.org/does-meta-labeling-add-to-signal-efficacy-triple-barrier-method/)
- [Benjamini & Hochberg (1995) — Statsig explanation](https://www.statsig.com/perspectives/benjamini-hochberg-false-positives)
- [Nikolopoulos (2026) — Spurious Predictability in Financial ML (arXiv:2604.15531)](https://arxiv.org/abs/2604.15531)
- [Elliott Wave Backtesting — StratBase.ai](https://stratbase.ai/en/blog/elliott-wave-backtesting)
- [Look-Ahead Bias Prevention — QuantJourney](https://quantjourney.substack.com/p/advanced-look-ahead-bias-prevention)
- [Backtest overfitting ML era — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0950705124011110)
- [Statistical Power in Backtesting — QuestDB](https://questdb.com/glossary/statistical-power-analysis-in-backtesting-models/)
- [Minimum trades for valid backtest — BacktestBase](https://www.backtestbase.com/education/how-many-trades-for-backtest)
- [Probabilistic Sharpe Ratio — PortfolioOptimizer.io](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-hypothesis-testing-and-minimum-track-record-length-for-the-difference-of-sharpe-ratios/)
- [Interpretable Hypothesis-Driven Trading walk-forward (arXiv:2512.12924)](https://arxiv.org/abs/2512.12924)

---

*Document version 1.0 · Generated 2026-06-06 · Author: research agent for Ewace_2026*
*Do not git-commit without review by project owner.*
