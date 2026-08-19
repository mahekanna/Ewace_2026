# Cross-sectional test of the wave forecast — NEGATIVE

_Generated 2026-08-19 by `scripts/xs_test.py`. Pre-registered gate; result recorded
whether it passed or failed. Analysis tooling only — not investment advice._

## Why this test

`FORECAST_BACKTEST_2026-06.md` killed the forecast on a time-series basis: 48%/52%
direction win rate, Sharpe −0.013/+0.023, capturing **less than passive long**. But
that test is long-biased on a secular-bull semis universe, and the report itself
attributes every positive number in it to drift.

So the failure had two possible causes, and they demand different responses:

1. the forecast carries no information, or
2. it carries information that a drift-polluted, long-biased test cannot see.

A dollar-neutral cross-sectional test separates them. There is no drift to capture
in a long-short spread, so anything surviving is relative structural information.
Same feature, different confound.

## Design (pre-registered before any result was seen)

| | |
|---|---|
| Universe | 18 tradeable equities; indices/FX/crypto/VIX excluded as not comparable |
| Feature | signed conviction = ±`confidence` by forecast direction — the exact composite that failed time-series |
| Causality | forecast recomputed from bars ≤ rebalance date, `window=750` so every name is counted over equal history |
| Rebalance | every 21 trading days, ≥ 8 names required to score a date |
| Primary | mean cross-sectional Spearman rank IC vs 21-bar forward return |
| **Gate** | **mean IC > 0 and \|t\| ≥ 2.0** |
| Secondary | top-tercile − bottom-tercile spread > 0, t ≥ 2 |
| Control | scores permuted within date; IC must collapse to ~0 |
| Trials | 3 horizons × 1 feature, logged to `registry/trials.jsonl` |

## Result — 202 rebalances, 2009-07 → 2026-05

| H | n | mean IC | t(IC) raw | t(IC) adj | control IC | spread % | t(spread) adj | benchmark % |
|---|---|---|---|---|---|---|---|---|
| 5 | 202 | −0.0109 | −0.46 | −0.46 | −0.0206 | −0.105 | −0.41 | +0.653 |
| **21** | 202 | **−0.0141** | **−0.64** | **−0.64** | +0.0219 | **−0.612** | −1.33 | +2.586 |
| 63 | 200 | −0.0197 | −0.88 | −0.51 | +0.0024 | −3.148 | −1.75 | +7.637 |

`t adj` deflates for overlapping forward windows — at H=63, sampling every 21 bars
means consecutive observations share ⅔ of their window, which inflates raw \|t\| by
about √3. The raw H=63 spread t of **−3.02** looks significant and **is not**; it
is −1.75 once the overlap is removed. Recording that here because it is exactly the
kind of number that becomes a false discovery if quoted raw.

## Verdict: FAIL — and the failure is now better understood

Mean IC is negative at every horizon and statistically indistinguishable from
zero. It is not distinguishable from the permuted control either, which is the
cleanest statement of the result: **the forecast ranks instruments no better than
a shuffle of itself.**

Explanation (2) is dead. Removing the drift confound did not reveal hidden signal —
there was no signal underneath it. Two independent test designs, one time-series
and one cross-sectional, now agree.

Note the benchmark column: equal-weight universe returns +0.65% / +2.59% / +7.64%
over these horizons. That is the drift the earlier backtest was harvesting, shown
here explicitly next to a feature that adds nothing to it.

## Scope — what this does and does not establish

Does: the **composite** forecast (direction × confidence) has no measurable
directional skill, time-series or cross-sectional, on this universe.

Does not: condemn the wave geometry itself. The composite bundles pattern ID,
degree, direction and confidence into one scalar. A component could carry
information the bundle destroys — untested either way.

Limitations, stated rather than buried: median 9 names per date (thin for a
cross-section); pre-2018 the universe is semis-only, so early dates are
within-sector; all names are survivors.

## Next

1. **Decompose** — test components separately (wave-3 extension ratio, B-wave
   retracement depth, channel position, degree, confluence strand count) rather
   than the bundle.
2. **Change the target** — first-passage ("does the projected zone print before
   the invalidation?") is what the count actually claims; signed fixed-horizon
   return is the noisiest possible target.
3. **The 7th strand** — Hurst/FLD cycle timing is the only orthogonal information
   in the roadmap; everything above re-slices the same price geometry.

Registry now holds 68 logged trials. Every one counts against the Deflated Sharpe
of anything that eventually passes.
